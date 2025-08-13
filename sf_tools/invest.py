tool = {
    "name": "suggest_investments",
    "description": "Educational overview of investment options by risk and horizon (not financial advice).",
    "parameters": {
        "type":"object",
        "properties":{
            "risk":{"type":"string","enum":["low","medium","high"]},
            "horizon":{"type":"string","description":"timeframe, e.g., 1-3y, 3-5y"},
            "country":{"type":"string"}
        },
        "required":["risk"]
    },
    "execute": lambda args: _execute(args)
}

def _execute(args):
    risk = args["risk"]
    horizon = args.get("horizon","unspecified")
    country = args.get("country","EC region")
    buckets = {
        "low": ["High-yield savings (local bank)","Govt bonds/treasuries","Money market funds"],
        "medium":["Balanced mutual funds/ETFs","Corporate bonds","Dividend stocks"],
        "high": ["Broad-market stock ETFs","Thematic equities","Crypto (very high risk)"]
    }
    cautions = [
        "Diversify; avoid putting all funds in one asset.",
        "Consider fees, FX, and liquidity.",
        "This is educational, not investment advice."
    ]
    return {"country": country, "horizon": horizon, "options": buckets.get(risk, []), "cautions": cautions}
