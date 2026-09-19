# Your own YouSummary library

Turn a YouTube playlist into a searchable website with summaries, takeaways, and timestamped chapters. Updates run only when you ask. GitHub hosts the website and runs OpenCode for you; no computer needs to stay on.

[**Create your own library →**](https://github.com/inspiretelapps/vidbot-template/generate)

New to GitHub? [Start here first](#start-here-if-youre-new-to-github).

## The simple version

**Give it a YouTube playlist. Get your own website with easy-to-read video summaries.** Each summary includes the main takeaways and chapter links that jump to the right moment in the video.

1. **Create a free GitHub account** if you don’t already have one — follow the short guide below.
2. **Make your own copy** using the button above.
3. **Connect the AI** with an OpenCode Zen API key — a private access code that lets the app generate summaries using your account.
4. **Paste your playlist and run an update.** Your website is published for you. Share its link with anyone you want.

You don't need to install anything or leave your computer running. When you want new summaries, click the refresh icon on your site and then **Run workflow** on GitHub.

**You'll need:** a GitHub account, an OpenCode Zen account with access to your chosen model, and a public or unlisted YouTube playlist. You can choose Google Gemini or **DeepSeek V4.1 Flash**. AI usage may cost money. If YouTube blocks captions, you may also need a Supadata account, or you can upload a transcript yourself.

**Your library is public.** Anyone with the link can read it, and the playlist links and saved summaries are visible in your public GitHub copy. Use a playlist you're happy to share.

Prefer some help? Copy the prompt below into ChatGPT or Claude. If your assistant has connected GitHub tools or browser access, it can do the setup work it has permission to do. Otherwise, it can guide you through the clicks.

## Start here if you're new to GitHub

GitHub is the online home for your library. It stores your copy of this project, runs the updates, and publishes your website. You don't need to know how to code to use it.

1. Open [github.com/signup](https://github.com/signup) and follow the steps to create a **free personal account**.
2. Choose a username you'll be happy to see in your website address. For example, a username of `samreads` could give you `samreads.github.io/my-video-library/`.
3. Complete the email verification and any other account checks GitHub asks for. Keep your password and verification codes private.
4. Once you're signed in, come back here and click [**Create your own library**](https://github.com/inspiretelapps/vidbot-template/generate). You can also copy the assistant prompt below and let it guide you from this point.

You don't need GitHub Desktop or any other software installed. The free GitHub plan supports the public setup described here; AI usage and any optional transcript service are separate costs.

A few names you'll see during setup:

- **Repository:** your project's folder on GitHub. Your own copy holds your library's files and settings.
- **Actions:** the page where you start an update and see whether it finished.
- **Pages:** the setting that publishes your library as a website.
- **Secret:** a protected setting for an API key, so the app can use it without showing it publicly.

If you get stuck creating your account, use [GitHub's account setup guide](https://docs.github.com/en/account-and-profile/how-tos/account-management/creating-an-account-on-github). People who only want to read your finished library do **not** need a GitHub account.

## Copy this prompt into ChatGPT or Claude

Copy the whole box and send it as a message. You don't need to change anything first.

```text
Help me set up my own YouSummary website from this template:
https://github.com/inspiretelapps/vidbot-template

I'm not technical. Read the current README and setup files first, then help me get a working website. Use plain language and keep explanations short.

First, ask whether I already have a GitHub account. If not, explain briefly what GitHub is and guide me through creating a free personal account at https://github.com/signup, including email verification. I'll enter passwords and verification codes myself; don't ask me to share them in chat. Don't assume I know terms such as repository, Actions, Pages, or secret — explain each simply when needed.

Once my account is ready, ask me for my GitHub username, my YouTube playlist link, and what I'd like to name my library. Check whether you have tools that can access my GitHub account. If you do, carry out the setup steps your access allows. If you don't, guide me through one small step at a time with clear links and button names. Never claim you changed a setting or deployed something unless you verified it.

Create a new public repository in my account from the template, with an empty library. Work only in my new copy. I understand that the website, playlist links, and saved summaries will be public. If the name is already taken, ask before using an existing repository.

Help me obtain an OpenCode Zen API key and save it as the GitHub repository secret OPENCODE_API_KEY. Don't ask me to paste keys into this chat or into a file; direct me to the secure GitHub settings page. I'll handle sign-in, account creation, and any payment details myself.

Use DeepSeek V4.1 Flash unless I choose a Google Gemini option. Read the exact supported model IDs from the template's current update workflow. Use GitHub Pages for the website, with its publishing source set to GitHub Actions. Keep updates manual; no scheduled jobs or WhatsApp delivery.

Test one video from my playlist first. If YouTube captions fail, explain the issue simply and help me choose between adding a Supadata key as SUPADATA_API_KEY or uploading a transcript. Explain any extra service costs before I enable it. Don't invent a summary when captions are unavailable.

Run the first update when the required settings are ready. Check the run result, open the published website, and verify that a real summary and its chapter links are present. An empty website alone is not a completed test. If your tools cannot perform a step, tell me exactly what to click and continue once I've done it.

Finish by giving me my website link, my GitHub repository link, and a short explanation of how to update my library next time. Clearly state anything that still needs my attention.
```

## Detailed setup and reference

The sections below explain the individual settings and provide troubleshooting help. You can use them yourself or let your assistant follow them.

## Set up once — no coding

Before you begin, sign in to GitHub. If you haven't created an account yet, follow [the beginner guide above](#start-here-if-youre-new-to-github).

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
