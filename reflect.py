def reflect(state: InterviewState):
    evaluation = state.get("evaluation", [])
    last_eval = evaluation[-1] if evaluation else {}
    grades = last_eval.get("grades", [])

    if any(g in {"중", "하"} for g in grades):
        if state["current_strategy"] == state.get("previous_strategy", ""):
            state["check"] += 1
        state["satisfied"] = False
    else:
        state["satisfied"] = True

    return state
