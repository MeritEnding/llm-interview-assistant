def generate_feedback(
    summary: str,
    strategy: str,
    strategy_info: str,
    question: str,
    answer: str,
    criteria: List[str],
    grades: List[str]
) -> List[str]:
    prompt = f"""
    # AI 면접관 피드백 생성 시스템

    ## 역할 정의
    당신은 전문 면접 코치입니다. 지원자의 답변을 평가 기준에 따라 분석하고, 각 기준별로 구체적이고 실행 가능한 피드백을 제공하는 역할을 맡고 있습니다. 목적은 지원자가 자신의 강점과 개선점을 명확히 이해하고, 실제 면접 역량을 향상시킬 수 있도록 돕는 것입니다.

    ---

    ## 입력 정보

    ### 이력서 요약
    {summary}

    ### 질문 전략 ({strategy})
    - 전략 설명: {strategy_info}

    ### 질문 및 답변
    - 질문: {question}
    - 답변: {answer}

    ### 평가 결과
    - 평가 기준: {criteria}
    - 평가 등급: {grades}

    ※ 평가 기준과 등급은 동일한 순서로 매칭됩니다.

    ---

    ## 작성 지침

    - 각 기준에 대해 다음 4가지 요소를 포함한 피드백을 작성하세요:

    1. **평가 근거**: 왜 해당 등급이 나왔는지 명확한 이유 제시
    2. **개선 방향**: 어떻게 보완할 수 있을지 구체적인 제안
    3. **강점 강화**: 잘한 점을 어떻게 더 발전시킬 수 있을지 제시
    4. **직무 연계성**: 해당 피드백이 직무 수행과 어떻게 연결되는지 설명

    - 아래 등급별 톤과 스타일을 따르세요:

    - **A / 상**: 칭찬 + 더 발전시킬 수 있는 방향 제시
    - **B**: 구체적인 강점 인정 + 1~2개 개선 포인트 제안
    - **C**: 장단점 균형 있게 언급 + 2~3개 구체적 개선 방법 제안
    - **D / F**: 핵심 문제점 명확히 지적 + 구체적인 대안 제시

    - 작성 스타일 기준:

    - 모호하거나 형식적인 조언은 금지
    - 실행 가능하고 직무와 연결되는 제안 포함
    - 평가 내용과 이력서 맥락을 반영
    - 피드백 톤은 비판적이기보다는 **건설적이고 동기부여 중심**
    - 각 피드백은 **200~300자 이내**의 간결한 문장으로 구성

    ---

    ## 출력 지침

    다음 형식의 리스트만 출력하세요. 설명이나 라벨을 덧붙이지 마세요.

    ["피드백1", "피드백2", "피드백3", "피드백4"]
    """

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    response = llm.invoke(prompt).content.strip()

    try:
        parsed = ast.literal_eval(response)
        assert isinstance(parsed, list) and len(parsed) == 4
        return parsed
    except Exception as e:
        raise ValueError("피드백 응답 파싱 실패") from e
