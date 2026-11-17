import fs from 'fs';
const html = fs.readFileSync(new URL('../index.html', import.meta.url),'utf8');
const core = html.split('/* ==== CORE')[1].split('/* ==== END CORE')[0].replace(/^[^\n]*\n/,'');
const { extractPaths } = new Function(core + '; return {extractPaths};')();
const id = 'AHRPTWkXyz0123456789abcdefghijklmnopqrstuvwxyzABC';
const cases = [
  [`https://lh3.googleusercontent.com/grass-cs/${id}=w146-h195-k-no`, [`grass-cs/${id}`]],
  [`https://www.google.com/maps/place/X/@1,2,3a,75y,90t/data=!3m8!1e2!3m6!1s${id}!2e10!3e12!6shttps:%2F%2Flh3.googleusercontent.com%2Fgps-cs-s%2F${id}%3Dw203-h152-k-no!7i4032!8i3024`, [`gps-cs-s/${id}`]],
  [`background-image: url("https://lh3.googleusercontent.com/p/${id}=w203-h152-k-no");`, [`p/${id}`]],
  [`https://lh3.googleusercontent.com/a/${id}=s40 https://lh3.googleusercontent.com/a-/${id}=s40`, []],
  [`gps-cs-s/${id},p/${id}2,gps-cs-s/${id}`, [`gps-cs-s/${id}`, `p/${id}2`]],
  [`"https:\\/\\/lh5.googleusercontent.com\\/p\\/${id}\\u003dw100"`, [`p/${id}`]],
  [`a https://lh3.googleusercontent.com/x/${id}=s0, https://lh3.googleusercontent.com/x/${id}=w10`, [`x/${id}`]],
];
let ok = 0;
for (const [inp, exp] of cases) {
  const got = extractPaths(inp);
  const pass = JSON.stringify(got) === JSON.stringify(exp);
  ok += pass; if (!pass) console.log('FAIL', inp.slice(0,80), '\n got', got, '\n exp', exp);
}
console.log(`${ok}/${cases.length} passed`);
