import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import transcript_service as service
import pipeline


class ServiceTests(unittest.TestCase):
    def test_native_mode_and_millisecond_conversion(self):
        with patch.object(service, 'request_json', return_value={'content': [{'offset': 1500, 'duration': 2500, 'text': 'Hello'}]}) as request:
            self.assertEqual([{'offset': 1.5, 'duration': 2.5, 'text': 'Hello'}], service.fetch('abcdefghijk', 'en', 'test'))
        self.assertIn('mode=native', request.call_args.args[0])
        self.assertNotIn('test', request.call_args.args[0])

    def test_async_result_and_failure(self):
        with patch.object(service.time, 'sleep'), patch.object(service, 'request_json', side_effect=[{'jobId': 'job-123'}, {'status': 'completed', 'result': {'content': [{'offset': 0, 'duration': 1000, 'text': 'Hello'}]}}]):
            self.assertEqual(1, service.fetch('abcdefghijk', 'en', 'test')[0]['duration'])
        with patch.object(service.time, 'sleep'), patch.object(service, 'request_json', side_effect=[{'jobId': 'job-123'}, {'status': 'failed'}]):
            with self.assertRaises(ValueError): service.fetch('abcdefghijk', 'en', 'test')

    def test_service_only_called_after_free_tools_fail_with_key(self):
        with patch.object(pipeline, 'direct_transcript', side_effect=ValueError('blocked')), patch.dict(os.environ, {'SUPADATA_API_KEY': 'test'}), patch.object(service, 'fetch', return_value=[{'offset': 0, 'duration': 1, 'text': 'Hello'}]) as paid:
            rows, source = pipeline.transcript('abcdefghijk')
        self.assertEqual('supadata-native', source)
        paid.assert_called_once()
        with patch.object(pipeline, 'direct_transcript', return_value=([], 'free')), patch.object(service, 'fetch') as paid:
            pipeline.transcript('abcdefghijk')
        paid.assert_not_called()

    def test_no_key_never_calls_paid_service(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(pipeline, 'direct_transcript', side_effect=ValueError('blocked')), patch.object(service, 'fetch') as paid:
            with self.assertRaisesRegex(ValueError, 'SUPADATA_API_KEY'): pipeline.transcript('abcdefghijk')
        paid.assert_not_called()
