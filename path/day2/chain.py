# Hallucination 평가 적용하다가 오류 나는 상태인데 그대로 저장해둠.
import getpass
import os
import json
import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

os.environ["OPENAI_API_KEY"] = getpass.getpass()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]

loader = WebBaseLoader(
    web_paths=(
        urls
    ),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title")
        )
    ),
)

docs = loader.load()

splits = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
).split_documents(docs)

vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})

promptForRag = hub.pull("rlm/rag-prompt")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

parser = JsonOutputParser()

promptForLLM = PromptTemplate(
    template="""
    Determine if the retrieved text (context) is relevant to the user’s query (question). 
    - Focus on conceptual and semantic alignment, ignoring minor wording differences.
    - Mark as relevant if the context reasonably helps answer the question; otherwise, it is not.

    Respond strictly in JSON format:
    {{
        "relevance": true
    }}

    \n{format_instructions}\n{question}\n{context}\n
    """,
    input_variables=["question", "context"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)


llmChain = promptForLLM | llm | parser

# Hallucination 평가를 위한 프롬프트
hallucination_prompt = PromptTemplate(
    template="""
    You are an AI system responsible for evaluating the accuracy and factual integrity of an AI-generated response to a user's query. Your task is to determine whether the response contains hallucinations (false or fabricated information that is not supported by the provided context).

    **Criteria for Evaluation**:
    1. **Alignment with Context**: Verify if the response aligns with the context provided. If information is introduced that is not present or supported in the context, it should be flagged as hallucination.
    2. **Logical Accuracy**: Check whether the response makes logical sense and avoids introducing fabricated details.
    3. **External Knowledge**: Do not rely on external information beyond the provided context. Your judgment should only depend on the content supplied.

    **Response Format**:
    - If hallucination is detected, output: `{{'hallucination': 'yes'}}`
    - If no hallucination is found, output: `{{'hallucination': 'no'}}`

    **Input**:
    User Query: {query}  
    AI Response: {response}  
    Context: {context}

    **Task**:
    Based on the query, the AI response, and the context, evaluate if the response contains hallucinations. Output your evaluation strictly in the specified format.
    """,
    input_variables=["query", "response", "context"],
)

hallucination_chain = hallucination_prompt | llm | parser

query = "What is Task Decomposition?"

chainForRag = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | promptForRag
)

context = chainForRag.invoke(query)

# LLM 응답 처리 및 JSON 파싱
try:
    response = llmChain.invoke({"question": query, "context": context})
    print("Raw LLM Response:", response)
    parsed_response = json.loads(response)
except json.JSONDecodeError as e:
    print("JSON Parsing Error:", e)
    parsed_response = None

# 응답 유효성 및 처리
if parsed_response and parsed_response.get("relevance", False):
    print("Response is relevant.")
    # 사용자 질문에 대한 응답 생성
    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    chain = prompt | llm | parser
    ai_response = chain.invoke({"query": query})
    print(f"AI Response: {ai_response}")

    # Hallucination 평가 실행
    try:
        hallucination_result = hallucination_chain.invoke({
            "query": query,
            "response": ai_response,
            "context": context,
        })
        print("Hallucination Evaluation:", hallucination_result)
        if hallucination_result["hallucination"] == "yes":
            print("The response contains hallucinations.")
        else:
            print("The response does not contain hallucinations.")
    except Exception as e:
        print("Hallucination Evaluation Error:", e)
else:
    print("Response is not relevant or parsing failed.")
