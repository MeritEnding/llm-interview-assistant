def preProcessing_Interview(file_path: str) -> InterviewState:
    # 1. 이력서 텍스트 추출
    resume_text = extract_text_from_file(file_path)

    # 2. 상태 초기화
    initial_state: InterviewState = {
        "resume_text": resume_text,
        "resume_summary": "",
        "resume_keywords": [],
        "strategy_dict": {},
        "strategy_order": [],
        "current_question": "",
        "current_answer": "",
        "current_strategy": "",
        "current_strategy_index": 0,
        # "used_keywords": set(),
        "conversation": [],
        "evaluation": [],
        "next_step": "",
        "previous_strategy": "",
        "check": 0,
        "satisfied": False
    }

    # 3. 이력서 분석 (요약 + 키워드)
    state = analyze_resume(initial_state)

    # 4. 질문 전략 수립 (예시 질문 포함)
    state = generate_question_strategy(state)

    # 5. 도입 질문 생성
    strategy_key = state["strategy_order"][0]                                                         # 첫 번째 카테고리 선택
    selected_question = state["strategy_dict"][strategy_key].get("예시질문", "자기소개를 해주세요.")  # 해당 카테고리의 예시 질문 꺼내기
    # used_keywords = {kw for kw in state["resume_keywords"] if kw in selected_question}                # 지금 사용된 핵심 키워드 저장

    return {
        **state,
        "current_strategy": strategy_key,
        "current_strategy_index": 0,
        "current_question": selected_question,
        # "used_keywords": used_keywords
    }
