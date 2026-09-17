"""エージェントの「次の一手」を Jev に決めさせる。
state には文字列だけでなく辞書も渡せる。判断だけを Jev に任せ、実行はコード側でやる。
実行: python3 03_agent_decision.py"""
from jev import evaluate

agent_state = {
    "goal": "ユーザーの注文 #1234 をキャンセルする",
    "toolsTried": ["lookup_order"],
    "lastToolResult": {"status": "shipped", "shippedAt": "2026-09-16"},
    "attempts": 1,
}

answers = evaluate(agent_state, {
    "nextAction": {
        "type": "choice",
        "instructions": "次に取るべき行動は?",
        "criteria": {
            "cancel_order": "キャンセル API を呼ぶ(未発送のときだけ可能)",
            "start_return": "発送済みなので返品手続きを始める",
            "ask_user": "ユーザーに確認が必要",
            "give_up": "これ以上は無理。停止する",
        },
    },
    "needsHuman": {
        "type": "boolean",
        "instructions": "人間の担当者にエスカレーションすべきか?",
    },
})["answers"]

print("判断:", answers)

# ここから先は普通のコード。LLM の文章をパースする必要がない。
match answers["nextAction"]["choice"]:
    case "cancel_order": print("→ cancel_order() を呼ぶ")
    case "start_return": print("→ start_return() を呼ぶ")
    case "ask_user":     print("→ ユーザーに質問する")
    case "give_up":      print("→ 停止")

if answers["needsHuman"]["probability"] > 0.7:
    print("→ 人間に引き継ぐ")
