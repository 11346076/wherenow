#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
chmod +x .githooks/prepare-commit-msg .githooks/commit-msg
git config core.hooksPath .githooks
echo "已啟用 .githooks"
