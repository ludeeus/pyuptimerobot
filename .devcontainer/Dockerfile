FROM mcr.microsoft.com/vscode/devcontainers/base:debian

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /usr/src

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

USER vscode

ENV VIRTUAL_ENV="/home/vscode/.local/venv"
RUN --mount=type=bind,source=.python-version,target=.python-version \
    uv python install \
    && uv venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Shell completion for uv
RUN echo 'eval "$(uv generate-shell-completion bash)"' >> /home/vscode/.bashrc

WORKDIR /workspaces

# Set the default shell to bash instead of sh
ENV SHELL=/bin/bash
