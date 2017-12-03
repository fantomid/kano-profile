#
# Makefile
#
# Copyright (C) 2017 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPLv2
#

REPORT_DIR = reports


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
	-coverage run --module behave
	-coverage run --append --module pytest
	# Generate reports
	coverage xml
	coverage html


test: check
