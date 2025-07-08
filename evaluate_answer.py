def evaluate_answer(state: InterviewState) -> InterviewState:
    summary = state["resume_summary"]
    keywords = ", ".join(state.get("resume_keywords", []))
    strategy = state["current_strategy"]
    strategy_info = state["strategy_dict"][strategy]["질문전략"]
    question = state.get("current_question", "")
    answer = state.get("current_answer", "")

    # 프롬프트 템플릿 구성
    prompt = ChatPromptTemplate.from_template("""
        # AI 면접관 1차 답변 평가 시스템

        ## 역할 정의
        당신은 전문 면접 평가자로서, 지원자의 답변을 전략적 질문 목적에 따라 분석하고, 적절한 평가 기준을 선택해 등급을 부여하는 역할을 맡고 있습니다. 평가 목적은 지원자의 실질적 역량, 표현력, 직무 적합성을 정량적으로 판단하는 것입니다.

        ---

        ## 입력 정보

        ### 이력서 요약
        {summary}

        ### 핵심 키워드
        {keywords}

        ### 현재 질문 전략 ({strategy})
        - 전략 설명: {strategy_info}

        ### 질문 및 답변
        - 질문: {question}
        - 답변: {answer}

        ---

        ## 작성 지침

        - 아래 10가지 평가 기준 중 **질문 및 답변에 가장 적합한 4개**를 선택하세요.
        - 선택한 각 기준에 대해 **상 / 중 / 하** 중 하나의 등급을 부여하세요.
        - 기준 선택 시 다음 요소를 반드시 고려하세요:
        1. 해당 전략에서 가장 중요하게 평가하는 역량
        2. 이력서와 키워드를 통해 드러난 강점 또는 약점
        3. 직무 수행 능력과의 연관성

        ---

        ## 평가 기준 설명

        1. **질문 이해도**: 질문의 핵심 의도와 맥락을 명확히 파악하고, 정확히 대응하는가
        2. **경험 구체성**: 실제 사례, 수치, 행동 중심으로 구체적인 설명을 제공하는가
        3. **논리적 구조화**: 답변이 도입-전개-결론 구조로 조직되고, 논리적으로 연결되는가
        4. **직무 적합성**: 제시된 역량이 해당 직무와 실질적으로 얼마나 연관되는가
        5. **전문성 입증**: 전문 지식이나 기술적 통찰력을 드러내고 있는가
        6. **성과 지향성**: 결과와 임팩트 중심으로 자신의 기여를 보여주는가
        7. **문제 해결력**: 문제 인식 → 접근 방식 → 해결 → 결과의 과정이 체계적으로 설명되는가
        8. **팀워크와 협업**: 팀 내 역할, 갈등 해결, 공동 성과 창출 경험이 구체적으로 언급되는가
        9. **적응력과 학습능력**: 새로운 환경이나 기술 변화에 능동적으로 적응하고 학습하는가
        10. **동기와 열정**: 직무 또는 산업에 대한 진정성 있는 관심과 장기적인 비전을 가지고 있는가

        ---

        ## 등급 정의

        - **상**: 기준을 매우 우수하게 충족함. 답변이 전략 목적에 정확히 부합하며 인상적인 강점을 보임.
        - **중**: 기준을 기본적으로 충족함. 의미 있는 내용이 있으나 구조나 깊이 면에서 개선 여지가 있음.
        - **하**: 기준 충족이 부족함. 질문의 의도를 제대로 반영하지 못하거나 내용이 모호하고 피상적임.

        ---

        ## 출력 지침

        다음 형식의 리스트만 출력하세요. 부가 설명이나 해석은 포함하지 마세요.

        ["기준1", "기준2", "기준3", "기준4", "등급1", "등급2", "등급3", "등급4"]

        예시: ["질문 이해도", "경험 구체성", "문제 해결력", "동기와 열정", "중", "상", "하", "중"]
    """)

    # LLM 체인 구성 및 호출
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | llm
    response = chain.invoke({
        "summary": summary,
        "keywords": keywords,
        "strategy": strategy,
        "strategy_info": strategy_info,
        "question": question,
        "answer": answer
    })
    content = response.content.strip()

    # 응답 파싱
    try:
        parsed = ast.literal_eval(content)
        assert isinstance(parsed, list) and len(parsed) == 8
    except Exception as e:
        raise ValueError("답변 평가 응답 파싱 실패") from e

    # 리스트 분리
    criteria = parsed[:4]
    grades = parsed[4:]

    # 대화 기록 업데이트
    conversation = state.get("conversation", [])
    conversation.append({
        "s": strategy,
        "q": question,
        "a": answer
    })

    # 평가 결과 업데이트
    evaluation = state.get("evaluation", [])
    evaluation.append({
        "question_index": len(conversation) - 1,
        "criteria": criteria,
        "grades": grades
    })

    return state
