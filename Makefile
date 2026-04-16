eval-general:
	npx promptfoo@latest eval --config evals/general/promptfooconfig.yaml

eval-excel:
	npx promptfoo@latest eval --config evals/excel-qa/promptfooconfig.yaml

eval-all:
	$(MAKE) eval-general
	$(MAKE) eval-excel
