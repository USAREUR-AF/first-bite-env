# Gates for every dictionary under dictionaries/. `make check` is what a pull
# request must pass. The bite that runs them is one of the USAREUR-AF/first-bite
# commit in first-bite.ref: built by `make bite`, or the release archive of that
# commit that .github/workflows/check.yml installs.

FIRST_BITE_URL ?= https://github.com/USAREUR-AF/first-bite
FIRST_BITE_REF := $(shell tr -d '[:space:]' < first-bite.ref)
# `make bite` builds this one; any bite of the pinned commit will do.
BITE ?= $(if $(wildcard .first-bite/target/release/bite),.first-bite/target/release/bite,bite)
# One dictionary, for tables, import and diff: make tables D=harbour-buoy
D ?=
# A released version of that dictionary, for diff: make diff D=harbour-buoy OLD=<directory>
OLD ?=

DICTIONARIES := $(patsubst dictionaries/%/dictionary/dictionary.json,%,$(wildcard dictionaries/*/dictionary/dictionary.json))

.PHONY: check fmt tables import diff first-bite bite leak-check list help

check: ## format, structure and vectors, conventions, coverage, for every dictionary
	@test -n "$(DICTIONARIES)" || { echo "no dictionary under dictionaries/"; exit 2; }
	@$(BITE) --version
	@rc=0; for d in $(DICTIONARIES); do \
	  echo "== $$d"; \
	  $(BITE) fmt --check dictionaries/$$d/dictionary || rc=1; \
	  $(BITE) check --strict dictionaries/$$d/dictionary || rc=1; \
	  $(BITE) lint dictionaries/$$d/dictionary || rc=1; \
	  $(BITE) coverage --strict dictionaries/$$d/dictionary || rc=1; \
	done; exit $$rc

list: ## the dictionaries make check covers
	@for d in $(DICTIONARIES); do echo $$d; done

fmt: ## rewrite every dictionary in canonical form
	@for d in $(DICTIONARIES); do $(BITE) fmt dictionaries/$$d/dictionary; done

tables: ## dictionary -> tables, to edit in a spreadsheet: make tables D=<name>
	@test -n "$(D)" || { echo "usage: make tables D=<dictionary>"; exit 2; }
	$(BITE) export-csv dictionaries/$(D)/dictionary --out dictionaries/$(D)/tables

import: ## tables -> dictionary: make import D=<name>
	@test -n "$(D)" || { echo "usage: make import D=<dictionary>"; exit 2; }
	$(BITE) import-csv dictionaries/$(D)/tables --into dictionaries/$(D)/dictionary

diff: ## what changed against a released version: make diff D=<name> OLD=<directory>
	@test -n "$(D)" -a -n "$(OLD)" || { echo "usage: make diff D=<dictionary> OLD=<directory of the released dictionary>"; exit 2; }
	$(BITE) diff --check-version $(OLD) dictionaries/$(D)/dictionary

first-bite: ## check out first-bite at first-bite.ref into .first-bite/ (needs git)
	@echo "$(FIRST_BITE_REF)" | grep -Eq '^[0-9a-f]{40}$$' || { echo "first-bite.ref must hold one full 40-character commit sha"; exit 2; }
	@test -d .first-bite/.git || git init -q .first-bite
	git -C .first-bite fetch -q --depth 1 $(FIRST_BITE_URL) $(FIRST_BITE_REF)
	git -C .first-bite checkout -q --detach FETCH_HEAD

bite: first-bite ## build bite from first-bite at first-bite.ref into .first-bite/ (needs git and cargo)
	cd .first-bite && cargo build --release --locked -p bite
	.first-bite/target/release/bite --version

leak-check: first-bite ## first-bite's tools/check-public-tree.sh over this tree; names from .leak-needles or LEAK_NEEDLES
	.first-bite/tools/check-public-tree.sh

help: ## this list
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sed 's/:.*## /\t/'
