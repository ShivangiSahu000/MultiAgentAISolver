from typing import TypedDict, List, Dict


class AgentState(TypedDict, total=False):

    initial_prompt: str

    clarification_batch: int
    max_clarification_batches: int

    questions: List[str]

    current_batch_answers: List[str]

    clarification_answers: List[Dict[str, str]]

    clarification_history: List[Dict]

    final_requirements: str

    solution_a: str
    solution_b: str
    solution_c: str

    citations_a: List[str]
    citations_b: List[str]
    citations_c: List[str]

    adversarial_feedback_a: str
    adversarial_feedback_b: str
    adversarial_feedback_c: str

    refinement_round: int
    max_refinement_rounds: int

    final_answer: str
    final_citations: List[str]