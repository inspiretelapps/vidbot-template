"""Optional Supadata fallback, native captions only (no audio-generation charges)."""
import json
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen

BASE = 'https://api.supadata.ai/v1/transcript'


def request_json(url, key):
    try:
        with urlopen(Request(url, headers={'x-api-key': key, 'Accept': 'application/json'}), timeout=60) as response:
            return json.load(response)
    except HTTPError as exc:
        raise ValueError(f'Transcript service returned HTTP {exc.code}. Check SUPADATA_API_KEY, credits, and video availability.') from None
    except (URLError, TimeoutError, json.JSONDecodeError):
        raise ValueError('Transcript service could not complete the request; retry later.') from None


def fetch(video_id, language, key):
    if not re.fullmatch(r'[\w-]{11}', video_id):
        raise ValueError('Invalid video ID')
    query = urlencode({'url': f'https://www.youtube.com/watch?v={video_id}',
                       'lang': language, 'text': 'false', 'mode': 'native'})
    result = request_json(BASE + '?' + query, key)
    if result.get('jobId'):
        job_id = quote(str(result['jobId']), safe='')
        for _ in range(30):
            time.sleep(2)
            result = request_json(BASE + '/' + job_id, key)
            if result.get('status') == 'completed':
                result = result.get('result', result)
                break
            if result.get('status') == 'failed':
                raise ValueError('Transcript service could not retrieve captions for this video')
        else:
            raise ValueError('Transcript service is still processing; retry later')
    content = result.get('content')
    if not isinstance(content, list) or not content:
        raise ValueError('Transcript service returned no timestamped captions')
    try:
        return [{'offset': float(row['offset']) / 1000,
                 'duration': float(row.get('duration', 0)) / 1000,
                 'text': row['text']} for row in content]
    except (KeyError, TypeError, ValueError):
        raise ValueError('Transcript service returned malformed caption data') from None
