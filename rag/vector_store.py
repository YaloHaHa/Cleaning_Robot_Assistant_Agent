# Vector Store Service
# Manages Chroma vector DB: loads documents (PDF/TXT) → splits into chunks → embeds and stores.
# Tracks loaded files via MD5 hex to avoid duplicate ingestion.
# Exposes a retriever for semantic search (used by RagSummarizeService).

from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.config_handler import chroma_conf
from utils.file_handler import pdf_loader, txt_loader, listdir_with_allowed_type, get_file_md5_hex
from langchain_openai import OpenAIEmbeddings
from model.factory import embedding_model
import os
from utils.logger_handler import logger

from utils.path_tool import get_abs_path



class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf["collection_name"],
            embedding_function=embedding_model,
            persist_directory=chroma_conf["persist_directory"]
        )
        self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=chroma_conf["chunk_size"],
                chunk_overlap=chroma_conf["chunk_overlap"],
                separators = chroma_conf["separator"],
                length_function=len,
        )

    def get_retriever(self):
        # Set the embedding function for the vector store
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["retriever_k"]})
    
    def load_document(self):
        # load document if not yet loaded

        def check_md5_hex(md5_to_check: str) -> bool:
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                return False
            # Check if the md5_hex exists in the vector store
            with open (get_abs_path(chroma_conf["md5_hex_store"]), "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() == md5_to_check:
                        return True
            return False
        
        def save_md5_hex(md5_to_save: str):
            with open (get_abs_path(chroma_conf["md5_hex_store"]), "a", encoding="utf-8") as f:
                f.write(md5_to_save + "\n")

        def get_file_documents(filepath: str):
            if filepath.endswith(".pdf"):
                return pdf_loader(filepath)
            elif filepath.endswith(".txt"):
                return txt_loader(filepath)
        
        allowed_files_path: list[str] = listdir_with_allowed_type(
            get_abs_path(chroma_conf["data_path"]),
            tuple(chroma_conf["allowed_file_types"])
        )
        for file in allowed_files_path:
            md5_hex = get_file_md5_hex(file)
            if check_md5_hex (md5_hex):
                logger.info(f"{file} has already been loaded, skipping.")
                continue

            try:
                documents = get_file_documents(file)
                if not documents:
                    logger.warning(f"No documents found in {file}, skipping.")
                    continue

                # split and store:
                split_docs = self.splitter.split_documents(documents)
                self.vector_store.add_documents(split_docs)
                save_md5_hex(md5_hex)
                logger.info(f"{file} loaded successfully with {len(split_docs)} chunks.")
            except Exception as e:
                logger.error(f"Error loading {file}: {e}", exc_info=True)
                continue

if __name__ == "__main__":
    vs = VectorStoreService()
    vs.load_document()
    retriever = vs.get_retriever()
    res = retriever.invoke("迷路")
    for r in res:
        print(r.page_content)
        print("-"*20)

