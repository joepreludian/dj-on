FROM astral/uv:python3.14-bookworm-slim AS builder

ARG BUILD_MODE

COPY pyproject.toml uv.lock /

RUN pip install toml-cli && toml get --toml-path pyproject.toml project.version > /tmp/PROJECT_VERSION

RUN if [ "${BUILD_MODE}" = "IS_DEV" ] ; then uv export --no-editable --no-emit-project -o /tmp/requirements.txt ; fi
RUN if [ "${BUILD_MODE}" = "IS_PROD" ] ; then uv export --no-dev --no-editable --no-emit-project -o /tmp/requirements.txt ; fi

FROM docker.io/alpine/git AS git_info

COPY . /app/
WORKDIR /app/
RUN git rev-parse --short HEAD > /tmp/PROJECT_GIT_SHA

FROM python:{{cookiecutter.python_version}}

WORKDIR /app/

COPY --from=builder /tmp/requirements.txt /app_support/
COPY --from=builder /tmp/PROJECT_VERSION /app_support/
COPY --from=git_info /tmp/PROJECT_GIT_SHA /app_support/

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y gettext \
    && apt clean all

RUN pip install -r /app_support/requirements.txt

COPY ./ /app/

EXPOSE {{ cookiecutter.app_container_port }}

WORKDIR /app/src/

CMD ["daphne", "-b", "0.0.0.0", "-p", "{{cookiecutter.app_container_port}}", "{{cookiecutter.project_slug}}.asgi:application"]
