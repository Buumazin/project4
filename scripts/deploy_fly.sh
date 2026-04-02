#!/usr/bin/env bash
set -e

# Build docker image
docker build -t finally:latest .

# Login to fly (requires flyctl installed, already authed)
# flyctl auth login

# Create fly app if not created
# flyctl apps create finally || true

# Deploy to fly
flyctl deploy --config fly.toml --remote-only
