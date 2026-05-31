FROM mcr.microsoft.com/vscode/devcontainers/python:3-3.14

COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /uvx /usr/local/bin/

RUN echo 'eval "$(uv generate-shell-completion bash)"' >> /etc/bash.bashrc
