// エージェントの「次の一手」を Jev に決めさせる。
// state には文字列だけでなくオブジェクトも渡せる。判断だけを Jev に任せ、実行はコード側でやる。
import { experimental_evaluate as evaluate } from 'ai';

const agentState = {
  goal: 'ユーザーの注文 #1234 をキャンセルする',
  toolsTried: ['lookup_order'],
  lastToolResult: { status: 'shipped', shippedAt: '2026-09-16' },
  attempts: 1,
};

const { answers } = await evaluate({
  model: 'typesafe-ai/jev',
  state: agentState,
  questions: {
    nextAction: {
      type: 'choice',
      instructions: '次に取るべき行動は?',
      criteria: {
        cancel_order: 'キャンセル API を呼ぶ(未発送のときだけ可能)',
        start_return: '発送済みなので返品手続きを始める',
        ask_user: 'ユーザーに確認が必要',
        give_up: 'これ以上は無理。停止する',
      },
    },
    needsHuman: {
      type: 'boolean',
      instructions: '人間の担当者にエスカレーションすべきか?',
    },
  },
});

console.log('判断:', answers);

// ここから先は普通のコード。LLM の文章をパースする必要がない。
switch (answers.nextAction.choice) {
  case 'cancel_order':  console.log('→ cancelOrder() を呼ぶ'); break;
  case 'start_return':  console.log('→ startReturn() を呼ぶ'); break;
  case 'ask_user':      console.log('→ ユーザーに質問する'); break;
  case 'give_up':       console.log('→ 停止'); break;
}
if (answers.needsHuman.probability > 0.7) console.log('→ 人間に引き継ぐ');
