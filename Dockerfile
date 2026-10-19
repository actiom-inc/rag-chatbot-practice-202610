# RAGハンズオン用実行環境。Python/uvはホスト側に不要。
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    HF_HOME=/models \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# sentence-transformers / PyTorch のCPU実行に必要なランタイムを導入
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir "uv==0.12.10"

# 依存パッケージはDocker build時に導入。実行時はuv sync不要。
COPY pyproject.toml ./
RUN uv sync --no-dev --no-install-project \
    && rm -rf /root/.cache/uv

RUN useradd --create-home --uid 1000 workshop \
    && mkdir -p /models /app/.data \
    && chown -R workshop:workshop /models /app /opt/venv

# .dockerignoreで.envなどを除外する。Compose実行時はリポジトリをbind mount。
COPY --chown=workshop:workshop . .

USER workshop
EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
