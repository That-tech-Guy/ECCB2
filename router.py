import json
from sf_tools import tool_specs_for_llm, execute_tool


def build_system_prompt():
    with open("system_prompt.txt","r",encoding="utf-8") as f:
        return f.read()

def as_openai_messages(history, system_text):
    # history is a list of dicts: {"role":"user"/"assistant","content":"..."}
    msgs = [{"role":"system","content":system_text}]
    msgs.extend(history)
    return msgs

def respond(history, llm_client):
    """
    history: list[{"role":"user"|"assistant","content":str}] (Streamlit session_state messages)
    llm_client: function(messages, tools)-> message
    returns: (assistant_text, trace)
    """
    tools = tool_specs_for_llm()
    system_text = build_system_prompt()
    messages = as_openai_messages(history, system_text)

    # First call: let model decide if a tool is needed
    m = llm_client(messages, tools)

    trace = {"tool_calls": []}

    if getattr(m, "tool_calls", None):
        # Execute each tool call, then send a follow-up message to get final text
        for call in m.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments or "{}")
            result = execute_tool(name, args)
            trace["tool_calls"].append({"name": name, "args": args, "result": result})
            messages.append({
                "role": "assistant",
                "content": m.content or "",
                "tool_calls": [tc.model_dump() for tc in m.tool_calls]  # for completeness
            })
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "name": name,
                "content": json.dumps(result)
            })

        # Second call: ask model to summarize tool result for the user
        m2 = llm_client(messages, tools)
        return (m2.content or "Done.", trace)

    # No tool call—just answer directly
    return (m.content or "Done.", trace)
