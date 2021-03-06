#!/bin/bash

version="$1"; shift
message="$@"

if [ -z "$version" ]; then
	echo "Version must not be empty"
	exit 1
fi
if [ -z "$message" ]; then
	echo "Message must not be empty"
	exit 1
fi
pip install --upgrade .

rm -Rvf dist/

python setup.py sdist
python setup.py bdist_wheel

gpg --detach-sign -a dist/dbml2dot-$version.tar.gz

git tag --sign --message "$message" "v${version}"
git push --tags
twine upload dist/dbml2dot-$version.tar.gz dist/dbml2dot-$version.tar.gz.asc
