def generate_question_strategy(state: InterviewState) -> InterviewState:
    summary = state["resume_summary"]
    keywords = ", ".join(state.get("resume_keywords", []))

    # 프롬프트 템플릿 구성
    prompt = ChatPromptTemplate.from_template("""
        # AI 면접관 질문 전략 수립 시스템

        ## 역할 정의
        당신은 15년 경력의 전문 면접관입니다. 지원자의 이력과 핵심 역량을 바탕으로, 다양한 평가 카테고리에 맞는 전략적 질문 프레임워크를 설계하는 역할을 맡고 있습니다. 목적은 각 전략별로 지원자의 역량을 정확히 검증할 수 있는 질문 방향과 구체적 문항을 수립하는 것입니다.

        ---

        ## 입력 정보

        ### 이력서 요약
        {summary}

        ### 핵심 키워드
        {keywords}

        ---

        ## 작성 지침

        다음 7가지 질문 전략 카테고리에 대해 각각 아래 2가지 항목을 작성하세요:

        1. **지원동기**: 진정성, 포부, 열정, 직무 이해도
        2. **경험**: 성과, 깊이 있는 실무 역량
        3. **협업**: 팀워크, 갈등 해결, 의사소통, 리더십
        4. **가치관**: 직업 윤리, 조직문화 적합성
        5. **직무이해**: 전문 지식, 업계 동향, 기술 이해
        6. **조직적응**: 변화 수용력, 스트레스 대처, 조직 내 행동방식
        7. **상황대처**: 문제 해결력, 의사결정, 위기 대응

        ### 항목별 작성 내용
        - **질문전략**: 해당 전략이 중요하게 평가해야 할 이유와 목표, 어떤 답변 신호를 중점적으로 볼 것인지 설명
        - **예시질문**: STAR(상황-과제-행동-결과) 방식 기반의 구체적이고 개방형 질문 문장

        ---

        ## 출력 지침

        다음 형식에 맞춰 모든 카테고리에 대해 출력하세요. 형식을 변경하거나 설명을 추가하지 마세요.

        [지원동기]
        질문전략: 전략 설명
        예시질문: 개방형 질문

        [경험]
        질문전략: ...
        예시질문: ...

        ... 이하 동일
    """)

    # LLM 체인 구성 및 호출
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.4)
    chain = prompt | llm
    response = chain.invoke({
        "summary": summary,
        "keywords": keywords
    })
    content = response.content.strip()

    # 응답 파싱
    strategy_dict ={}
    current_category = None

    for line in content.splitlines():  # 응답을 줄바꿈 단위로 잘라서 리스트로 만듦
        line = line.strip()

        if line.startswith("[") and line.endswith("]"):
            current_category = line.strip("[]").strip()
            strategy_dict[current_category] = {}  # current_category를 key로, 딕셔너리를 value로

        elif line.startswith("질문전략:") and current_category:
            strategy_dict[current_category]["질문전략"] = line.replace("질문전략:", "").strip()  # 질문전략이 value 딕셔너리의 key가 됨

        elif line.startswith("예시질문:") and current_category:
            strategy_dict[current_category]["예시질문"] = line.replace("예시질문:", "").strip()  # 예시질문도 value 딕셔너리의 key가 됨

    return {
        **state,
        "strategy_dict": strategy_dict,
        "strategy_order": list(strategy_dict.keys())
    }
