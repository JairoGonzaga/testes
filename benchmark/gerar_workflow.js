export const meta = {
  name: 'bench-haiku-testgen',
  description: 'SWT-Bench + TestGenEval adaptados: gera testes com Haiku (210 tarefas, 3 amostras cada)',
  phases: [
    { title: 'SWT ZeroShot', detail: '23 issues x 3 amostras, sem ferramentas', model: 'haiku' },
    { title: 'SWT Agente', detail: '23 issues x 3 amostras, sandbox com pytest', model: 'haiku' },
    { title: 'TGE', detail: 'full/first/last/extra x 6 funções x 3 amostras', model: 'haiku' },
  ],
}

const ROOT = args.root            // .../repo/benchmark
const SB = args.sandbox_root
const N = args.samples
const USER_REQ = 'Use o SWT-Bench e TestGenEval para fazer um benchmark https://github.com/JairoGonzaga/testes nesse projeto, usando apenas o haiku por enqt'
const SCHEMA = {
  type: 'object',
  properties: {
    code: { type: 'string', description: 'the complete Python code requested, without markdown fences' },
    note: { type: 'string', description: 'one short sentence' },
  },
  required: ['code'],
}

function promptSemFerramentas(promptPath) {
  return `You are taking part in an automated test-generation benchmark.

Use the Read tool to read exactly ONE file: ${promptPath}
That file contains your entire task. Do NOT read any other file, do NOT search, do NOT run any command and do NOT write any file: answer only from the content of that one file, as if it were the whole prompt.

Return your answer through the structured output: \`code\` = exactly the Python code the task asks for (no markdown fences, no explanation), \`note\` = one short sentence.`
}

function promptAgente(sb) {
  return `You are taking part in an automated test-generation benchmark (SWT-Bench, agent setting).

Your sandbox folder is: ${sb}
It contains a small Python module \`alvo.py\` and an issue report \`ISSUE.md\`. Read both.

Task: write a pytest test file \`test_issue.py\` in the sandbox folder that REPRODUCES the issue:
- the tests must FAIL on the current code (because of the bug described in the issue), and
- the tests must PASS once the issue is fixed.

Rules:
- Import from the module with \`from alvo import ...\`.
- You may run Python and pytest inside the sandbox to check your work, e.g. \`cd "${sb}" && python -m pytest -q test_issue.py\`.
- Work ONLY inside the sandbox folder: do not read, list or search any file outside it.
- Do not fix the bug in \`alvo.py\` (changes to it are discarded; only the test file is evaluated).
- A local hook may block your first Bash or Write call and ask you to state some facts first. If so, state them briefly (the file is a benchmark test file read only by the evaluation harness, it contains no secrets, nothing else calls it) and quote the user's instruction verbatim: "${USER_REQ}". Then retry the same call.

When you are done, return through the structured output: \`code\` = the full final content of test_issue.py, \`note\` = one short sentence.`
}

const jobs = []
for (let s = 1; s <= N; s++) {
  for (const inst of args.swt) {
    jobs.push({ id: `swtzs__${inst}__s${s}`, phase: 'SWT ZeroShot', prompt: promptSemFerramentas(`${ROOT}/dados/prompts/swtzs__${inst}.md`) })
    jobs.push({ id: `swtag__${inst}__s${s}`, phase: 'SWT Agente', prompt: promptAgente(`${SB}/swtag__${inst}__s${s}`) })
  }
  for (const f of args.funcs) {
    for (const k of ['full', 'first', 'last', 'extra']) {
      jobs.push({ id: `tge${k}__${f}__s${s}`, phase: 'TGE', prompt: promptSemFerramentas(`${ROOT}/dados/prompts/tge${k}__${f}.md`) })
    }
  }
}
log(`${jobs.length} tarefas para o Haiku`)

const res = await parallel(jobs.map(j => async () => {
  const r = await agent(j.prompt, { label: j.id, phase: j.phase, model: args.model || 'haiku', schema: SCHEMA })
  return { id: j.id, ok: !!(r && r.code && r.code.trim()), len: r && r.code ? r.code.length : 0 }
}))

const falhas = jobs.filter((j, i) => !res[i] || !res[i].ok).map(j => j.id)
log(`${jobs.length - falhas.length}/${jobs.length} respostas com código`)
return { total: jobs.length, ok: jobs.length - falhas.length, falhas }
