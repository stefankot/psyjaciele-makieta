#!/bin/zsh
set -e
cd "$(dirname "$0")/.."
python3 wordpress/sync.py check
python3 -m unittest discover -s wordpress -p test_sync.py
python3 wordpress/sync.py build
printf '\nGotowe: paczka i plan zmian w ../wordpress-staging/generated.\nNic nie zostało opublikowane ani zmienione w WordPressie.\n'
