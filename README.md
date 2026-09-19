# jev-learn

Jev(TypeSafe AI の評価モデル)を Python の標準ライブラリだけで触るための 4 本のスクリプト。
追加インストールは不要。

Jev は文章を生成しない。「状況(state)」と「型付きの質問(questions)」を渡すと、
選択肢・点数・真偽の確率を直接返す。

勉強用のコードです。コピーして自由に使ってください(MIT License)。
発表スライドは [slides/index.html](slides/index.html)(ブラウザで開く。1 枚 1280×720)。

## 準備

必要なもの: Python 3.10 以上(03 が `match` 文を使う)、Vercel のアカウント。

**macOS の場合**

```bash
npx vercel ai-gateway setup
```

これで AI Gateway の API キーが Keychain に保存される。
各スクリプトが実行時に Keychain から読むので、`.env` もターミナルの再起動も不要。

**それ以外の OS の場合**

Vercel のダッシュボードで AI Gateway の API キーを作り、環境変数に入れる。
環境変数があればそちらが優先されるので、Keychain は読みに行かない。

```bash
export AI_GATEWAY_API_KEY=...
```

どちらも無いときは、使い方を書いたメッセージを出して終了する(Linux / Windows でも
トレースバックにはならない)。

## 順番に動かす

```bash
python3 01_hello.py            # boolean 1 問。返り値の形を見る。全部この中に書いてある
python3 02_three_types.py      # boolean / choice / score を 1 回で
python3 03_agent_decision.py   # state に辞書を渡し、判断で分岐する
python3 04_vs_llm.py           # 同じ分類を Claude Haiku と比べる
```

`jev.py` は 02 以降が共有する部品(キー取得、`evaluate`、`confidence` を取り出す
`confidences`、比較用の `chat`)。`evaluate` の中身は 01 と同じなので、01 を理解すれば読める。

## 見るポイント

- `probability` は 0〜1。しきい値をコード側で決める(03 では 0.7)
- `choice` と `score` には各選択肢の `probabilities` も付く。迷っているかが分かる
- `score` は段階番号の期待値なので 1.04 のような小数になる
- Jev 自身の確信度 `confidence` は `answers` ではなく
  `providerMetadata.typesafe.confidence` に入っている。`confidences()` で取り出す。
  `choice` と `score` にだけ付き、`boolean` には付かない
- `probabilities` の最上位と `confidence` は別物。曖昧な入力だと最上位 0.51 でも
  `confidence` は 0.26 まで落ちる。`choice` のしきい値はこちらで切るほうが素直(03 では 0.5)
- 確率は `rounding.probabilityDecimals`(実測 2)で丸めて返る。`1.00` は厳密な 1 ではない
- 質問は「詳しい人が数秒で判断できる粒度」に分ける。複雑な判断は複数の質問に分解する
- 型付きで返っても正しい保証はない。重要な判断には人の確認を挟む

## 料金

Jev は入力 100 万トークンあたり $0.042、出力は 0。この 4 本を全部動かしても 1 円未満。

## 注意

Jev を呼ぶ HTTP の形(URL とヘッダー)は公式ドキュメント未掲載の内部仕様で、
JavaScript の公式ライブラリが送っているものを写した。Vercel が変える可能性がある。

`confidence` も Vercel の Evaluation ドキュメントには記載がなく、レスポンスを
ダンプして見つけたもの。同じく変わる可能性があるので、`confidences()` は
キーが無ければ空の辞書を返すようにしてある。
