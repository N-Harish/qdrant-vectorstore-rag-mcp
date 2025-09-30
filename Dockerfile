# Multi-stage build for MCP Server
# Stage-1
FROM python:3.11.13-alpine3.22 AS builder
WORKDIR /build
COPY requirements.txt .
RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    find /usr/local/lib/python3.11/site-packages -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -type f -name "*.pyc" -delete 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -type f -name "*.pyo" -delete 2>/dev/null || true

# Stage-2 
FROM python:3.11.13-alpine3.22 AS runtime
RUN apk add --no-cache \
    libffi \
    openssl \
    && rm -rf /var/cache/apk/*
WORKDIR /mcp
ENV NOMIC_API_KEY=""
ENV QDRANT_URL=""
ENV QDRANT_API_KEY=""
ENV AUTH0_DOMAIN=""
ENV AUTH0_API_AUDIENCE=""
ENV PYTHONPATH="/mcp:/usr/local/lib/python3.11/site-packages"
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY qdrant_vector_mcp_server.py utils.py ./
EXPOSE 8000
# CMD ["/usr/local/bin/fastmcp", "run", "qdrant_vector_mcp_server.py", "--transport", "http", "--host", "0.0.0.0"]
# CMD ["/usr/local/bin/gunicorn", "--bind", "0.0.0.0:8000", "qdrant_vector_mcp_server:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-", "--capture-output"]
CMD ["uvicorn", "qdrant_vector_mcp_server:app", "--host", "0.0.0.0", "--port", "8000"]
