import { captionsInSeconds } from './transcript_adapter.mjs';
const id = process.argv[2];
if (!/^[\w-]{11}$/.test(id || '')) throw new Error('Invalid YouTube video ID');
try {
  process.stdout.write(JSON.stringify(await captionsInSeconds(id, process.argv[3] || 'en')));
} catch {
  console.error('YouTube captions unavailable via youtube-transcript. Trying fallback.');
  process.exitCode = 1;
}
