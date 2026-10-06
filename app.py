# # # import uuid

# # # import streamlit as st

# # # from langgraph.types import Command

# # # from graph import build_graph


# # # st.set_page_config(
# # #     page_title="Multi-Agent AI Solver",
# # #     page_icon="🤖",
# # #     layout="wide"
# # # )


# # # if "graph" not in st.session_state:

# # #     st.session_state.graph = build_graph()


# # # if "thread_id" not in st.session_state:

# # #     st.session_state.thread_id = str(
# # #         uuid.uuid4()
# # #     )


# # # if "started" not in st.session_state:

# # #     st.session_state.started = False


# # # if "result" not in st.session_state:

# # #     st.session_state.result = None


# # # if "interrupt_data" not in st.session_state:

# # #     st.session_state.interrupt_data = None


# # # def get_config():

# # #     return {
# # #         "configurable": {
# # #             "thread_id":
# # #                 st.session_state.thread_id
# # #         }
# # #     }


# # # def get_interrupt_data():

# # #     snapshot = (
# # #         st.session_state.graph.get_state(
# # #             get_config()
# # #         )
# # #     )

# # #     if not snapshot.interrupts:

# # #         return None

# # #     return snapshot.interrupts[0].value


# # # st.title(
# # #     "🤖 Multi-Agent AI Solver"
# # # )

# # # st.caption(
# # #     "Clarification → Independent Solutions → "
# # #     "Cross-Adversarial Refinement → Synthesis"
# # # )


# # # # ------------------------------------------------
# # # # SIDEBAR
# # # # ------------------------------------------------

# # # st.sidebar.title(
# # #     "Workflow"
# # # )

# # # st.sidebar.markdown(
# # #     """
# # # ### 1. Clarification

# # # **Groq**

# # # `openai/gpt-oss-120b`

# # # 5 questions per batch

# # # Maximum 10 batches

# # # ---

# # # ### 2. Solution Generation

# # # **A:** DeepSeek-R1

# # # **B:** Qwen

# # # **C:** GPT-OSS

# # # ---

# # # ### 3. Cross-Adversarial Review

# # # `A → B`

# # # `B → C`

# # # `C → A`

# # # ---

# # # ### 4. Refinement

# # # Maximum **3 rounds**

# # # ---

# # # ### 5. Synthesis

# # # Independent Hugging Face model
# # # """
# # # )


# # # st.sidebar.divider()

# # # st.sidebar.write(
# # #     f"Session: `{st.session_state.thread_id}`"
# # # )


# # # # ------------------------------------------------
# # # # INITIAL PROMPT
# # # # ------------------------------------------------

# # # if not st.session_state.started:

# # #     st.header(
# # #         "1. Enter Your Requirement"
# # #     )

# # #     prompt = st.text_area(
# # #         "Initial prompt",
# # #         height=200,
# # #         placeholder=(
# # #             "Describe the problem you want "
# # #             "the multi-agent system to solve..."
# # #         )
# # #     )

# # #     if st.button(
# # #         "Start Analysis",
# # #         type="primary",
# # #         use_container_width=True
# # #     ):

# # #         if not prompt.strip():

# # #             st.error(
# # #                 "Please enter a requirement."
# # #             )

# # #         else:

# # #             initial_state = {

# # #                 "initial_prompt":
# # #                     prompt,

# # #                 "clarification_batch":
# # #                     1,

# # #                 "max_clarification_batches":
# # #                     10,

# # #                 "questions":
# # #                     [],

# # #                 "current_batch_answers":
# # #                     [],

# # #                 "clarification_answers":
# # #                     [],

# # #                 "clarification_history":
# # #                     [],

# # #                 "final_requirements":
# # #                     "",

# # #                 "solution_a":
# # #                     "",

# # #                 "solution_b":
# # #                     "",

# # #                 "solution_c":
# # #                     "",

# # #                 "citations_a":
# # #                     [],

# # #                 "citations_b":
# # #                     [],

# # #                 "citations_c":
# # #                     [],

# # #                 "adversarial_feedback_a":
# # #                     "",

# # #                 "adversarial_feedback_b":
# # #                     "",

# # #                 "adversarial_feedback_c":
# # #                     "",

# # #                 "refinement_round":
# # #                     0,

# # #                 "max_refinement_rounds":
# # #                     3,

# # #                 "final_answer":
# # #                     "",

# # #                 "final_citations":
# # #                     []
# # #             }

# # #             with st.spinner(
# # #                 "Generating clarification questions..."
# # #             ):

# # #                 result = (
# # #                     st.session_state.graph.invoke(
# # #                         initial_state,
# # #                         config=get_config()
# # #                     )
# # #                 )

# # #             st.session_state.started = True

# # #             st.session_state.result = result

# # #             st.session_state.interrupt_data = (
# # #                 get_interrupt_data()
# # #             )

# # #             st.rerun()


# # # # ------------------------------------------------
# # # # CLARIFICATION BATCH
# # # # ------------------------------------------------

# # # if st.session_state.started:

# # #     interrupt_data = (
# # #         get_interrupt_data()
# # #     )

# # #     if interrupt_data:

# # #         st.divider()

# # #         batch_number = (
# # #             interrupt_data["batch"]
# # #         )

# # #         questions = (
# # #             interrupt_data["questions"]
# # #         )

# # #         st.header(
# # #             f"2. Clarification Batch "
# # #             f"{batch_number} / 10"
# # #         )

# # #         st.info(
# # #             "Answer all five questions below. "
# # #             "Your answers will be mapped to their "
# # #             "corresponding questions."
# # #         )

# # #         answers = []

# # #         for index, question in enumerate(
# # #             questions
# # #         ):

# # #             st.markdown(
# # #                 f"### Question {index + 1}"
# # #             )

# # #             st.write(
# # #                 question
# # #             )

# # #             answer = st.text_area(
# # #                 f"Answer {index + 1}",

# # #                 key=(
# # #                     f"batch_{batch_number}"
# # #                     f"_answer_{index}"
# # #                 ),

# # #                 height=100,

# # #                 placeholder=(
# # #                     "Enter your answer..."
# # #                 )
# # #             )

# # #             answers.append(answer)

# # #             st.divider()


# # #         if st.button(
# # #             f"Submit Batch {batch_number}",

# # #             type="primary",

# # #             use_container_width=True
# # #         ):

# # #             empty_answers = [
# # #                 answer
# # #                 for answer in answers
# # #                 if not answer.strip()
# # #             ]

# # #             if empty_answers:

# # #                 st.warning(
# # #                     "Please answer all five "
# # #                     "questions before submitting."
# # #                 )

# # #             else:

# # #                 with st.spinner(
# # #                     "Processing your answers..."
# # #                 ):

# # #                     result = (
# # #                         st.session_state.graph.invoke(

# # #                             Command(
# # #                                 resume=answers
# # #                             ),

# # #                             config=get_config()
# # #                         )
# # #                     )

# # #                 st.session_state.result = result

# # #                 st.rerun()


# # #     else:

# # #         result = (
# # #             st.session_state.result
# # #         )

# # #         if result:

# # #             st.divider()

# # #             st.header(
# # #                 "3. Processing Complete"
# # #             )

# # #             st.success(
# # #                 "Clarification phase completed."
# # #             )

# # #             requirements = result.get(
# # #                 "final_requirements"
# # #             )

# # #             if requirements:

# # #                 with st.expander(
# # #                     "View Final Requirements"
# # #                 ):

# # #                     st.markdown(
# # #                         requirements
# # #                     )

# # #             st.divider()

# # #             st.header(
# # #                 "4. Multi-Agent Processing"
# # #             )

# # #             st.info(
# # #                 "The three solution models are "
# # #                 "now generating and cross-reviewing "
# # #                 "their solutions."
# # #             )

# # #             col1, col2, col3 = st.columns(3)

# # #             with col1:

# # #                 st.subheader(
# # #                     "Solution A"
# # #                 )

# # #                 st.write(
# # #                     "DeepSeek-R1"
# # #                 )

# # #                 if result.get(
# # #                     "solution_a"
# # #                 ):

# # #                     st.success(
# # #                         "Completed"
# # #                     )

# # #             with col2:

# # #                 st.subheader(
# # #                     "Solution B"
# # #                 )

# # #                 st.write(
# # #                     "Qwen"
# # #                 )

# # #                 if result.get(
# # #                     "solution_b"
# # #                 ):

# # #                     st.success(
# # #                         "Completed"
# # #                     )

# # #             with col3:

# # #                 st.subheader(
# # #                     "Solution C"
# # #                 )

# # #                 st.write(
# # #                     "GPT-OSS"
# # #                 )

# # #                 if result.get(
# # #                     "solution_c"
# # #                 ):

# # #                     st.success(
# # #                         "Completed"
# # #                     )


# # #             st.divider()

# # #             st.header(
# # #                 "5. Cross-Adversarial Review"
# # #             )

# # #             st.write(
# # #                 """
# # #                 **A → B → Refine A**

# # #                 **B → C → Refine B**

# # #                 **C → A → Refine C**
# # #                 """
# # #             )

# # #             round_number = result.get(
# # #                 "refinement_round",
# # #                 0
# # #             )

# # #             st.metric(
# # #                 "Refinement rounds completed",
# # #                 f"{round_number} / 3"
# # #             )


# # #             if result.get(
# # #                 "final_answer"
# # #             ):

# # #                 st.divider()

# # #                 st.header(
# # #                     "6. Final Synthesized Answer"
# # #                 )

# # #                 st.markdown(
# # #                     result["final_answer"]
# # #                 )


# # #                 citations = result.get(
# # #                     "final_citations",
# # #                     []
# # #                 )

# # #                 if citations:

# # #                     st.subheader(
# # #                         "Citations"
# # #                     )

# # #                     for citation in citations:

# # #                         st.markdown(
# # #                             f"- [{citation}]"
# # #                             f"({citation})"
# # #                         )


# # import streamlit as st
# # from langgraph.types import Command

# # from graph import graph


# # st.set_page_config(
# #     page_title="Multi-Agent AI Solver",
# #     page_icon="🤖",
# #     layout="wide"
# # )


# # if "thread_id" not in st.session_state:
# #     import uuid
# #     st.session_state.thread_id = str(uuid.uuid4())

# # if "started" not in st.session_state:
# #     st.session_state.started = False

# # if "processing" not in st.session_state:
# #     st.session_state.processing = False

# # if "progress" not in st.session_state:
# #     st.session_state.progress = []

# # if "initial_prompt" not in st.session_state:
# #     st.session_state.initial_prompt = ""


# # def get_config():
# #     return {
# #         "configurable": {
# #             "thread_id": st.session_state.thread_id
# #         }
# #     }


# # def node_name(name):
# #     names = {
# #         "clarification_agent": "Generating clarification questions",
# #         "collect_answers": "Waiting for your answers",
# #         "increment_clarification_batch": "Updating clarification batch",
# #         "build_final_requirements": "Building final requirements",

# #         "solution_a": "Generating Solution A",
# #         "solution_b": "Generating Solution B",
# #         "solution_c": "Generating Solution C",

# #         "adversarial_a": "Model A reviewing Solution C",
# #         "adversarial_b": "Model B reviewing Solution A",
# #         "adversarial_c": "Model C reviewing Solution B",

# #         "refine_a": "Refining Solution A",
# #         "refine_b": "Refining Solution B",
# #         "refine_c": "Refining Solution C",

# #         "increment_refinement_round": "Joining refinement branches",
# #         "synthesizer": "Synthesizing final answer"
# #     }

# #     return names.get(name, name)


# # def run_graph(graph_input, config, progress_container):

# #     st.session_state.processing = True

# #     for chunk in graph.stream(
# #         graph_input,
# #         config=config,
# #         stream_mode="updates"
# #     ):

# #         if not chunk:
# #             continue

# #         for node, update in chunk.items():

# #             if node == "__interrupt__":
# #                 continue

# #             display_name = node_name(node)

# #             st.session_state.progress.append(display_name)

# #             progress_container.write(
# #                 f"✅ {display_name}"
# #             )

# #     st.session_state.processing = False


# # def get_interrupt_data():

# #     snapshot = graph.get_state(
# #         get_config()
# #     )

# #     if not snapshot.interrupts:
# #         return None

# #     return snapshot.interrupts[0].value


# # # ------------------------------------------------
# # # SIDEBAR
# # # ------------------------------------------------

# # with st.sidebar:

# #     st.title("Workflow")

# #     st.markdown("### 1. Clarification")
# #     st.success("Groq")
# #     st.caption("openai/gpt-oss-120b")
# #     st.write("5 questions per batch")
# #     st.write("Maximum 10 batches")

# #     st.divider()

# #     st.markdown("### 2. Solution Generation")
# #     st.write("A: Groq")
# #     st.write("B: Groq")
# #     st.write("C: Groq")

# #     st.divider()

# #     st.markdown("### 3. Adversarial Review")
# #     st.write("A ← reviewed by B")
# #     st.write("B ← reviewed by C")
# #     st.write("C ← reviewed by A")

# #     st.divider()

# #     st.markdown("### 4. Refinement")
# #     st.write("Maximum 3 rounds")

# #     st.divider()

# #     st.markdown("### 5. Synthesis")
# #     st.write("Groq")


# # # ------------------------------------------------
# # # MAIN
# # # ------------------------------------------------

# # st.title("🤖 Multi-Agent AI Solver")

# # st.caption(
# #     "Clarification → Parallel Solutions → "
# #     "Adversarial Review → Refinement → Synthesis"
# # )


# # # ------------------------------------------------
# # # INITIAL PROMPT
# # # ------------------------------------------------

# # if not st.session_state.started:

# #     st.subheader("Enter your problem")

# #     initial_prompt = st.text_area(
# #         "What do you want the AI system to solve?",
# #         height=180,
# #         placeholder="Enter your problem here..."
# #     )

# #     if st.button(
# #         "Start Analysis",
# #         type="primary",
# #         use_container_width=True
# #     ):

# #         if not initial_prompt.strip():

# #             st.warning("Please enter a problem first.")

# #         else:

# #             st.session_state.initial_prompt = initial_prompt
# #             st.session_state.started = True
# #             st.session_state.progress = []

# #             initial_state = {
# #                 "initial_prompt": initial_prompt,
# #                 "clarification_batch": 1,
# #                 "max_clarification_batches": 10,
# #                 "clarification_history": [],
# #                 "refinement_round": 0,
# #                 "max_refinement_rounds": 3
# #             }

# #             progress_box = st.empty()

# #             progress_box.info(
# #                 "🚀 Starting workflow..."
# #             )

# #             try:

# #                 run_graph(
# #                     initial_state,
# #                     get_config(),
# #                     progress_box
# #                 )

# #             except Exception as e:

# #                 st.session_state.processing = False

# #                 st.error(
# #                     f"Workflow error: {str(e)}"
# #                 )

# #                 st.exception(e)

# #             st.rerun()


# # # ------------------------------------------------
# # # CURRENT INTERRUPT
# # # ------------------------------------------------

# # interrupt_data = get_interrupt_data()


# # if interrupt_data:

# #     batch = interrupt_data["batch"]
# #     questions = interrupt_data["questions"]

# #     st.subheader(
# #         f"Clarification Batch {batch} / 10"
# #     )

# #     st.info(
# #         "Answer all 5 questions and submit the batch."
# #     )

# #     answers = []

# #     for index, question in enumerate(questions):

# #         st.markdown(
# #             f"### Question {index + 1}"
# #         )

# #         answer = st.text_area(
# #             question,
# #             key=f"batch_{batch}_question_{index}",
# #             height=100
# #         )

# #         answers.append(answer)

# #     all_answered = all(
# #         answer.strip()
# #         for answer in answers
# #     )

# #     if st.button(
# #         f"Submit Batch {batch}",
# #         type="primary",
# #         disabled=not all_answered,
# #         use_container_width=True
# #     ):

# #         st.session_state.progress = []

# #         st.subheader("Workflow Progress")

# #         progress_box = st.empty()

# #         progress_box.info(
# #             "⏳ Processing your answers..."
# #         )

# #         try:

# #             run_graph(
# #                 Command(resume=answers),
# #                 get_config(),
# #                 progress_box
# #             )

# #         except Exception as e:

# #             st.session_state.processing = False

# #             st.error(
# #                 f"Workflow error: {str(e)}"
# #             )

# #             st.exception(e)

# #         st.rerun()


# # # ------------------------------------------------
# # # PROGRESS
# # # ------------------------------------------------

# # if st.session_state.progress:

# #     with st.expander(
# #         "Workflow execution log",
# #         expanded=True
# #     ):

# #         for item in st.session_state.progress:

# #             st.write(
# #                 f"✅ {item}"
# #             )


# # # ------------------------------------------------
# # # FINAL RESULT
# # # ------------------------------------------------

# # snapshot = graph.get_state(
# #     get_config()
# # )

# # state = snapshot.values


# # if state.get("final_answer"):

# #     st.success(
# #         "🎉 Workflow completed successfully"
# #     )

# #     st.divider()

# #     st.subheader("Final Synthesized Answer")

# #     st.markdown(
# #         state["final_answer"]
# #     )

# #     citations = state.get(
# #         "final_citations",
# #         []
# #     )

# #     if citations:

# #         st.divider()

# #         st.subheader("Citations")

# #         for citation in citations:

# #             st.write(citation)


# import uuid

# import streamlit as st

# from langgraph.types import Command

# from graph import graph


# st.set_page_config(
#     page_title="Multi-Agent AI Solver",
#     page_icon="🤖",
#     layout="wide"
# )


# # ============================================================
# # SESSION STATE
# # ============================================================

# if "thread_id" not in st.session_state:
#     st.session_state.thread_id = str(uuid.uuid4())

# if "started" not in st.session_state:
#     st.session_state.started = False

# if "progress" not in st.session_state:
#     st.session_state.progress = []

# if "initial_prompt" not in st.session_state:
#     st.session_state.initial_prompt = ""


# # ============================================================
# # CONFIG
# # ============================================================

# def get_config():

#     return {
#         "configurable": {
#             "thread_id":
#                 st.session_state.thread_id
#         }
#     }


# # ============================================================
# # PROGRESS LABELS
# # ============================================================

# NODE_LABELS = {

#     "clarification_agent":
#         "Generating clarification questions",

#     "collect_answers":
#         "Waiting for your answers",

#     "increment_clarification_batch":
#         "Updating clarification batch",

#     "build_final_requirements":
#         "Building final requirements",

#     "solution_a":
#         "Generating Solution A",

#     "solution_b":
#         "Generating Solution B",

#     "solution_c":
#         "Generating Solution C",

#     "adversarial_b":
#         "Model B reviewing Solution A",

#     "adversarial_c":
#         "Model C reviewing Solution B",

#     "adversarial_a":
#         "Model A reviewing Solution C",

#     "refine_a":
#         "Refining Solution A",

#     "refine_b":
#         "Refining Solution B",

#     "refine_c":
#         "Refining Solution C",

#     "increment_refinement_round":
#         "Completed refinement round",

#     "synthesizer":
#         "Generating final synthesized answer"
# }


# def label(node):

#     return NODE_LABELS.get(
#         node,
#         node
#     )


# # ============================================================
# # SHOW PROGRESS
# # ============================================================

# def show_progress():

#     st.subheader("Workflow Progress")

#     for item in st.session_state.progress:

#         st.success(
#             f"✓ {item}"
#         )


# # ============================================================
# # GET INTERRUPT
# # ============================================================

# def get_interrupt_data():

#     snapshot = graph.get_state(
#         get_config()
#     )

#     if not snapshot.interrupts:
#         return None

#     return snapshot.interrupts[0].value


# # ============================================================
# # SIDEBAR
# # ============================================================

# with st.sidebar:

#     st.title("Workflow")

#     st.markdown("### 1. Clarification")

#     st.success(
#         "Groq — GPT-OSS 120B"
#     )

#     st.write(
#         "5 questions per batch"
#     )

#     st.write(
#         "Maximum 10 batches"
#     )

#     st.divider()

#     st.markdown(
#         "### 2. Solution Generation"
#     )

#     st.write(
#         "A → Groq"
#     )

#     st.write(
#         "B → Groq"
#     )

#     st.write(
#         "C → Groq"
#     )

#     st.caption(
#         "Serial execution"
#     )

#     st.divider()

#     st.markdown(
#         "### 3. Adversarial Review"
#     )

#     st.write(
#         "B reviews A"
#     )

#     st.write(
#         "C reviews B"
#     )

#     st.write(
#         "A reviews C"
#     )

#     st.caption(
#         "Serial execution"
#     )

#     st.divider()

#     st.markdown(
#         "### 4. Refinement"
#     )

#     st.write(
#         "A → B → C"
#     )

#     st.write(
#         "Maximum 3 rounds"
#     )

#     st.divider()

#     st.markdown(
#         "### 5. Synthesis"
#     )

#     st.write(
#         "Groq"
#     )


# # ============================================================
# # HEADER
# # ============================================================

# st.title(
#     "🤖 Multi-Agent AI Solver"
# )

# st.caption(
#     "Serial execution: "
#     "Clarification → Solutions → "
#     "Adversarial Review → Refinement → Synthesis"
# )


# # ============================================================
# # INITIAL PROMPT
# # ============================================================

# if not st.session_state.started:

#     st.subheader(
#         "Enter your problem"
#     )

#     initial_prompt = st.text_area(
#         "Problem",
#         height=180,
#         placeholder=(
#             "Enter the problem you want "
#             "the AI system to solve..."
#         )
#     )

#     if st.button(
#         "Start Analysis",
#         type="primary",
#         use_container_width=True
#     ):

#         if not initial_prompt.strip():

#             st.warning(
#                 "Please enter a problem."
#             )

#         else:

#             st.session_state.initial_prompt = (
#                 initial_prompt
#             )

#             st.session_state.started = True

#             st.session_state.progress = []

#             initial_state = {

#                 "initial_prompt":
#                     initial_prompt,

#                 "clarification_batch":
#                     1,

#                 "max_clarification_batches":
#                     10,

#                 "questions":
#                     [],

#                 "current_batch_answers":
#                     [],

#                 "clarification_answers":
#                     [],

#                 "clarification_history":
#                     [],

#                 "refinement_round":
#                     0,

#                 "max_refinement_rounds":
#                     1
#             }

#             try:

#                 with st.spinner(
#                     "Starting workflow..."
#                 ):

#                     for chunk in graph.stream(
#                         initial_state,
#                         config=get_config(),
#                         stream_mode="updates"
#                     ):

#                         if not chunk:
#                             continue

#                         for node in chunk:

#                             if node == "__interrupt__":
#                                 continue

#                             st.session_state.progress.append(
#                                 label(node)
#                             )

#             except Exception as e:

#                 st.error(
#                     f"Workflow error: {e}"
#                 )

#                 st.exception(e)

#             st.rerun()


# # ============================================================
# # CLARIFICATION
# # ============================================================

# interrupt_data = get_interrupt_data()


# if interrupt_data:

#     batch = interrupt_data["batch"]

#     questions = interrupt_data["questions"]

#     st.subheader(
#         f"Clarification Batch {batch} / 10"
#     )

#     st.info(
#         "Answer all 5 questions before submitting."
#     )

#     answers = []

#     for i, question in enumerate(
#         questions
#     ):

#         st.markdown(
#             f"### Question {i + 1}"
#         )

#         answer = st.text_area(
#             question,
#             key=(
#                 f"batch_{batch}_"
#                 f"question_{i}"
#             ),
#             height=100
#         )

#         answers.append(answer)

#     all_answered = all(
#         answer.strip()
#         for answer in answers
#     )

#     if st.button(
#         f"Submit Batch {batch}",
#         type="primary",
#         disabled=not all_answered,
#         use_container_width=True
#     ):

#         st.session_state.progress = []

#         try:

#             with st.spinner(
#                 "Processing your answers..."
#             ):

#                 for chunk in graph.stream(
#                     Command(
#                         resume=answers
#                     ),
#                     config=get_config(),
#                     stream_mode="updates"
#                 ):

#                     if not chunk:
#                         continue

#                     for node in chunk:

#                         if node == "__interrupt__":
#                             continue

#                         st.session_state.progress.append(
#                             label(node)
#                         )

#         except Exception as e:

#             st.error(
#                 f"Workflow error: {e}"
#             )

#             st.exception(e)

#         st.rerun()


# # ============================================================
# # PROGRESS
# # ============================================================

# if st.session_state.progress:

#     st.divider()

#     show_progress()


# # ============================================================
# # FINAL RESULT
# # ============================================================

# snapshot = graph.get_state(
#     get_config()
# )

# state = snapshot.values


# if state.get("final_answer"):

#     st.divider()

#     st.success(
#         "🎉 Workflow completed"
#     )

#     st.subheader(
#         "Final Synthesized Answer"
#     )

#     st.markdown(
#         state["final_answer"]
#     )

#     citations = state.get(
#         "final_citations",
#         []
#     )

#     if citations:

#         st.divider()

#         st.subheader(
#             "Citations"
#         )

#         for citation in citations:

#             st.write(
#                 citation
#             )



import uuid

import streamlit as st

from langgraph.types import Command

from graph import graph


st.set_page_config(
    page_title="Multi-Agent AI Solver",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(
        uuid.uuid4()
    )

if "started" not in st.session_state:
    st.session_state.started = False

if "progress" not in st.session_state:
    st.session_state.progress = []

if "initial_prompt" not in st.session_state:
    st.session_state.initial_prompt = ""


# ============================================================
# CONFIG
# ============================================================

def get_config():

    return {
        "configurable": {
            "thread_id":
                st.session_state.thread_id
        }
    }


# ============================================================
# NODE LABELS
# ============================================================

NODE_LABELS = {

    "clarification_agent":
        "Generating clarification questions",

    "collect_answers":
        "Waiting for your answers",

    "increment_clarification_batch":
        "Updating clarification batch",

    "build_final_requirements":
        "Building final requirements",

    "solution_a":
        "Generating Solution A",

    "solution_b":
        "Generating Solution B",

    "solution_c":
        "Generating Solution C",

    "adversarial_b":
        "Model B reviewing Solution A",

    "adversarial_c":
        "Model C reviewing Solution B",

    "adversarial_a":
        "Model A reviewing Solution C",

    "refine_a":
        "Refining Solution A",

    "refine_b":
        "Refining Solution B",

    "refine_c":
        "Refining Solution C",

    "increment_refinement_round":
        "Completed refinement round",

    "synthesizer":
        "Synthesizing final answer"
}


def get_label(node):

    return NODE_LABELS.get(
        node,
        node
    )


# ============================================================
# GRAPH RUNNER
# ============================================================

def run_graph(
    graph_input,
    progress_placeholder
):

    for chunk in graph.stream(
        graph_input,
        config=get_config(),
        stream_mode="updates"
    ):

        if not chunk:
            continue

        for node in chunk.keys():

            if node == "__interrupt__":
                continue

            label = get_label(node)

            if label not in (
                st.session_state.progress
            ):

                st.session_state.progress.append(
                    label
                )

            progress_placeholder.markdown(
                "\n\n".join(
                    f"✅ {item}"
                    for item in
                    st.session_state.progress
                )
            )


# ============================================================
# INTERRUPT
# ============================================================

def get_interrupt():

    snapshot = graph.get_state(
        get_config()
    )

    if not snapshot.interrupts:
        return None

    return snapshot.interrupts[0].value


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("Workflow")

    st.markdown(
        "### 1. Clarification"
    )

    st.success(
        "Groq — GPT-OSS 120B"
    )

    st.write(
        "5 questions per batch"
    )

    st.write(
        "Maximum 10 batches"
    )

    st.divider()

    st.markdown(
        "### 2. Solutions"
    )

    st.write(
        "Solution A → Groq"
    )

    st.write(
        "Solution B → Groq"
    )

    st.write(
        "Solution C → Groq"
    )

    st.caption(
        "Serial execution"
    )

    st.divider()

    st.markdown(
        "### 3. Adversarial Review"
    )

    st.write(
        "B → reviews A"
    )

    st.write(
        "C → reviews B"
    )

    st.write(
        "A → reviews C"
    )

    st.caption(
        "Serial execution"
    )

    st.divider()

    st.markdown(
        "### 4. Refinement"
    )

    st.write(
        "A → B → C"
    )

    st.write(
        "Maximum 3 rounds"
    )

    st.divider()

    st.markdown(
        "### 5. Synthesis"
    )

    st.write(
        "Groq — GPT-OSS 120B"
    )


# ============================================================
# HEADER
# ============================================================

st.title(
    "🤖 Multi-Agent AI Solver"
)

st.caption(
    "Serial multi-agent workflow"
)


# ============================================================
# START SCREEN
# ============================================================

if not st.session_state.started:

    st.subheader(
        "Enter your problem"
    )

    initial_prompt = st.text_area(
        "Problem",
        height=180,
        placeholder=(
            "Enter the problem you want "
            "the system to solve..."
        )
    )

    if st.button(
        "Start Analysis",
        type="primary",
        use_container_width=True
    ):

        if not initial_prompt.strip():

            st.warning(
                "Please enter a problem."
            )

        else:

            st.session_state.started = True

            st.session_state.initial_prompt = (
                initial_prompt
            )

            st.session_state.progress = []

            initial_state = {

                "initial_prompt":
                    initial_prompt,

                "clarification_batch":
                    1,

                "max_clarification_batches":
                    10,

                "questions":
                    [],

                "current_batch_answers":
                    [],

                "clarification_answers":
                    [],

                "clarification_history":
                    [],

                "solution_a":
                    "",

                "solution_b":
                    "",

                "solution_c":
                    "",

                "citations_a":
                    [],

                "citations_b":
                    [],

                "citations_c":
                    [],

                "adversarial_feedback_a":
                    "",

                "adversarial_feedback_b":
                    "",

                "adversarial_feedback_c":
                    "",

                "refinement_round":
                    0,

                "max_refinement_rounds":
                    3,

                "final_answer":
                    "",

                "final_citations":
                    []
            }

            progress_placeholder = st.empty()

            progress_placeholder.info(
                "Starting workflow..."
            )

            try:

                run_graph(
                    initial_state,
                    progress_placeholder
                )

            except Exception as e:

                st.error(
                    "Workflow failed"
                )

                st.exception(e)

            st.rerun()


# ============================================================
# CHECK FOR INTERRUPT
# ============================================================

interrupt_data = get_interrupt()


if interrupt_data:

    batch = interrupt_data[
        "batch"
    ]

    questions = interrupt_data[
        "questions"
    ]

    st.subheader(
        f"Clarification Batch "
        f"{batch} / 10"
    )

    st.info(
        "Answer all 5 questions and "
        "submit the batch."
    )

    answers = []

    for index, question in enumerate(
        questions
    ):

        st.markdown(
            f"### Question {index + 1}"
        )

        answer = st.text_area(
            question,
            key=(
                f"batch_{batch}_"
                f"question_{index}"
            ),
            height=100
        )

        answers.append(answer)

    all_answered = all(
        answer.strip()
        for answer in answers
    )

    if st.button(
        f"Submit Batch {batch}",
        type="primary",
        disabled=not all_answered,
        use_container_width=True
    ):

        st.session_state.progress = []

        progress_placeholder = st.empty()

        progress_placeholder.info(
            "Processing your answers..."
        )

        try:

            run_graph(
                Command(
                    resume=answers
                ),
                progress_placeholder
            )

        except Exception as e:

            st.error(
                "Workflow failed"
            )

            st.exception(e)

        st.rerun()


# ============================================================
# PROGRESS
# ============================================================

if st.session_state.progress:

    st.divider()

    st.subheader(
        "Workflow Progress"
    )

    for item in (
        st.session_state.progress
    ):

        st.write(
            f"✅ {item}"
        )


# ============================================================
# FINAL ANSWER
# ============================================================

snapshot = graph.get_state(
    get_config()
)

state = snapshot.values


if state.get("final_answer"):

    st.divider()

    st.success(
        "🎉 Workflow completed successfully"
    )

    st.subheader(
        "Final Synthesized Answer"
    )

    st.markdown(
        state["final_answer"]
    )

    citations = state.get(
        "final_citations",
        []
    )

    if citations:

        st.divider()

        st.subheader(
            "Citations"
        )

        for citation in citations:

            st.write(
                citation
            )