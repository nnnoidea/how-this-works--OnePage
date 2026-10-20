import { readFileSync, writeFileSync } from 'node:fs';

const license = readFileSync(new URL('../vendor/answer-me-with-html/LICENSE', import.meta.url), 'utf8');
const marker = '<!-- Answer Me with HTML — retained license';

export function finishPage(path) {
  let html = readFileSync(path, 'utf8');
  html = html.replace(/(<header class="am-head">)<p class="am-colophon">[\s\S]*?<\/p>/g, '$1');
  if (!html.includes(marker)) {
    html = html.replace('</head>', `${marker}\nhttps://github.com/QingYunA/answer-me-with-html\n${license}\n-->\n</head>`);
  }
  writeFileSync(path, html);
}
