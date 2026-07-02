import os


def get_project_info(project_path):

    total_files = 0
    languages = set()

    extensions = {
        ".py": "Python",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".html": "HTML",
        ".css": "CSS",
        ".xml": "XML",
        ".properties": "Properties",
        ".json": "JSON",
        ".sql": "SQL"
    }

    for root, dirs, files in os.walk(project_path):

        for file in files:

            total_files += 1

            ext = os.path.splitext(file)[1].lower()

            if ext in extensions:
                languages.add(extensions[ext])

    return {
        "files": total_files,
        "languages": sorted(list(languages))
    }

