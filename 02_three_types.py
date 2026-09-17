"""3 種類の質問 (boolean / choice / score) を 1 リクエストで並列に評価する。
実行: python3 02_three_types.py"""
from jev import evaluate

state = "3日前から Stripe 連携がずっと失敗しています。売上が止まっていて困っています。至急お願いします。"

result = evaluate(state, {
    "isUrgent": {
        "type": "boolean",
        "instructions": "この問い合わせは緊急か?",
    },
    "department": {
        "type": "choice",
        "instructions": "どのチームが対応すべきか?",
        "criteria": {
            "billing": "料金・請求・返金の話",
            "technical": "不具合や連携の問題",
            "sales": "価格や契約の相談",
        },
    },
    "frustration": {
        "type": "score",
        "instructions": "顧客の苛立ちの度合い",
        "criteria": ["落ち着いている", "困っているが丁寧", "かなり怒っている"],
    },
})

for name, answer in result["answers"].items():
    print(f"\n{name}: {answer}")
