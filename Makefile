#
# Makefile
#
# Copyright (C) 2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPLv2
#

# Run tests, excluding these tagged items, e.g
#     make check OMITTED_TAGS="tag1 tag2"
OMITTED_TAGS =

empty:=
space:= $(empty) $(empty)

REPORT_DIR = reports

# Elaborate mechanism just to get the correct syntax for the pytest markers param
_FIRST_TAG := $(firstword $(OMITTED_TAGS))
PYTEST_TAGS_EXPR := $(foreach tag, $(OMITTED_TAGS), $(if $(filter $(tag), $(_FIRST_TAG)),not $(tag),and not $(tag)))

ifeq ($(PYTEST_TAGS_EXPR), )
	PYTEST_TAGS_FLAG :=
else
	PYTEST_TAGS_FLAG := -m "$(strip $(PYTEST_TAGS_EXPR))"
endif
BEHAVE_TAGS_FLAG := $(join $(addprefix --tags=-,$(OMITTED_TAGS)), $(space))


#
# Run the tests
#
# Requirements:
#     - pytest
#     - behave
#     - pytest-cov
#
check:
	# Refresh the reports directory
	rm -rf $(REPORT_DIR)
	mkdir -p $(REPORT_DIR)
	# Run the tests
	-coverage run --module pytest $(PYTEST_TAGS_FLAG)
	-coverage run --append --module behave $(BEHAVE_TAGS_FLAG)
	# Generate reports
	coverage xml
	coverage html


test: check
