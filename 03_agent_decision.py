"""エージェントの「次の一手」を Jev に決めさせる。
state には文字列だけでなく辞書も渡せる。判断だけを Jev に任せ、実行はコード側でやる。
迷っている判断で動かないように、choice の confidence でしきい値を切る。
実行: python3 03_agent_decision.py"""
from jev import confidences, evaluate

agent_state = {
    "goal": "ユーザーの注文 #1234 をキャンセルする",
    "toolsTried": ["lookup_order"],
    "lastToolResult": {"status": "shipped", "shippedAt": "2026-09-16"},
    "attempts": 1,
}

# 下のガードが働くところを見たいときは、こちらに差し替える。
# 注文の状態が分からないので判断が 3 つに割れ、confidence が 0.3 前後まで落ちる。
# 最上位は cancel_order だが確率は約 0.49。この程度の根拠で課金 API を呼ぶのは危ない。
# agent_state = {
#     "goal": "ユーザーの注文 #1234 をキャンセルする",
#     "toolsTried": ["lookup_order", "lookup_order", "cancel_order"],
#     "lastToolResult": {"status": "unknown", "error": "timeout"},
#     "attempts": 3,
# }

result = evaluate(agent_state, {
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
})

answers = result["answers"]
conf = confidences(result)  # choice の nextAction にだけ付く

print("判断:", answers)
print("confidence:", conf)

# ここから先は普通のコード。LLM の文章をパースする必要がない。
# confidence が低い = 選択肢の間で迷っている。迷ったまま副作用のある API を呼ばない。
# 取れなかったときは 0.0 として扱う。分からないなら動かない、が安全側。
if conf.get("nextAction", 0.0) < 0.5:
    print(f"→ confidence が {conf.get('nextAction')} と低い。実行せず確認に回す")
else:
    match answers["nextAction"]["choice"]:
        case "cancel_order": print("→ cancel_order() を呼ぶ")
        case "start_return": print("→ start_return() を呼ぶ")
        case "ask_user":     print("→ ユーザーに質問する")
        case "give_up":      print("→ 停止")

# boolean には confidence が付かないので、こちらは probability でしきい値を切る。
if answers["needsHuman"]["probability"] > 0.7:
    print("→ 人間に引き継ぐ")
