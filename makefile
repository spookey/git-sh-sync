LIB_NAME	=	git-sh-sync
MAIN_DIR	=	git_sh_sync
TEST_DIR	=	tests
DOCS_DIR	=	docs
HCOV_DIR	=	htmlcov

DOC_BUILD	=	$(DOCS_DIR)/_build

CMD_DELETE	:=	rm -vf
CMD_FIND	:=	find
CMD_ISORT	:=	isort
CMD_PYLINT	:=	pylint
CMD_PYREV	:=	pyreverse
CMD_PYTEST	:=	pytest
CMD_PYTHON	:=	python3
CMD_SPHINX	:=	sphinx-build

PLOTS		:=	$(patsubst %,%_$(LIB_NAME).png,classes packages)

.PHONY: help
.PHONY: clean cleancov cleandoc cleanplot cleanpyc cleantest
.PHONY: docs docsw
.PHONY: lint lintt plot sort sortt
.PHONY: test testc testcov testhcov testhcovw

help:
	@echo "$(LIB_NAME) makefile"
	@echo "\t"	"just for development"
	@echo
	@echo "clean"		"\t\t"	"clean all temporary files"
	@echo "cleancov"	"\t"	"clean test coverage files"
	@echo "cleandoc"	"\t"	"clean sphinx documentation files"
	@echo "cleanplot"	"\t"	"clean generated graphics"
	@echo "cleanpyc"	"\t"	"clean .pyc and __pycache__ files"
	@echo "cleantest"	"\t"	"clean test cache files"
	@echo "docs"		"\t\t"	"buld documentation with sphinx"
	@echo "docw"		"\t\t"	"browse generated documentation"
	@echo "lint"		"\t\t"	"run pylint on code"
	@echo "lintt"		"\t\t"	"run pylint on tests"
	@echo "plot"		"\t\t"	"generate graphics with pyreverse"
	@echo "sort"		"\t\t"	"sort imports with isort"
	@echo "sortt"		"\t\t"	"sort test imports with isort"
	@echo "test"		"\t\t"	"run tests with pytest"
	@echo "testcov"		"\t"	"run test coverage with pytest"
	@echo "testhcov"	"\t"	"run test coverage html with pytest"
	@echo "testhcovw"	"\t"	"browse test coverage html"
	@echo "travis"		"\t\t"	"run travis-ci command"
	@echo


define _browser_run
	@$(CMD_PYTHON) \
		-m "webbrowser" \
		-t "file://$$(cd "$(1)" || exit 2 && pwd)/$(2)"
endef

define _sphinx_run
	@$(CMD_SPHINX) \
		-M "$(1)" \
		"$(DOCS_DIR)" \
		"$(DOC_BUILD)"
endef

define _pylint_msg_tpl
{C} {path}:{line}:{column} - {msg}
	↪  {category} {module}.{obj} ({symbol} {msg_id})
endef
export _pylint_msg_tpl

define _pylint
	@$(CMD_PYLINT) \
		--msg-template="$$_pylint_msg_tpl" \
		--output-format="colorized" \
			$(1)
endef

define _pylint_run
	$(call _pylint,"$(MAIN_DIR)")
endef
define _pylint_run_test
	$(call _pylint,--disable "C0111" "$(TEST_DIR)")
endef

define _pyreverse_run
	@$(CMD_PYREV) \
		--output png \
		--all-ancestors \
		--module-names=y \
		--project="$(LIB_NAME)" \
		--filter-mode="ALL" \
			"$(1)"
endef

define _isort_run
	@$(CMD_ISORT) \
		--combine-star \
		--force-sort-within-sections \
		--multi-line 5 \
		--apply \
		--recursive \
			"$(1)"
endef

define _pytest_run
	@$(CMD_PYTEST) \
		$(1) -vv "$(TEST_DIR)"
endef

define _pytest_run_cov
	$(call _pytest_run,$(1) --cov="$(MAIN_DIR)")
endef


clean: cleancov cleandoc cleanplot cleanpyc cleantest

cleancov:
	@$(CMD_DELETE) -r $(HCOV_DIR)
	@$(CMD_DELETE) .coverage

cleandoc:
	$(call _sphinx_run,clean)

cleanplot:
	@$(CMD_DELETE) $(PLOTS)

cleanpyc:
	@$(CMD_FIND) "$(MAIN_DIR)" "$(TEST_DIR)" \
		-name '*.pyc' -delete -print \
			-o \
		-name '__pycache__' -delete -print \

cleantest:
	@$(CMD_DELETE) -r .pytest_cache



docs:
	$(call _sphinx_run,html)

docsw: docs
	$(call _browser_run,$(DOC_BUILD)/html,index.html)



lint:
	$(call _pylint_run)
lintt:
	$(call _pylint_run_test)


$(PLOTS): plot
plot:
	$(call _pyreverse_run,$(MAIN_DIR))



sort:
	$(call _isort_run,$(MAIN_DIR))
sortt:
	$(call _isort_run,$(TEST_DIR))



test:
	$(call _pytest_run)

testcov:
	$(call _pytest_run_cov)

$(HCOV_DIR): testhcov
testhcov:
	$(call _pytest_run_cov,--cov-report="html:$(HCOV_DIR)")

testhcovw: $(HCOV_DIR)
	$(call _browser_run,$(HCOV_DIR),index.html)



travis: testcov
	$(call _pylint_run) || true
