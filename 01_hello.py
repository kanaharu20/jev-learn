"""01_hello.mjs の Python 版。追加ライブラリなし(標準ライブラリのみ)。
実行: python3 01_hello.py

AI SDK が裏で送っている HTTP リクエストをそのまま自分で送る。
  POST https://ai-gateway.vercel.sh/v4/ai/evaluation-model
  ヘッダー: Authorization, ai-model-id, バージョン指定が 2 つ
  本文:     { "state": ..., "questions": {...} }
"""
import json
import os
import subprocess
import urllib.request


def load_api_key():
    """環境変数にあればそれを、なければ macOS の Keychain から読む。"""
    key = os.environ.get("AI_GATEWAY_API_KEY")
    if not key:
        key = subprocess.run(
            ["/usr/bin/security", "find-generic-password",
             "-s", "Vercel AI Gateway", "-a", "vercel-ai-gateway", "-w"],
            capture_output=True, text=True,
        ).stdout.strip()
    if not key:
        raise SystemExit("API キーが見つかりません。npx vercel ai-gateway setup を再実行してください。")
    return key


API_KEY = load_api_key()


def evaluate(model, state, questions):
    req = urllib.request.Request(
        "https://ai-gateway.vercel.sh/v4/ai/evaluation-model",
        data=json.dumps({"state": state, "questions": questions}).encode(),
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "ai-model-id": model,
            "ai-evaluation-model-specification-version": "4",
            "ai-gateway-protocol-version": "0.0.1",
            "ai-gateway-auth-method": "api-key",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as res:
        return json.load(res)


result = evaluate(
    model="typesafe-ai/jev",
    state="サポート担当者は顧客に全額返金を実施した。",
    questions={
        "refunded": {"type": "boolean", "instructions": "返金は行われたか?"},
    },
)

print(json.dumps(result["answers"], indent=2, ensure_ascii=False))
print("usage:", result.get("usage"))
