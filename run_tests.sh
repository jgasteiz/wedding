#!/bin/sh
set -eu

pushd "$(dirname "$0")"

python manage.py test --settings=wedding.settings_test $@

popd