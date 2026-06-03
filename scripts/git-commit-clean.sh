#!/usr/bin/env bash
# 以 nasircy 身分提交
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

if [ $# -lt 1 ]; then
  echo "用法: $0 \"commit 訊息\"" >&2
  exit 1
fi

MSG="$1"
export GIT_AUTHOR_NAME="nasircy"
export GIT_AUTHOR_EMAIL="238443453+nasircy@users.noreply.github.com"
export GIT_COMMITTER_NAME="nasircy"
export GIT_COMMITTER_EMAIL="238443453+nasircy@users.noreply.github.com"

git add -A
git commit -m "$MSG"

if git log -1 --format=%B | grep -q 'Co-authored-by: Cursor <cursoragent@cursor.com>'; then
  echo "正在修正最後一筆 commit…" >&2
  TREE=$(git write-tree)
  PARENT=$(git rev-parse HEAD^)
  NEW=$(printf '%s\n' "$MSG" | GIT_AUTHOR_NAME="$GIT_AUTHOR_NAME" GIT_AUTHOR_EMAIL="$GIT_AUTHOR_EMAIL" \
    GIT_COMMITTER_NAME="$GIT_COMMITTER_NAME" GIT_COMMITTER_EMAIL="$GIT_COMMITTER_EMAIL" \
    git commit-tree "$TREE" -p "$PARENT")
  git reset --hard "$NEW"
fi

git log -1 --format='%h %an <%ae>%n%B'
