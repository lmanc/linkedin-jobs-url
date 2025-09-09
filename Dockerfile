FROM debian:bookworm-slim AS base

FROM base AS builder
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_INSTALL_DIR=/python \
    UV_PYTHON_PREFERENCE=only-managed
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN uv python install 3.13
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

FROM builder AS tester
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked && \
    uv run pytest -q

FROM base
RUN useradd --uid 10001 --home-dir /app/ app
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"
COPY --from=builder /python/ /python/
COPY --from=builder --chown=app:app /app/.venv/ /app/.venv/
COPY --from=builder --chown=app:app /app/src/ /app/src/
COPY --from=builder --chown=app:app --chmod=u+x /app/start.sh /app/start.sh
USER app
ENTRYPOINT []
CMD ["/app/start.sh"]
