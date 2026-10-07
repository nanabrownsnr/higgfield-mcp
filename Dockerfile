FROM node:20-alpine AS ui-build
WORKDIR /workspace/app/ui/file_dir
COPY app/ui/file_dir/. .
RUN npm install --ignore-engines && \
    npm run build

FROM python:3.12-slim
WORKDIR /app

# Copy dist from stage 1 - it outputs to ./dist relative to WORKDIR
COPY app/ui/file_dir/dist/ ./dist/
COPY . .

RUN pip install uv && uv sync --no-dev

ENV FASTMCP_LOG_LEVEL=INFO
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
