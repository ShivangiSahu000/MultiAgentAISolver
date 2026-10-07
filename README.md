# Multi-Agent AI Solver

## Overview

Multi-Agent AI Solver is a **LangGraph + LangChain + Streamlit** application that uses multiple AI agents to solve complex user problems through a structured workflow.

The application first clarifies the user's requirements, then generates **three independent solutions**. Each solution is reviewed by a different agent, refined based on the feedback, and finally all three refined solutions are passed to a synthesizer to generate one final answer.

The workflow is executed **sequentially**, meaning one LLM call runs at a time. This makes the system easier to debug, reduces concurrent API pressure, and provides clearer execution logs.

## High-Level Architecture
The system is built around a sequential LangGraph workflow.

<img width="319" height="282" alt="image" src="https://github.com/user-attachments/assets/abb06626-18c3-4e55-80fb-95418c40d510" />


## How to Run
1. Clone the Repository
```git clone <repository-url>
cd MultiAgentAISolver
```

2. Create a Virtual Environment
Windows
```python -m venv .venv
.venv\Scripts\activate
```
macOS/Linux
```python3 -m venv .venv
source .venv/bin/activate
```
3. Install Dependencies
   
```pip install -r requirements.txt```
If requirements.txt is not available, install the required packages:
```pip install streamlit langgraph langchain langchain-groq python-dotenv```

4. Configure Environment Variables
Create a .env file in the project root:
```GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
```
Replace your_groq_api_key with your actual Groq API key.
Do not commit .env or your API key to GitHub.
5. Run the Application
Start the Streamlit application:
```streamlit run app.py```
The application will open in your browser, usually at:
```http://localhost:8501```
6. Testing Configuration
For initial testing, keep the workflow small:
Maximum clarification batches = 1 or 2
Maximum refinement rounds = 1

Once the workflow is working correctly, the recommended production configuration is:
Maximum clarification batches = 10
Maximum refinement rounds = 3

This keeps testing faster and reduces unnecessary LLM/API usage.

## Execution Flow
When the application starts, the user:
1. Enters the initial problem.
2. Answers the clarification questions.
3. The system generates the final requirements.
4. Three independent solutions are generated.
5. Each solution is reviewed by another model.
6. Each solution is refined using the review feedback.
7. The refinement cycle can repeat.
8. The final synthesizer combines all refined solutions.
9. The final answer is displayed in the Streamlit UI.
