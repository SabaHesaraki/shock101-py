from typing import Callable, Dict
import datetime

REGISTRY: Dict[str, Callable[[str], str]] = {}

class ToolError(Exception):
    pass

def tool(fn: Callable[[str], str]) -> Callable[[str], str]:
    REGISTRY[fn.__name__] = fn
    return fn

@tool
def calc(arg: str) -> str:
    
    try:
        
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in arg):
            raise ToolError("Invalid chars")
        
        res = eval(arg, {"__builtins__": {}}, {})
        return str(res)
    except Exception:
        raise ToolError("calc crash")

@tool
def word_count(arg: str) -> str:
    if not arg.strip():
        return "0"
    return str(len(arg.split()))

@tool
def utc_now(arg: str) -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def dispatch(name: str, arg: str) -> str:
    if name not in REGISTRY:
        raise ToolError(f"Unknown tool: {name}")
    try:
        return REGISTRY[name](arg)
    except Exception as e:
        raise ToolError(str(e))

