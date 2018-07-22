LIB_NAME	=	git-sh-sync
MAIN_DIR	=	git_sh_sync
DOCS_DIR	=	docs

DOC_BUILD	=	$(DOCS_DIR)/_build

CMD_ISORT	:=	isort
CMD_PYLINT	:=	pylint
CMD_PYREV	:=	pyreverse
CMD_PYTHON	:=	python3
CMD_SPHINX	:=	sphinx-build

PLOTS		:=	$(patsubst %,%_$(LIB_NAME).png,classes packages)

.PHONY: help
.PHONY: clean cleandoc cleanplot
.PHONY: docs docsw
.PHONY: lint plot sort

help:
	@echo "$(LIB_NAME) makefile"
	@echo "\t"	"just for development"
	@echo
	@echo "clean"		"\t\t"	"clean all temporary files"
	@echo "cleandoc"	"\t"	"clean sphinx documentation files"
	@echo "docs"		"\t\t"	"buld documentation with sphinx"
	@echo "docw"		"\t\t"	"browse generated documentation"
	@echo "lint"		"\t\t"	"run pylint on code"
	@echo "plot"		"\t\t"	"generate graphics with pyreverse"
	@echo "sort"		"\t\t"	"sort imports with isort"


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

define _pylint_run
	@$(CMD_PYLINT) \
		--disable "C0111" \
		--disable "RP0401" \
		--msg-template="$$_pylint_msg_tpl" \
		--output-format="colorized" \
		"$(1)"
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


clean: cleandoc cleanplot


cleandoc:
	$(call _sphinx_run,clean)

cleanplot:
	@$(CMD_DELETE) $(PLOTS)



docs:
	$(call _sphinx_run,html)

docsw: docs
	$(call _browser_run,$(DOC_BUILD)/html,index.html)



lint:
	$(call _pylint_run,$(MAIN_DIR))


$(PLOTS): plot
plot:
	$(call _pyreverse_run,$(MAIN_DIR))



sort:
	$(call _isort_run,$(MAIN_DIR))
