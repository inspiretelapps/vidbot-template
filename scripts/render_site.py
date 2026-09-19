"""Publish only the site and validated library, never credentials or transcripts."""
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render(root=ROOT):
    config = json.loads((root / 'config.json').read_text())
    videos = json.loads((root / 'data/videos.json').read_text())
    public = root / 'public'
    public.mkdir(exist_ok=True)
    shutil.copy2(root / 'site/index.html', public / 'index.html')
    repository = os.environ.get('GITHUB_REPOSITORY', '')
    workflow_url = f'https://github.com/{repository}/actions/workflows/update-library.yml' if re.fullmatch(r'[\w.-]+/[\w.-]+', repository) else ''
    payload = {'playlist': {'title': config['playlist_title'], 'url': config['playlist_url']},
               'updated_at': datetime.now(timezone.utc).isoformat(),
               'workflow_url': workflow_url, 'videos': videos}
    (public / 'videos.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    (public / '.nojekyll').touch()
    return len(videos)


if __name__ == '__main__':
    print(f'Rendered {render()} videos')
