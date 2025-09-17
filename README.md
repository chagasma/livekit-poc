# livekit-poc

A proof of concept for LiveKit Voice AI Agent implementation.

## Setup

1. Install dependencies:

```bash
uv sync
```

2. Configure environment variables in `.env` file:

```bash
DEEPGRAM_API_KEY=your_deepgram_key
OPENAI_API_KEY=your_openai_key
CARTESIA_API_KEY=your_cartesia_key
LIVEKIT_API_KEY=your_livekit_key
LIVEKIT_API_SECRET=your_livekit_secret
LIVEKIT_URL=wss://your-url.livekit.cloud
```

3. Download model files (one-time setup):

```bash
uv run src/main.py download-files
```

## Running the Agent

### Development Mode

Runs the agent and connects to LiveKit Cloud, waiting for web/mobile app connections:

```bash
uv run src/main.py dev
```

### Console Mode

Runs the agent locally with terminal interface for testing. Requires PortAudio for microphone input:

```bash
# Install PortAudio first (Ubuntu/Debian):
sudo apt install portaudio19-dev

# Run console mode:
uv run src/main.py console
```

In console mode:

- Press `Ctrl+B` to toggle between Text/Audio mode
- Press `Q` to quit

## Features

- Speech-to-Text using Deepgram Nova-3
- Large Language Model using OpenAI GPT-4o-mini
- Text-to-Speech using Cartesia Sonic-2
- Voice Activity Detection using Silero VAD
- Noise cancellation and turn detection
- Multilingual support