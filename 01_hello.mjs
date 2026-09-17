// 最初の 1 回。boolean 質問を 1 つだけ投げて、返ってきたものを丸ごと見る。
import { experimental_evaluate as evaluate } from 'ai';

const result = await evaluate({
  model: 'typesafe-ai/jev',
  state: 'サポート担当者は顧客に全額返金を実施した。',
  questions: {
    refunded: { type: 'boolean', instructions: '返金は行われたか?' },
  },
});

console.log(JSON.stringify(result.answers, null, 2));
console.log('usage:', result.usage);
