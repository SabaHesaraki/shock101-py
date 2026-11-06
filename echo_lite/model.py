import json

class FakeModel:
    def __call__(self, messages: list[dict]) -> str:
        last_msg = messages[-1]["content"]
        if "12*7" in last_msg:
            return json.dumps({"tool": "calc", "arg": "12*7"})
        elif "time in UTC" in last_msg:
            return json.dumps({"tool": "utc_now", "arg": ""})
        else:
            return json.dumps({"final": "12*7 = 84; UTC time: 2026-11-02T14:03:00Z"})

