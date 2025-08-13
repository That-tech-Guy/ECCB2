from .currency import tool as convert_currency
from .budget import tool as generate_budget
from .invest import tool as suggest_investments
from .hustles import tool as list_small_hustles
from .scams import tool as lookup_scams
from .quiz import tool as start_quiz

TOOLS = [
    convert_currency,
    generate_budget,
    suggest_investments,
    list_small_hustles,
    lookup_scams,
    start_quiz,
]

def tool_specs_for_llm():
    specs = []
    for t in TOOLS:
        specs.append({
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["parameters"]
            }
        })
    return specs

def execute_tool(name: str, args: dict):
    tool = next((t for t in TOOLS if t["name"] == name), None)
    if not tool:
        raise ValueError(f"Unknown tool: {name}")
    return tool["execute"](args or {})
