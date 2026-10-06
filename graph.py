# # # # from langgraph.graph import (
# # # #     StateGraph,
# # # #     START,
# # # #     END
# # # # )

# # # # from langgraph.types import interrupt

# # # # from langgraph.checkpoint.memory import (
# # # #     MemorySaver
# # # # )

# # # # from state import AgentState

# # # # from models import (
# # # #     clarification_llm,
# # # #     llm_a,
# # # #     llm_b,
# # # #     llm_c,
# # # #     synthesizer_llm
# # # # )

# # # # from prompts import (
# # # #     CLARIFICATION_PROMPT,
# # # #     CLARIFICATION_DECISION_PROMPT,
# # # #     REQUIREMENT_SUMMARY_PROMPT,
# # # #     SOLUTION_PROMPT,
# # # #     ADVERSARIAL_PROMPT,
# # # #     REFINEMENT_PROMPT,
# # # #     SYNTHESIS_PROMPT
# # # # )

# # # # from services.citations import (
# # # #     extract_citations
# # # # )


# # # # def clarification_agent(
# # # #     state: AgentState
# # # # ):

# # # #     response = clarification_llm.invoke(
# # # #         CLARIFICATION_PROMPT.format(
# # # #             prompt=state["initial_prompt"],
# # # #             history=state.get(
# # # #                 "clarification_history",
# # # #                 []
# # # #             )
# # # #         )
# # # #     )

# # # #     questions = []

# # # #     for line in response.content.splitlines():

# # # #         line = line.strip()

# # # #         if not line:
# # # #             continue

# # # #         if line[0].isdigit():

# # # #             if "." in line:

# # # #                 line = line.split(
# # # #                     ".",
# # # #                     1
# # # #                 )[1].strip()

# # # #             questions.append(line)

# # # #     return {
# # # #         "questions":
# # # #             questions[:5]
# # # #     }


# # # # def collect_answers(
# # # #     state: AgentState
# # # # ):

# # # #     questions = state["questions"]

# # # #     batch_number = (
# # # #         state["clarification_batch"]
# # # #     )

# # # #     answers = interrupt({

# # # #         "type":
# # # #             "clarification_batch",

# # # #         "batch":
# # # #             batch_number,

# # # #         "questions":
# # # #             questions
# # # #     })

# # # #     history = state.get(
# # # #         "clarification_history",
# # # #         []
# # # #     )

# # # #     batch_data = []

# # # #     for question, answer in zip(
# # # #         questions,
# # # #         answers
# # # #     ):

# # # #         batch_data.append({

# # # #             "question":
# # # #                 question,

# # # #             "answer":
# # # #                 answer
# # # #         })

# # # #     history.append({

# # # #         "batch":
# # # #             batch_number,

# # # #         "questions":
# # # #             questions,

# # # #         "answers":
# # # #             batch_data
# # # #     })

# # # #     return {

# # # #         "current_batch_answers":
# # # #             answers,

# # # #         "clarification_answers":
# # # #             batch_data,

# # # #         "clarification_history":
# # # #             history
# # # #     }


# # # # def increment_clarification_batch(
# # # #     state: AgentState
# # # # ):

# # # #     return {

# # # #         "clarification_batch":
# # # #             state["clarification_batch"] + 1
# # # #     }


# # # # def clarification_decision(
# # # #     state: AgentState
# # # # ):

# # # #     if (
# # # #         state["clarification_batch"]
# # # #         > state["max_clarification_batches"]
# # # #     ):

# # # #         return "finish"

# # # #     response = clarification_llm.invoke(
# # # #         CLARIFICATION_DECISION_PROMPT.format(

# # # #             prompt=
# # # #                 state["initial_prompt"],

# # # #             history=
# # # #                 state.get(
# # # #                     "clarification_history",
# # # #                     []
# # # #                 )
# # # #         )
# # # #     )

# # # #     decision = (
# # # #         response.content
# # # #         .strip()
# # # #         .upper()
# # # #     )

# # # #     if decision == "CONTINUE":

# # # #         return "continue"

# # # #     return "finish"


# # # # def build_final_requirements(
# # # #     state: AgentState
# # # # ):

# # # #     response = clarification_llm.invoke(
# # # #         REQUIREMENT_SUMMARY_PROMPT.format(

# # # #             prompt=
# # # #                 state["initial_prompt"],

# # # #             history=
# # # #                 state.get(
# # # #                     "clarification_history",
# # # #                     []
# # # #                 )
# # # #         )
# # # #     )

# # # #     return {

# # # #         "final_requirements":
# # # #             response.content
# # # #     }


# # # # def solution_a(
# # # #     state: AgentState
# # # # ):

# # # #     response = llm_a.invoke(
# # # #         SOLUTION_PROMPT.format(

# # # #             requirements=
# # # #                 state["final_requirements"]
# # # #         )
# # # #     )

# # # #     return {

# # # #         "solution_a":
# # # #             response.content,

# # # #         "citations_a":
# # # #             extract_citations(
# # # #                 response.content
# # # #             )
# # # #     }


# # # # def solution_b(
# # # #     state: AgentState
# # # # ):

# # # #     response = llm_b.invoke(
# # # #         SOLUTION_PROMPT.format(

# # # #             requirements=
# # # #                 state["final_requirements"]
# # # #         )
# # # #     )

# # # #     return {

# # # #         "solution_b":
# # # #             response.content,

# # # #         "citations_b":
# # # #             extract_citations(
# # # #                 response.content
# # # #             )
# # # #     }


# # # # def solution_c(
# # # #     state: AgentState
# # # # ):

# # # #     response = llm_c.invoke(
# # # #         SOLUTION_PROMPT.format(

# # # #             requirements=
# # # #                 state["final_requirements"]
# # # #         )
# # # #     )

# # # #     return {

# # # #         "solution_c":
# # # #             response.content,

# # # #         "citations_c":
# # # #             extract_citations(
# # # #                 response.content
# # # #             )
# # # #     }


# # # # def adversarial_b(
# # # #     state: AgentState
# # # # ):

# # # #     response = llm_b.invoke(
# # # #         ADVERSARIAL_PROMPT.format(

# # # #             requirements=
# # # #                 state["final_requirements"],

# # # #             solution=
# # # #                 state["solution_a"]
# # # #         )
# # # #     )

# # # #     return {

# # # #         "adversarial_feedback_a":
# # # #             response.content
# # # #     }


# # # # def adversarial_c(
# # # #     state: AgentState
# # # # ):

# # # #     response = llm_c.invoke(
# # # #         ADVERSARIAL_PROMPT.format(

# # # #             requirements=
# # # #                 state["final_requirements"],

# # # #             solution=
# # # #                 state["solution_b"]
# # # #         )
# # # #     )

# # # #     return {

# # # #         "adversarial_feedback_b":
# # # #             response.content
# # # #     }


# # # # def adversarial_a(
# # # #     state: AgentState
# # # # ):

# # # #     response = llm_a.invoke(
# # # #         ADVERSARIAL_PROMPT.format(

# # # #             requirements=
# # # #                 state["final_requirements"],

# # # #             solution=
# # # #                 state["solution_c"]
# # # #         )
# # # #     )

# # # #     return {

# # # #         "adversarial_feedback_c":
# # # #             response.content
# # # #     }


# # # # def refine_a(
# # # #     state: AgentState
# # # # ):

# # # #     response = llm_a.invoke(
# # # #         REFINEMENT_PROMPT.format(

# # # #             requirements=
# # # #                 state["final_requirements"],

# # # #             solution=
# # # #                 state["solution_a"],

# # # #             feedback=
# # # #                 state["adversarial_feedback_a"]
# # # #         )
# # # #     )

# # # #     return {

# # # #         "solution_a":
# # # #             response.content,

# # # #         "citations_a":
# # # #             extract_citations(
# # # #                 response.content
# # # #             )
# # # #     }


# # # # def refine_b(
# # # #     state: AgentState
# # # # ):

# # # #     response = llm_b.invoke(
# # # #         REFINEMENT_PROMPT.format(

# # # #             requirements=
# # # #                 state["final_requirements"],

# # # #             solution=
# # # #                 state["solution_b"],

# # # #             feedback=
# # # #                 state["adversarial_feedback_b"]
# # # #         )
# # # #     )

# # # #     return {

# # # #         "solution_b":
# # # #             response.content,

# # # #         "citations_b":
# # # #             extract_citations(
# # # #                 response.content
# # # #             )
# # # #     }


# # # # def refine_c(
# # # #     state: AgentState
# # # # ):

# # # #     response = llm_c.invoke(
# # # #         REFINEMENT_PROMPT.format(

# # # #             requirements=
# # # #                 state["final_requirements"],

# # # #             solution=
# # # #                 state["solution_c"],

# # # #             feedback=
# # # #                 state["adversarial_feedback_c"]
# # # #         )
# # # #     )

# # # #     return {

# # # #         "solution_c":
# # # #             response.content,

# # # #         "citations_c":
# # # #             extract_citations(
# # # #                 response.content
# # # #             )
# # # #     }


# # # # def increment_refinement_round(
# # # #     state: AgentState
# # # # ):

# # # #     return {

# # # #         "refinement_round":
# # # #             state["refinement_round"] + 1
# # # #     }


# # # # def refinement_router(
# # # #     state: AgentState
# # # # ):

# # # #     if (
# # # #         state["refinement_round"]
# # # #         >= state["max_refinement_rounds"]
# # # #     ):

# # # #         return "finish"

# # # #     return [
# # # #         "adversarial_b",
# # # #         "adversarial_c",
# # # #         "adversarial_a"
# # # #     ]


# # # # def synthesizer(
# # # #     state: AgentState
# # # # ):

# # # #     response = synthesizer_llm.invoke(
# # # #         SYNTHESIS_PROMPT.format(

# # # #             requirements=
# # # #                 state["final_requirements"],

# # # #             solution_a=
# # # #                 state["solution_a"],

# # # #             solution_b=
# # # #                 state["solution_b"],

# # # #             solution_c=
# # # #                 state["solution_c"],

# # # #             citations_a=
# # # #                 state.get(
# # # #                     "citations_a",
# # # #                     []
# # # #                 ),

# # # #             citations_b=
# # # #                 state.get(
# # # #                     "citations_b",
# # # #                     []
# # # #                 ),

# # # #             citations_c=
# # # #                 state.get(
# # # #                     "citations_c",
# # # #                     []
# # # #                 )
# # # #         )
# # # #     )

# # # #     return {

# # # #         "final_answer":
# # # #             response.content,

# # # #         "final_citations":
# # # #             extract_citations(
# # # #                 response.content
# # # #             )
# # # #     }


# # # # def build_graph():

# # # #     graph = StateGraph(
# # # #         AgentState
# # # #     )

# # # #     graph.add_node(
# # # #         "clarification_agent",
# # # #         clarification_agent
# # # #     )

# # # #     graph.add_node(
# # # #         "collect_answers",
# # # #         collect_answers
# # # #     )

# # # #     graph.add_node(
# # # #         "increment_clarification_batch",
# # # #         increment_clarification_batch
# # # #     )

# # # #     graph.add_node(
# # # #         "build_final_requirements",
# # # #         build_final_requirements
# # # #     )

# # # #     graph.add_node(
# # # #         "solution_a",
# # # #         solution_a
# # # #     )

# # # #     graph.add_node(
# # # #         "solution_b",
# # # #         solution_b
# # # #     )

# # # #     graph.add_node(
# # # #         "solution_c",
# # # #         solution_c
# # # #     )

# # # #     graph.add_node(
# # # #         "adversarial_b",
# # # #         adversarial_b
# # # #     )

# # # #     graph.add_node(
# # # #         "adversarial_c",
# # # #         adversarial_c
# # # #     )

# # # #     graph.add_node(
# # # #         "adversarial_a",
# # # #         adversarial_a
# # # #     )

# # # #     graph.add_node(
# # # #         "refine_a",
# # # #         refine_a
# # # #     )

# # # #     graph.add_node(
# # # #         "refine_b",
# # # #         refine_b
# # # #     )

# # # #     graph.add_node(
# # # #         "refine_c",
# # # #         refine_c
# # # #     )

# # # #     graph.add_node(
# # # #         "increment_refinement_round",
# # # #         increment_refinement_round
# # # #     )

# # # #     graph.add_node(
# # # #         "synthesizer",
# # # #         synthesizer
# # # #     )

# # # #     graph.add_edge(
# # # #         START,
# # # #         "clarification_agent"
# # # #     )

# # # #     graph.add_edge(
# # # #         "clarification_agent",
# # # #         "collect_answers"
# # # #     )

# # # #     graph.add_edge(
# # # #         "collect_answers",
# # # #         "increment_clarification_batch"
# # # #     )

# # # #     graph.add_conditional_edges(
# # # #         "increment_clarification_batch",

# # # #         clarification_decision,

# # # #         {
# # # #             "continue":
# # # #                 "clarification_agent",

# # # #             "finish":
# # # #                 "build_final_requirements"
# # # #         }
# # # #     )

# # # #     graph.add_edge(
# # # #         "build_final_requirements",
# # # #         "solution_a"
# # # #     )

# # # #     graph.add_edge(
# # # #         "build_final_requirements",
# # # #         "solution_b"
# # # #     )

# # # #     graph.add_edge(
# # # #         "build_final_requirements",
# # # #         "solution_c"
# # # #     )

# # # #     graph.add_edge(
# # # #         "solution_a",
# # # #         "adversarial_b"
# # # #     )

# # # #     graph.add_edge(
# # # #         "solution_b",
# # # #         "adversarial_c"
# # # #     )

# # # #     graph.add_edge(
# # # #         "solution_c",
# # # #         "adversarial_a"
# # # #     )

# # # #     graph.add_edge(
# # # #         "adversarial_b",
# # # #         "refine_a"
# # # #     )

# # # #     graph.add_edge(
# # # #         "adversarial_c",
# # # #         "refine_b"
# # # #     )

# # # #     graph.add_edge(
# # # #         "adversarial_a",
# # # #         "refine_c"
# # # #     )

# # # #     graph.add_edge(
# # # #         "refine_a",
# # # #         "increment_refinement_round"
# # # #     )

# # # #     graph.add_edge(
# # # #         "refine_b",
# # # #         "increment_refinement_round"
# # # #     )

# # # #     graph.add_edge(
# # # #         "refine_c",
# # # #         "increment_refinement_round"
# # # #     )

# # # #     graph.add_conditional_edges(
# # # #         "increment_refinement_round",

# # # #         refinement_router,

# # # #         {
# # # #             "adversarial_b":
# # # #                 "adversarial_b",

# # # #             "adversarial_c":
# # # #                 "adversarial_c",

# # # #             "adversarial_a":
# # # #                 "adversarial_a",

# # # #             "finish":
# # # #                 "synthesizer"
# # # #         }
# # # #     )

# # # #     graph.add_edge(
# # # #         "synthesizer",
# # # #         END
# # # #     )

# # # #     checkpointer = MemorySaver()

# # # #     return graph.compile(
# # # #         checkpointer=checkpointer
# # # #     )









# # # from langgraph.graph import StateGraph, START, END
# # # from langgraph.checkpoint.memory import MemorySaver
# # # from langgraph.types import interrupt

# # # from state import AgentState
# # # from models import (
# # #     clarification_llm,
# # #     llm_a,
# # #     llm_b,
# # #     llm_c,
# # #     synthesizer_llm
# # # )
# # # from prompts import (
# # #     CLARIFICATION_PROMPT,
# # #     CLARIFICATION_DECISION_PROMPT,
# # #     REQUIREMENT_SUMMARY_PROMPT,
# # #     SOLUTION_PROMPT,
# # #     ADVERSARIAL_PROMPT,
# # #     REFINEMENT_PROMPT,
# # #     SYNTHESIS_PROMPT
# # # )
# # # from services.citations import extract_citations


# # # def clarification_agent(state):
# # #     response = clarification_llm.invoke(
# # #         CLARIFICATION_PROMPT.format(
# # #             prompt=state["initial_prompt"],
# # #             history=state.get("clarification_history", [])
# # #         )
# # #     )

# # #     questions = []

# # #     for line in response.content.splitlines():
# # #         line = line.strip()

# # #         if not line:
# # #             continue

# # #         if line[0].isdigit() and "." in line:
# # #             line = line.split(".", 1)[1].strip()
# # #             questions.append(line)

# # #     return {
# # #         "questions": questions[:5]
# # #     }


# # # def collect_answers(state):
# # #     answers = interrupt({
# # #         "type": "clarification_batch",
# # #         "batch": state["clarification_batch"],
# # #         "questions": state["questions"]
# # #     })

# # #     history = state.get("clarification_history", [])
# # #     batch_data = []

# # #     for question, answer in zip(
# # #         state["questions"],
# # #         answers
# # #     ):
# # #         batch_data.append({
# # #             "question": question,
# # #             "answer": answer
# # #         })

# # #     history.append({
# # #         "batch": state["clarification_batch"],
# # #         "questions": state["questions"],
# # #         "answers": batch_data
# # #     })

# # #     return {
# # #         "current_batch_answers": answers,
# # #         "clarification_answers": batch_data,
# # #         "clarification_history": history
# # #     }


# # # def increment_clarification_batch(state):
# # #     return {
# # #         "clarification_batch":
# # #         state["clarification_batch"] + 1
# # #     }


# # # def clarification_decision(state):
# # #     if (
# # #         state["clarification_batch"]
# # #         > state["max_clarification_batches"]
# # #     ):
# # #         return "finish"

# # #     response = clarification_llm.invoke(
# # #         CLARIFICATION_DECISION_PROMPT.format(
# # #             prompt=state["initial_prompt"],
# # #             history=state.get(
# # #                 "clarification_history",
# # #                 []
# # #             )
# # #         )
# # #     )

# # #     decision = response.content.strip().upper()

# # #     if decision == "CONTINUE":
# # #         return "continue"

# # #     return "finish"


# # # def build_final_requirements(state):
# # #     response = clarification_llm.invoke(
# # #         REQUIREMENT_SUMMARY_PROMPT.format(
# # #             prompt=state["initial_prompt"],
# # #             history=state.get(
# # #                 "clarification_history",
# # #                 []
# # #             )
# # #         )
# # #     )

# # #     return {
# # #         "final_requirements": response.content
# # #     }


# # # def solution_a(state):
# # #     response = llm_a.invoke(
# # #         SOLUTION_PROMPT.format(
# # #             requirements=state["final_requirements"]
# # #         )
# # #     )

# # #     return {
# # #         "solution_a": response.content,
# # #         "citations_a": extract_citations(
# # #             response.content
# # #         )
# # #     }


# # # def solution_b(state):
# # #     response = llm_b.invoke(
# # #         SOLUTION_PROMPT.format(
# # #             requirements=state["final_requirements"]
# # #         )
# # #     )

# # #     return {
# # #         "solution_b": response.content,
# # #         "citations_b": extract_citations(
# # #             response.content
# # #         )
# # #     }


# # # def solution_c(state):
# # #     response = llm_c.invoke(
# # #         SOLUTION_PROMPT.format(
# # #             requirements=state["final_requirements"]
# # #         )
# # #     )

# # #     return {
# # #         "solution_c": response.content,
# # #         "citations_c": extract_citations(
# # #             response.content
# # #         )
# # #     }


# # # def adversarial_b(state):
# # #     response = llm_b.invoke(
# # #         ADVERSARIAL_PROMPT.format(
# # #             requirements=state["final_requirements"],
# # #             solution=state["solution_a"]
# # #         )
# # #     )

# # #     return {
# # #         "adversarial_feedback_a": response.content
# # #     }


# # # def adversarial_c(state):
# # #     response = llm_c.invoke(
# # #         ADVERSARIAL_PROMPT.format(
# # #             requirements=state["final_requirements"],
# # #             solution=state["solution_b"]
# # #         )
# # #     )

# # #     return {
# # #         "adversarial_feedback_b": response.content
# # #     }


# # # def adversarial_a(state):
# # #     response = llm_a.invoke(
# # #         ADVERSARIAL_PROMPT.format(
# # #             requirements=state["final_requirements"],
# # #             solution=state["solution_c"]
# # #         )
# # #     )

# # #     return {
# # #         "adversarial_feedback_c": response.content
# # #     }


# # # def refine_a(state):
# # #     response = llm_a.invoke(
# # #         REFINEMENT_PROMPT.format(
# # #             requirements=state["final_requirements"],
# # #             solution=state["solution_a"],
# # #             feedback=state["adversarial_feedback_a"]
# # #         )
# # #     )

# # #     return {
# # #         "solution_a": response.content,
# # #         "citations_a": extract_citations(
# # #             response.content
# # #         )
# # #     }


# # # def refine_b(state):
# # #     response = llm_b.invoke(
# # #         REFINEMENT_PROMPT.format(
# # #             requirements=state["final_requirements"],
# # #             solution=state["solution_b"],
# # #             feedback=state["adversarial_feedback_b"]
# # #         )
# # #     )

# # #     return {
# # #         "solution_b": response.content,
# # #         "citations_b": extract_citations(
# # #             response.content
# # #         )
# # #     }


# # # def refine_c(state):
# # #     response = llm_c.invoke(
# # #         REFINEMENT_PROMPT.format(
# # #             requirements=state["final_requirements"],
# # #             solution=state["solution_c"],
# # #             feedback=state["adversarial_feedback_c"]
# # #         )
# # #     )

# # #     return {
# # #         "solution_c": response.content,
# # #         "citations_c": extract_citations(
# # #             response.content
# # #         )
# # #     }


# # # def increment_refinement_round(state):
# # #     return {
# # #         "refinement_round":
# # #         state["refinement_round"] + 1
# # #     }


# # # def refinement_router(state):
# # #     if (
# # #         state["refinement_round"]
# # #         >= state["max_refinement_rounds"]
# # #     ):
# # #         return "finish"

# # #     return "continue"


# # # def synthesizer(state):
# # #     response = synthesizer_llm.invoke(
# # #         SYNTHESIS_PROMPT.format(
# # #             requirements=state["final_requirements"],
# # #             solution_a=state["solution_a"],
# # #             solution_b=state["solution_b"],
# # #             solution_c=state["solution_c"],
# # #             citations_a=state.get("citations_a", []),
# # #             citations_b=state.get("citations_b", []),
# # #             citations_c=state.get("citations_c", [])
# # #         )
# # #     )

# # #     return {
# # #         "final_answer": response.content,
# # #         "final_citations": extract_citations(
# # #             response.content
# # #         )
# # #     }


# # # def build_graph():

# # #     graph = StateGraph(AgentState)

# # #     graph.add_node(
# # #         "clarification_agent",
# # #         clarification_agent
# # #     )

# # #     graph.add_node(
# # #         "collect_answers",
# # #         collect_answers
# # #     )

# # #     graph.add_node(
# # #         "increment_clarification_batch",
# # #         increment_clarification_batch
# # #     )

# # #     graph.add_node(
# # #         "build_final_requirements",
# # #         build_final_requirements
# # #     )

# # #     graph.add_node(
# # #         "solution_a",
# # #         solution_a
# # #     )

# # #     graph.add_node(
# # #         "solution_b",
# # #         solution_b
# # #     )

# # #     graph.add_node(
# # #         "solution_c",
# # #         solution_c
# # #     )

# # #     graph.add_node(
# # #         "adversarial_b",
# # #         adversarial_b
# # #     )

# # #     graph.add_node(
# # #         "adversarial_c",
# # #         adversarial_c
# # #     )

# # #     graph.add_node(
# # #         "adversarial_a",
# # #         adversarial_a
# # #     )

# # #     graph.add_node(
# # #         "refine_a",
# # #         refine_a
# # #     )

# # #     graph.add_node(
# # #         "refine_b",
# # #         refine_b
# # #     )

# # #     graph.add_node(
# # #         "refine_c",
# # #         refine_c
# # #     )

# # #     graph.add_node(
# # #         "increment_refinement_round",
# # #         increment_refinement_round
# # #     )

# # #     graph.add_node(
# # #         "synthesizer",
# # #         synthesizer
# # #     )

# # #     graph.add_edge(
# # #         START,
# # #         "clarification_agent"
# # #     )

# # #     graph.add_edge(
# # #         "clarification_agent",
# # #         "collect_answers"
# # #     )

# # #     graph.add_edge(
# # #         "collect_answers",
# # #         "increment_clarification_batch"
# # #     )

# # #     graph.add_conditional_edges(
# # #         "increment_clarification_batch",
# # #         clarification_decision,
# # #         {
# # #             "continue": "clarification_agent",
# # #             "finish": "build_final_requirements"
# # #         }
# # #     )

# # #     graph.add_edge(
# # #         "build_final_requirements",
# # #         "solution_a"
# # #     )

# # #     graph.add_edge(
# # #         "solution_a",
# # #         "solution_b"
# # #     )

# # #     graph.add_edge(
# # #         "solution_b",
# # #         "solution_c"
# # #     )

# # #     graph.add_edge(
# # #         "solution_c",
# # #         "adversarial_b"
# # #     )

# # #     graph.add_edge(
# # #         "adversarial_b",
# # #         "adversarial_c"
# # #     )

# # #     graph.add_edge(
# # #         "adversarial_c",
# # #         "adversarial_a"
# # #     )

# # #     graph.add_edge(
# # #         "adversarial_a",
# # #         "refine_a"
# # #     )

# # #     graph.add_edge(
# # #         "refine_a",
# # #         "refine_b"
# # #     )

# # #     graph.add_edge(
# # #         "refine_b",
# # #         "refine_c"
# # #     )

# # #     graph.add_edge(
# # #         "refine_c",
# # #         "increment_refinement_round"
# # #     )

# # #     graph.add_conditional_edges(
# # #         "increment_refinement_round",
# # #         refinement_router,
# # #         {
# # #             "continue": "adversarial_b",
# # #             "finish": "synthesizer"
# # #         }
# # #     )

# # #     graph.add_edge(
# # #         "synthesizer",
# # #         END
# # #     )

# # #     checkpointer = MemorySaver()

# # #     return graph.compile(
# # #         checkpointer=checkpointer
# # #     )


# # # if __name__ == "__main__":

# # #     app = build_graph()

# # #     png = app.get_graph().draw_mermaid_png()

# # #     with open(
# # #         "output/workflow.png",
# # #         "wb"
# # #     ) as file:
# # #         file.write(png)

# # #     print("Workflow graph generated:")
# # #     print("output/workflow.png")



# # from langgraph.graph import StateGraph, START, END
# # from langgraph.types import interrupt
# # from langgraph.checkpoint.memory import MemorySaver

# # from state import AgentState
# # from models import (
# #     clarification_llm,
# #     llm_a,
# #     llm_b,
# #     llm_c,
# #     synthesizer_llm,
# # )
# # from prompts import (
# #     CLARIFICATION_PROMPT,
# #     CLARIFICATION_DECISION_PROMPT,
# #     REQUIREMENT_SUMMARY_PROMPT,
# #     SOLUTION_PROMPT,
# #     ADVERSARIAL_PROMPT,
# #     REFINEMENT_PROMPT,
# #     SYNTHESIS_PROMPT,
# # )
# # from services.citations import extract_citations


# # def log(message):
# #     print(f"\n[GRAPH] {message}", flush=True)


# # def clarification_agent(state):
# #     log("START → clarification_agent")
# #     log(f"Clarification batch: {state['clarification_batch']}")

# #     response = clarification_llm.invoke(
# #         CLARIFICATION_PROMPT.format(
# #             prompt=state["initial_prompt"],
# #             history=state.get("clarification_history", [])
# #         )
# #     )

# #     questions = []

# #     for line in response.content.splitlines():
# #         line = line.strip()

# #         if not line:
# #             continue

# #         if line[0].isdigit() and "." in line:
# #             line = line.split(".", 1)[1].strip()
# #             questions.append(line)

# #     questions = questions[:5]

# #     log(f"Generated {len(questions)} questions")
# #     log("NEXT → collect_answers")

# #     return {
# #         "questions": questions
# #     }


# # def collect_answers(state):
# #     log("START → collect_answers")
# #     log(f"Waiting for answers for batch {state['clarification_batch']}")

# #     answers = interrupt({
# #         "type": "clarification_batch",
# #         "batch": state["clarification_batch"],
# #         "questions": state["questions"]
# #     })

# #     log("Answers received")

# #     history = state.get("clarification_history", [])

# #     batch_data = []

# #     for question, answer in zip(state["questions"], answers):
# #         batch_data.append({
# #             "question": question,
# #             "answer": answer
# #         })

# #     history.append({
# #         "batch": state["clarification_batch"],
# #         "questions": state["questions"],
# #         "answers": batch_data
# #     })

# #     log("NEXT → increment_clarification_batch")

# #     return {
# #         "current_batch_answers": answers,
# #         "clarification_answers": batch_data,
# #         "clarification_history": history
# #     }


# # def increment_clarification_batch(state):
# #     new_batch = state["clarification_batch"] + 1

# #     log(
# #         f"START → increment_clarification_batch | "
# #         f"{state['clarification_batch']} → {new_batch}"
# #     )

# #     return {
# #         "clarification_batch": new_batch
# #     }


# # def clarification_decision(state):
# #     log("START → clarification_decision")

# #     if state["clarification_batch"] > state["max_clarification_batches"]:
# #         log("Maximum clarification batches reached")
# #         log("DECISION → FINISH")
# #         return "finish"

# #     log("Calling Groq for clarification decision")

# #     response = clarification_llm.invoke(
# #         CLARIFICATION_DECISION_PROMPT.format(
# #             prompt=state["initial_prompt"],
# #             history=state.get("clarification_history", [])
# #         )
# #     )

# #     decision = response.content.strip().upper()

# #     log(f"LLM decision: {decision}")

# #     if decision == "CONTINUE":
# #         log("DECISION → CONTINUE")
# #         log("NEXT → clarification_agent")
# #         return "continue"

# #     log("DECISION → FINISH")
# #     log("NEXT → build_final_requirements")

# #     return "finish"


# # def build_final_requirements(state):
# #     log("START → build_final_requirements")

# #     response = clarification_llm.invoke(
# #         REQUIREMENT_SUMMARY_PROMPT.format(
# #             prompt=state["initial_prompt"],
# #             history=state.get("clarification_history", [])
# #         )
# #     )

# #     log("Final requirements generated")
# #     log("NEXT → solution_a + solution_b + solution_c")

# #     return {
# #         "final_requirements": response.content
# #     }


# # def solution_a(state):
# #     log("START → solution_a")

# #     response = llm_a.invoke(
# #         SOLUTION_PROMPT.format(
# #             requirements=state["final_requirements"]
# #         )
# #     )

# #     log("solution_a completed")

# #     return {
# #         "solution_a": response.content,
# #         "citations_a": extract_citations(response.content)
# #     }


# # def solution_b(state):
# #     log("START → solution_b")

# #     response = llm_b.invoke(
# #         SOLUTION_PROMPT.format(
# #             requirements=state["final_requirements"]
# #         )
# #     )

# #     log("solution_b completed")

# #     return {
# #         "solution_b": response.content,
# #         "citations_b": extract_citations(response.content)
# #     }


# # def solution_c(state):
# #     log("START → solution_c")

# #     response = llm_c.invoke(
# #         SOLUTION_PROMPT.format(
# #             requirements=state["final_requirements"]
# #         )
# #     )

# #     log("solution_c completed")

# #     return {
# #         "solution_c": response.content,
# #         "citations_c": extract_citations(response.content)
# #     }


# # def adversarial_b(state):
# #     log("START → adversarial_b")
# #     log("Model B reviewing Solution A")

# #     response = llm_b.invoke(
# #         ADVERSARIAL_PROMPT.format(
# #             requirements=state["final_requirements"],
# #             solution=state["solution_a"]
# #         )
# #     )

# #     log("adversarial_b completed")

# #     return {
# #         "adversarial_feedback_a": response.content
# #     }


# # def adversarial_c(state):
# #     log("START → adversarial_c")
# #     log("Model C reviewing Solution B")

# #     response = llm_c.invoke(
# #         ADVERSARIAL_PROMPT.format(
# #             requirements=state["final_requirements"],
# #             solution=state["solution_b"]
# #         )
# #     )

# #     log("adversarial_c completed")

# #     return {
# #         "adversarial_feedback_b": response.content
# #     }


# # def adversarial_a(state):
# #     log("START → adversarial_a")
# #     log("Model A reviewing Solution C")

# #     response = llm_a.invoke(
# #         ADVERSARIAL_PROMPT.format(
# #             requirements=state["final_requirements"],
# #             solution=state["solution_c"]
# #         )
# #     )

# #     log("adversarial_a completed")

# #     return {
# #         "adversarial_feedback_c": response.content
# #     }


# # def refine_a(state):
# #     log("START → refine_a")

# #     response = llm_a.invoke(
# #         REFINEMENT_PROMPT.format(
# #             requirements=state["final_requirements"],
# #             solution=state["solution_a"],
# #             feedback=state["adversarial_feedback_a"]
# #         )
# #     )

# #     log("refine_a completed")

# #     return {
# #         "solution_a": response.content,
# #         "citations_a": extract_citations(response.content)
# #     }


# # def refine_b(state):
# #     log("START → refine_b")

# #     response = llm_b.invoke(
# #         REFINEMENT_PROMPT.format(
# #             requirements=state["final_requirements"],
# #             solution=state["solution_b"],
# #             feedback=state["adversarial_feedback_b"]
# #         )
# #     )

# #     log("refine_b completed")

# #     return {
# #         "solution_b": response.content,
# #         "citations_b": extract_citations(response.content)
# #     }


# # def refine_c(state):
# #     log("START → refine_c")

# #     response = llm_c.invoke(
# #         REFINEMENT_PROMPT.format(
# #             requirements=state["final_requirements"],
# #             solution=state["solution_c"],
# #             feedback=state["adversarial_feedback_c"]
# #         )
# #     )

# #     log("refine_c completed")

# #     return {
# #         "solution_c": response.content,
# #         "citations_c": extract_citations(response.content)
# #     }


# # def increment_refinement_round(state):
# #     new_round = state["refinement_round"] + 1

# #     log(
# #         f"START → increment_refinement_round | "
# #         f"{state['refinement_round']} → {new_round}"
# #     )

# #     return {
# #         "refinement_round": new_round
# #     }


# # def refinement_router(state):
# #     current_round = state["refinement_round"]
# #     max_rounds = state["max_refinement_rounds"]

# #     log(
# #         f"START → refinement_router | "
# #         f"round={current_round}/{max_rounds}"
# #     )

# #     if current_round >= max_rounds:
# #         log("REFINEMENT COMPLETE")
# #         log("NEXT → synthesizer")
# #         return "finish"

# #     log("NEXT REFINEMENT ROUND")
# #     log("Parallel adversarial branches:")
# #     log("  adversarial_b")
# #     log("  adversarial_c")
# #     log("  adversarial_a")

# #     return [
# #         "adversarial_b",
# #         "adversarial_c",
# #         "adversarial_a"
# #     ]


# # def synthesizer(state):
# #     log("START → synthesizer")

# #     response = synthesizer_llm.invoke(
# #         SYNTHESIS_PROMPT.format(
# #             requirements=state["final_requirements"],
# #             solution_a=state["solution_a"],
# #             solution_b=state["solution_b"],
# #             solution_c=state["solution_c"],
# #             citations_a=state.get("citations_a", []),
# #             citations_b=state.get("citations_b", []),
# #             citations_c=state.get("citations_c", [])
# #         )
# #     )

# #     log("FINAL SYNTHESIS COMPLETED")
# #     log("NEXT → END")

# #     return {
# #         "final_answer": response.content,
# #         "final_citations": extract_citations(response.content)
# #     }


# # def build_graph():

# #     log("Building LangGraph")

# #     graph = StateGraph(AgentState)

# #     graph.add_node("clarification_agent", clarification_agent)
# #     graph.add_node("collect_answers", collect_answers)
# #     graph.add_node(
# #         "increment_clarification_batch",
# #         increment_clarification_batch
# #     )

# #     graph.add_node(
# #         "build_final_requirements",
# #         build_final_requirements
# #     )

# #     graph.add_node("solution_a", solution_a)
# #     graph.add_node("solution_b", solution_b)
# #     graph.add_node("solution_c", solution_c)

# #     graph.add_node("adversarial_a", adversarial_a)
# #     graph.add_node("adversarial_b", adversarial_b)
# #     graph.add_node("adversarial_c", adversarial_c)

# #     graph.add_node("refine_a", refine_a)
# #     graph.add_node("refine_b", refine_b)
# #     graph.add_node("refine_c", refine_c)

# #     graph.add_node(
# #         "increment_refinement_round",
# #         increment_refinement_round
# #     )

# #     graph.add_node("synthesizer", synthesizer)

# #     graph.add_edge(
# #         START,
# #         "clarification_agent"
# #     )

# #     graph.add_edge(
# #         "clarification_agent",
# #         "collect_answers"
# #     )

# #     graph.add_edge(
# #         "collect_answers",
# #         "increment_clarification_batch"
# #     )

# #     graph.add_conditional_edges(
# #         "increment_clarification_batch",
# #         clarification_decision,
# #         {
# #             "continue": "clarification_agent",
# #             "finish": "build_final_requirements"
# #         }
# #     )

# #     # ------------------------------------------------
# #     # PARALLEL SOLUTION GENERATION
# #     # ------------------------------------------------

# #     graph.add_edge(
# #         "build_final_requirements",
# #         "solution_a"
# #     )

# #     graph.add_edge(
# #         "build_final_requirements",
# #         "solution_b"
# #     )

# #     graph.add_edge(
# #         "build_final_requirements",
# #         "solution_c"
# #     )

# #     # ------------------------------------------------
# #     # INITIAL ADVERSARIAL REVIEW
# #     # ------------------------------------------------

# #     graph.add_edge(
# #         "solution_a",
# #         "adversarial_b"
# #     )

# #     graph.add_edge(
# #         "solution_b",
# #         "adversarial_c"
# #     )

# #     graph.add_edge(
# #         "solution_c",
# #         "adversarial_a"
# #     )

# #     # ------------------------------------------------
# #     # REFINEMENT
# #     # ------------------------------------------------

# #     graph.add_edge(
# #         "adversarial_b",
# #         "refine_a"
# #     )

# #     graph.add_edge(
# #         "adversarial_c",
# #         "refine_b"
# #     )

# #     graph.add_edge(
# #         "adversarial_a",
# #         "refine_c"
# #     )

# #     # ------------------------------------------------
# #     # JOIN ALL THREE REFINEMENTS
# #     # ------------------------------------------------

# #     graph.add_edge(
# #         "refine_a",
# #         "increment_refinement_round"
# #     )

# #     graph.add_edge(
# #         "refine_b",
# #         "increment_refinement_round"
# #     )

# #     graph.add_edge(
# #         "refine_c",
# #         "increment_refinement_round"
# #     )

# #     # ------------------------------------------------
# #     # NEXT ROUND / SYNTHESIS
# #     # ------------------------------------------------

# #     graph.add_conditional_edges(
# #         "increment_refinement_round",
# #         refinement_router,
# #         {
# #             "adversarial_a": "adversarial_a",
# #             "adversarial_b": "adversarial_b",
# #             "adversarial_c": "adversarial_c",
# #             "finish": "synthesizer"
# #         }
# #     )

# #     graph.add_edge(
# #         "synthesizer",
# #         END
# #     )

# #     checkpointer = MemorySaver()

# #     compiled_graph = graph.compile(
# #         checkpointer=checkpointer
# #     )

# #     log("Graph compiled successfully")

# #     return compiled_graph


# # graph = build_graph()



# from langgraph.graph import StateGraph, START, END
# from langgraph.types import interrupt
# from langgraph.checkpoint.memory import MemorySaver

# from state import AgentState

# from models import (
#     clarification_llm,
#     llm_a,
#     llm_b,
#     llm_c,
#     synthesizer_llm,
# )

# from prompts import (
#     CLARIFICATION_PROMPT,
#     CLARIFICATION_DECISION_PROMPT,
#     REQUIREMENT_SUMMARY_PROMPT,
#     SOLUTION_PROMPT,
#     ADVERSARIAL_PROMPT,
#     REFINEMENT_PROMPT,
#     SYNTHESIS_PROMPT,
# )

# from services.citations import extract_citations


# def log(message):
#     print(f"\n[GRAPH] {message}", flush=True)


# # ============================================================
# # CLARIFICATION
# # ============================================================

# def clarification_agent(state):

#     log("========================================")
#     log("START: clarification_agent")
#     log(f"Batch: {state['clarification_batch']}")
#     log("Calling Groq...")
    
#     response = clarification_llm.invoke(
#         CLARIFICATION_PROMPT.format(
#             prompt=state["initial_prompt"],
#             history=state.get("clarification_history", [])
#         )
#     )

#     questions = []

#     for line in response.content.splitlines():

#         line = line.strip()

#         if not line:
#             continue

#         if line[0].isdigit() and "." in line:

#             line = line.split(".", 1)[1].strip()

#             questions.append(line)

#     questions = questions[:5]

#     log(f"Generated {len(questions)} questions")
#     log("END: clarification_agent")

#     return {
#         "questions": questions
#     }


# def collect_answers(state):

#     log("========================================")
#     log("START: collect_answers")
#     log(f"Waiting for Batch {state['clarification_batch']} answers")

#     answers = interrupt({
#         "type": "clarification_batch",
#         "batch": state["clarification_batch"],
#         "questions": state["questions"]
#     })

#     log("Answers received")

#     history = state.get(
#         "clarification_history",
#         []
#     )

#     batch_data = []

#     for question, answer in zip(
#         state["questions"],
#         answers
#     ):

#         batch_data.append({
#             "question": question,
#             "answer": answer
#         })

#     history.append({
#         "batch": state["clarification_batch"],
#         "questions": state["questions"],
#         "answers": batch_data
#     })

#     log("END: collect_answers")

#     return {
#         "current_batch_answers": answers,
#         "clarification_answers": batch_data,
#         "clarification_history": history
#     }


# def increment_clarification_batch(state):

#     new_batch = (
#         state["clarification_batch"] + 1
#     )

#     log("========================================")
#     log("START: increment_clarification_batch")
#     log(
#         f"{state['clarification_batch']} → {new_batch}"
#     )

#     return {
#         "clarification_batch": new_batch
#     }


# def clarification_decision(state):

#     log("========================================")
#     log("START: clarification_decision")

#     if (
#         state["clarification_batch"]
#         > state["max_clarification_batches"]
#     ):

#         log("Maximum clarification batches reached")
#         log("DECISION: FINISH")

#         return "finish"

#     log("Calling Groq for decision...")

#     response = clarification_llm.invoke(
#         CLARIFICATION_DECISION_PROMPT.format(
#             prompt=state["initial_prompt"],
#             history=state.get(
#                 "clarification_history",
#                 []
#             )
#         )
#     )

#     decision = response.content.strip().upper()

#     log(f"Groq decision: {decision}")

#     if decision == "CONTINUE":

#         log("DECISION: CONTINUE")

#         return "continue"

#     log("DECISION: FINISH")

#     return "finish"


# def build_final_requirements(state):

#     log("========================================")
#     log("START: build_final_requirements")
#     log("Calling Groq...")

#     response = clarification_llm.invoke(
#         REQUIREMENT_SUMMARY_PROMPT.format(
#             prompt=state["initial_prompt"],
#             history=state.get(
#                 "clarification_history",
#                 []
#             )
#         )
#     )

#     log("Final requirements generated")

#     return {
#         "final_requirements": response.content
#     }


# # ============================================================
# # SOLUTIONS
# # ============================================================

# def solution_a(state):

#     log("========================================")
#     log("START: solution_a")
#     log("Model A / Groq")

#     response = llm_a.invoke(
#         SOLUTION_PROMPT.format(
#             requirements=state["final_requirements"]
#         )
#     )

#     log("Solution A completed")

#     return {
#         "solution_a": response.content,
#         "citations_a": extract_citations(
#             response.content
#         )
#     }


# def solution_b(state):

#     log("========================================")
#     log("START: solution_b")
#     log("Model B / Groq")

#     response = llm_b.invoke(
#         SOLUTION_PROMPT.format(
#             requirements=state["final_requirements"]
#         )
#     )

#     log("Solution B completed")

#     return {
#         "solution_b": response.content,
#         "citations_b": extract_citations(
#             response.content
#         )
#     }


# def solution_c(state):

#     log("========================================")
#     log("START: solution_c")
#     log("Model C / Groq")

#     response = llm_c.invoke(
#         SOLUTION_PROMPT.format(
#             requirements=state["final_requirements"]
#         )
#     )

#     log("Solution C completed")

#     return {
#         "solution_c": response.content,
#         "citations_c": extract_citations(
#             response.content
#         )
#     }


# # ============================================================
# # ADVERSARIAL REVIEW
# # ============================================================

# def adversarial_b(state):

#     log("========================================")
#     log("START: adversarial_b")
#     log("Model B reviewing Solution A")

#     response = llm_b.invoke(
#         ADVERSARIAL_PROMPT.format(
#             requirements=state["final_requirements"],
#             solution=state["solution_a"]
#         )
#     )

#     log("B finished reviewing A")

#     return {
#         "adversarial_feedback_a": response.content
#     }


# def adversarial_c(state):

#     log("========================================")
#     log("START: adversarial_c")
#     log("Model C reviewing Solution B")

#     response = llm_c.invoke(
#         ADVERSARIAL_PROMPT.format(
#             requirements=state["final_requirements"],
#             solution=state["solution_b"]
#         )
#     )

#     log("C finished reviewing B")

#     return {
#         "adversarial_feedback_b": response.content
#     }


# def adversarial_a(state):

#     log("========================================")
#     log("START: adversarial_a")
#     log("Model A reviewing Solution C")

#     response = llm_a.invoke(
#         ADVERSARIAL_PROMPT.format(
#             requirements=state["final_requirements"],
#             solution=state["solution_c"]
#         )
#     )

#     log("A finished reviewing C")

#     return {
#         "adversarial_feedback_c": response.content
#     }


# # ============================================================
# # REFINEMENT
# # ============================================================

# def refine_a(state):

#     log("========================================")
#     log("START: refine_a")

#     response = llm_a.invoke(
#         REFINEMENT_PROMPT.format(
#             requirements=state["final_requirements"],
#             solution=state["solution_a"],
#             feedback=state["adversarial_feedback_a"]
#         )
#     )

#     log("Solution A refined")

#     return {
#         "solution_a": response.content,
#         "citations_a": extract_citations(
#             response.content
#         )
#     }


# def refine_b(state):

#     log("========================================")
#     log("START: refine_b")

#     response = llm_b.invoke(
#         REFINEMENT_PROMPT.format(
#             requirements=state["final_requirements"],
#             solution=state["solution_b"],
#             feedback=state["adversarial_feedback_b"]
#         )
#     )

#     log("Solution B refined")

#     return {
#         "solution_b": response.content,
#         "citations_b": extract_citations(
#             response.content
#         )
#     }


# def refine_c(state):

#     log("========================================")
#     log("START: refine_c")

#     response = llm_c.invoke(
#         REFINEMENT_PROMPT.format(
#             requirements=state["final_requirements"],
#             solution=state["solution_c"],
#             feedback=state["adversarial_feedback_c"]
#         )
#     )

#     log("Solution C refined")

#     return {
#         "solution_c": response.content,
#         "citations_c": extract_citations(
#             response.content
#         )
#     }


# # ============================================================
# # REFINEMENT ROUND
# # ============================================================

# def increment_refinement_round(state):

#     new_round = (
#         state["refinement_round"] + 1
#     )

#     log("========================================")
#     log("REFINEMENT ROUND COMPLETE")
#     log(
#         f"Round {new_round} / "
#         f"{state['max_refinement_rounds']}"
#     )

#     return {
#         "refinement_round": new_round
#     }


# def refinement_router(state):

#     current_round = (
#         state["refinement_round"]
#     )

#     maximum = (
#         state["max_refinement_rounds"]
#     )

#     log("========================================")
#     log("START: refinement_router")

#     if current_round >= maximum:

#         log("Maximum refinement rounds reached")
#         log("NEXT: synthesizer")

#         return "finish"

#     log(
#         f"Starting refinement round "
#         f"{current_round + 1}"
#     )

#     return "continue"


# # ============================================================
# # SYNTHESIS
# # ============================================================

# def synthesizer(state):

#     log("========================================")
#     log("START: synthesizer")
#     log("Calling Groq...")

#     response = synthesizer_llm.invoke(
#         SYNTHESIS_PROMPT.format(
#             requirements=state["final_requirements"],

#             solution_a=state["solution_a"],
#             solution_b=state["solution_b"],
#             solution_c=state["solution_c"],

#             citations_a=state.get(
#                 "citations_a",
#                 []
#             ),

#             citations_b=state.get(
#                 "citations_b",
#                 []
#             ),

#             citations_c=state.get(
#                 "citations_c",
#                 []
#             )
#         )
#     )

#     log("FINAL ANSWER GENERATED")

#     return {
#         "final_answer": response.content,
#         "final_citations": extract_citations(
#             response.content
#         )
#     }


# # ============================================================
# # GRAPH
# # ============================================================

# def build_graph():

#     log("========================================")
#     log("BUILDING SERIAL LANGGRAPH")

#     graph = StateGraph(AgentState)

#     # Clarification
#     graph.add_node(
#         "clarification_agent",
#         clarification_agent
#     )

#     graph.add_node(
#         "collect_answers",
#         collect_answers
#     )

#     graph.add_node(
#         "increment_clarification_batch",
#         increment_clarification_batch
#     )

#     graph.add_node(
#         "build_final_requirements",
#         build_final_requirements
#     )

#     # Solutions
#     graph.add_node(
#         "solution_a",
#         solution_a
#     )

#     graph.add_node(
#         "solution_b",
#         solution_b
#     )

#     graph.add_node(
#         "solution_c",
#         solution_c
#     )

#     # Reviews
#     graph.add_node(
#         "adversarial_b",
#         adversarial_b
#     )

#     graph.add_node(
#         "adversarial_c",
#         adversarial_c
#     )

#     graph.add_node(
#         "adversarial_a",
#         adversarial_a
#     )

#     # Refinements
#     graph.add_node(
#         "refine_a",
#         refine_a
#     )

#     graph.add_node(
#         "refine_b",
#         refine_b
#     )

#     graph.add_node(
#         "refine_c",
#         refine_c
#     )

#     graph.add_node(
#         "increment_refinement_round",
#         increment_refinement_round
#     )

#     # Synthesis
#     graph.add_node(
#         "synthesizer",
#         synthesizer
#     )

#     # ========================================================
#     # CLARIFICATION
#     # ========================================================

#     graph.add_edge(
#         START,
#         "clarification_agent"
#     )

#     graph.add_edge(
#         "clarification_agent",
#         "collect_answers"
#     )

#     graph.add_edge(
#         "collect_answers",
#         "increment_clarification_batch"
#     )

#     graph.add_conditional_edges(
#         "increment_clarification_batch",
#         clarification_decision,
#         {
#             "continue":
#                 "clarification_agent",

#             "finish":
#                 "build_final_requirements"
#         }
#     )

#     # ========================================================
#     # SERIAL SOLUTION GENERATION
#     # ========================================================

#     graph.add_edge(
#         "build_final_requirements",
#         "solution_a"
#     )

#     graph.add_edge(
#         "solution_a",
#         "solution_b"
#     )

#     graph.add_edge(
#         "solution_b",
#         "solution_c"
#     )

#     # ========================================================
#     # SERIAL CROSS ADVERSARIAL REVIEW
#     # ========================================================

#     graph.add_edge(
#         "solution_c",
#         "adversarial_b"
#     )

#     graph.add_edge(
#         "adversarial_b",
#         "adversarial_c"
#     )

#     graph.add_edge(
#         "adversarial_c",
#         "adversarial_a"
#     )

#     # ========================================================
#     # SERIAL REFINEMENT
#     # ========================================================

#     graph.add_edge(
#         "adversarial_a",
#         "refine_a"
#     )

#     graph.add_edge(
#         "refine_a",
#         "refine_b"
#     )

#     graph.add_edge(
#         "refine_b",
#         "refine_c"
#     )

#     graph.add_edge(
#         "refine_c",
#         "increment_refinement_round"
#     )

#     # ========================================================
#     # NEXT ROUND OR SYNTHESIS
#     # ========================================================

#     graph.add_conditional_edges(
#         "increment_refinement_round",
#         refinement_router,
#         {
#             "continue":
#                 "adversarial_b",

#             "finish":
#                 "synthesizer"
#         }
#     )

#     graph.add_edge(
#         "synthesizer",
#         END
#     )

#     checkpointer = MemorySaver()

#     compiled_graph = graph.compile(
#         checkpointer=checkpointer
#     )

#     log("SERIAL GRAPH COMPILED")

#     return compiled_graph


# graph = build_graph()



from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt
from langgraph.checkpoint.memory import MemorySaver

from state import AgentState

from models import (
    clarification_llm,
    llm_a,
    llm_b,
    llm_c,
    synthesizer_llm,
)

from prompts import (
    CLARIFICATION_PROMPT,
    CLARIFICATION_DECISION_PROMPT,
    REQUIREMENT_SUMMARY_PROMPT,
    SOLUTION_PROMPT,
    ADVERSARIAL_PROMPT,
    REFINEMENT_PROMPT,
    SYNTHESIS_PROMPT,
)

from services.citations import extract_citations


def log(message):
    print(f"[GRAPH] {message}", flush=True)


# ============================================================
# 1. CLARIFICATION
# ============================================================

def clarification_agent(state):

    log("========================================")
    log("START: clarification_agent")
    log(
        f"Batch "
        f"{state['clarification_batch']}/"
        f"{state['max_clarification_batches']}"
    )

    log("Calling Groq...")

    response = clarification_llm.invoke(
        CLARIFICATION_PROMPT.format(
            prompt=state["initial_prompt"],
            history=state.get(
                "clarification_history",
                []
            )
        )
    )

    questions = []

    for line in response.content.splitlines():

        line = line.strip()

        if not line:
            continue

        if line[0].isdigit() and "." in line:

            line = line.split(".", 1)[1].strip()

            questions.append(line)

    questions = questions[:5]

    log(
        f"Generated {len(questions)} questions"
    )

    log("END: clarification_agent")

    return {
        "questions": questions
    }


def collect_answers(state):

    log("========================================")
    log("START: collect_answers")
    log(
        f"Waiting for answers for "
        f"Batch {state['clarification_batch']}"
    )

    answers = interrupt({
        "type": "clarification_batch",
        "batch": state["clarification_batch"],
        "questions": state["questions"]
    })

    log("RESUMED collect_answers")
    log("Answers received")

    history = state.get(
        "clarification_history",
        []
    )

    batch_data = []

    for question, answer in zip(
        state["questions"],
        answers
    ):

        batch_data.append({
            "question": question,
            "answer": answer
        })

    history.append({
        "batch": state["clarification_batch"],
        "questions": state["questions"],
        "answers": batch_data
    })

    log("END: collect_answers")

    return {
        "current_batch_answers": answers,
        "clarification_answers": batch_data,
        "clarification_history": history
    }


def increment_clarification_batch(state):

    new_batch = (
        state["clarification_batch"] + 1
    )

    log("========================================")
    log(
        f"Clarification batch: "
        f"{state['clarification_batch']} "
        f"-> {new_batch}"
    )

    return {
        "clarification_batch": new_batch
    }


def clarification_decision(state):

    log("========================================")
    log("START: clarification_decision")

    if (
        state["clarification_batch"]
        > state["max_clarification_batches"]
    ):

        log(
            "Maximum clarification batches reached"
        )

        return "finish"

    log("Calling Groq for decision...")

    response = clarification_llm.invoke(
        CLARIFICATION_DECISION_PROMPT.format(
            prompt=state["initial_prompt"],
            history=state.get(
                "clarification_history",
                []
            )
        )
    )

    decision = (
        response.content
        .strip()
        .upper()
    )

    log(f"Decision received: {decision}")

    if "CONTINUE" in decision:

        log(
            "NEXT: clarification_agent"
        )

        return "continue"

    log(
        "NEXT: build_final_requirements"
    )

    return "finish"


# ============================================================
# 2. FINAL REQUIREMENTS
# ============================================================

def build_final_requirements(state):

    log("========================================")
    log("START: build_final_requirements")
    log("Calling Groq...")

    response = clarification_llm.invoke(
        REQUIREMENT_SUMMARY_PROMPT.format(
            prompt=state["initial_prompt"],
            history=state.get(
                "clarification_history",
                []
            )
        )
    )

    log("Final requirements generated")

    log(
        "NEXT: solution_a"
    )

    return {
        "final_requirements": response.content
    }


# ============================================================
# 3. SOLUTION A
# ============================================================

def solution_a(state):

    log("========================================")
    log("START: solution_a")
    log("Calling Groq...")

    response = llm_a.invoke(
        SOLUTION_PROMPT.format(
            requirements=state["final_requirements"]
        )
    )

    log("Solution A completed")
    log("NEXT: solution_b")

    return {
        "solution_a": response.content,
        "citations_a": extract_citations(
            response.content
        )
    }


# ============================================================
# 4. SOLUTION B
# ============================================================

def solution_b(state):

    log("========================================")
    log("START: solution_b")
    log("Calling Groq...")

    response = llm_b.invoke(
        SOLUTION_PROMPT.format(
            requirements=state["final_requirements"]
        )
    )

    log("Solution B completed")
    log("NEXT: solution_c")

    return {
        "solution_b": response.content,
        "citations_b": extract_citations(
            response.content
        )
    }


# ============================================================
# 5. SOLUTION C
# ============================================================

def solution_c(state):

    log("========================================")
    log("START: solution_c")
    log("Calling Groq...")

    response = llm_c.invoke(
        SOLUTION_PROMPT.format(
            requirements=state["final_requirements"]
        )
    )

    log("Solution C completed")
    log("NEXT: adversarial_b")

    return {
        "solution_c": response.content,
        "citations_c": extract_citations(
            response.content
        )
    }


# ============================================================
# 6. B REVIEWS A
# ============================================================

def adversarial_b(state):

    log("========================================")
    log("START: adversarial_b")
    log("Model B reviewing Solution A")
    log("Calling Groq...")

    response = llm_b.invoke(
        ADVERSARIAL_PROMPT.format(
            requirements=state["final_requirements"],
            solution=state["solution_a"]
        )
    )

    log("B finished reviewing A")
    log("NEXT: adversarial_c")

    return {
        "adversarial_feedback_a":
            response.content
    }


# ============================================================
# 7. C REVIEWS B
# ============================================================

def adversarial_c(state):

    log("========================================")
    log("START: adversarial_c")
    log("Model C reviewing Solution B")
    log("Calling Groq...")

    response = llm_c.invoke(
        ADVERSARIAL_PROMPT.format(
            requirements=state["final_requirements"],
            solution=state["solution_b"]
        )
    )

    log("C finished reviewing B")
    log("NEXT: adversarial_a")

    return {
        "adversarial_feedback_b":
            response.content
    }


# ============================================================
# 8. A REVIEWS C
# ============================================================

def adversarial_a(state):

    log("========================================")
    log("START: adversarial_a")
    log("Model A reviewing Solution C")
    log("Calling Groq...")

    response = llm_a.invoke(
        ADVERSARIAL_PROMPT.format(
            requirements=state["final_requirements"],
            solution=state["solution_c"]
        )
    )

    log("A finished reviewing C")
    log("NEXT: refine_a")

    return {
        "adversarial_feedback_c":
            response.content
    }


# ============================================================
# 9. REFINE A
# ============================================================

def refine_a(state):

    log("========================================")
    log("START: refine_a")
    log("Calling Groq...")

    response = llm_a.invoke(
        REFINEMENT_PROMPT.format(
            requirements=state["final_requirements"],
            solution=state["solution_a"],
            feedback=state["adversarial_feedback_a"]
        )
    )

    log("Solution A refined")
    log("NEXT: refine_b")

    return {
        "solution_a": response.content,
        "citations_a": extract_citations(
            response.content
        )
    }


# ============================================================
# 10. REFINE B
# ============================================================

def refine_b(state):

    log("========================================")
    log("START: refine_b")
    log("Calling Groq...")

    response = llm_b.invoke(
        REFINEMENT_PROMPT.format(
            requirements=state["final_requirements"],
            solution=state["solution_b"],
            feedback=state["adversarial_feedback_b"]
        )
    )

    log("Solution B refined")
    log("NEXT: refine_c")

    return {
        "solution_b": response.content,
        "citations_b": extract_citations(
            response.content
        )
    }


# ============================================================
# 11. REFINE C
# ============================================================

def refine_c(state):

    log("========================================")
    log("START: refine_c")
    log("Calling Groq...")

    response = llm_c.invoke(
        REFINEMENT_PROMPT.format(
            requirements=state["final_requirements"],
            solution=state["solution_c"],
            feedback=state["adversarial_feedback_c"]
        )
    )

    log("Solution C refined")
    log("NEXT: increment_refinement_round")

    return {
        "solution_c": response.content,
        "citations_c": extract_citations(
            response.content
        )
    }


# ============================================================
# 12. INCREMENT REFINEMENT ROUND
# ============================================================

def increment_refinement_round(state):

    new_round = (
        state["refinement_round"] + 1
    )

    log("========================================")
    log(
        f"REFINEMENT ROUND "
        f"{new_round}/"
        f"{state['max_refinement_rounds']}"
    )

    return {
        "refinement_round": new_round
    }


# ============================================================
# 13. REFINEMENT ROUTER
# ============================================================

def refinement_router(state):

    current = state["refinement_round"]

    maximum = state[
        "max_refinement_rounds"
    ]

    log("========================================")
    log(
        f"REFINEMENT ROUTER: "
        f"{current}/{maximum}"
    )

    if current >= maximum:

        log(
            "Maximum refinement rounds reached"
        )

        log(
            "NEXT: synthesizer"
        )

        return "finish"

    log(
        "Starting another adversarial cycle"
    )

    log(
        "NEXT: adversarial_b"
    )

    return "continue"


# ============================================================
# 14. SYNTHESIZER
# ============================================================

def synthesizer(state):

    log("========================================")
    log("START: synthesizer")
    log("Calling Groq...")

    response = synthesizer_llm.invoke(
        SYNTHESIS_PROMPT.format(
            requirements=
                state["final_requirements"],

            solution_a=
                state["solution_a"],

            solution_b=
                state["solution_b"],

            solution_c=
                state["solution_c"],

            citations_a=
                state.get(
                    "citations_a",
                    []
                ),

            citations_b=
                state.get(
                    "citations_b",
                    []
                ),

            citations_c=
                state.get(
                    "citations_c",
                    []
                )
        )
    )

    log("FINAL ANSWER GENERATED")
    log("WORKFLOW COMPLETE")

    return {
        "final_answer":
            response.content,

        "final_citations":
            extract_citations(
                response.content
            )
    }


# ============================================================
# GRAPH
# ============================================================

def build_graph():

    log("========================================")
    log("BUILDING SERIAL GRAPH")

    workflow = StateGraph(
        AgentState
    )

    # Clarification
    workflow.add_node(
        "clarification_agent",
        clarification_agent
    )

    workflow.add_node(
        "collect_answers",
        collect_answers
    )

    workflow.add_node(
        "increment_clarification_batch",
        increment_clarification_batch
    )

    workflow.add_node(
        "build_final_requirements",
        build_final_requirements
    )

    # Solutions
    workflow.add_node(
        "solution_a",
        solution_a
    )

    workflow.add_node(
        "solution_b",
        solution_b
    )

    workflow.add_node(
        "solution_c",
        solution_c
    )

    # Reviews
    workflow.add_node(
        "adversarial_b",
        adversarial_b
    )

    workflow.add_node(
        "adversarial_c",
        adversarial_c
    )

    workflow.add_node(
        "adversarial_a",
        adversarial_a
    )

    # Refinement
    workflow.add_node(
        "refine_a",
        refine_a
    )

    workflow.add_node(
        "refine_b",
        refine_b
    )

    workflow.add_node(
        "refine_c",
        refine_c
    )

    workflow.add_node(
        "increment_refinement_round",
        increment_refinement_round
    )

    # Synthesis
    workflow.add_node(
        "synthesizer",
        synthesizer
    )

    # ========================================================
    # CLARIFICATION
    # ========================================================

    workflow.add_edge(
        START,
        "clarification_agent"
    )

    workflow.add_edge(
        "clarification_agent",
        "collect_answers"
    )

    workflow.add_edge(
        "collect_answers",
        "increment_clarification_batch"
    )

    workflow.add_conditional_edges(
        "increment_clarification_batch",
        clarification_decision,
        {
            "continue":
                "clarification_agent",

            "finish":
                "build_final_requirements"
        }
    )

    # ========================================================
    # IMPORTANT:
    # FULLY SERIAL SOLUTION FLOW
    # ========================================================

    workflow.add_edge(
        "build_final_requirements",
        "solution_a"
    )

    workflow.add_edge(
        "solution_a",
        "solution_b"
    )

    workflow.add_edge(
        "solution_b",
        "solution_c"
    )

    # ========================================================
    # CROSS ADVERSARIAL REVIEW
    # ========================================================

    workflow.add_edge(
        "solution_c",
        "adversarial_b"
    )

    workflow.add_edge(
        "adversarial_b",
        "adversarial_c"
    )

    workflow.add_edge(
        "adversarial_c",
        "adversarial_a"
    )

    # ========================================================
    # REFINEMENT
    # ========================================================

    workflow.add_edge(
        "adversarial_a",
        "refine_a"
    )

    workflow.add_edge(
        "refine_a",
        "refine_b"
    )

    workflow.add_edge(
        "refine_b",
        "refine_c"
    )

    workflow.add_edge(
        "refine_c",
        "increment_refinement_round"
    )

    # ========================================================
    # REPEAT OR SYNTHESIZE
    # ========================================================

    workflow.add_conditional_edges(
        "increment_refinement_round",
        refinement_router,
        {
            "continue":
                "adversarial_b",

            "finish":
                "synthesizer"
        }
    )

    workflow.add_edge(
        "synthesizer",
        END
    )

    checkpointer = MemorySaver()

    compiled = workflow.compile(
        checkpointer=checkpointer
    )

    log("GRAPH COMPILED SUCCESSFULLY")

    return compiled


graph = build_graph()