from abc import ABC, abstractmethod
from typing import Optional
from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings
from utils.config_handler import rag_conf

class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[ChatOpenAI | OpenAI]:
        pass

class ChatModelFactory(BaseModelFactory):
    def generator(self):
        return ChatOpenAI(model=rag_conf["chat_model_name"])
    
class EmbeddingModelFactory(BaseModelFactory):
    def generator(self):
        return OpenAIEmbeddings(model=rag_conf["embedding_model_name"])
    
chat_model = ChatModelFactory().generator()
embedding_model = EmbeddingModelFactory().generator()