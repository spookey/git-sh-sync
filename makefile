LIB_NAME	=	git-sh-sync
MAIN_DIR	=	git_sh_sync
DOCS_DIR	=	docs

DOC_BUILD	=	$(DOCS_DIR)/_build

CMD_PYTHON	:=	python3
CMD_SPHINX	:=	sphinx-build

.PHONY: help
.PHONY: clean cleandoc
.PHONY: docs docsw

help:
	@echo "$(LIB_NAME) makefile"
	@echo "\t"	"just for development"
	@echo
	@echo "clean"		"\t\t"	"clean all temporary files"
	@echo "cleandoc"	"\t"	"clean sphinx documentation files"
	@echo "docs"		"\t\t"	"buld documentation with sphinx"
	@echo "docw"		"\t\t"	"browse generated documentation"


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


clean: cleandoc

cleandoc:
	$(call _sphinx_run,clean)



docs:
	$(call _sphinx_run,html)

docsw: docs
	$(call _browser_run,$(DOC_BUILD)/html,index.html)
