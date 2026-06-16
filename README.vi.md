<div align="center">
<h1 align="center"> NarratoAI </h1>
<h3>Công cụ AI tất cả trong một cho bình luận phim, cắt ghép video tự động, lồng tiếng và tạo phụ đề.</h3>

<p align="center">
  <a href="README.md">English</a> | <a href="README.vi.md">Tiếng Việt</a> | <a href="https://www.narratoai.cn">☁️ Phiên bản Cloud</a>
</p>

![Home](docs/index-en.png)

</div>

## Tính năng

- **Tạo kịch bản AI** — Viết kịch bản bình luận bằng LLM từ video đầu vào
- **Cắt ghép video tự động** — Chọn, ghép clip và sắp xếp timeline thông minh
- **Lồng tiếng (TTS)** — Nhiều engine: Edge TTS, Azure, Tencent Cloud, IndexTTS (sao chép giọng nói), OmniVoice, DoubaoTTS, Qwen3-TTS
- **Tạo phụ đề** — Tự động tạo và burn-in phụ đề với kiểu dáng tùy chỉnh và che phủ phụ đề gốc
- **Bình luận phim ngắn** — Pipeline riêng cho bình luận phim truyền hình với phân tích cảnh
- **Phân tích khung hình tài liệu** — Trích xuất từng khung hình với vision LLM
- **Chuyển speech thành text (Fun-ASR)** — One-click tạo phụ đề từ giọng nói (local hoặc cloud)
- **Hỗ trợ đa LLM** — OpenAI, DeepSeek, Gemini, Qwen, SiliconFlow và bất kỳ endpoint tương thích OpenAI
- **Giao diện Web** — Streamlit-based cho quản lý dự án, xem trước và xuất file
- **Triển khai Docker** — Setup một lệnh với health check và tự khởi động lại
- **Xuất bản Jianying** — Xuất dự án sang định dạng draft Jianying (CapCut)
- **Tích hợp tìm kiếm** — Tavily web search cho hiểu nội dung phim ngắn

## Yêu cầu hệ thống

| Thành phần | Tối thiểu |
|------------|-----------|
| CPU | 4 lõi |
| RAM | 8 GB |
| GPU | Không bắt buộc |
| OS | Windows 10/11, macOS 11.0+, hoặc Linux |
| Python | 3.12+ |
| FFmpeg | Bắt buộc (cài đặt tự động trong Docker) |

## Bắt đầu nhanh

### Cách 1: Docker (Khuyến nghị)

```bash
git clone https://github.com/linyqh/NarratoAI.git
cd NarratoAI

# Sao chép và chỉnh sửa cấu hình
cp config.example.toml config.toml
# Chỉnh sửa config.toml với API key của bạn (xem phần Cấu hình)

# Khởi động
docker compose up -d

# Truy cập tại http://localhost:8501
```

### Cách 2: Cài đặt cục bộ

```bash
git clone https://github.com/linyqh/NarratoAI.git
cd NarratoAI

# Tạo môi trường ảo (khuyến nghị)
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Cài đặt phụ thuộc
pip install -r requirements.txt

# Sao chép và chỉnh sửa cấu hình
cp config.example.toml config.toml
# Chỉnh sửa config.toml (xem phần Cấu hình)

# Khởi động
streamlit run webui.py --server.maxUploadSize=2048

# Truy cập tại http://localhost:8501
```

## Cấu hình

### config.toml

Sao chép `config.example.toml` thành `config.toml` và điền API key.

#### Cấu hình LLM

```toml
[app]
# Mô hình thị giác — dùng để hiểu khung hình video
vision_llm_provider = "openai"
vision_openai_model_name = "Qwen/Qwen3.5-122B-A10B"
vision_openai_api_key = "your-api-key"
vision_openai_base_url = "https://api.siliconflow.cn/v1"

# Mô hình văn bản — dùng để tạo kịch bản/bình luận
text_llm_provider = "openai"
text_openai_model_name = "Pro/zai-org/GLM-5"
text_openai_api_key = "your-api-key"
text_openai_base_url = "https://api.siliconflow.cn/v1"

# Timeout và retry
llm_vision_timeout = 120
llm_text_timeout = 180
llm_max_retries = 3
```

**Nhà cung cấp LLM được hỗ trợ** (tất cả qua API tương thích OpenAI):

| Nhà cung cấp | Mô hình ví dụ | Base URL |
|---------------|---------------|----------|
| SiliconFlow | Qwen/Qwen3.5-122B-A10B | `https://api.siliconflow.cn/v1` |
| OpenAI | gpt-4o, gpt-4o-mini | `https://api.openai.com/v1` |
| DeepSeek | deepseek-chat, deepseek-reasoner | `https://api.deepseek.com/v1` |
| Gemini | gemini-2.0-flash, gemini-1.5-pro | `https://generativelanguage.googleapis.com/v1beta/openai/` |
| Qwen | qwen-plus, qwen-turbo | `https://dashscope.aliyuncs.com/compatible-mode/v1` |

#### Cấu hình TTS

Chọn một engine trong `[ui]`:

```toml
[ui]
tts_engine = "edge_tts"  # Các tùy chọn: edge_tts, azure_speech, tencent_tts, indextts, indextts2, omnivoice, doubaotts, qwen3_tts

# Edge TTS (miễn phí, không cần API key)
edge_voice_name = "vi-VN-HoaiMyNeural-Female"
edge_volume = 80
edge_rate = 1.0
```

Các engine TTS khác cần API key tương ứng (xem `config.example.toml` để biết đầy đủ tùy chọn).

#### Che phủ phụ đề (Tùy chọn)

```toml
[ui]
subtitle_mask_enabled = true  # Che phụ đề gốc trước khi burn-in phụ đề mới
subtitle_mask_landscape_x_percent = 10
subtitle_mask_landscape_y_percent = 78
subtitle_mask_landscape_width_percent = 80
subtitle_mask_landscape_height_percent = 14
```

#### Cấu hình Proxy

```toml
[proxy]
http = "http://127.0.0.1:7890"
https = "http://127.0.0.1:7890"
enabled = false
```

#### Xử lý video

```toml
[frames]
frame_interval_input = 3       # Giây giữa các lần trích xuất keyframe
vision_batch_size = 10          # Số khung hình mỗi batch LLM
vision_max_concurrency = 2      # Số lượng vision request song song
```

### Biến môi trường

| Biến | Mô tả | Mặc định |
|------|-------|----------|
| `PYTHONUNBUFFERED` | Tắt bộ đệm output Python | `1` |
| `TZ` | Timezone container | `Asia/Shanghai` |

Các biến này đã được cấu hình sẵn trong `docker-compose.yml`.

## Hướng dẫn sử dụng

### 1. Bình luận phim (Phim điện ảnh/Tài liệu)

1. Mở giao diện Web tại `http://localhost:8501`
2. Tải lên file video hoặc cung cấp URL
3. Chọn loại video (phim, tài liệu, v.v.)
4. AI phân tích khung hình và tạo kịch bản bình luận
5. Xem trước và chỉnh sửa kịch bản trong giao diện **Video Review**
6. Chọn engine TTS và giọng nói
7. Nhấn **Generate** — NarratoAI xử lý cắt ghép, lồng tiếng và burn-in phụ đề
8. Tải video hoàn chỉnh hoặc xuất sang draft Jianying

### 2. Bình luận phim ngắn

1. Nhập tên phim ngắn trong tab **Short Drama**
2. Bật tìm kiếm Tavily để hiểu nội dung (tùy chọn)
3. Tải lên các tập phim hoặc cung cấp đường dẫn file
4. NarratoAI ghép cảnh, chuyển speech thành text và tạo bình luận
5. Xem trước và xuất file

### 3. Chuyển speech thành text một chạm (Fun-ASR)

1. Bật `auto_transcribe_enabled = true` trong `config.toml`
2. Đặt `backend` thành `"local"` (cần FunASR-Pack đang chạy) hoặc `"bailian"` (Alibaba cloud)
3. Tải lên video — phụ đề được tự động tạo

## Triển khai Docker

### Docker Compose

```bash
# Build và khởi động
docker compose up -d --build

# Xem log
docker compose logs -f

# Dừng
docker compose down

# Khởi động lại
docker compose restart
```

### Lệnh Make

```bash
make deploy    # Triển khai một lệnh (chạy docker-deploy.sh)
make build     # Build Docker image
make up        # Khởi động dịch vụ
make down      # Dừng dịch vụ
make restart   # Khởi động lại dịch vụ
make logs      # Xem log
make shell     # Vào shell container
make ps        # Kiểm tra trạng thái dịch vụ
make clean     # Dọn dẹp tài nguyên Docker không sử dụng
```

### Volumes

| Container Path | Host Mount | Mục đích |
|----------------|------------|----------|
| `/NarratoAI/storage` | `./storage` | Dữ liệu task, file tạm, kịch bản |
| `/NarratoAI/config.toml` | `./config.toml` | File cấu hình |
| `/NarratoAI/resource` | `./resource` | Audio tham chiếu, tài nguyên |

## Tích hợp với CreatorHub

NarratoAI có thể được tích hợp vào pipeline CreatorHub như một dịch vụ bình luận video:

1. **Tích hợp API** — Sử dụng backend Streamlit theo chương trình với tham số task tùy chỉnh
2. **Storage chia sẻ** — Mount volume `storage/` chung cho quản lý task CreatorHub
3. **Truyền config** — Cấu hình sẵn `config.toml` với API key do CreatorHub quản lý
4. **Docker Network** — Thêm NarratoAI vào mạng Docker CreatorHub cho giao dịch liên service:

```yaml
# Trong docker-compose.yml của CreatorHub
services:
  narratoai:
    image: narratoai:latest
    networks:
      - creatorhub-net

networks:
  creatorhub-net:
    external: true
```

5. **Hàng đợi task** — Đặt định nghĩa task trong `storage/tasks/` để NarratoAI xử lý

## Xử lý sự cố

| Vấn đề | Giải pháp |
|--------|-----------|
| Port 8501 đã bị chiếm | Thay đổi port trong `docker-compose.yml` hoặc dừng service đang dùng port |
| `config.toml not found` | Chạy `cp config.example.toml config.toml` |
| Lỗi API key | Kiểm tra key đúng và còn quota; kiểm tra `base_url` khớp với nhà cung cấp |
| TTS thất bại | Đảm bảo engine TTS đã chọn có thông tin xác thực hợp lệ trong `config.toml` |
| Video quá lớn / tải lên thất bại | Tăng `--server.maxUploadSize` (mặc định 2048 MB) |
| FFmpeg không tìm thấy | Cài FFmpeg (`brew install ffmpeg` / `apt install ffmpeg`) hoặc dùng Docker |
| Xử lý chậm | Giảm `vision_batch_size`, dùng mô hình thị giác nhanh hơn, hoặc tăng `vision_max_concurrency` |
| Docker build thất bại | Chạy `make clean` rồi thử lại; đảm cấp Docker đủ bộ nhớ |
| Health check container thất bại | Kiểm tra log với `docker compose logs narratoai-webui` |
| Lỗi ImageMagick policy | Dockerfile tự sửa policy ImageMagick; nếu chạy cục bộ, chỉnh sửa `/etc/ImageMagick-6/policy.xml` |

### Log

```bash
# Docker
docker compose logs -f narratoai-webui

# Cục bộ
# Log được in ra stdout qua Streamlit
```

## Giấy phép

Dự án này chỉ dùng cho mục đích học tập và nghiên cứu. Không được sử dụng thương mại. Xem chi tiết tại [`LICENSE`](LICENSE).

## Lời cảm ơn

- [MoneyPrinter](https://github.com/FujiwaraChoki/MoneyPrinter)
- [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=linyqh/NarratoAI&type=Date)](https://star-history.com/#linyqh/NarratoAI&Date)
