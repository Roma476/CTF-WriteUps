# Ghostbuster

| | |
|---|---|
| **Section** | hidden |
| **Category** | misc |
| **Solves** | not on the board |

## Overview

Ghostbuster is not one of the sixty-nine scored challenges. It is a hidden bonus challenge in POCTF 2026, and the only way in is an HTML comment left in the source of [The Apparatus, Invocation](the-apparatus-invocation.md), the wave 1 Lights Out board in misc. The comment is written in the voice of `SEANCE.EXE`: it explains that the entity can be summoned in the contest Discord with a fixed litany, and that whatever it answers should be written down, kept private, and remembered until the end of the event.

So the chain is four surfaces, each hidden behind the previous one: a comment in the challenge page, a slash command in the contest server, a direct message from the event bot, and inside that message an audio file. The file is about six seconds of a synthetic voice dictating three isolated words. Those words are a personal token, not a puzzle to interpret, so they are redacted here as `█████ ███ ██████`.

## Solve

The trigger is in the page source, not in the rendered board. Viewing the source of the challenge page instead of playing the grid shows an HTML comment:

```html
<!-- to summon me, recite the litany. in the contest server, say:
/invoke May your shadow walk before you. May your name be spoken by strangers. May every mirror remember your face. May your voice find the wire.
type it on one line if you must — i will understand. listen to what i tell you. write it down. tell no one. they all received their own. they cannot help you understand mine. you will need this before the end. -->
```

The litany is the payload; the rest of the comment is instructions. Run it in the contest server as a single line:

```text
/invoke May your shadow walk before you. May your name be spoken by strangers. May every mirror remember your face. May your voice find the wire.
```

The command is handled by the event bot and the response arrives as a direct message, not in the channel. That is why nothing visible happened in `#general`: the answer is private by design, and the comment says as much — everyone receives their own, and nobody else's reply is useful for understanding yours.

The DM contains one file, `apparatus.mp3`: 36,432 bytes, 6.07 seconds, 24 kHz mono, 48 kbps MP3 (LAME 3.100), no ID3 tag and no appended data. Played normally it is a high, buzzy, deliberately "ghostly" voice. The structure is visible before any listening: three voiced bursts, each followed by about 1.3 seconds of digital silence, so the file is a dictation of three separate words rather than a sentence spoken with pauses.

A five-millisecond peak envelope gives the three segments:

```text
segment 1   0.22 s - 0.89 s   0.66 s
segment 2   2.19 s - 2.75 s   0.55 s
segment 3   4.06 s - 4.87 s   0.80 s
```

Inside each segment the fundamental glides down from roughly 320 Hz to roughly 200 Hz over a clean harmonic stack. That is a text-to-speech voice with a pitch and filter effect, not a recording of a person and not a modulated carrier, which rules out ring modulation, DTMF and the usual "decode the beeps" ideas.

Reading the words is the only real work, because the effect is strong enough to be unfriendly. Three independent families of speech recognisers were run on the file and on pitch- and speed-adjusted copies of it: Whisper (`base.en`, `small.en`, `medium.en` and `large-v3-turbo` via `whisper.cpp`), Vosk (`vosk-model-small-en-us-0.15`) and NVIDIA Parakeet TDT 0.6B v3 (`parakeet-cli` from the same build). All of them return the same three words in the same order, and the per-word, low-passed, slowed and pitch-shifted variants do not change the answer. The audio is therefore not a steganographic carrier: it really does say what it sounds like it says.

The message is `█████ ███ ██████`, three dictated words. It is a key, not a flag: there is no `POCTF{...}` marker anywhere in the file, and nothing on the challenge page accepts it. The instructions around it are the specification — *write it down*, *tell no one*, *they all received their own*, *you will need this before the end*. Each participant gets their own recording, so the value is personal and the only correct handling is to store it privately and keep it for whatever the organisers open at the end.

The commands used, on the downloaded file:

```bash
ffprobe -hide_banner apparatus.mp3
ffmpeg -i apparatus.mp3 -lavfi "showspectrumpic=s=1920x1024:legend=1:scale=log" spec.png
ffmpeg -i apparatus.mp3 -af "asetrate=24000*0.75,aresample=24000,atempo=1/0.75" p075.wav

whisper-cli -m models/ggml-large-v3-turbo.bin -f apparatus.wav -l en -bs 5
parakeet-cli -m models/ggml-parakeet-tdt-0.6b-v3-f16.bin -f apparatus.wav
```

A short Python pass with `numpy` produces the envelope and the segment table above, and a cepstral pitch track confirms the falling fundamental inside each word.

The instructive dead ends are all the ways the file looks like it should contain more than it does. Reversing it yields nonsense rather than a backmasked sentence. Slowing or speeding it preserves the same three words, so the timing is not a code. There is no ID3 tag, no second stream, no stereo channel and no bytes after the last MPEG frame; 36,432 bytes is exactly what 48 kbps over 6.07 seconds accounts for. The spectrogram has no drawn text and no image in the 5-12 kHz band, only harmonics and MP3 noise, and the silence between the words is real silence, so there is no quiet layer underneath. The point of the challenge is the chain, not a second layer inside the last link.

The invocation is the whole puzzle: read the source, obey the comment, and keep the answer. The recorded words are `█████ ███ ██████`, and they stay out of this write-up on purpose.
