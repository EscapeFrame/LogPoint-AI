from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from output_parser import correction
import os
load_dotenv()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_dpi(a, b, r):
    prompts = """
        오직 계산된 보정비율만을 응답할 수 있습니다.
        보정비율은 소수점 셋째자리에서 반올림하여 응답해야합니다.
        contnet 태그 안의 내용을 참고하여 보정해주십시오 :
        <content>
        아래 글에서 말하는 수식 (1)은 루트 ( (ax - rx) ** 2 + (ax - ry) ** 2 ) / ( (ax - bx) ** 2 + (ax - by) ** 2 )입니다.
        {context}
        </content>
        
        응답은 다음과 같은 형식으로 해야합니다. {output_parser}
        응답 : {Question}
    """
    prompt = PromptTemplate.from_template(prompts)
    embedder = OpenAIEmbeddings()
    vector_store = PineconeVectorStore(index_name=os.getenv("INDEX_NAME"), embedding=embedder)
    llm = ChatOpenAI(model="gpt-4o-mini")

    # -- 더미 데이터 --
    # a = (0, 0)
    # b = (3, 5)
    # r = (7, 8)

    query = f"시작점 : {a}, 목표점 : {b},  클릭점 : {r}, 이 정보들을 토대로 2D감도를 수치화 알고리즘을 사용하여 보정하세요."

    chain = {"context" : vector_store.as_retriever() | format_docs, "Question" : RunnablePassthrough(), "output_parser" : lambda _ : correction.get_format_instructions()} | prompt | llm
    res = chain.invoke(query)
    res = correction.parse(res.content)
    print(res)
    return res