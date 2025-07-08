def decide_next_step(state: InterviewState) -> InterviewState:
	idx = state["current_strategy_index"]
	count = state.get("check", 0)
	evaluation = state.get("evaluation", [])
	last_eval = evaluation[-1] if evaluation else {}
	grades = last_eval.get("grades", [])
	order = state["strategy_order"]
	
	if idx < 5:
			if count <2 and any(g in {"C", "D", "F"} for g in grades):
					new_idx =idx
					next_step = "generate"
					new_strategy = order[idx]
			else:
					new_idx = idx + 1
					next_step = "generate"
					new_strategy = order[new_idx]
					state["check"] = 0
					
	else:
			new_idx = idx + 1
			if new_idx >= len(order):
					next_step = "end"
					new_strategy = ""
			else:
					next_step = "generate"
					new_strategy = order[new_idx]
	
	return {
		**state,
		"next_step": next_step,
		"previous_strategy": order[idx],
		"current_strategy_index": new_idx,
		"current_strategy": new_strategy
	}
