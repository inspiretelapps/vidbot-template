import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import pipeline as p
from render_site import render

ROWS = [{'start_seconds': 0, 'duration': 60, 'text': 'A complete transcript.'}]
SUMMARY = {'summary': 'An evidence-based overview.', 'why_valuable': 'Explains the topic.',
           'key_takeaways': ['A concrete lesson.'], 'chapters': [{'start_seconds': 0, 'title': 'Introduction',
           'description': 'Explains the introduction. Describes the lesson.'}]}


class PipelineTests(unittest.TestCase):
    def fixture(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        for folder in ('data', 'site', 'transcripts'):
            (root / folder).mkdir()
        p.write(root / 'config.json', {'playlist_url': '', 'playlist_title': 'Test', 'model': p.MODELS[0]})
        p.write(root / 'data/videos.json', [])
        p.write(root / 'data/state.json', {'seen': {}})
        (root / 'site/index.html').write_text('<title>Library</title>')
        return root

    def test_playlist_url_is_normalized_and_rejects_other_hosts(self):
        self.assertEqual('https://www.youtube.com/playlist?list=PL123', p.playlist_url('https://youtube.com/playlist?list=PL123&si=abc'))
        for bad in ('http://youtube.com/playlist?list=PL123', 'https://youtube.com.evil.test/playlist?list=x', 'https://youtube.com/watch?v=x'):
            with self.assertRaises(ValueError): p.playlist_url(bad)

    def test_uploaded_transcript_does_not_call_network(self):
        root = self.fixture()
        p.write(root / 'transcripts/abcdefghijk.json', ROWS)
        with patch.object(p, 'run_json') as network:
            rows, source = p.transcript('abcdefghijk', root=root)
        network.assert_not_called()
        self.assertEqual('uploaded', source)
        self.assertEqual(ROWS, rows)

    def test_empty_and_oversized_transcripts_fail(self):
        for rows in ([], [{'text': '', 'offset': 0}], [{'text': 'x' * 180001}], [{'text': 'x', 'offset': float('nan')}]):
            with self.assertRaises(ValueError): p.normalize_transcript(rows)

    def test_model_output_cannot_override_trusted_metadata(self):
        generated = p.validate_summary({**SUMMARY, 'url': 'javascript:alert(1)', 'id': '../bad'}, ROWS)
        self.assertNotIn('url', generated)
        self.assertNotIn('id', generated)
        self.assertEqual('generated', generated['chapters'][0]['source'])

    def test_chapter_timestamps_are_checked(self):
        for start in (-1, 61, float('inf'), '0', True):
            value = {**SUMMARY, 'chapters': [{**SUMMARY['chapters'][0], 'start_seconds': start}]}
            with self.assertRaises(ValueError): p.validate_summary(value, ROWS)

    def test_model_events_handle_json_and_errors(self):
        output = json.dumps({'type': 'text', 'part': {'text': '```json\n' + json.dumps(SUMMARY) + '\n```'}})
        self.assertEqual(SUMMARY, p.parse_model_events(output))
        with self.assertRaises(ValueError): p.parse_model_events('{"type":"error"}')
        with self.assertRaises(ValueError): p.parse_model_events('garbage')

    def test_partial_failure_preserves_success_and_retries_failed_video(self):
        root = self.fixture()
        entries = [{'id': 'abcdefghijk', 'title': 'A'}, {'id': 'lmnopqrstuv', 'title': 'B'}]
        env = {'PLAYLIST_URL': 'https://youtube.com/playlist?list=PL123', 'OPENCODE_API_KEY': 'test-only', 'MAX_VIDEOS': '3'}
        with patch.dict(os.environ, env, clear=True), patch.object(p, 'scan', return_value={'entries': entries}), patch.object(p, 'metadata', side_effect=lambda x: x), patch.object(p, 'summarize', return_value=SUMMARY), patch.object(p, 'transcript', side_effect=[(ROWS, 'test'), ValueError('No captions')]):
            report = p.update(root)
        self.assertEqual(['abcdefghijk'], report['succeeded'])
        self.assertEqual(['abcdefghijk'], list(p.read(root / 'data/state.json')['seen']))
        with patch.dict(os.environ, env, clear=True), patch.object(p, 'scan', return_value={'entries': entries}), patch.object(p, 'metadata', side_effect=lambda x: x), patch.object(p, 'summarize', return_value=SUMMARY), patch.object(p, 'transcript', return_value=(ROWS, 'test')) as transcript:
            report = p.update(root)
        self.assertEqual(['lmnopqrstuv'], report['succeeded'])
        self.assertEqual(1, transcript.call_count)
        self.assertEqual(2, len(p.read(root / 'data/videos.json')))

    def test_playlist_changes_do_not_mix_libraries(self):
        root = self.fixture()
        config = p.read(root / 'config.json')
        config['playlist_url'] = 'https://youtube.com/playlist?list=OLD'
        p.write(root / 'config.json', config)
        with patch.dict(os.environ, {'PLAYLIST_URL': 'https://youtube.com/playlist?list=NEW'}, clear=True):
            with self.assertRaisesRegex(ValueError, 'another playlist'): p.update(root)

    def test_publish_contains_no_secrets_or_transcripts(self):
        root = self.fixture()
        p.write(root / 'transcripts/abcdefghijk.json', ROWS)
        with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'owner/copy', 'OPENCODE_API_KEY': 'never-publish-me'}):
            render(root)
        payload = p.read(root / 'public/videos.json')
        self.assertEqual('https://github.com/owner/copy/actions/workflows/update-library.yml', payload['workflow_url'])
        self.assertNotIn('never-publish-me', json.dumps(payload))
        self.assertEqual({'.nojekyll', 'index.html', 'videos.json'}, {x.name for x in (root / 'public').iterdir()})

    def test_new_template_is_empty_and_not_tied_to_original_owner(self):
        root = Path(__file__).resolve().parents[1]
        html = (root / 'site/index.html').read_text()
        self.assertNotIn('tailscale', html.lower())
        self.assertNotIn('.ts.net', html)
        self.assertNotIn('WhatsApp', html)
        self.assertIn('workflow_url', html)


if __name__ == '__main__': unittest.main()
