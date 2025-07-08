class InterviewState(TypedDict):
    # 면접 준비 단계
    resume_text: str                      # 이력서 원문 텍스트
    resume_summary: str                   # 이력서 요약문
    resume_keywords: List[str]            # 핵심 키워드 리스트
    strategy_dict: Dict[str, Dict]        # 질문 전략 딕셔너리
    strategy_order: List[str]             # 질문 전략 순서 리스트

    # 면접 진행 단계
    current_question: str                 # 현재 질문
    current_answer: str                   # 현재 답변
    current_strategy: str                 # 현재 질문이 속한 질문 전략
    current_strategy_index: int           # 질문 전략 순회용 인덱스
    # used_keywords: Set[str]               # 질문에 사용된 키워드 집합
    conversation: List[Dict[str, str]]    # 누적된 질문-답변 기록
    evaluation: List[Dict]                # 각 답변에 대한 평가 결과
    next_step: str                        # 다음 단계 결정 지표

    # 답변 평가용
    previous_strategy: str                # 이전 질문이 속한 질문 전략
    check: int                            # 동일 질문 전략 연속 횟수
    satisfied: bool                       # 현재 질문 전략 완료 여부
