# AI Agent 提示词管理

基于 [promptfoo](https://promptfoo.dev) 的 AI Agent 提示词模板集合与评测示例。

## 提示词

| 文件 | 说明 |
|------|------|
| `prompts/assistant.md` | 通用助手 |
| `prompts/code-reviewer.md` | 代码审查（含安全与质量检测） |
| `prompts/data-analyst.md` | 数据解读与趋势分析 |

## 快速开始

安装 promptfoo：

```bash
npm install -g promptfoo
```

设置 API Key：

```bash
export ANTHROPIC_API_KEY=你的密钥
export ANTHROPIC_BASE_URL=https://open.bigmodel.cn/api/anthropic
```

## 运行评测

```bash
# 执行所有评测
promptfoo eval

# 在浏览器中查看结果
promptfoo view
```

## CI

在 `prompts/`、`tests/` 或 `promptfooconfig.yaml` 有改动时，GitHub Actions 会自动触发评测。

所需 Secret：`ANTHROPIC_API_KEY`

## 目录结构

```
├── prompts/               # 提示词模板
├── tests/                 # 测试用例（cases.yaml）
├── results/               # 评测输出（已 gitignore）
└── promptfooconfig.yaml
```
