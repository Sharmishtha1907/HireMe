from typing import Literal
from pydantic import BaseModel, Field


class CurrentUser(BaseModel):
    keycloak_id: str
    username: str | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None

    groups: list[str] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)

    @property
    def is_premium(self) -> bool:
        return "premium" in self.roles

    @property
    def is_basic(self) -> bool:
        return "basic" in self.roles


class Experience(BaseModel):
    company: str = ""
    role: str = ""
    duration: str = ""
    responsibilities: list[str] = Field(default_factory=list)


class Project(BaseModel):
    name: str = ""
    description: str = ""
    technologies: list[str] = Field(default_factory=list)


class CandidateProfile(BaseModel):
    name: str = ""
    email: str = ""
    experience_years: int | None = None

    skills: list[str] = Field(default_factory=list)

    experience: list[Experience] = Field(default_factory=list)

    projects: list[Project] = Field(default_factory=list)

    education: list[str] = Field(default_factory=list)

    resume_text: str = ""


class InterviewQuestion(BaseModel):
    action: Literal[
        "ask_question",
        "end_round",
    ]

    question: str | None = None
    topic: str | None = None

    difficulty: Literal[
        "easy",
        "medium",
        "hard",
    ] | None = None


class CandidateAnswer(BaseModel):
    answer: str


class InterviewMessage(BaseModel):
    role: Literal[
        "system",
        "interviewer",
        "candidate",
    ]

    content: str


class Evaluation(BaseModel):
    score: float = Field(
        ge=0,
        le=100,
    )

    strengths: list[str] = Field(default_factory=list)

    weaknesses: list[str] = Field(default_factory=list)

    technical_gaps: list[str] = Field(default_factory=list)

    communication_score: float = Field(
        ge=0,
        le=100,
    )

    feedback: str = ""

    improvement_plan: list[str] = Field(default_factory=list)


class AgentResponse(BaseModel):
    action: Literal[
        "ask_question",
        "end_round",
    ]

    question: str | None = None
    topic: str | None = None

    difficulty: Literal[
        "easy",
        "medium",
        "hard",
    ] | None = None

    evaluation: Evaluation | None = None


class FinalEvaluation(BaseModel):
    overall_score: float = Field(
        ge=0,
        le=100,
    )

    readiness: Literal[
        "excellent",
        "good",
        "developing",
        "needs_improvement",
    ]

    strengths: list[str] = Field(default_factory=list)

    weaknesses: list[str] = Field(default_factory=list)

    improvement_plan: list[str] = Field(default_factory=list)

    summary: str = ""