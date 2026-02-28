import os
from pathlib import Path
from functools import lru_cache


@lru_cache
def get_project_version():

    APP_SUPPORT_DIR = Path("/app_support/")

    def _read_file_contents(filename):
        if os.path.isfile( APP_SUPPORT_DIR / filename):
            with open( APP_SUPPORT_DIR / filename) as f:
                return f.read().strip()

        return "__NOT_AVAILABLE__"

    return _read_file_contents("PROJECT_VERSION"), _read_file_contents(
        "PROJECT_GIT_SHA"
    )
