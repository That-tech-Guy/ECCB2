tool = {
    "name": "convert_currency",
    "description": "Convert between currencies like XCD, USD, GBP.",
    "parameters": {
        "type": "object",
        "properties": {
            "amount": {"type": "number"},
            "from": {"type": "string", "description": "ISO code, e.g., XCD"},
            "to": {"type": "string", "description": "ISO code, e.g., USD"},
        },
        "required": ["amount", "from", "to"]
    },
    "execute": lambda args: _execute(args)
}

# TODO: replace with your real converter/rates source
RATES = {
    ("XCD","USD"): 0.37,
    ("USD","XCD"): 2.70,
}

def _execute(args):
    amt = float(args["amount"])
    src = args["from"].upper()
    dst = args["to"].upper()
    rate = RATES.get((src,dst))
    if rate is None:
        return {"error": f"Rate {src}->{dst} not available"}
    return {"amount": amt, "from": src, "to": dst, "rate": rate, "converted": round(amt*rate, 2)}
