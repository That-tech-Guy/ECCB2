tool = {
    "name": "generate_budget",
    "description": "Create a budget plan with totals and leftover.",
    "parameters": {
        "type": "object",
        "properties": {
            "income": {"type": "number"},
            "expenses": {"type": "array", "items": {
                "type":"object",
                "properties": {
                    "name":{"type":"string"},
                    "amount":{"type":"number"}
                },
                "required":["name","amount"]
            }},
            "goal": {"type":"string"}
        },
        "required": ["income","expenses"]
    },
    "execute": lambda args: _execute(args)
}

def _execute(args):
    income = float(args["income"])
    expenses = args.get("expenses", [])
    total = sum(float(e["amount"]) for e in expenses)
    leftover = income - total
    pct = {e["name"]: round((float(e["amount"])/income)*100,1) if income else 0 for e in expenses}
    suggestions = []
    if leftover < 0:
        suggestions.append("You're over budget—reduce discretionary spends by 10–15% first.")
    elif leftover < 0.1 * income:
        suggestions.append("Consider a 50/30/20 guideline to raise savings above 10% of income.")
    return {
        "summary": {"income": income, "total_expenses": total, "leftover": leftover},
        "breakdown_pct": pct,
        "suggestions": suggestions
    }
