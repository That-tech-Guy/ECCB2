# tools/quiz.py
# ECCU Financial Literacy quiz (education only)
tool = {
    "name": "start_quiz",
    "description": "Start or continue an ECCU financial literacy quiz turn with a chosen difficulty.",
    "parameters": {
        "type": "object",
        "properties": {
            "topic": {"type": "string", "description": "Optional topic (savings, budgeting, credit, fraud)."},
            "level": {"type": "string", "enum": ["easy", "hard", "big_leagues"]},
            "country": {"type": "string", "description": "ECCU country for localization."}
        }
    },
    "execute": lambda args: _execute(args)
}

# Sample banks/contexts and Qs kept short; extend as you like.
QS = {
    "easy": [
        {"q": "Emergency funds usually cover how many months of expenses?", "a": "3-6"},
        {"q": "If XCD is pegged to USD at ~2.7, what’s $27 USD in XCD (about)?", "a": "≈73"}  # 27*2.7=72.9
    ],
    "hard": [
        {"q": "A loan APR is 18% with monthly compounding. What’s the main risk if you only pay the minimum?", "a": "Interest snowball / slow principal reduction"},
        {"q": "Name one fee to check for when using foreign cards in the ECCU.", "a": "FX fee / ATM fee"}
    ],
    "big_leagues": [
        {"q": "Why can a 10% ‘guaranteed’ return in an unlicensed scheme be a red flag?", "a": "Promises guaranteed high returns; likely a scam"},
        {"q": "If a bond fund’s yield rises, what likely happened to bond prices?", "a": "They fell (inverse relation)"}
    ]
}

def _execute(args):
    level = (args.get("level") or "easy").lower()
    topic = (args.get("topic") or "").lower()
    country = args.get("country") or "ECCU"
    deck = QS.get(level, QS["easy"])
    q = deck[0] if deck else {"q":"No questions yet.","a":None}
    return {
        "mode": "quiz_turn",
        "country": country,
        "level": level,
        "topic": topic or "general",
        "question": q["q"],
        "accepts_answer": True,
        "note": "Educational content; not financial advice."
    }
