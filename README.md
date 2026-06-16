<div align="center">
<h1 align="center"> NarratoAI </h1>
<h3>All-in-one AI tool for film commentary, automated video editing, voice-over, and subtitle generation.</h3>

<p align="center">
  <a href="README.md">English</a> | <a href="README.vi.md">Tiếng Việt</a> | <a href="https://www.narratoai.cn">☁️ Cloud Version</a>
</p>

![Home](docs/index-en.png)

</div>

## Features

- **AI Script Generation** — LLM-powered narration script writing from video input
- **Automated Video Editing** — intelligent clip selection, merging, and timeline assembly
- **Voice-Over (TTS)** — multiple engines: Edge TTS, Azure, Tencent Cloud, IndexTTS (voice cloning), OmniVoice, DoubaoTTS, Qwen3-TTS
- **Subtitle Generation** — auto-generate and burn subtitles with customizable styling and mask overlays
- **Short Drama Commentary** — dedicated pipeline for drama/series commentary with scene analysis
- **Documentary Frame Analysis** — frame-by-frame extraction with vision LLM understanding
- **Fun-ASR Transcription** — one-click speech-to-text for subtitle creation (local or cloud)
- **Multi-LLM Support** — OpenAI, DeepSeek, Gemini, Qwen, SiliconFlow, and any OpenAI-compatible endpoint
- **Web UI** — Streamlit-based interface for project management, preview, and export
- **Docker Deployment** — one-command setup with health checks and auto-restart
- **Jianying Draft Export** — export projects to Jianying (CapCut) draft format
- **Search Integration** — Tavily web search for drama plot understanding

## System Requirements

| Component | Minimum |
|-----------|---------|
| CPU | 4 cores |
| RAM | 8 GB |
| GPU | Not required |
| OS | Windows 10/11, macOS 11.0+, or Linux |
| Python | 3.12+ |
| FFmpeg | Required (installed automatically in Docker) |

## Quick Start

### Option 1: Docker (Recommended)

```bash
git clone https://github.com/linyqh/NarratoAI.git
cd NarratoAI

# Copy and edit configuration
cp config.example.toml config.toml
# Edit config.toml with your API keys (see Configuration section)

# Start
docker compose up -d

# Access at http://localhost:8501
```

### Option 2: Local Installation

```bash
git clone https://github.com/linyqh/NarratoAI.git
cd NarratoAI

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Copy and edit configuration
cp config.example.toml config.toml
# Edit config.toml (see Configuration section)

# Start
streamlit run webui.py --server.maxUploadSize=2048

# Access at http://localhost:8501
```

## Configuration

### config.toml

Copy `config.example.toml` to `config.toml` and fill in your API keys.

#### LLM Configuration

```toml
[app]
# Vision model — used for video frame understanding
vision_llm_provider = "openai"
vision_openai_model_name = "Qwen/Qwen3.5-122B-A10B"
vision_openai_api_key = "your-api-key"
vision_openai_base_url = "https://api.siliconflow.cn/v1"

# Text model — used for script/narration generation
text_llm_provider = "openai"
text_openai_model_name = "Pro/zai-org/GLM-5"
text_openai_api_key = "your-api-key"
text_openai_base_url = "https://api.siliconflow.cn/v1"

# Timeout and retry
llm_vision_timeout = 120
llm_text_timeout = 180
llm_max_retries = 3
```

**Supported LLM providers** (all via OpenAI-compatible API):

| Provider | Example Models | Base URL |
|----------|---------------|----------|
| SiliconFlow | Qwen/Qwen3.5-122B-A10B | `https://api.siliconflow.cn/v1` |
| OpenAI | gpt-4o, gpt-4o-mini | `https://api.openai.com/v1` |
| DeepSeek | deepseek-chat, deepseek-reasoner | `https://api.deepseek.com/v1` |
| Gemini | gemini-2.0-flash, gemini-1.5-pro | `https://generativelanguage.googleapis.com/v1beta/openai/` |
| Qwen | qwen-plus, qwen-turbo | `https://dashscope.aliyuncs.com/compatible-mode/v1` |

#### TTS Configuration

Choose one engine in `[ui]`:

```toml
[ui]
tts_engine = "edge_tts"  # Options: edge_tts, azure_speech, tencent_tts, indextts, indextts2, omnivoice, doubaotts, qwen3_tts

# Edge TTS (free, no API key needed)
edge_voice_name = "zh-CN-XiaoyiNeural-Female"
edge_volume = 80
edge_rate = 1.0
```

Other TTS engines require their respective API keys (see `config.example.toml` for full options).

#### Subtitle Mask (Optional)

```toml
[ui]
subtitle_mask_enabled = true  # Mask original subtitles before burning new ones
subtitle_mask_landscape_x_percent = 10
subtitle_mask_landscape_y_percent = 78
subtitle_mask_landscape_width_percent = 80
subtitle_mask_landscape_height_percent = 14
```

#### Proxy Configuration

```toml
[proxy]
http = "http://127.0.0.1:7890"
https = "http://127.0.0.1:7890"
enabled = false
```

#### Video Processing

```toml
[frames]
frame_interval_input = 3       # Seconds between keyframe extraction
vision_batch_size = 10          # Frames per LLM batch
vision_max_concurrency = 2      # Parallel vision requests
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PYTHONUNBUFFERED` | Disable Python output buffering | `1` |
| `TZ` | Container timezone | `Asia/Shanghai` |

These are pre-configured in `docker-compose.yml`.

## Usage Guide

### 1. Film Commentary (Movie/Documentary)

1. Open the Web UI at `http://localhost:8501`
2. Upload a video file or provide a URL
3. Select the video type (movie, documentary, etc.)
4. The AI analyzes video frames and generates a narration script
5. Review and edit the script in the **Video Review** interface
6. Select TTS engine and voice
7. Click **Generate** — NarratoAI handles editing, voice-over, and subtitle burn-in
8. Download the finished video or export as Jianying draft

### 2. Short Drama Commentary

1. Enter the drama name in the **Short Drama** tab
2. Optionally enable Tavily search for plot understanding
3. Upload episode videos or provide file paths
4. NarratoAI merges scenes, transcribes, and generates commentary
5. Review and export

### 3. One-Click Transcription (Fun-ASR)

1. Enable `auto_transcribe_enabled = true` in `config.toml`
2. Set `backend` to `"local"` (requires FunASR-Pack running) or `"bailian"` (Alibaba cloud)
3. Upload video — subtitles are auto-generated

## Docker Deployment

### Docker Compose

```bash
# Build and start
docker compose up -d --build

# View logs
docker compose logs -f

# Stop
docker compose down

# Restart
docker compose restart
```

### Make Commands

```bash
make deploy    # One-click deploy (runs docker-deploy.sh)
make build     # Build Docker image
make up        # Start service
make down      # Stop service
make restart   # Restart service
make logs      # View logs
make shell     # Enter container shell
make ps        # Check service status
make clean     # Clean unused Docker resources
```

### Volumes

| Container Path | Host Mount | Purpose |
|----------------|------------|---------|
| `/NarratoAI/storage` | `./storage` | Task data, temp files, scripts |
| `/NarratoAI/config.toml` | `./config.toml` | Configuration file |
| `/NarratoAI/resource` | `./resource` | Reference audio, assets |

## Integration with CreatorHub

NarratoAI can be integrated into the CreatorHub pipeline as a video narration service:

1. **API Integration** — Use the Streamlit backend programmatically via `streamlit run` with custom task parameters
2. **Shared Storage** — Mount a shared `storage/` volume for CreatorHub task orchestration
3. **Config Passthrough** — Pre-configure `config.toml` with CreatorHub-managed API keys
4. **Docker Network** — Add NarratoAI to a CreatorHub Docker network for inter-service communication:

```yaml
# In CreatorHub's docker-compose.yml
services:
  narratoai:
    image: narratoai:latest
    networks:
      - creatorhub-net

networks:
  creatorhub-net:
    external: true
```

5. **Task Queue** — Place task definitions in `storage/tasks/` for NarratoAI to pick up

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8501 already in use | Change port in `docker-compose.yml` or stop the conflicting service |
| `config.toml not found` | Run `cp config.example.toml config.toml` |
| API key errors | Verify key is correct and has quota; check `base_url` matches your provider |
| TTS fails | Ensure the selected TTS engine has valid credentials in `config.toml` |
| Video too large / upload fails | Increase `--server.maxUploadSize` (default 2048 MB) |
| FFmpeg not found | Install FFmpeg (`brew install ffmpeg` / `apt install ffmpeg`) or use Docker |
| Slow processing | Reduce `vision_batch_size`, use a faster vision model, or increase `vision_max_concurrency` |
| Docker build fails | Run `make clean` then retry; ensure Docker has enough memory allocated |
| Container health check failing | Check logs with `docker compose logs narratoai-webui` |
| ImageMagick policy error | The Dockerfile patches ImageMagick policy automatically; if running locally, edit `/etc/ImageMagick-6/policy.xml` |

### Logs

```bash
# Docker
docker compose logs -f narratoai-webui

# Local
# Logs are printed to stdout via Streamlit
```

## License

This project is for learning and research purposes only. Commercial use is prohibited. See [`LICENSE`](LICENSE) for details.

## Acknowledgments

- [MoneyPrinter](https://github.com/FujiwaraChoki/MoneyPrinter)
- [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=linyqh/NarratoAI&type=Date)](https://star-history.com/#linyqh/NarratoAI&Date)
