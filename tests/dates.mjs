import fs from 'fs';
const html = fs.readFileSync(new URL('../index.html', import.meta.url),'utf8');
const core = html.split('/* ==== CORE')[1].split('/* ==== END CORE')[0].replace(/^[^\n]*\n/,'');
const { toDate15 } = new Function(core + '; return {toDate15};')();
const now = new Date(2026, 10, 13);   // 13/11/2026
const cases = [
  ['Tháng 5 2024','15/05/2024'], ['tháng 12, 2023','15/12/2023'], ['Thg 3 năm 2025','15/03/2025'],
  ['May 2024','15/05/2024'], ['Aug. 2023','15/08/2023'], ['September 2022','15/09/2022'],
  ['3 tuần trước','15/10/2026'], ['2 tháng trước','15/09/2026'], ['một năm trước','15/11/2025'],
  ['11 months ago','15/12/2025'], ['a year ago','15/11/2025'], ['5 ngày trước','15/11/2026'],
  ['Hôm qua','15/11/2026'], ['20 days ago','15/10/2026'], ['', ''], ['Không rõ', ''],
];
let ok = 0;
for (const [i, e] of cases) { const g = toDate15(i, now); ok += g === e; if (g !== e) console.log('FAIL', JSON.stringify(i), 'got', g, 'exp', e); }
// month overflow: 31/3 minus 1 month must be Feb, not Mar
const g = toDate15('1 tháng trước', new Date(2026, 2, 31)); ok += g === '15/02/2026'; if (g !== '15/02/2026') console.log('FAIL overflow', g);
console.log(`${ok}/${cases.length + 1} passed`);
