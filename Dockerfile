# Dockerfile
# Stage 1 – build UI
FROM node:20-alpine AS ui-build
WORKDIR /workspace
COPY app/ui/file_dir/package.json app/ui/file_dir/vite.config.js /workspace/app/ui/file_dir/
RUN cd /workspace/app/ui/file_dir && npm ci && npm run build

# Stage 2 – final image
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv pip install --no-cache-dir -r uv.lock
COPY . .
# Copy built UI into static directory
COPY --from=ui-build /workspace/app/ui/file_dir/dist/ /app/ui/file_dir/dist
ENV FASTMCP_LOG_LEVEL=INFO
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
