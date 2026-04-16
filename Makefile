eval-assistant:
	npx promptfoo@latest eval --config evals/general/promptfooconfig.yaml

eval-code-reviewer:
	npx promptfoo@latest eval --config evals/code-reviewer/promptfooconfig.yaml

eval-data-analyst:
	npx promptfoo@latest eval --config evals/data-analyst/promptfooconfig.yaml

eval-general: eval-assistant eval-code-reviewer eval-data-analyst

eval-excel:
	npx promptfoo@latest eval --config evals/excel-qa/promptfooconfig.yaml

eval-tool-call:
	npx promptfoo@latest eval --config evals/tool-call/promptfooconfig.yaml

eval-all:
	$(MAKE) eval-general
	$(MAKE) eval-excel
	$(MAKE) eval-tool-call
