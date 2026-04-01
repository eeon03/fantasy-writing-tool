import json
import os

current_project = None

def set_project(project_name):
    global current_project
    current_project = project_name
    os.makedirs(_project_path(), exist_ok=True)

def get_project():
    return current_project

def _project_path():
    if not current_project:
        raise Exception("No project selected. Call set_project() first.")
    return os.path.join("data", "projects", current_project)

def save(filename, data):
    path = _project_path()
    filepath = os.path.join(path, f"{filename}.json")
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def load(filename):
    path = _project_path()
    filepath = os.path.join(path, f"{filename}.json")
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

def list_projects():
    projects_path = os.path.join("data", "projects")
    if not os.path.exists(projects_path):
        return []
    return [
        d for d in os.listdir(projects_path)
        if os.path.isdir(os.path.join(projects_path, d))
    ]

def create_project(project_name):
    clean_name = project_name.lower().replace(" ", "-")
    project_path = os.path.join("data", "projects", clean_name)
    if os.path.exists(project_path):
        return False, clean_name
    os.makedirs(project_path, exist_ok=True)
    return True, clean_name

def delete_project(project_name):
    import shutil
    project_path = os.path.join("data", "projects", project_name)
    if not os.path.exists(project_path):
        return False
    shutil.rmtree(project_path)
    return True

def rename_project(old_name, new_name):
    import shutil
    old_path = os.path.join("data", "projects", old_name)
    clean_new = new_name.lower().replace(" ", "-")
    new_path = os.path.join("data", "projects", clean_new)
    if not os.path.exists(old_path):
        return False, "Project not found."
    if os.path.exists(new_path):
        return False, "A project with that name already exists."
    shutil.move(old_path, new_path)
    return True, clean_new

def project_summary():
    projects_path = os.path.join("data", "projects")
    if not os.path.exists(projects_path):
        return {}
    
    summary = {}
    for project in list_projects():
        path = os.path.join(projects_path, project)
        counts = {}
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                filepath = os.path.join(path, filename)
                with open(filepath, "r") as f:
                    try:
                        data = json.load(f)
                        counts[filename.replace(".json", "")] = len(data)
                    except:
                        counts[filename.replace(".json", "")] = 0
        summary[project] = counts
    return summary
