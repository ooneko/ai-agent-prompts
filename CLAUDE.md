# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 运行评测

```bash
make eval-general   # 通用提示词评测
make eval-excel     # excel-qa 提示词评测
make eval-all       # 全部
```

单独运行（不用 make）：

```bash
npx promptfoo@latest eval --config evals/general/promptfooconfig.yaml
npx promptfoo@latest eval --config evals/excel-qa/promptfooconfig.yaml
```

查看结果：

```bash
npx promptfoo@latest view
```

## 环境变量

参考 `.env.example`，必须设置三个变量：

```bash
ANTHROPIC_API_KEY=...
ANTHROPIC_BASE_URL=...   # 第三方兼容 Anthropic API 的 base URL
MODEL=...                # 模型名称，如 MiniMax-M2.7-highspeed
```

## 目录结构

```
prompts/          # 提示词模板（.md 文件，支持 {{变量}} 插值）
tests/
  general/        # 通用提示词测试用例，变量：{{input}}
  excel-qa/       # 表格问答测试用例，变量：{{table}} + {{question}}
evals/
  general/        # 通用评测配置，引用 prompts/ 下三个 prompt
  excel-qa/       # 表格问答评测配置，引用 prompts/excel-qa.md
results/          # 评测输出（gitignore）
```

## 架构说明

- **Provider**：使用 Anthropic Messages API 协议对接第三方模型，provider id、key、base URL 均通过环境变量注入，切换模型只需改环境变量。
- **评测与测试分离**：`evals/` 存放 promptfoo 配置，`tests/` 存放测试用例，两者目录名一一对应（`general`、`excel-qa`）。
- **llm-rubric 断言**：大多数测试用 `llm-rubric` 由同一 provider 做 LLM 评判，少量用 `icontains` 做确定性检查。
- **CI**：`.github/workflows/eval.yml` 在 `prompts/`、`tests/`、`evals/`、`Makefile`、workflow 文件本身有变更时自动触发，所需 Secrets：`ANTHROPIC_API_KEY`、`ANTHROPIC_BASE_URL`、`MODEL`。

## 添加新 prompt 的步骤

1. 在 `prompts/` 创建 `.md` 文件，用 `{{变量名}}` 定义输入
2. 在 `tests/<name>/cases.yaml` 编写测试用例，变量与 prompt 对应
3. 在 `evals/<name>/promptfooconfig.yaml` 创建评测配置
4. 在 `Makefile` 添加对应 target
