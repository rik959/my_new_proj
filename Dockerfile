FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl fonts-dejavu-core imagemagick \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m eberrik
USER eberrik
WORKDIR /home/eberrik/app

COPY --chown=eberrik:eberrik app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt
ENV PATH="/home/eberrik/.local/bin:${PATH}"

COPY --chown=eberrik:eberrik app/ ./app/
COPY --chown=eberrik:eberrik photos/ ./photos/
COPY --chown=eberrik:eberrik assets/ ./assets/
COPY --chown=eberrik:eberrik anniversary_magazine.pdf ./anniversary_magazine.pdf

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app/love_pipeline.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--browser.gatherUsageStats=false"]
