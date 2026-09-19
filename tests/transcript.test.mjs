import { test } from 'node:test';
import assert from 'node:assert/strict';
import { captionsInSeconds } from '../scripts/transcript_adapter.mjs';

function mockFetch(xml) {
  return async url => new Response(String(url).includes('timedtext') ? xml : JSON.stringify({
    captions: { playerCaptionsTracklistRenderer: { captionTracks: [{ languageCode: 'en', baseUrl: 'https://www.youtube.com/api/timedtext?v=abcdefghijk' }] } },
  }));
}
test('srv3 timestamps become seconds', async () => {
  const rows = await captionsInSeconds('abcdefghijk', 'en', mockFetch('<timedtext><p t="1500" d="2500"><s>Hello</s></p></timedtext>'));
  assert.deepEqual(rows, [{ text: 'Hello', offset: 1.5, duration: 2.5 }]);
});
test('classic timestamps remain seconds', async () => {
  const rows = await captionsInSeconds('abcdefghijk', 'en', mockFetch('<transcript><text start="1500" dur="2.5">Hello</text></transcript>'));
  assert.deepEqual(rows, [{ text: 'Hello', offset: 1500, duration: 2.5 }]);
});
test('empty caption response fails instead of fabricating content', async () => {
  await assert.rejects(captionsInSeconds('abcdefghijk', 'en', mockFetch('<transcript/>')), /No captions/);
});
