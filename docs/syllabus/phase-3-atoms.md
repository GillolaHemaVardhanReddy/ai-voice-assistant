# Phase 3 — The EARS (Speech-to-Text)

Goal: turn microphone audio into text. Easy hosted win first, then free local Whisper. 🔧 = open-the-hood atom.

| Atom | Idea you'll learn | What you'll do | You'll end up with |
|------|-------------------|----------------|--------------------|
| **3.0 🔧** | Sound = an array of numbers (samples, sample rate) | Look at raw audio numbers | Audio demystified |
| **3.1** | Recording from the mic | Capture a 5-sec clip, save `.wav` | Your own audio file |
| **3.2 🔧** | Whisper = audio → mel spectrogram → **transformer** | Read the intuition + a visual ref | Meet a transformer live |
| **3.3** | Fast win: hosted transcription | Send the clip, get text | Speech → text working |
| **3.4** | Free & local | Install `faster-whisper`, transcribe | No per-minute bill |
| **3.5** | The money math | Hosted $/min vs local (free) | A cost decision |
| **3.6** | Wrap it up | A `listen()` → returns text | **Reusable "ears"** |
