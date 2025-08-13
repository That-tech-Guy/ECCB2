tool = {
    "name": "lookup_scams",
    "description": "List common scams and red flags; educational prevention tips.",
    "parameters": {
        "type":"object",
        "properties":{
            "country":{"type":"string"},
            "type":{"type":"string"}
        }
    },
    "execute": lambda args: _execute(args)
}

BASE = [
    {"name":"Phishing SMS/Email","red_flags":["urgent tone","suspicious links","unknown sender"]},
    {"name":"Investment Doublers","red_flags":["guaranteed returns","pressure to act now"]},
    {"name":"Romance Scams","red_flags":["requests for money","refusal to meet"]},
]

def _execute(args):
    country = args.get("country","EC region")
    t = args.get("type")
    items = BASE
    if t:
        items = [i for i in items if t.lower() in i["name"].lower()]
    tips = ["Verify via official channels","Never share one-time codes","Use strong, unique passwords"]
    return {"country": country, "scams": items, "tips": tips}
