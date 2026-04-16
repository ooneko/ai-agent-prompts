# AI Agent Prompts

A collection of AI agent prompt templates with [promptfoo](https://promptfoo.dev) evaluations.

## Prompts

| Prompt | Description |
|--------|-------------|
| `prompts/assistant.md` | General-purpose helpful assistant |
| `prompts/code-reviewer.md` | Code review with security and quality focus |
| `prompts/data-analyst.md` | Data interpretation and trend analysis |

## Setup

```bash
npm install -g promptfoo
```

Set your API keys:

```bash
export OPENAI_API_KEY=your_key
export ANTHROPIC_API_KEY=your_key
```

## Run Evals

```bash
# Run all evaluations
promptfoo eval

# View results in browser
promptfoo view
```

## CI

GitHub Actions automatically runs evals on any changes to `prompts/`, `tests/`, or `promptfooconfig.yaml`.

Required secrets: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`

## Structure

```
├── prompts/          # Prompt template files
├── tests/            # Test cases (cases.yaml)
├── results/          # Eval outputs (gitignored)
└── promptfooconfig.yaml
```
