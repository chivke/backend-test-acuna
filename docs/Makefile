
SPHINXOPTS    ?= 
SPHINXBUILD   ?= sphinx-build -c .
SOURCEDIR     = ./_source
BUILDDIR      = ./_build
APP = /app

.PHONY: help livehtml apidocs Makefile

help:
	@$(SPHINXBUILD) help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

livehtml:
	sphinx-autobuild -b html --host 0.0.0.0 --port 7000 --watch $(APP) -c . $(SOURCEDIR) $(BUILDDIR)/html

apidocs:
	sphinx-apidoc -o $(SOURCEDIR)/api /app

%: Makefile
	@$(SPHINXBUILD) -b $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
