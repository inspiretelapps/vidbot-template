import { fetchTranscript } from 'youtube-transcript';

// youtube-transcript 1.3.1 returns milliseconds for srv3 XML, seconds for
// classic XML. Detect the actual response format, never guess from magnitude.
export async function captionsInSeconds(id, language = 'en', fetchImpl = fetch) {
  let divisor = 1;
  const rows = await fetchTranscript(id, {
    lang: language,
    fetch: async (url, options) => {
      const response = await fetchImpl(url, { ...options, signal: AbortSignal.timeout(25000) });
      if (new URL(url).pathname.includes('timedtext')) {
        const xml = await response.clone().text();
        divisor = /<p\s+t="\d+"\s+d="\d+"/.test(xml) ? 1000 : 1;
      }
      return response;
    },
  });
  if (!rows.length) throw new Error('No captions returned');
  return rows.map(row => ({ text: row.text, offset: row.offset / divisor, duration: row.duration / divisor }));
}
