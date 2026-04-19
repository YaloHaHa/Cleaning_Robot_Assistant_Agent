import yaml
from utils.path_tool import get_abs_path


def load_rag_config(config_path: str = "config/rag.yaml") -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_chroma_config(config_path: str = "config/chroma.yaml") -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    
def load_prompts_config(config_path: str = "config/prompts.yaml") -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_agent_config(config_path: str = "config/agent.yaml") -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.FullLoader)

rag_conf = load_rag_config()
chroma_conf = load_chroma_config()
prompts_conf = load_prompts_config()
agent_conf = load_agent_config()

if __name__ == "__main__":
    print(rag_conf["chat_model_name"])