#!/usr/bin/env python3
import json
from os import path, PathLike
from pathlib import Path
from pprint import pprint
from typing import Optional
from urllib import request

def unwrap(source: Optional[str|dict|PathLike]) -> dict:
    try:
        return source.get('response').get('elements')
    except:
        pass

    try:
        with open(source) as fd:
            raw_data = fd.read()
            json_data = json.loads(raw_data)
            return json_data.get('response').get('elements')
    except:
        pass

    try:
        req = request.urlopen(source)
        response = req.read().decode('utf-8')
        req.close()
        json_data = json.loads(response)
        return json_data.get('response').get('elements')        
    except:
        pass

    raise ValueError(f"source of type {type(source).__name__} and value '{str(source)}' cannot be unwrapped")
