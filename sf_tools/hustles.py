tool = {
    "name": "list_small_hustles",
    "description": "Suggest side hustles; filter by remote and low cost.",
    "parameters": {
        "type":"object",
        "properties":{
            "remote_only":{"type":"boolean"},
            "low_cost_only":{"type":"boolean"}
        }
    },
    "execute": lambda args: _execute(args)
}

HUSTLES = [
    {"title":"Online Tutoring", "remote":True, "low_cost":True},
    {"title":"Graphic Design", "remote":True, "low_cost":True},
    {"title":"Delivery Driver", "remote":False, "low_cost":False},
    {"title":"Handyman Services", "remote":False, "low_cost":False},
    {"title":"Affiliate Marketing", "remote":True, "low_cost":True},
    {"title":"Selling Digital Products", "remote":True, "low_cost":True},
]

def _execute(args):
    remote_only = bool(args.get("remote_only", False))
    low_cost_only = bool(args.get("low_cost_only", False))
    res = HUSTLES
    if remote_only:
        res = [h for h in res if h["remote"]]
    if low_cost_only:
        res = [h for h in res if h["low_cost"]]
    return {"results": res}
