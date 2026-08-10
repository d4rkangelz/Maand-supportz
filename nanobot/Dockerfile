FROM python:3.12.11-slim-bookworm

ARG NANOBOT_WHEEL_URL="https://files.pythonhosted.org/packages/e0/87/767aeb88ff044da112fb86ffdb92a1f98f79904dc91359ea280297901a8b/nanobot_ai-0.2.2-py3-none-any.whl#sha256=3f71011e2b0b5f97f2480151d013ed167b2163a4d92913d8e00aceafc648a82e"

ENV PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8765

RUN pip install --no-cache-dir "${NANOBOT_WHEEL_URL}"

COPY entrypoint.py /usr/local/bin/railway-nanobot
RUN chmod 0755 /usr/local/bin/railway-nanobot \
    && mkdir -p /root/.nanobot/workspace

VOLUME ["/root/.nanobot"]
EXPOSE 8765

ENTRYPOINT ["python", "/usr/local/bin/railway-nanobot"]

