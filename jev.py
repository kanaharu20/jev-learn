"""Jev を呼ぶための共通部品。02 以降はここから import する。
中身は 01_hello.py と同じ。標準ライブラリのみ。"""
import json
import os
import subprocess
import time
import urllib.error
import urllib.request

GATEWAY = "https://ai-gateway.vercel.sh"


def load_api_key():
    """環境変数にあればそれを、なければ macOS の Keychain から読む。"""
    key = os.environ.get("AI_GATEWAY_API_KEY")
    if not key:
        try:
            key = subprocess.run(
                ["/usr/bin/security", "find-generic-password",
                 "-s", "Vercel AI Gateway", "-a", "vercel-ai-gateway", "-w"],
                capture_output=True, text=True,
            ).stdout.strip()
        except FileNotFoundError:
            key = ""  # macOS 以外。Keychain が無いので環境変数で渡してもらう
    if not key:
        raise SystemExit(
            "API キーが見つかりません。\n"
            "  macOS      : npx vercel ai-gateway setup\n"
            "  それ以外の OS: export AI_GATEWAY_API_KEY=..."
        )
    return key


API_KEY = load_api_key()


def _post(path, body, extra_headers):
    req = urllib.request.Request(
        GATEWAY + path,
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {API_KEY}",
                 "Content-Type": "application/json", **extra_headers},
        method="POST",
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req) as res:
                return json.load(res)
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == 3:
                raise
            time.sleep(2 ** attempt)  # 5xx は 1, 2, 4 秒待って再試行


def evaluate(state, questions, model="typesafe-ai/jev"):
    """Jev に state と questions を投げ、レスポンス全体をそのまま返す。
    キーは answers / rounding / usage / warnings / providerMetadata。"""
    return _post(
        "/v4/ai/evaluation-model",
        {"state": state, "questions": questions},
        {"ai-model-id": model,
         "ai-evaluation-model-specification-version": "4",
         "ai-gateway-protocol-version": "0.0.1",
         "ai-gateway-auth-method": "api-key"},
    )


def confidences(result):
    """evaluate の返り値から confidence を {質問名: 0〜1} で取り出す。

    confidence は answers の中ではなく providerMetadata に入っている。
    付くのは choice と score だけで、boolean の質問はキーが入らない
    (質問が boolean だけなら空の辞書が返る)。
    """
    return (result.get("providerMetadata", {})
            .get("typesafe", {})
            .get("confidence", {}))


def chat(prompt, model="anthropic/claude-haiku-4-5"):
    """比較用。普通の LLM に文章を生成させ、返ってきた文字列を返す。"""
    res = _post(
        "/v1/chat/completions",
        {"model": model, "messages": [{"role": "user", "content": prompt}]},
        {},
    )
    return res["choices"][0]["message"]["content"]
