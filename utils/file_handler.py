import os
import hashlib
from sys import path
import utils.logger_handler as logger_handler
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader

def get_file_md5_hex(filepath: str) -> str:
    # Check if the file exists
    if not os.path.isfile(filepath):
        raise ValueError(f"{filepath} is not a valid file path.")
    
    # Create an MD5 hash object. Avoid the memory overflow by reading the file in chunks
    md5_hashlib = hashlib.md5()
    chunk_size = 8192  # Read the file in 8KB chunks
    try:
        with open(filepath,"rb") as f:
            while chunk := f.read(chunk_size):
                md5_hashlib.update(chunk)
    except Exception as e:
        logger_handler.logger.error(f"Error reading file {filepath}: {e}")
        raise e
    
    return md5_hashlib.hexdigest()

def listdir_with_allowed_type(filepath: str, allowed_types: tuple[str]) -> tuple[str]:
    files = []
    # Check if the path is a valid directory
    if not os.path.isdir(filepath):
        raise ValueError(f"{filepath} is not a valid directory path.")
    # List all files in the directory and filter by allowed types
    for filename in os.listdir(filepath):
        if filename.endswith(allowed_types):
            files.append(os.path.join(filepath, filename))
    
    return tuple(files)

def pdf_loader(filepath: str) -> list[Document]:
    return PyPDFLoader(filepath).load()

def txt_loader(filepath: str) -> list[Document]:
    return TextLoader(filepath, encoding = 'utf-8').load()
