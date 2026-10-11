// typo_tp.js — wsadowe wywołanie tp() z biblioteki typografia-www (typo-biblioteka.js).
// Wejście (stdin): JSON [[klucz_bloku, tekst], …]. Wyjście (stdout): JSON [tekst, …] w tej samej kolejności.
// Stan cudzysłowów (głębokość i poprzedni znak) jest osobny dla każdego bloku, tak jak w przeglądarce (typo.js, run()).
const { tp } = require('./typo-biblioteka.js');

let data = '';
process.stdin.on('data', (c) => { data += c; }).on('end', () => {
  const states = new Map();
  const out = JSON.parse(data).map(([key, text]) => {
    let st = states.get(key);
    if (!st) states.set(key, (st = { d: 0 }));
    return tp(text, st, false);
  });
  process.stdout.write(JSON.stringify(out));
});
