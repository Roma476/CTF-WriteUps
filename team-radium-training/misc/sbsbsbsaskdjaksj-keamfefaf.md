# sbsbsbsaskdjaksj keamfefaf

| | |
|---|---|
| **Section** | Misc |
| **Category** | misc |
| **Solves** | 16 |

## Overview

The challenge provides only a YouTube link: `https://www.youtube.com/watch?v=4z3yBjCstj0`. The video is 49 seconds of a cat, and the title is the same gibberish as the challenge name. There is no prompt and no file. The flag is hidden in the video's subtitle track.

## Solve

Open the video on YouTube and enable subtitles. The default English track only shows `[Cat sounds]`, which matches the audio and is a red herring.

The tell is in the subtitle language list: besides English, there is an unexpected **Sanskrit** track. Selecting it and seeking to around **0:25** makes the flag appear as a subtitle line:

```
itsos{████…}
```

No steganography, audio analysis, or frame extraction is needed. The video contains nothing but a cat; the flag lives in an uploaded subtitle track under an obscure language, timed to a specific moment so it is invisible unless that track is selected and the video is played at the right point.