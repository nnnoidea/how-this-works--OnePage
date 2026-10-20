// Exercise the distributable folder away from the repository, with two linked pages.
import assert from 'node:assert/strict';
import { cpSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = mkdtempSync(join(tmpdir(), 'htw-package-test-'));
try {
  const skill = resolve(dirname(fileURLToPath(import.meta.url)), '..');
  cpSync(skill, join(root, 'skill'), { recursive: true });
  writeFileSync(join(root, 'impl.py'), 'def run():\n    return "SOURCE_CODE_MARKER"\n');
  writeFileSync(join(root, 'index.md'), '---\ntemplate: doc\ntitle: Overview\n---\n## A Request path\n[Details](details.html#panel-A)\n\n```flow\nRequest -> Worker\nWorker -> Result\n```\n');
  writeFileSync(join(root, 'details.md'), '---\ntemplate: doc\ntitle: Execution\n---\n## A Implementation\n[Overview](index.html#panel-A)\n\n```python src=impl.py lines=1-2\n```\n');
  const originals = ['index.md', 'details.md'].map(f => readFileSync(join(root, f), 'utf8'));
  const render = (input, output, ...options) => spawnSync(process.execPath,
    [join(root, 'skill/scripts/render.mjs'), input, output, ...options], { cwd: root, encoding: 'utf8' });
  for (const name of ['index', 'details']) {
    const result = render(`${name}.md`, `${name}.html`);
    assert.equal(result.status, 0, result.stdout + result.stderr);
  }
  const overview = readFileSync(join(root, 'index.html'), 'utf8');
  const details = readFileSync(join(root, 'details.html'), 'utf8');
  assert.match(overview, /<svg[\s>]/);
  assert.match(overview, /href="details.html#panel-A"/);
  assert.match(details, /href="index.html#panel-A"/);
  for (const page of [overview, details]) {
    assert.match(page, /id="panel-A"/);
    assert.match(page, /id="am-source"/);
    assert.doesNotMatch(page, /<p class="am-colophon">/);
    assert.match(page, /<!-- Answer Me with HTML — retained license/);
    assert.match(page, /Copyright \(c\) 2026 Answer me with HTML contributors/);
    assert.match(page, /Permission is hereby granted, free of charge/);
  }
  assert.match(details, /SOURCE_CODE_MARKER/);
  mkdirSync(join(root, 'snapshot'));
  writeFileSync(join(root, 'snapshot/impl.py'), 'def run():\n    return "FIXED_SOURCE_MARKER"\n');
  const explicit = render('details.md', 'details.html', '--source-dir', 'snapshot');
  assert.equal(explicit.status, 0, explicit.stdout + explicit.stderr);
  assert.match(readFileSync(join(root, 'details.html'), 'utf8'), /FIXED_SOURCE_MARKER/);
  assert.doesNotMatch(readFileSync(join(root, 'details.html'), 'utf8'), /SOURCE_CODE_MARKER/);
  const verifyPages = () => spawnSync('python3', [join(root, 'skill/scripts/check_pages.py'), root], { encoding: 'utf8' });
  assert.equal(verifyPages().status, 0);
  writeFileSync(join(root, 'index.md'), originals[0].replace('details.html#panel-A', 'missing.html#panel-Z'));
  assert.equal(render('index.md', 'index.html').status, 0); // The upstream renderer permits broken links.
  const broken = verifyPages();
  assert.equal(broken.status, 1);
  assert.match(broken.stdout, /Local target does not exist/);
  writeFileSync(join(root, 'index.md'), originals[0]);
  assert.equal(render('index.md', 'index.html').status, 0);
  assert.deepEqual(['index.md', 'details.md'].map(f => readFileSync(join(root, f), 'utf8')), originals);
  assert.notEqual(render('missing.md', 'index.html').status, 0);
  assert.equal(readFileSync(join(root, 'index.html'), 'utf8'), overview);
  assert.notEqual(render('index.md', 'index.html', '--source-dir', 'missing-directory').status, 0);
  assert.equal(readFileSync(join(root, 'index.html'), 'utf8'), overview);
  assert.notEqual(render('index.md', 'index.md').status, 0);
  assert.equal(readFileSync(join(root, 'index.md'), 'utf8'), originals[0]);
  assert.deepEqual(readdirSync(root).sort(), ['details.html', 'details.md', 'impl.py', 'index.html', 'index.md', 'skill', 'snapshot']);
  console.log('Portable package, link verification, explicit source directory, diagrams and failed-render preservation passed.');
} finally {
  rmSync(root, { recursive: true, force: true });
}
