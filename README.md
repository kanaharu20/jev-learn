# jev-learn

Jev(TypeSafe AI の評価モデル)を Python の標準ライブラリだけで触るための 4 本のスクリプト。
追加インストールは不要。

Jev は文章を生成しない。「状況(state)」と「型付きの質問(questions)」を渡すと、
選択肢・点数・真偽の確率を直接返す。

勉強用のコードです。コピーして自由に使ってください(MIT License)。
発表スライドは [slides/index.html](slides/index.html)(ブラウザで開く)と
[slides/jev-learn.pdf](slides/jev-learn.pdf)(19 枚、1 枚 1280×720)。

## 準備

必要なもの:

- **Python 3.10 以上**(03 が `match` 文を使う。追加ライブラリは不要)
- **Vercel のアカウント**(AI Gateway の API キーを作るため)
- **Node.js**(下の `npx` を使う場合だけ。ダッシュボードでキーを作るなら不要)

### どの OS でも通る方法

API キーを 1 つ作って、環境変数に入れる。

```bash
npx vercel login                       # 初回だけ
npx vercel ai-gateway api-keys create  # 表示されたキーをコピーする
export AI_GATEWAY_API_KEY=...
```

Vercel のダッシュボード(AI Gateway → API Keys)で作っても同じ。
環境変数があれば必ずそちらが使われる。

### macOS の近道

```bash
npx vercel ai-gateway setup
```

キーが Keychain に保存され、各スクリプトが実行時に読む。
`export` もターミナルの再起動も要らない。

ただしこれは本来「ローカルのコーディングエージェント(Claude Code など)を
AI Gateway に接続する」ためのコマンドで、対象のエージェントが入っていないと
うまく進まないことがある。その場合は上の方法を使う。

キーがどちらにも無いときは、使い方を書いたメッセージを出して終了する
(Linux / Windows でもトレースバックにはならない)。

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

## うまくいかないとき

- **`API キーが見つかりません`** … キーをどこにも用意していない。上の「準備」をやる
- **`urllib.error.HTTPError: HTTP Error 401: Unauthorized`** …
  キーが違うか期限切れ。作り直して `AI_GATEWAY_API_KEY` を設定し直す。
  トレースバックが長いが、最後の 1 行だけ見ればいい
- **`npx: command not found`** … Node.js が入っていない。
  ダッシュボードでキーを作って環境変数に入れれば Node.js は要らない
- **`SyntaxError`(03 で `match` の行)** … Python が 3.10 より古い。
  01・02・04 は古い Python でも動く

## 料金

Jev は入力 100 万トークンあたり $0.042、出力は 0。この 4 本を全部動かしても 1 円未満。

## 注意

Jev を呼ぶ HTTP の形(URL とヘッダー)は公式ドキュメント未掲載の内部仕様で、
JavaScript の公式ライブラリが送っているものを写した。Vercel が変える可能性がある。

`confidence` も Vercel の Evaluation ドキュメントには記載がなく、レスポンスを
ダンプして見つけたもの。同じく変わる可能性があるので、`confidences()` は
キーが無ければ空の辞書を返すようにしてある。
