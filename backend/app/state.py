from typing import Literal, TypedDict

from app.schemas import (
    CandidateProfile,
    Evaluation,
    FinalEvaluation,
    InterviewMessage,
)


InterviewRound = Literal[
    "hr",
    "technical",
    "manager",
    "completed",
]


class InterviewState(TypedDict):
    candidate_profile: CandidateProfile
    job_description: str

    current_round: InterviewRound
    question_number: int
    max_questions: int

    recent_messages: list[InterviewMessage]
    conversation_summary: str

    topics_covered: list[str]

    current_question: str
    current_topic: str

    latest_answer: str

    hr_evaluation: Evaluation | None
    technical_evaluation: Evaluation | None
    manager_evaluation: Evaluation | None

    final_evaluation: FinalEvaluation | None

    round_complete: bool
    interview_complete: bool