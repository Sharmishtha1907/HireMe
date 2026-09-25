from langchain_core.prompts import ChatPromptTemplate
from backend.app.state import InterviewState
from backend.app.llm_core.llm_connection import get_llm
from backend.app.schemas import AgentResponse
from backend.app.prompts import dic

llm = get_llm()


def hr_agent(state: InterviewState) -> InterviewState:

    structured_llm= llm.with_structured_output(
        AgentResponse
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", dic["HR_SYSTEM_PROMPT"]),
            (
                "human",
                """
                Candidate Profile:
                {candidate_profile}

                Job Description:
                {job_description}

                Current Question:
                {current_question}

                Current Topic:
                {current_topic}

                Latest Candidate Answer:
                {latest_answer}

                Questions Already Asked:
                {question_number}

                Maximum Questions:
                {max_questions}

                Topics Already Covered:
                {topics_covered}

                Recent Conversation:
                {conversation}

                Conversation Summary:
                {conversation_summary}
                """,
                            ),
                        ]
                    )

    chain = prompt | structured_llm

    conversation = "\n".join(
        f"{message.role}: {message.content}"
        for message in state["recent_messages"]
    )

    response: AgentResponse = chain.invoke(
        {
            "candidate_profile": state[
                "candidate_profile"
            ].model_dump_json(indent=2),
            "job_description": state["job_description"],
            "current_question": state["current_question"],
            "current_topic": state["current_topic"],
            "latest_answer": state["latest_answer"],
            "question_number": state["question_number"],
            "max_questions": state["max_questions"],
            "topics_covered": ", ".join(
                state["topics_covered"]
            ),
            "conversation": conversation,
            "conversation_summary": state[
                "conversation_summary"
            ],
        }
    )

    if response.evaluation:
        state["hr_evaluation"] = response.evaluation

    if response.action == "end_round":
        state["round_complete"] = True
        state["current_question"] = ""
        state["current_topic"] = ""
        return state

    state["current_question"] = response.question or ""
    state["current_topic"] = response.topic or ""

    if response.topic and response.topic not in state["topics_covered"]:
        state["topics_covered"].append(response.topic)

    state["round_complete"] = False

    state["question_number"] += 1

    return state