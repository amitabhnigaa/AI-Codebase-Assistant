import os
import uuid
from git import Repo


BASE_DIR = "repositories"


def clone_repository(repo_url):

    os.makedirs(BASE_DIR, exist_ok=True)

    repo_name = repo_url.rstrip("/").split("/")[-1]

    unique_id = str(uuid.uuid4())[:8]

    destination = os.path.join(
        BASE_DIR,
        f"{repo_name}_{unique_id}"
    )

    Repo.clone_from(
        repo_url,
        destination
    )

    return destination