# Makefile
#
#    Makefile to simplify common developer tasks (e.g. testing,
#    releasing).
#
# ==============================================================
# Main rules
# ==============================================================
#
# test:
#	Run all tests for python 2.7 and 3.6.
#
# package:
#	If no pypi.org package with current version exists, create
#       package/wheel and upload to PyPI.org.
#
# test-package:
#	Same as package, but for the test server testpypi.org.
#
# ==============================================================
# Secondary rules
# ==============================================================
#
# test_2.7:
#	Run all tests for python 2.7.
#
# test_3.6:
#	Run all tests for python 3.6.
#
# clean-package:
#       Delete all the package and wheel files from pysto/dist/.
#
# check-download-url:
#	Check that the download URL in setup.py points to the correct version.
#
# update-README-rst:
#	Convert README.md to README.rst.
#
# github-tag:
#	Create remote github tag for current commit, if not done yet.


#    Copyright (C) 2017  Ramón Casero <rcasero@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

SHELL := /bin/bash

SRCFILES = pysto/imgproc.py \
	pysto/imgprocITK.py
TESTFILES = tests/test_block_split.py \
	tests/test_block_stack.py \
	tests/test_imfuse.py \
	tests/test_imshow.py\
	tests/test_matchHist.py

PACKAGE_JSON_URL = https://pypi.python.org/pypi/pysto/json
TEST_PACKAGE_JSON_URL = https://testpypi.python.org/pypi/pysto/json

## Testing

dist/all_tests_2.7_OK.txt: $(SRCFILES) $(TESTFILES)
	tput setaf 1; echo "** Testing pysto for python 2.7"; tput sgr0
	source activate pysto_2.7 \
	&& pytest tests \
	&& touch dist/all_tests_2.7_OK.txt

dist/all_tests_3.6_OK.txt: $(SRCFILES) $(TESTFILES)
	tput setaf 1; echo "** Testing pysto for python 3.6"; tput sgr0
	source activate pysto_3.6 \
	&& pytest tests \
	&& touch dist/all_tests_3.6_OK.txt

test_2.7: dist/all_tests_2.7_OK.txt

test_3.6: dist/all_tests_3.6_OK.txt

test: test_2.7 test_3.6

## Releasing

clean-package:
	rm -f dist/pysto-*.tar.gz dist/pysto-*-py?-none-any.whl

check-download-url:
	tput setaf 1 && echo "** Checking download URL" && tput sgr0 
	LOCAL_VERSION=`grep -e "^    version" setup.py | grep -oP "(?<=').*?(?=')"` \
	&& DOWNLOAD_URL_MATCHED_TO_LOCAL=`grep download_url setup.py | grep "/$${LOCAL_VERSION}.tar.gz"` \
	&& echo "Local version: $$LOCAL_VERSION" \
	&& echo $$DOWNLOAD_URL_MATCHED_TO_LOCAL \
	&& if [ -z "$${DOWNLOAD_URL_MATCHED_TO_LOCAL}" ]; then \
		echo Error: download URL does not match local version; \
		exit 1; \
	else \
		echo Pass: Download URL matches local version; \
	fi

README.rst: README.md
	pandoc --from=markdown --to=rst --output=README.rst README.md
	git commit README.rst -m "convert README.md to README.rst"
	git push

github-tag:
	tput setaf 1 && echo "** Creating github tag if necessary" && tput sgr0
	git fetch --tags
	LOCAL_VERSION=`grep -e "^    version" setup.py | grep -oP "(?<=').*?(?=')"`; \
	LOCAL_TAG_EXISTS=`git tag | grep -x "$$LOCAL_VERSION"`; \
	if [ -z "$${LOCAL_TAG_EXISTS}" ]; then \
		echo Creating local tag \
		&& git tag "$$LOCAL_VERSION"; \
	else \
		echo "Skipping: Local tag already exists"; \
	fi; \
	REMOTE_TAG_EXISTS=`git ls-remote --tags origin | grep refs/tags/"$$LOCAL_VERSION"`; \
	if [ -z "$${REMOTE_TAG_EXISTS}" ]; then \
		echo Pushing tag to remote \
		&& git push origin --tags; \
	else \
		echo "Skipping: Remote tag already exists"; \
	fi

package: check-download-url README.rst github-tag
	tput setaf 1 && echo "** Creating release package and uploading to PyPI.org" && tput sgr0 
	LOCAL_VERSION=`grep -e "^    version" setup.py | grep -oP "(?<=').*?(?=')"`; \
	LOCAL_VERSION_IS_IN_SERVER=`curl -s $(PACKAGE_JSON_URL) | jq  -r '.releases | keys | .[]' | grep $$LOCAL_VERSION`; \
	if [ -z $$LOCAL_VERSION_IS_IN_SERVER ]; then \
		python setup.py check \
		&& python setup.py sdist bdist_wheel \
		&& twine upload --repository pypi dist/*$$LOCAL_VERSION*; \
	else \
		echo "Local version $$LOCAL_VERSION is already on PyPI server"; \
	fi

test-package: check-download-url github-tag
	tput setaf 1 && echo "** Creating release package and uploading to PyPI.org" && tput sgr0 
	LOCAL_VERSION=`grep -e "^    version" setup.py | grep -oP "(?<=').*?(?=')"`; \
	LOCAL_VERSION_IS_IN_SERVER=`curl -s $(TEST_PACKAGE_JSON_URL) | jq  -r '.releases | keys | .[]' | grep $$LOCAL_VERSION`; \
	if [ -z $$LOCAL_VERSION_IS_IN_SERVER ]; then \
		python setup.py check \
		&& python setup.py sdist bdist_wheel \
		&& twine upload --repository pypitest dist/*$$LOCAL_VERSION*; \
	else \
		echo "Local version $$LOCAL_VERSION is already on PyPI test server"; \
	fi

