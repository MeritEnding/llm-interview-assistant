import gradio as gr

# 세션 상태 초기화 함수
def initialize_state():
    return {
        "state": None,               # 면접 관련 상태 정보 저장
        "interview_started": False,  # 면접 시작 여부
        "interview_ended": False,    # 면접 종료 여부
        "chat_history": []           # 사용자와 AI 면접관의 대화 내역
    }

# 이력서 업로드 후 초기 질문 설정 및 상태 갱신
def upload_and_initialize(file_obj, session_state):
    if file_obj is None:
        return session_state, "📝 파일을 업로드해주세요."

    file_path = file_obj.name
    state = preProcessing_Interview(file_path)  # 이력서 전처리 및 질문 전략 수립

    session_state["state"] = state
    session_state["interview_started"] = True

    first_question = state["current_question"]
    session_state["chat_history"].append(["🤖 AI 면접관", first_question])

    return session_state, session_state["chat_history"]

# 사용자 입력 처리 및 인터뷰 흐름 관리
def chat_interview(user_input, session_state):
    if not session_state["interview_started"]:
        return session_state, "먼저 이력서를 업로드하고 가상면접을 시작하세요."

    # 사용자 답변 저장
    session_state["chat_history"].append(["🙋‍♂️ 지원자", user_input])

    # 답변 상태 갱신
    session_state["state"] = update_current_answer(session_state["state"], user_input)
    session_state["state"] = graph.invoke(session_state["state"])

    # 인터뷰 종료 여부 확인
    if session_state["state"]["next_step"] == "end":
        session_state["interview_ended"] = True

        # 최종 면접 요약 생성
        final_summary = "✅ 면접이 종료되었습니다. 아래는 각 문항에 대한 피드백입니다.\n\n"
        for i, turn in enumerate(session_state["state"]["conversation"]):
            final_summary += f"---\n\n**[Q{i + 1}]** _({turn['s']})_\n{turn['q']}\n"
            final_summary += f"**[A{i + 1}]**\n{turn['a']}\n"

            if i < len(session_state["state"]["evaluation"]):
                eval_result = session_state["state"]["evaluation"][i]
                criteria = eval_result.get("criteria", [])
                grades = eval_result.get("grades", [])
                feedback = generate_feedback(
                    session_state["state"]["resume_summary"],
                    turn["s"],
                    session_state["state"]["strategy_dict"][turn["s"]]["질문전략"],
                    turn["q"],
                    turn["a"],
                    criteria,
                    grades
                )

                final_summary += "\n📌 피드백\n"
                for c, g, f in zip(criteria, grades, feedback):
                    final_summary += f"[{c} | {g}]\n👉 {f}\n"

        final_summary += "\n---\n\n😊 수고하셨습니다!"

        # 최종 요약을 대화 내역에 추가
        session_state["chat_history"].append(["🤖 AI 면접관", final_summary])

        return session_state, session_state["chat_history"], gr.update(value="")

    else:
        # 다음 질문 출력
        next_question = session_state["state"]["current_question"]
        session_state["chat_history"].append(["🤖 AI 면접관", next_question])

        return session_state, session_state["chat_history"], gr.update(value="")

# Gradio UI 구성
with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as demo:
    session_state = gr.State(initialize_state())

    # 상단 제목 및 설명
    gr.Markdown("# 🎙️ KK기업 AI 모의면접")
    gr.Markdown("지원자의 이력서를 기반으로 면접이 진행됩니다. 최소 7개, 최대 17개의 질문을 받게 됩니다.")

    # 파일 업로드 + 인터뷰 시작 버튼
    with gr.Row():
        with gr.Column(scale=2):
            file_input = gr.File(label="📝 이력서 업로드 (PDF 또는 DOCX)")
        with gr.Column(scale=1):
            upload_btn = gr.Button("🚀 인터뷰 시작", size="lg")

    # 채팅 인터페이스 및 입력창
    chatbot = gr.Chatbot(label="💬 AI 면접관 대화창", height=500)
    user_input = gr.Textbox(show_label=False, placeholder="답변을 입력하고 Enter를 눌러주세요.", lines=1)

    # 버튼 클릭 시 파일 업로드 및 초기 질문 출력
    upload_btn.click(upload_and_initialize, inputs=[file_input, session_state], outputs=[session_state, chatbot])

    # 사용자 입력 제출 시 인터뷰 처리
    user_input.submit(chat_interview, inputs=[user_input, session_state], outputs=[session_state, chatbot])
    user_input.submit(lambda: "", None, user_input)  # 입력창 초기화용

# 앱 실행
demo.launch(share=True)
