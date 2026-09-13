#!/bin/bash
#
# AI 사용량 카드를 최근 30일 기준으로 다시 만들고, 바뀐 경우에만 커밋·푸시한다.
# launchd(com.joejaeyoung.profile-ai-usage)가 매일 아침 실행한다.
#
#   수동 실행:  ./update-ai-usage.sh
#   로그:       ~/Library/Logs/profile-ai-usage.log
#
set -uo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="$HOME/Library/Logs/profile-ai-usage.log"
WINDOW_DAYS=30

# launchd는 PATH가 거의 비어 있다. 필요한 경로를 직접 넣는다.
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

mkdir -p "$(dirname "$LOG")"
log() { printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >> "$LOG"; }

log "── 시작 (window ${WINDOW_DAYS}일)"
cd "$REPO_DIR" || { log "!! 저장소 디렉터리 없음: $REPO_DIR"; exit 1; }

# 다른 곳에서 먼저 올린 변경이 있을 수 있다
if ! git pull --rebase --quiet origin main 2>>"$LOG"; then
  log "!! pull 실패 — 중단"
  exit 1
fi

TMP="$(mktemp -t ai-usage)"
trap 'rm -f "$TMP"' EXIT

if ! python3 gen_ai_usage.py --days "$WINDOW_DAYS" > "$TMP" 2>>"$LOG"; then
  log "!! 카드 생성 실패 — 기존 파일 유지"
  exit 1
fi

# 빈 출력이나 비정상적으로 작은 결과로 덮어쓰지 않는다
SIZE=$(wc -c < "$TMP" | tr -d ' ')
if [ "$SIZE" -lt 1000 ]; then
  log "!! 생성 결과가 너무 작음 (${SIZE}B) — 중단"
  exit 1
fi

mv "$TMP" ai-usage.svg
trap - EXIT

if git diff --quiet -- ai-usage.svg; then
  log "변화 없음 — 커밋 생략"
  exit 0
fi

git add ai-usage.svg
git commit --quiet -m "chore: AI 사용량 카드 갱신 (최근 ${WINDOW_DAYS}일, $(date '+%Y-%m-%d'))" 2>>"$LOG"

if git push --quiet origin main 2>>"$LOG"; then
  log "갱신 완료 · 푸시됨 (${SIZE}B)"
else
  log "!! 푸시 실패 — 커밋은 로컬에 남아 있음"
  exit 1
fi
