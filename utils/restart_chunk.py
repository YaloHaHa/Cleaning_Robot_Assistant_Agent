import os
import shutil
from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path
from utils.logger_handler import logger
from langchain_chroma import Chroma
from model.factory import embedding_model


def _get_vector_store() -> Chroma:
    return Chroma(
        collection_name=chroma_conf["collection_name"],
        embedding_function=embedding_model,
        persist_directory=chroma_conf["persist_directory"],
    )


def clear_md5_store():
    """Clear the MD5 hex store so all documents are treated as new."""
    md5_path = get_abs_path(chroma_conf["md5_hex_store"])
    if os.path.exists(md5_path):
        os.remove(md5_path)
        logger.info(f"MD5 store cleared: {md5_path}")
    else:
        logger.info("MD5 store does not exist, nothing to clear.")


def clear_chroma():
    """Delete the entire Chroma collection directory."""
    chroma_dir = chroma_conf["persist_directory"]
    if os.path.exists(chroma_dir):
        shutil.rmtree(chroma_dir)
        logger.info(f"Chroma directory deleted: {chroma_dir}")
    else:
        logger.info("Chroma directory does not exist, nothing to clear.")


def rechunk_all():
    """Clear all chunks and MD5 records. Does not re-load documents."""
    clear_chroma()
    clear_md5_store()
    logger.info("All chunks and MD5 records cleared.")


def delete_by_filename(filename: str):
    """Delete all chunks from Chroma whose source metadata contains the given filename.

    Args:
        filename: The filename (or partial path) to match against the 'source' metadata.
                  e.g. "尺码推荐.txt" or "data_bot/尺码推荐.txt"
    """
    vs = _get_vector_store()
    collection = vs._collection

    # Get all documents with their metadata
    results = collection.get(include=["metadatas"])
    ids_to_delete = [
        doc_id
        for doc_id, meta in zip(results["ids"], results["metadatas"])
        if meta and filename in meta.get("source", "")
    ]

    if not ids_to_delete:
        logger.info(f"No chunks found matching filename: {filename}")
        return

    vs.delete(ids_to_delete)
    logger.info(f"Deleted {len(ids_to_delete)} chunks matching '{filename}'.")

    # Also remove the corresponding MD5 from the store if we can recompute it
    # (User should re-run load_document() after to re-ingest if needed)


def remove_md5_for_file(filepath: str):
    """Remove a specific file's MD5 from the store so it will be re-loaded next time.

    Args:
        filepath: Absolute path to the file whose MD5 should be removed.
    """
    from utils.file_handler import get_file_md5_hex
    md5_path = get_abs_path(chroma_conf["md5_hex_store"])
    if not os.path.exists(md5_path):
        logger.info("MD5 store does not exist.")
        return

    target_md5 = get_file_md5_hex(filepath)
    with open(md5_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    remaining = [line for line in lines if line.strip() != target_md5]

    if len(remaining) == len(lines):
        logger.info(f"MD5 for {filepath} not found in store.")
        return

    with open(md5_path, "w", encoding="utf-8") as f:
        f.writelines(remaining)
    logger.info(f"Removed MD5 for {filepath} from store.")


def rechunk_file(filepath: str):
    """Clear chunks for a single file from Chroma and remove its MD5. Does not re-load.

    Args:
        filepath: Absolute path to the file to clear.
    """
    filename = os.path.basename(filepath)
    delete_by_filename(filename)
    remove_md5_for_file(filepath)
    logger.info(f"Chunks and MD5 for {filename} cleared.")


if __name__ == "__main__":
    import sys

    usage = """Usage:
  python -m utils.restart_chunk all              # Re-chunk all documents
  python -m utils.restart_chunk file <filepath>   # Re-chunk a single file
  python -m utils.restart_chunk delete <filename>  # Delete chunks by filename
"""
    if len(sys.argv) < 2:
        print(usage)
        sys.exit(1)

    command = sys.argv[1]

    if command == "all":
        rechunk_all()
    elif command == "file" and len(sys.argv) >= 3:
        rechunk_file(get_abs_path(sys.argv[2]))
    elif command == "delete" and len(sys.argv) >= 3:
        delete_by_filename(sys.argv[2])
    else:
        print(usage)
        sys.exit(1)
