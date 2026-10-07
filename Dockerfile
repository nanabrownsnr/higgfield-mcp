# Dockerfile
# Stage 1 – build UI
FROM node:20-alpine AS ui-build
WORKDIR /workspace
COPY app/ui/file_dir/package.json app/ui/file_dir/vite.config.js /workspace/app/ui/file_dir/

# Install dependencies and build
RUN cd /workspace/app/ui/file_dir && npm install && npm run build

# Stage 2 – final image
FROM python:3.12-slim
WORKDIR /app

# Install uv for Python dependencies
COPY pyproject.toml .
RUN pip install uv && uv sync --no-dev

# Copy built UI into static dir
COPY --from=ui-build /workspace/app/ui/file_dir/dist/ /app/ui/file_dir/dist

# Copy application code
COPY . .

ENV FASTMCP_LOG_LEVEL=INFO
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]