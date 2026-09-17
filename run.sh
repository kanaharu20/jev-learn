#!/bin/sh
# Keychain から AI Gateway のキーを読んで node を起動する。
# 環境変数 AI_GATEWAY_API_KEY が既にあればそれを使う。
if [ -z "$AI_GATEWAY_API_KEY" ]; then
  AI_GATEWAY_API_KEY="$(/usr/bin/security find-generic-password -s 'Vercel AI Gateway' -a 'vercel-ai-gateway' -w 2>/dev/null)"
  export AI_GATEWAY_API_KEY
fi
if [ -z "$AI_GATEWAY_API_KEY" ]; then
  echo "AI_GATEWAY_API_KEY が見つかりません。npx vercel ai-gateway setup を再実行してください。" >&2
  exit 1
fi
exec node "$@"
