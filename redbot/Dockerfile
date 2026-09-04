FROM python:3.11.13-slim-bookworm

ARG REDBOT_WHEEL_URL="https://files.pythonhosted.org/packages/00/b2/a5f5c3ec9e61c26c6e792bc041586f1b5e78f8b5412d88d9877304b36062/red_discordbot-3.5.24-py3-none-any.whl#sha256=3cbdbdd8bb0b6dbab1f5f909151f12dcd40798b06df8beb791fd22b9e1b2c8bd"

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8080 \
    DISCORD_PREFIX=!

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git libffi-dev libssl-dev \
    && pip install --no-cache-dir "${REDBOT_WHEEL_URL}" \
    && apt-get purge -y --auto-remove build-essential libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.py supervisor.py /usr/local/lib/railway-redbot/
RUN chmod 0755 /usr/local/lib/railway-redbot/entrypoint.py \
    && mkdir -p /data

EXPOSE 8080

ENTRYPOINT ["python", "/usr/local/lib/railway-redbot/entrypoint.py"]

