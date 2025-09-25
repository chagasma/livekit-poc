# livekit-poc

A proof of concept for LiveKit Voice AI Agent implementation.

## Quick Start

This project includes a Makefile for simplified command execution. Run `make help` to see all available commands.

### Basic Setup

```bash
# Install dependencies and download models
make setup
```

### Running the Agent

```bash
# Development mode
make dev

# Console mode for local testing
make console

# Using Docker
make docker
```

## Detailed Setup

### 1. Environment Configuration

Configure environment variables in `.env` file based on `.env.example`:

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 2. Manual Installation (alternative to `make setup`)

```bash
# Install dependencies
uv sync

# Download model files (one-time setup)
uv run src/main.py download-files
```

## Running Options

The agent uses the `base-stt_llm_tts` session configuration. To change sessions, edit the `session_name` variable in `src/main.py`.

### 1. Development Mode

Connects to LiveKit Cloud, waiting for web/mobile app connections:

```bash
# Using Makefile (recommended)
make dev

# Direct command
uv run src/main.py dev
```

### 2. Console Mode

Local testing with terminal interface. Requires PortAudio for microphone input:

```bash
# Install PortAudio first (Ubuntu/Debian)
sudo apt install portaudio19-dev

# Using Makefile (recommended)
make console

# Direct command
uv run src/main.py console
```

**Console Mode Controls:**

- Press `Ctrl+B` to toggle between Text/Audio mode
- Press `Q` to quit

### 3. Docker Mode

Run the agent in a containerized environment:

```bash
# Using Makefile (recommended)
make docker

# Direct Docker commands
cd docker
docker-compose up --build
```

The Docker setup:

- Uses UV for fast Python package management
- Pre-downloads all required models
- Runs as non-root user for security
- Includes all necessary dependencies

## Maintenance

```bash
# Clean cache and temporary files
make clean
```

## Testing & Documentation

### Performance Analysis

Detailed performance analysis and test results for different STT/LLM/TTS configurations can be found in:

📊 **[docs/docs.md](docs/docs.md)** - Complete analysis of tested configurations including:

- Audio quality comparisons
- STT accuracy for Portuguese
- LLM reasoning capabilities
- Tool execution performance
- Recommended optimal configuration
