# jev-learn

Jev(TypeSafe AI の評価モデル)を Python の標準ライブラリだけで触るための 4 本のスクリプト。
追加インストールは不要。

Jev は文章を生成しない。「状況(state)」と「型付きの質問(questions)」を渡すと、
選択肢・点数・真偽の確率を直接返す。

## 準備

API キーは `vercel ai-gateway setup` が macOS の Keychain に保存済み。
各スクリプトが実行時に Keychain から読むので、`.env` もターミナルの再起動も不要。

## 順番に動かす

```bash
python3 01_hello.py            # boolean 1 問。返り値の形を見る。全部この中に書いてある
python3 02_three_types.py      # boolean / choice / score を 1 回で
python3 03_agent_decision.py   # state に辞書を渡し、判断で分岐する
python3 04_vs_llm.py           # 同じ分類を Claude Haiku と比べる
```

`jev.py` は 02 以降が共有する部品(キー取得、`evaluate`、比較用の `chat`)。
中身は 01 と同じなので、01 を理解すれば読める。

## 見るポイント

- `probability` は 0〜1。しきい値をコード側で決める(03 では 0.7)
- `choice` と `score` には各選択肢の `probabilities` も付く。迷っているかが分かる
- `score` は段階番号の期待値なので 1.04 のような小数になる
- 質問は「詳しい人が数秒で判断できる粒度」に分ける。複雑な判断は複数の質問に分解する
- 型付きで返っても正しい保証はない。重要な判断には人の確認を挟む

## 料金

Jev は入力 100 万トークンあたり $0.042、出力は 0。この 4 本を全部動かしても 1 円未満。

## 注意

Jev を呼ぶ HTTP の形(URL とヘッダー)は公式ドキュメント未掲載の内部仕様で、
JavaScript の公式ライブラリが送っているものを写した。Vercel が変える可能性がある。
