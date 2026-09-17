// 同じ分類を「Jev」と「普通の LLM」でやって、速度・手間・出力の形を比べる。
import { experimental_evaluate as evaluate, generateText } from 'ai';

const state = '請求書の金額が先月の2倍になっています。理由を教えてください。';
const categories = { billing: '料金・請求', technical: '不具合', sales: '契約相談' };

// --- Jev: 型付きの答えが直接返る ---
let t = Date.now();
const jev = await evaluate({
  model: 'typesafe-ai/jev',
  state,
  questions: {
    category: { type: 'choice', instructions: '問い合わせの種別は?', criteria: categories },
  },
});
console.log(`Jev   ${Date.now() - t}ms →`, jev.answers.category);

// --- LLM: 文章で返るので、パースが必要 ---
t = Date.now();
const llm = await generateText({
  model: 'anthropic/claude-haiku-4-5',
  prompt: `次の問い合わせを ${Object.keys(categories).join(' / ')} のどれかに分類し、キー名だけを答えてください。\n\n${state}`,
});
console.log(`LLM   ${Date.now() - t}ms →`, JSON.stringify(llm.text.trim()));
