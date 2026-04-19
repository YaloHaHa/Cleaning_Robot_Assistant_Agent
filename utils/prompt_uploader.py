# Prompt Uploader is developed as a standalone tool to upload prompts to the database.
# Giving more flexibility to users to manage their prompts without needing to interact with the main application.


from utils.config_handler import prompts_conf
from utils.file_handler import get_file_md5_hex
from utils.logger_handler import logger
from utils.path_tool import get_abs_path


def load_system_prompts() -> str:
    try:
        system_prompt_path = get_abs_path(prompts_conf["main_prompt_path"])
    except Exception as e:
        logger.error(f"Error loading system prompt path: {e}")
        raise e
    
    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"Error reading system prompt: {e}")
        raise e

def load_rag_prompts() -> str:
    try:
        rag_prompt_path = get_abs_path(prompts_conf["rag_summarize_prompt_path"])
    except Exception as e:
        logger.error(f"Error loading RAG prompt path: {e}")
        raise e
    
    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"Error reading RAG prompt: {e}")
        raise e

def load_report_prompts() -> str:
    try:
        report_prompt_path = get_abs_path(prompts_conf["report_prompt_path"])
    except Exception as e:
        logger.error(f"Error loading report prompt path: {e}")
        raise e
    
    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"Error reading report prompt: {e}")
        raise e
    

if __name__ == "__main__":
    print(load_system_prompts())
    