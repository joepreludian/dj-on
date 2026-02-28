from ninja import Router

from {{ cookiecutter.project_slug }}.settings import PROJECT_VERSION, PROJECT_GIT_SHA

router = Router()


@router.get("/healthcheck/")
def healthcheck(request):
    return {"status": "ok", "api_version": PROJECT_VERSION, "commit": PROJECT_GIT_SHA}
