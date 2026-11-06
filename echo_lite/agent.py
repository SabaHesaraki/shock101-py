import os
import json
from dataclasses import dataclass, field
from datetime import datetime
from echo_lite.tools import dispatch, ToolError
from echo_lite.model import FakeModel

@dataclass
class Message:
    role: str
    content: str

def run(task: str, model=None, max_steps: int = 5, log_dir: str = "runs") -> str:
    if model is None:
        model = FakeModel()
    
    messages = [{"role": "user", "content": task}]
    log_records = []
    
    for _ in range(max_steps):
        raw_response = model(messages)
        log_records.append({"step": "model", "response": raw_response})
        
        try:
            res_dict = json.loads(raw_response)
        except Exception:
            raise ToolError("Invalid JSON from model")
            
        if "final" in res_dict:
            log_records.append({"step": "final", "content": res_dict["final"]})
            _save_log(log_dir, log_records)
            return res_dict["final"]
            
        if "tool" in res_dict:
            tool_name = res_dict["tool"]
            tool_arg = res_dict.get("arg", "")
            messages.append({"role": "assistant", "content": raw_response})
            
            try:
                tool_result = dispatch(tool_name, tool_arg)
            except Exception as e:
                tool_result = f"ERROR: {e}"
                
            messages.append({"role": "tool", "content": tool_result})
            log_records.append({"step": "tool", "name": tool_name, "result": tool_result})
            
    _save_log(log_dir, log_records)
    raise ToolError("Max steps reached without final answer")

def _save_log(log_dir: str, records: list):
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S_%f")
    file_path = os.path.join(log_dir, f"{timestamp}.jsonl")
    with open(file_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")

