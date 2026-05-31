FROM mcr.microsoft.com/vscode/devcontainers/base:debian@sha256:a07f1804d8e665ff64bf6adcd60f4d9b9223dc52ee18a1f1a7a8e1ee1a134d34

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /usr/src

COPY --from=ghcr.io/astral-sh/uv:0.8.22@sha256:9874eb7afe5ca16c363fe80b294fe700e460df29a55532bbfea234a0f12eddb1 /uv /uvx /usr/local/bin/

USER vscode

ENV VIRTUAL_ENV="/home/vscode/.local/pyuptimerobot-venv"
RUN --mount=type=bind,source=.python-version,target=.python-version \
    uv python install \
    && uv venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /workspaces

# Set the default shell to bash instead of sh
ENV SHELL=/bin/bash
