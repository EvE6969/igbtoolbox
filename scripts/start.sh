#!/usr/bin/env bash

BASEDIR=$(dirname "$0")/..
PYTHONEXEC=$HOME/venv/igbtoolbox-3/bin/python
export PYTHONPATH=$BASEDIR/server

# NRADMIN will be set for newrelic to instrument python code
if [ "$NRADMIN" != "" ]; then
	$NRADMIN run-program "$PYTHONEXEC" -m igbtoolbox.server --modules "$BASEDIR/bower_components" "$@"
else
	$PYTHONEXEC -m igbtoolbox.server --modules "$BASEDIR/bower_components" "$@"
fi
