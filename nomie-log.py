#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib import request

NOMIE_LOG__API_KEY = 'NOMIE_LOG__API_KEY'
NOMIE_LOG__EDITOR = 'NOMIE_LOG__EDITOR'

NOMIE_LOG_URL = 'https://nomieapi.com/log'


def main():
    with NamedTemporaryFile('w+b') as f:
        editor = require_env(NOMIE_LOG__EDITOR)
        res = subprocess.run([editor, f.name])
        if res.returncode != 0:
            print('Editor ends with non zero code:', res.returncode)
            return
        contents = Path(f.name).read_text('utf-8')
        if not contents:
            print('Exit, note content is empty')
            return
        send_note(contents)
        print('Done')


def send_note(contents):
    key = require_env(NOMIE_LOG__API_KEY)
    data = json.dumps(dict(
        note=contents,
        api_key=key
    ))
    req = request.Request(
        NOMIE_LOG_URL,
        data=data.encode('utf8'),
        headers={"Content-Type": "application/json"}
    )
    request.urlopen(req, timeout=20)


def require_env(name):
    val = os.environ.get(name)
    if val is None:
        print('Env {} is required', name)
        sys.exit(1)
    return str(val)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
