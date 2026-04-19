# RAG Summarization Service
# Flow: User question → retriever (semantic search from Chroma) → retrieved docs → build context string
#       → prompt_template | model | StrOutputParser → summarized answer (str)

from xml.dom.minidom import Document

from rag.vector_store import VectorStoreService
from utils.prompt_uploader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import get_chat_model
from langchain_core.output_parsers import StrOutputParser

def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*20)
    return prompt

class RagSummarizeService:
    def __init__(self):
        self.vector_store_service = VectorStoreService()
        self.retriever = self.vector_store_service.get_retriever()
        self.prompt_text = load_rag_prompts()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = get_chat_model()
        self.chain = self._init_chain()
    
    def _init_chain(self):
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return chain

    def retrieve_docs(self, query:str) -> list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query:str) -> str:
        retrieved_docs = self.retrieve_docs(query)
        context = ""
        counter = 0
        for doc in retrieved_docs:
            context += f"Reference Document {counter}:\n{doc.page_content}, meta: {doc.metadata}\n\n"
            counter += 1
        return self.chain.invoke(
            {
                "input": query,
                "context": context
            }
        )

if __name__ == '__main__':
    rag = RagSummarizeService()

    print(rag.rag_summarize("小户型适合哪些扫地机器人"))