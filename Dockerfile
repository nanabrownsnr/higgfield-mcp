# Stage 1 – build UI
FROM node:20-alpine AS ui-build
WORKDIR /workspace/app/ui/file_dir
COPY app/ui/file_dir/. .
RUN npm install --ignore-engines && \
    npm run build

# Stage 2 – final image  
FROM python:3.12-slim
WORKDIR /app
COPY --from=ui-build /workspace/app/ui/file_dir/dist/ ./dist/
COPY pyproject.toml uv.lock main.py .env.* requirements.txt apps templates .gitignore .dockerignore README.md .
RUN pip install uv && uv sync --no-dev

ENV FASTMCP_LOG_LEVEL=INFO
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
