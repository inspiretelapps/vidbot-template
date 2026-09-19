# Your own YouSummary library

Turn a YouTube playlist into a searchable website with summaries, takeaways, and timestamped chapters. Updates run only when you ask. GitHub hosts the website and runs OpenCode for you; no computer needs to stay on.

[**Create your own library →**](https://github.com/inspiretelapps/vidbot-template/generate)

## Set up once — no coding

1. **Create your copy.** Click the link above (or **Use this template → Create a new repository**). Choose a name, such as `my-video-library`, and choose **Public** for the simplest GitHub Free setup. Each copy starts with an empty library. Public repositories and their libraries are readable by anyone: unlisted YouTube links do not make this website private.
2. **Get your AI key.** Sign in to [OpenCode Zen](https://opencode.ai/auth), add credits if needed, and create an API key. This is a Zen API key, not a Google key, DeepSeek key, or a coding-agent subscription login. Model use is billed to your account. You do not need to install OpenCode.
3. **Save the key securely.** In **your copy** on GitHub, open **Settings → Secrets and variables → Actions → New repository secret**. Name it `OPENCODE_API_KEY` and paste your key as the value. Never put it in a file or commit it.
4. **Enable your website.** Open **Settings → Pages**. Under **Build and deployment**, set **Source** to **GitHub Actions**. You do not need to create a deployment branch.
5. **Run your first update.** Open **Actions → Update library → Run workflow**. If GitHub asks you to enable workflows, enable them. Leave the branch on `main`. Paste your playlist link into **YouTube playlist link**, select a model, choose **1** video for your first test, and click **Run workflow**.
6. **If captions are blocked, add the fallback key.** A live test on GitHub’s runner failed to retrieve captions even though the same video worked locally. For unattended retrieval, create a [Supadata account](https://supadata.ai/) and add its key as a second repository secret named `SUPADATA_API_KEY`. It is used only after both free caption tools fail. This may incur transcript-service charges. You can instead upload transcripts manually as described below.
7. **Open your website.** Wait for the workflow to finish. The deployment link appears in the run, or open **Settings → Pages → Visit site**. It will normally be `https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/`.

For later updates, use the refresh icon on your website. It opens GitHub's **Update library** page: sign in as the repository owner, click **Run workflow**, and leave the playlist field blank to reuse it. The public website cannot spend your API credits on its own. Readers need only the website link.

## Choose a model

One OpenCode Zen key works for all three choices in the update form:

| Choice | Suggested use |
| --- | --- |
| `opencode/gemini-3.5-flash-lite` | Default: a lightweight Google model for transcript summaries |
| `opencode/deepseek-v4.1-flash` | DeepSeek **V4.1 Flash**, an alternative using the same key |
| `opencode/gemini-3-flash` | Another Google option if you prefer its summaries |

The workflow selection determines the model for that run. Existing summaries are not regenerated or charged again. Check [current Zen pricing](https://opencode.ai/docs/zen/) and [available models](https://opencode.ai/zen/v1/models); availability and prices can change. Google models receive the fetched transcript just like DeepSeek; this workflow does not rely on direct YouTube video ingestion.

## Three actions you can run

- **Update library:** scan the saved playlist, retrieve captions, summarize up to your selected limit, save the results, and publish the site.
- **Publish website only:** publish the current library without an API key or model call. Useful for testing setup or website changes.
- **Check YouTube captions:** test a video's captions from GitHub's runner, without an OpenCode key, model call, or website change. If you have set `SUPADATA_API_KEY`, the fallback can consume transcript-service credits. Paste the 11-character video ID from its YouTube URL into the test field.

No cron jobs, WhatsApp, database account, GitHub app installation, Vercel account, or personal access token is required.

## What happens if captions fail?

YouTube sometimes blocks cloud servers, and some videos have no captions in the configured language. This app first tries the `youtube-transcript` npm package, then yt-dlp. Neither guarantees access. If `SUPADATA_API_KEY` is configured, it next requests existing captions through [Supadata](https://docs.supadata.ai/get-transcript). The fallback uses `mode=native`, so it does not automatically generate speech-to-text audio transcripts.

A failed video remains available for retry. Successful summaries are saved and published even if another video fails; the workflow then shows a failure status so you know to read its summary. It never invents a summary from the title when captions are missing.

If retrying does not help, [upload a timestamped transcript](transcripts/README.md) using GitHub's file-upload screen and run the update again. There is no automatic speech-to-text generation in this version. The optional Supadata service has its own account and pricing. Metadata retrieval can also fail independently; in that case the website identifies an unavailable creator description.

## Limits and troubleshooting

- Start with one video to check your key and captions. Updates process 1–10 new videos per run and scan up to the first 500 playlist entries. Repeat updates for a larger library. Failed entries at the start of the pending list are retried first; supplying their transcripts or removing inaccessible videos from the source playlist avoids repeated failures.
- English captions are requested by default. To use another caption language, edit `language` in `config.json` on GitHub, for example `af`. Generated summaries remain in English.
- Very long transcripts over 180,000 characters are rejected rather than silently truncated. Each AI call has a five-minute timeout; the whole workflow has a one-hour limit.
- Use public or unlisted playlists you can access. Private playlists requiring a YouTube login are not supported. Create another template copy for another playlist; the workflow prevents accidentally mixing libraries.
- If publishing fails, check **Settings → Pages → Source: GitHub Actions**. If committing fails, check repository/organization branch protection and Actions policies allow this workflow to write to the default branch. Avoid editing library data while an update is running.
- If AI fails, check the secret name, Zen credits, and selected model. Switching models does not fix missing captions.
- Read/archive status and theme preferences are saved in your browser. The published video library is shared across devices; your read marks are not synchronized.
- The site contains a `noindex` request, but this is not access control. Do not publish private material in a public repository or website.
- API charges and any GitHub charges depend on your accounts and usage. This template does not promise a free AI service.

## How it works

A manual GitHub workflow installs pinned tools, fetches playlist metadata and captions, then calls the OpenCode CLI with your selected Zen model. OpenCode has tools denied and session sharing disabled; it only returns a summary. Python validates the JSON and chapter timestamps and constructs video URLs independently of model output. Explicit workflow steps save the library and deploy only `public/` to GitHub Pages.

Using the CLI inside Actions avoids the issue/PR behavior of OpenCode's coding-assistant GitHub action. GitHub still provides the manual trigger, secrets, runner, and publishing. No OpenCode GitHub app is needed.

Files:
- `config.json`: playlist, title, caption language, and last-used model.
- `data/videos.json`: saved summaries, metadata, and timestamps.
- `data/state.json`: successfully completed video IDs.
- `transcripts/`: optional manually supplied captions.
- `site/index.html`: searchable library UI, adapted from [vidbot-library](https://github.com/inspiretelapps/vidbot-library).
- `.github/workflows/update-library.yml`: manual update and Pages deployment.

Developer checks: `npm ci`, `python3 -m pip install -r requirements.txt`, `python3 -m unittest discover -s tests -v`, `node --test tests/*.test.mjs`. Render locally with `python3 scripts/render_site.py`. Set `GITHUB_REPOSITORY=owner/repository` to generate a working update link locally. The CI tests use synthetic transcripts and mocked model responses; they do not spend API credits.
