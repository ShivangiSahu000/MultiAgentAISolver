# # import os

# # from dotenv import load_dotenv

# # from langchain_groq import ChatGroq
# # from langchain_huggingface import (
# #     ChatHuggingFace,
# #     HuggingFaceEndpoint
# # )


# # load_dotenv()


# # GROQ_API_KEY = os.getenv(
# #     "GROQ_API_KEY"
# # )

# # HF_TOKEN = os.getenv(
# #     "HF_TOKEN"
# # )


# # SOLUTION_MODEL_A = os.getenv(
# #     "SOLUTION_MODEL_A",
# #     "deepseek-ai/DeepSeek-R1"
# # )

# # SOLUTION_MODEL_B = os.getenv(
# #     "SOLUTION_MODEL_B",
# #     "Qwen/Qwen2.5-7B-Instruct-1M"
# # )

# # SOLUTION_MODEL_C = os.getenv(
# #     "SOLUTION_MODEL_C",
# #     "openai/gpt-oss-120b"
# # )

# # SYNTHESIZER_MODEL = os.getenv(
# #     "SYNTHESIZER_MODEL",
# #     "Qwen/Qwen2.5-72B-Instruct"
# # )


# # clarification_llm = ChatGroq(
# #     model="openai/gpt-oss-120b",
# #     temperature=0.2,
# #     max_tokens=4096,
# #     api_key=GROQ_API_KEY
# # )


# # def create_hf_llm(model_name: str):

# #     endpoint = HuggingFaceEndpoint(
# #         repo_id=model_name,
# #         huggingfacehub_api_token=HF_TOKEN,
# #         temperature=0.2,
# #         max_new_tokens=4096
# #     )

# #     return ChatHuggingFace(
# #         llm=endpoint
# #     )


# # llm_a = create_hf_llm(
# #     SOLUTION_MODEL_A
# # )


# # llm_b = create_hf_llm(
# #     SOLUTION_MODEL_B
# # )


# # llm_c = create_hf_llm(
# #     SOLUTION_MODEL_C
# # )


# # synthesizer_llm = create_hf_llm(
# #     SYNTHESIZER_MODEL
# # )



# # # serialized
# # # import os

# # # from dotenv import load_dotenv
# # # from langchain_groq import ChatGroq
# # # from langchain_openai import ChatOpenAI
# # # from langchain_google_genai import ChatGoogleGenerativeAI

# # # load_dotenv()


# # # GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# # # NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
# # # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# # # OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


# # # CLARIFICATION_MODEL = os.getenv(
# # #     "CLARIFICATION_MODEL",
# # #     "openai/gpt-oss-120b"
# # # )

# # # SOLUTION_MODEL_A = os.getenv(
# # #     "SOLUTION_MODEL_A",
# # #     "deepseek-ai/deepseek-v4.1-flash"
# # # )

# # # SOLUTION_MODEL_B = os.getenv(
# # #     "SOLUTION_MODEL_B",
# # #     "gemini-3.8-flash"
# # # )

# # # SOLUTION_MODEL_C = os.getenv(
# # #     "SOLUTION_MODEL_C",
# # #     "apodex/apodex-1.1-mini:free"
# # # )

# # # SYNTHESIZER_MODEL = os.getenv(
# # #     "SYNTHESIZER_MODEL",
# # #     "gemini-3.8-flash"
# # # )


# # # if not GROQ_API_KEY:
# # #     raise ValueError("GROQ_API_KEY is missing")

# # # if not NVIDIA_API_KEY:
# # #     raise ValueError("NVIDIA_API_KEY is missing")

# # # if not GEMINI_API_KEY:
# # #     raise ValueError("GEMINI_API_KEY is missing")

# # # if not OPENROUTER_API_KEY:
# # #     raise ValueError("OPENROUTER_API_KEY is missing")


# # # clarification_llm = ChatGroq(
# # #     model=CLARIFICATION_MODEL,
# # #     api_key=GROQ_API_KEY,
# # #     temperature=0.2,
# # #     max_tokens=4096,
# # # )


# # # llm_a = ChatOpenAI(
# # #     model=SOLUTION_MODEL_A,
# # #     api_key=NVIDIA_API_KEY,
# # #     base_url="https://integrate.api.nvidia.com/v1",
# # #     temperature=0.2,
# # #     max_tokens=4096,
# # # )


# # # llm_b = ChatGoogleGenerativeAI(
# # #     model=SOLUTION_MODEL_B,
# # #     google_api_key=GEMINI_API_KEY,
# # #     temperature=0.2,
# # #     max_output_tokens=4096,
# # # )


# # # llm_c = ChatOpenAI(
# # #     model=SOLUTION_MODEL_C,
# # #     api_key=OPENROUTER_API_KEY,
# # #     base_url="https://openrouter.ai/api/v1",
# # #     temperature=0.2,
# # #     max_tokens=4096,
# # #     default_headers={
# # #         "HTTP-Referer": "http://localhost:8501",
# # #         "X-Title": "Multi-Agent AI Solver",
# # #     },
# # # )


# # # synthesizer_llm = ChatGoogleGenerativeAI(
# # #     model=SYNTHESIZER_MODEL,
# # #     google_api_key=GEMINI_API_KEY,
# # #     temperature=0.2,
# # #     max_output_tokens=8192,
# # # )




# import os
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# if not GROQ_API_KEY:
#     raise ValueError("GROQ_API_KEY is missing")

# MODEL = "openai/gpt-oss-120b"

# def create_llm():
#     return ChatGroq(
#         model=MODEL,
#         api_key=GROQ_API_KEY,
#         temperature=0.2,
#         max_tokens=1024
#     )

# clarification_llm = create_llm()

# llm_a = create_llm()
# llm_b = create_llm()
# llm_c = create_llm()

# synthesizer_llm = create_llm()



import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env")

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)


def create_llm():
    return ChatGroq(
        model=MODEL_NAME,
        api_key=GROQ_API_KEY,
        temperature=0.2,
        max_tokens=4096,
        timeout=120,
        max_retries=2
    )


clarification_llm = create_llm()

llm_a = create_llm()
llm_b = create_llm()
llm_c = create_llm()

synthesizer_llm = create_llm()