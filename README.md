# jev-learn

Jev(TypeSafe AI の評価モデル)を最小構成で触るための 4 本のスクリプト。

Jev は文章を生成しない。「状況(state)」と「型付きの質問(questions)」を渡すと、
選択肢・点数・真偽の確率を直接返す。

## 準備

キーは `vercel ai-gateway setup` が Keychain に保存済み。`run.sh` が実行時に
Keychain から読むので、`.env` もターミナルの再起動も不要。

```bash
npm install
```

## 順番に動かす

```bash
npm run 1   # 01_hello.mjs          boolean 1 問。返り値の形を見る
npm run 2   # 02_three_types.mjs    boolean / choice / score を 1 回で
npm run 3   # 03_agent_decision.mjs state にオブジェクトを渡し、判断で分岐する
npm run 4   # 04_vs_llm.mjs         同じ分類を LLM と比べる
```

## 見るポイント

- `probability` は 0〜1。しきい値をコード側で決める(03 では 0.7)
- `choice` と `score` には各選択肢の `probabilities` も付く。迷っているかが分かる
- 質問は「詳しい人が数秒で判断できる粒度」に分ける。複雑な判断は複数の質問に分解する
- 型付きで返っても正しい保証はない。重要な判断には人の確認を挟む

## 料金

入力 100 万トークンあたり $0.042。出力トークンは 0。この 4 本を全部動かしても 1 円未満。
