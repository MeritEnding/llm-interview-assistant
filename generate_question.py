def generate_question(state: InterviewState) -> InterviewState:
    summary = state["resume_summary"]
    keywords = ", ".join(state.get("resume_keywords", []))
    # used_keywords = state.get("used_keywords", set())
    strategy = state["current_strategy"]
    strategy_info = state["strategy_dict"][strategy]["질문전략"]
    previous_strategy = state["previous_strategy"]
    conversation = state.get("conversation", [])
    evaluation = state.get("evaluation", [])

    # 마지막 질문/답변/평가
    last_qa = conversation[-1] if conversation else {}
    last_eval = evaluation[-1] if evaluation else {}

    # 지금까지 질문에 사용되지 않은 키워드
    # unused_keywords = set(state["resume_keywords"]) - used_keywords

    # 현재 질문 전략을 기반으로 유사 질문 검색
    results = database.similarity_search(
        query=last_qa.get("q", ""),
        k=3,
        filter={"strategy": strategy}
    )
    similar_questions = "\n".join([f"- {doc.page_content}" for doc in results])

    # 프롬프트 템플릿 구성
    prompt = ChatPromptTemplate.from_template("""
        # AI 면접관 질문 생성 시스템

        ## 역할 정의
        당신은 10년 경력의 전문 면접관입니다. 수천 명의 지원자를 평가한 경험을 바탕으로, 전략적 질문을 설계하여 지원자의 잠재력과 실질 역량을 검증하는 역할을 맡고 있습니다. 목표는 질문 전략에 맞는 심층적 질문을 생성하고, 전략 전환 여부에 따라 적절한 방향으로 면접을 이어가는 것입니다.

        ---

        ## 입력 정보

        ### 이력서 요약
        {summary}

        ### 핵심 키워드
        {keywords}

        ### 현재 질문 전략 ({strategy})
        - 전략 설명: {strategy_info}

        ### 직전 질문 및 평가
        - 직전 질문 전략: {previous_strategy}
        - 직전 질문: {last_question}
        - 직전 답변: {last_answer}
        - 직전 평가 기준: {last_eval_criteria}
        - 직전 평가 등급: {last_eval_grades}

        ### 유사 질문 참고
        {similar_questions}

        ---

        ## 작성 지침

        아래 조건에 따라 새로운 면접 질문을 한 문장 생성하세요.

        ### 전략이 동일한 경우 (현재 전략 == 직전 전략)
        - 직전 답변에서 불명확하거나 약점으로 평가된 부분을 후속 질문으로 심화하세요
        - 낮은 등급을 받은 평가 기준을 보완할 수 있도록 질문을 유도하세요
        - 피상적인 답변을 방지하기 위해 구체적 상황이나 사례를 요구하는 문장으로 구성하세요

        ### 전략이 바뀐 경우 (현재 전략 != 직전 전략)
        - 직전 질문과 무관하게 새로운 전략의 핵심 역량을 평가할 수 있는 질문을 생성하세요
        - 이력서 요약 및 핵심 키워드 중 해당 전략과 관련된 내용이 드러난 부분을 활용하세요
        - 지원자의 경험 또는 전문성을 새로운 관점에서 조명할 수 있는 질문으로 설계하세요

        ---

        ## 면접 질문 작성 원칙

        - 지원자의 사고 과정을 유도하는 비예측적·심층적 질문일 것
        - 단순 경험 나열이 아닌 행동과 판단, 가치관이 드러나도록 유도할 것
        - 현재 전략의 목적에 정밀하게 부합할 것
        - 면접관다운 자연스러운 톤과 구조로 작성할 것

        ---

        ## 출력 지침

        아래 조건을 정확히 따르세요.

        - 한 문장의 질문만 출력하세요
        - 부가 설명, 지시문, 여는 문구 등은 포함하지 마세요
        """
    )

    # LLM 체인 구성 및 호출
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6)  # 응답의 다양성 확보
    chain = prompt | llm
    response = chain.invoke({
        "summary": summary,
        "keywords": keywords,
        # "unused_keywords": unused_keywords,
        "strategy": strategy,
        "strategy_info": strategy_info,
        "previous_strategy": previous_strategy,
        "last_question": last_qa.get("q", ""),
        "last_answer": last_qa.get("a", ""),
        "last_eval_criteria": last_eval.get("criteria", []),
        "last_eval_grades": last_eval.get("grades", []),
        "similar_questions": similar_questions
    })

    # 질문 생성에 사용된 핵심 키워드 저장
    new_used = {kw for kw in state["resume_keywords"] if kw in response.content.strip()}

    return {
        **state,
        "current_question": response.content.strip(),
        "current_answer": "",  # 답변 초기화
        # "used_keywords": used_keywords.union(new_used)
    }
