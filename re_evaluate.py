def re_evaluate(state: InterviewState):
    summary = state["resume_summary"]
    keywords = ", ".join(state.get("resume_keywords", []))
    strategy = state["current_strategy"]
    strategy_info = state["strategy_dict"][strategy]["질문전략"]
    question = state.get("current_question", "")
    answer = state.get("current_answer", "")

    # evaluate 노드에서 평가한 결과 가져오기
    evaluation = state.get("evaluation", [])
    last_eval = evaluation[-1] if evaluation else {}
    prev_criteria = last_eval.get("criteria", [])  # 평가 기준
    prev_grades = last_eval.get("grades", [])      # 평가 등급

    # "중" 또는 "하"를 받은 평가 기준만 선별
    prev_eval = "\n".join([f"- {c}: {g}" for c, g in zip(prev_criteria, prev_grades) if g in {"중", "하"}])

    # 프롬프트 템플릿 구성
    prompt = ChatPromptTemplate.from_template("""
        # AI 면접관 정밀 답변 재평가 시스템

        ## 역할 정의
        당신은 GPT 기반의 정밀 AI 면접관입니다. 1차 평가에서 '중' 또는 '하' 등급을 받은 답변을 더 깊이 분석하여, 보다 정확하고 구체적인 판단을 내리는 역할을 맡고 있습니다. 목적은 모호하거나 부족했던 영역에 대해 A~F 등급으로 정밀하게 분류하는 것입니다.

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

        ### 1차 평가 결과 (중/하 등급 기준)
        {prev_eval}

        ---

        ## 작성 지침

        - 아래 30가지 평가 기준 중 **현재 질문과 답변에 가장 적합한 4개**를 선택하세요.
        - 각 기준에 대해 **A / B / C / D / F** 중 하나의 등급을 부여하세요.
        - 판단 시 다음 사항을 반드시 고려하세요:
        1. 질문 전략의 핵심 목적과 일치 여부
        2. 이력서 및 키워드와의 정합성
        3. 직무 적합성과 실질적 검증력
        4. 1차 평가에서 지적된 약점의 개선 여부 또는 반복 여부

        ---

        ## 평가 기준 설명

        1. **질문과의 연관성**: 질문의 핵심 의도에 적절하게 대응했는가
        2. **답변의 구체성**: 수치, 사례, 행동 중심으로 내용을 구체화했는가
        3. **논리적 구성**: 서론-본론-결론 흐름과 인과관계가 명확한가
        4. **표현의 명확성**: 문장 구성과 어휘 선택이 간결하고 정확한가
        5. **진정성**: 답변이 형식적이지 않고 진심이 느껴지는가
        6. **직무 이해도**: 해당 직무의 핵심 역할과 역량을 정확히 이해하고 있는가
        7. **자기 이해도**: 자신의 강점, 약점, 가치관을 명확히 이해하고 설명했는가
        8. **입사 동기 명확성**: 회사/직무와의 연결된 명확한 지원 동기가 제시되었는가
        9. **경험과 직무의 연결성**: 제시된 경험이 지원 직무와 밀접하게 연관되는가
        10. **문제 해결 과정 설명력**: 문제 인식, 접근법, 해결 결과가 구조적으로 설명되었는가
        11. **팀워크 경험 서술**: 협업 맥락에서의 역할, 기여, 소통 방식이 잘 드러났는가
        12. **리더십 경험**: 의사결정, 팀 조율, 갈등 해결 등 리더로서의 행동이 구체적으로 나타났는가
        13. **도전정신**: 안정적 상황이 아닌 도전적 목표나 과업에 스스로 임한 경험이 있는가
        14. **책임감**: 결과에 대해 끝까지 책임지고 이행한 태도가 드러나는가
        15. **주도성 / 적극성**: 스스로 과제를 정의하고 추진한 주체적인 행동이 있었는가
        16. **위기 / 스트레스 대응**: 예기치 못한 상황에서 침착하고 유연하게 대응했는가
        17. **자기계발 / 학습 의지**: 지속적 학습, 피드백 수용, 성장 노력이 나타났는가
        18. **기술 / 전공 역량**: 실질적인 직무 관련 지식, 기술을 보유하고 있는가
        19. **성과 중심 설명**: 성과를 수치, 결과 지표 등으로 구체화했는가
        20. **일관성 / 전체 흐름**: 답변 내용 간의 충돌 없이 전반적으로 흐름이 매끄러운가
        21. **기업 및 산업 이해도**: 조직 구조, 산업 구조, 경쟁 환경 등을 이해하고 있는가
        22. **성장 잠재력 및 학습 민첩성**: 새로운 지식이나 상황에 빠르게 적응하고 흡수하는 능력이 있는가
        23. **가치관 및 조직 적합성**: 개인 가치관과 기업 문화가 조화롭게 맞아떨어지는가
        24. **의사소통 효율성 및 설득력**: 전달 구조, 설득 논리, 수용성을 갖춘 표현을 했는가
        25. **성찰적 사고 및 피드백 수용**: 과거를 객관적으로 돌아보고 개선하려는 태도가 있는가
        26. **창의적 문제 해결**: 정형화된 방식 외에 창의적으로 문제에 접근한 사례가 있는가
        27. **데이터 기반 분석 및 의사결정**: 데이터를 기반으로 분석, 판단한 근거가 있는가
        28. **적응 유연성 및 변화 관리**: 환경 변화에 민첩하게 대응하고 주도한 경험이 있는가
        29. **윤리 의식 및 직업적 책임감**: 윤리 기준, 책임 태도에 대한 인식이 드러나는가
        30. **고객 중심 사고 및 서비스 지향성**: 이해관계자 입장에서 문제를 바라보고 해결한 태도가 있는가

        ---

        ## 등급 정의

        - **A (매우 우수)**: 기준을 완벽히 충족함. 깊이, 구체성, 전문성이 탁월하며 기대를 뛰어넘음
        - **B (우수)**: 기준을 충분히 충족함. 뚜렷한 강점이 있으며 구조와 논리도 잘 갖춤
        - **C (보통)**: 기준을 기본적으로 충족함. 구성은 있으나 깊이·명확성 부족
        - **D (미흡)**: 기준 충족이 부족함. 내용이 추상적이거나 논리 연결이 약함
        - **F (매우 미흡)**: 기준을 거의 충족하지 못함. 질문 의도를 반영하지 못하고 본질적으로 설득력이 떨어짐

        ---

        ## 출력 지침

        다음 형식의 리스트만 출력하세요. 설명 없이 아래 형식을 정확히 따르세요.

        ["기준1", "기준2", "기준3", "기준4", "등급1", "등급2", "등급3", "등급4"]

        예시: ["질문과의 연관성", "진정성", "책임감", "기업 및 산업 이해도", "A", "C", "B", "F"]
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
        "answer": answer,
        "prev_eval": prev_eval
    })
    content = response.content.strip()

    # 응답 파싱
    try:
        parsed = ast.literal_eval(content)
        assert isinstance(parsed, list) and len(parsed) == 8
    except Exception as e:
        raise ValueError("답변 재평가 응답 파싱 실패") from e

    # 리스트 분리
    criteria = parsed[:4]
    grades = parsed[4:]

    # 대화 기록 업데이트
    conversation = state.get("conversation", [])
    if conversation:
        conversation[-1] = {
            "s": strategy,
            "q": question,
            "a": answer
        }

    # 평가 결과 업데이트
    evaluation = state.get("evaluation", [])
    if evaluation:
        evaluation[-1] = {
            "question_index": len(conversation) - 1,
            "criteria": criteria,
            "grades": grades
        }

    return state
