PARENT_DIR = $(shell dirname $(shell pwd))

load_document:
	python load_knowledge_base.py

run_app:
	streamlit run app.py

evaluate:
	PYTHONPATH=${PARENT_DIR} promptfoo eval
