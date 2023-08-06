import json


try:
    import orjson  # type: ignore
except ModuleNotFoundError:
    HAS_ORJSON = False
else:
    HAS_ORJSON = True
    
if HAS_ORJSON:
    catline_json = orjson  # type: ignore
else:
    catline_json = json
