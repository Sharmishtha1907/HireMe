from typing import TypedDict

from app.schemas import CandidateProfile, Evaluation, FinalEvaluation


class InterviewMessage(TypedDict):
    role: str
    content: str


class InterviewState(TypedDict):
    # Candidate information
    candidate_profile: CandidateProfile
    job_description: str

    # Interview control
    current_round: str
    question_number: int
    max_questions: int

    # Conversation memory
    recent_messages: list[InterviewMessage]
    conversation_summary: str

    # Topics
    topics_covered: list[str]

    # Current question
    current_question: str
    current_topic: str

    # Candidate's latest answer
    latest_answer: str

    # Round evaluations
    hr_evaluation: Evaluation | None
    technical_evaluation: Evaluation | None
    manager_evaluation: Evaluation | None

    # Final result
    final_evaluation: FinalEvaluation | None

    # Flow control
    round_complete: bool
    interview_complete: bool