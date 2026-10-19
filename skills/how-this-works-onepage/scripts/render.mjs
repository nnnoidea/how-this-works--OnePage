#!/usr/bin/env node
import { mkdtempSync, rmSync, statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, extname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const args = process.argv.slice(2);
const usage = 'Usage: node render.mjs DRAFT.md OUTPUT.html [--source-dir DIRECTORY]';
if (args.length === 1 && args[0] === '--help') {
  console.log(usage + '\nRequires Node.js 20+. No browser launch or update check.\nSource-code blocks resolve within --source-dir, or the current directory when omitted.\nThis selects local files; it does not verify their Git revision. Draft/output paths remain relative to the calling directory.');
} else if (![2, 4].includes(args.length) || (args.length === 4 && args[2] !== '--source-dir') || extname(args[1]).toLowerCase() !== '.html') {
  console.error(usage);
  process.exitCode = 2;
} else if (Number(process.versions.node.split('.')[0]) < 20) {
  console.error('Node.js 20 or newer is required.');
  process.exitCode = 2;
} else {
  const renderer = join(dirname(fileURLToPath(import.meta.url)), '../vendor/answer-me-with-html/am.mjs');
  const home = mkdtempSync(join(tmpdir(), 'htw-render-'));
  try {
    const sourceDir = resolve(args[3] ?? process.cwd());
    if (!statSync(sourceDir).isDirectory()) throw new Error('Source directory is not a directory');
    const result = spawnSync(process.execPath,
      [renderer, 'render', resolve(args[0]), '-o', resolve(args[1]), '--no-open'],
      { cwd: sourceDir, stdio: 'inherit', env: { ...process.env, AM_HOME: home, AM_NO_UPDATE_CHECK: '1' } });
    if (result.error) console.error(result.error.message);
    process.exitCode = result.status ?? 1;
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  } finally {
    rmSync(home, { recursive: true, force: true });
  }
}
