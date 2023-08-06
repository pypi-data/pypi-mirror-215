from pathlib import Path
from typing import Any, List, Optional,Union

def print_flush(*args, **kwargs):
    print(*args, **kwargs, flush=True)