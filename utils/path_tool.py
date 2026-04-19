# To provide an unified absolute path for the project

import os

def get_project_root() -> str:
    #Get the root directory of the project
    current_file = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_file)
    project_root = os.path.dirname(current_folder)
    return project_root

def get_abs_path(relative_path:str) ->str:
    #Get the absolute path of a file given its relative path from the project root
    project_root = get_project_root()
    abs_path = os.path.join(project_root, relative_path)
    return abs_path

if __name__ == "__main__":
    print("="*50)
    print(get_abs_path("data/sample_data.csv"))