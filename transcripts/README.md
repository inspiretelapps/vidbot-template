# When YouTube does not supply captions

The app tries `youtube-transcript`, then yt-dlp, then optional Supadata if its key is configured. YouTube may block cloud runners or a video may have no available captions. A failed video is never marked complete or summarized from its title alone.

You can supply a transcript yourself:

1. Obtain a timestamped transcript for a video you can access.
2. Create a file named `VIDEO_ID.json`, replacing VIDEO_ID with the 11-character ID after `v=` in the video's YouTube link.
3. In this folder on GitHub, choose **Add file → Upload files**, upload it and commit the change.
4. Run **Update library** again. Uploaded transcripts are tried first.

Use an array like this (timestamps and durations are in **seconds**):

```json
[
  {"start_seconds": 0, "duration": 8, "text": "The actual words spoken at the beginning."},
  {"start_seconds": 8, "duration": 12, "text": "The next actual portion of the transcript."}
]
```

Do not upload this example as if it were a real transcript. Uploaded files are visible to anyone who can read your repository. They are not copied into the website. Automatic speech-to-text is not included in this version.
