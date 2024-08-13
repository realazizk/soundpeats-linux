#!/bin/sh

poetry run python -m nuitka --remove-output --onefile --standalone --output-filename=soundpeats --output-dir=build server.py 