PARENT_DIR = $(shell dirname $(shell pwd))

load_document:
	python load_knowledge_base.py

run_app:
	PYTHONPATH=${PARENT_DIR} streamlit run app.py

evaluate:
	PYTHONPATH=${PARENT_DIR} promptfoo eval -c evaluation/promptfooconfig.product_info.yaml --no-cache
	PYTHONPATH=${PARENT_DIR} promptfoo eval	-c evaluation/promptfooconfig.yaml

view:
	PYTHONPATH=${PARENT_DIR} promptfoo view