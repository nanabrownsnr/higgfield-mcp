# Dockerfile
FROM node:20-alpine AS ui-build
WORKDIR /workspace/app/ui/file_dir
COPY . .
RUN npm install --ignore-engines && \
    (npm run build || exit 1)

FROM python:3.12-slim
WORKDIR /app
COPY --from=ui-build /workspace/app/ui/file_dir/dist/ ./dist/
COPY pyproject.toml uv.lock requirements.txt main.py .
RUN pip install uv && uv sync --no-dev
COPY app main
ENV FASTMCP_LOG_LEVEL=INFO
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]