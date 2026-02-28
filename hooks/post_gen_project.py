"""Post-generation hook: write .env with a real SECRET_KEY, then run uv sync."""
import os
import secrets
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path.cwd()


def generate_secret_key() -> str:
    return secrets.token_urlsafe(50)


def write_env() -> None:
    env_example = PROJECT_DIR / ".env.example"
    env_file = PROJECT_DIR / ".env"

    if not env_example.exists():
        print("WARNING: .env.example not found, skipping .env creation.")
        return

    content = env_example.read_text()
    content = content.replace("CHANGE_ME", generate_secret_key())
    env_file.write_text(content)
    print(f"Created {env_file}")


def run_uv_sync() -> None:
    print("Running uv sync …")
    result = subprocess.run(
        ["uv", "sync"],
        cwd=PROJECT_DIR,
    )
    if result.returncode != 0:
        print("WARNING: uv sync failed. Run it manually after fixing any issues.")
    else:
        print("uv sync completed successfully.")


def run_docker_build() -> None:
    subprocess.run(["make", "build"], cwd=PROJECT_DIR)

def run_project_migrations() -> None:
    subprocess.run(["make", "migrations"], cwd=PROJECT_DIR)

def run_git_init() -> None:
    subprocess.run(["git", "init"], cwd=PROJECT_DIR)

def run_docker_compose_build() -> None:
    subprocess.run(["docker", "compose", "build", "--no-cache"], cwd=PROJECT_DIR)

def run_docker_compose_up() -> None:
    subprocess.run(["docker", "compose", "up", "--wait"], cwd=PROJECT_DIR)

def run_docker_compose_prepare() -> None:
    subprocess.run(["make", "migrate"], cwd=PROJECT_DIR)

def print_next_steps() -> None:
    slug = "{{ cookiecutter.project_slug }}"
    print(f"Project '{slug}' created successfully!")


if __name__ == "__main__":
    write_env()
    run_uv_sync()
    run_git_init()
    run_docker_compose_build()
    run_docker_compose_up()
    run_docker_compose_prepare()
    print_next_steps()
