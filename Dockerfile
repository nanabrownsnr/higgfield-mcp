# Stage 1 – build UI
FROM node:20-alpine AS ui-build
WORKDIR /workspace/app/ui/file_dir
COPY app/ui/file_dir/package.json index.html src package-lock.json vite.config.js ./
RUN npm install --ignore-engines && npm run build

# Stage 2 – final image  
FROM python:3.12-slim
WORKDIR /app
COPY --from=ui-build /workspace/app/ui/file_dir/dist/ ./dist/
COPY pyproject.toml uv.lock main.py .gitignore .dockerignore README.md LICENSE tests/ AGENTS.md CHANGELOG.md IMPROVEMENTS.md docker-compose.yml license.py usage.py auth.py config.py twynity.py core routers models api/ ./

RUN pip install uv && uv sync --no-dev

ENV FASTMCP_LOG_LEVEL=INFO
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
