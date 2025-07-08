def analyze_resume(state: InterviewState) -> InterviewState:
		resume_text = state["resume_text"]
		
		prompt = ChatPromptTemplate.from_template("""
        # AI 면접관 이력서 분석 시스템

        ## 역할 정의
        당신은 최고 수준의 인재 분석 전문가입니다. 지원자의 이력서를 정밀하게 분석하여, 이들의 경력, 역량, 성장 가능성, 차별화된 강점 등을 도출하고 면접 전략 수립에 필요한 핵심 정보를 제공해야 합니다.

        ---

        ## 입력 정보

        ### 이력서 원문
        {resume_text}

        ---

        ## 작성 지침

        아래 두 가지 작업을 순차적으로 수행하세요:

        ### 1. 전략적 요약 작성
        - 지원자의 경력 경로와 주요 성과를 파악하세요.
        - 보유한 기술 역량, 도메인 전문성, 자격증/교육 이력을 식별하세요.
        - 리더십과 문제 해결 경험, 프로젝트 추진력, 혁신 사례를 분석하세요.
        - 성장 가능성과 발전 궤적을 평가하세요.
        - 위 항목을 기반으로 **논리적 흐름이 있는 자연스러운 서술문**으로 **10문장 이내**로 요약하세요.

        ### 2. 전략적 키워드 추출
        - 핵심 기술 역량 (예: 분석 도구, 프로그래밍 언어, 문제 해결 방법론 등)
        - 주요 소프트 스킬 (예: 협업, 책임감, 커뮤니케이션 등)
        - 산업 및 직무 관련 경험/전문성
        - 면접 질문이 필요한 잠재적 약점 또는 논의 포인트
        - 경쟁자 대비 차별화 요소
        - 위 내용을 기반으로, 면접 전략에 활용 가능한 **핵심 키워드 5~10개**를 **쉼표로 구분된 목록** 형태로 추출하세요.

        ---

        ## 출력 지침

        다음 형식을 **정확히 유지**하여 출력하세요. 형식을 변경하거나 설명을 덧붙이지 마세요.

        요약: 지원자에 대한 통합적이고 심층적인 요약

        키워드: 키워드1, 키워드2, 키워드3, ...
    """)
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    chain = prompt | llm
    response = chain.invoke({"resume_text": resume_text})
    content = response.content.strip()
    
    resume_summary = ""
    resume_keywords = []
    
    for line in content.splitlines():
		    line = line.strip()
		    if line.startswith("요약:"):
				   resume_summary = line.replace("요약:", "").strip()
				elif line.startswith("키워드:"):
					 keywords = line.replace("키워드:", "").strip()
					 resume_keywords = [kw.strip() for kw in keywords.split("," if kw.strip()]
					     
	   return {
		   **state,
		   "resume_summary": resume_summary,
		   "resume_keywords": resume_keywords,
	   }
