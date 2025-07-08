def summarize_interview(state: InterviewState) -> InterviewState:
    conversation = state.get("conversation", [])
    evaluation = state.get("evaluation", [])
    summary = state["resume_summary"]
    strategy_dict = state["strategy_dict"]

    print("\n📝 인터뷰 보고서")
    print("=" * 100)

    for i, turn in enumerate(conversation):
        print(f"[Q{i + 1}] ({turn['s']}) {turn['q']}")
        print(f"[A{i + 1}] {turn['a']}\n")

        if i < len(evaluation):
            criteria = evaluation[i].get("criteria", [])
            grades = evaluation[i].get("grades", [])

            feedback = generate_feedback(
                summary, turn["s"], strategy_dict[turn["s"]]["질문전략"], turn["q"], turn["a"], criteria, grades
            )

            print("평가 요약:")
            for j, (c, g, f) in enumerate(zip(criteria, grades, feedback), 1):
                print(f"  {j}. {c} [{g}]")
                print(f"   - 피드백: {f}")
        else:
            print("평가 없음")

        print("-" * 100)

    print("\n😊 인터뷰가 종료되었습니다. 수고하셨습니다!")

    return state
