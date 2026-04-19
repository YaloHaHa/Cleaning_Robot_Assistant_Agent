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

_chat_model = None
_embedding_model = None

def get_chat_model():
    global _chat_model
    if _chat_model is None:
        _chat_model = ChatModelFactory().generator()
    return _chat_model

def get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = EmbeddingModelFactory().generator()
    return _embedding_model