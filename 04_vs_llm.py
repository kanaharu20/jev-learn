"""同じ分類を「Jev」と「普通の LLM」でやって、速度・手間・出力の形を比べる。
実行: python3 04_vs_llm.py"""
import time
from jev import chat, confidences, evaluate

state = "請求書の金額が先月の2倍になっています。理由を教えてください。"
categories = {"billing": "料金・請求", "technical": "不具合", "sales": "契約相談"}

# --- Jev: 型付きの答えが直接返る ---
t = time.time()
jev = evaluate(state, {
    "category": {"type": "choice", "instructions": "問い合わせの種別は?", "criteria": categories},
})
print(f"Jev  {int((time.time() - t) * 1000)}ms →", jev["answers"]["category"])
print("      confidence →", confidences(jev).get("category"))  # 迷っていれば下がる

# --- LLM: 文章で返るので、パースが必要 ---
t = time.time()
text = chat(f"次の問い合わせを {' / '.join(categories)} のどれかに分類し、キー名だけを答えてください。\n\n{state}")
print(f"LLM  {int((time.time() - t) * 1000)}ms →", repr(text.strip()))
