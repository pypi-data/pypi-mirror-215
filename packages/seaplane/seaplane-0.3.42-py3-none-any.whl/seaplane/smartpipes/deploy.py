import json
import os
import shutil
from typing import Any, Dict, List, Optional

import requests

from ..api.api_http import headers
from ..api.api_request import provision_req
from ..api.token_api import TokenAPI
from ..configuration import config, Configuration
from ..logging import log
from ..util import unwrap
from .build import build
from .coprocessor import Coprocessor
from .decorators import context
from .smartpipe import SmartPipe
from ..model.secrets import Secret
from .datasources import tenant_database

def create_coprocessor_docker_file(coprocessor: Coprocessor) -> None:
    docker_file = f"""FROM python:3.10

ENV SMARTPIPES_PRODUCTION True
ENV COPROCESSOR_ID {coprocessor.id}

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "demo.py"]
    """

    if not os.path.exists(f"build/{coprocessor.id}"):
        os.makedirs(f"build/{coprocessor.id}")

    with open(f"build/{coprocessor.id}/Dockerfile", "w") as file:
        file.write(docker_file)

    os.system(
        f"docker buildx build --platform linux/arm64,linux/amd64 -t us-central1-docker.pkg.dev/artifacts-356722/demo/coprocessors/{coprocessor.id}:latest  build/{coprocessor.id}  --push"  # noqa
    )


def create_http_api_entry_point_docker_file() -> None:
    docker_file = """FROM python:3.10

ENV SMARTPIPES_PRODUCTION True
ENV PORT 5000

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn


EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:${PORT} --workers 1 --timeout 300 demo:app
    """

    if not os.path.exists("build/http"):
        os.makedirs("build/http")

    with open("build/http/Dockerfile", "w") as file:
        file.write(docker_file)


def create_carrier_workload_file(
    tenant: str, smart_pipe_id: str, coprocessor: Coprocessor, next_coprocessors: List[str]
) -> Dict[str, Any]:
    output: Optional[Dict[str, Any]] = None

    if len(next_coprocessors) > 1:
        output = {
            "broker": {
                "outputs": (
                    {"carrier": {"subject": f"{smart_pipe_id}.{c_id}"}}
                    for c_id in next_coprocessors
                )
            }
        }
    elif len(next_coprocessors) == 1:
        output = {
            "label": "carrier_out",
            "carrier": {"subject": f"{smart_pipe_id}.{next_coprocessors[0]}"},
        }

    workload = {
        "tenant": tenant,
        "id": coprocessor.id,
        "input": {
            "label": "carrier_in",
            "carrier": {
                "subject": f"{smart_pipe_id}.{coprocessor.id}",
                "deliver": "all",
                "queue": coprocessor.id,
            },
        },
        "processor": {
            "docker": {
                "image": f"us-central1-docker.pkg.dev/artifacts-356722/demo/coprocessors/{coprocessor.id}:latest",  # noqa
                "args": [],
            }
        },
        "output": output,
    }

    if not os.path.exists(f"build/{coprocessor.id}"):
        os.makedirs(f"build/{coprocessor.id}")

    with open(f"build/{coprocessor.id}/workload.json", "w") as file:
        json.dump(workload, file, indent=2)
        log.debug(f"Created {coprocessor.id} workload")

    return workload


def copy_project_into_resource(id: str) -> None:
    source_folder = "."
    destination_folder = f"build/{id}"

    if not os.path.exists(f"build/{id}"):
        os.makedirs(f"build/{id}")

    for item in os.listdir(source_folder):
        if os.path.isdir(item) and item == "build":
            continue  # Skip the "build" folder

        elif os.path.isdir(item):
            destination_path = os.path.join(destination_folder, item)
            if os.path.exists(destination_path):
                shutil.rmtree(destination_path)
            shutil.copytree(item, destination_path)
        else:
            destination_path = os.path.join(destination_folder, item)
            shutil.copy2(item, destination_path)


def create_stream(name: str) -> Any:
    log.debug(f"Creating stream: {name}")
    url = f"{config.carrier_endpoint}/stream/{name}"
    req = provision_req(config._token_api)

    payload = {}

    return unwrap(
        req(
            lambda access_token: requests.put(
                url,
                json=payload,
                headers=headers(access_token),
            )
        )
    )


def delete_stream(name: str) -> Any:
    log.debug(f"Deleting stream: {name}")
    url = f"{config.carrier_endpoint}/stream/{name}"
    req = provision_req(config._token_api)

    return unwrap(
        req(
            lambda access_token: requests.delete(
                url,
                headers=headers(access_token),
            )
        )
    )

def get_secrets(config: Configuration) -> List[Secret]:
    secrets = []
    for key, value in config._api_keys.items():    
        secrets.append(Secret(key, value))
    
    return secrets

def add_secrets(name: str, secrets: List[Secret]) -> Any:    
    url = f"{config.carrier_endpoint}/flow/{name}/secrets"
    req = provision_req(config._token_api)

    flow_secrets = {}    
    for secret in secrets:
        flow_secrets[secret.key] = {
            "destination": "all",
            "value": secret.value
        }

    return unwrap(
        req(
            lambda access_token: requests.put(
                url,
                json=flow_secrets,
                headers=headers(access_token),
            )
        )
    )

def create_flow(name: str, workload: Dict[str, Any]) -> Any:
    log.debug(f"Creating flow: {name}")
    url = f"{config.carrier_endpoint}/flow/{name}"
    req = provision_req(config._token_api)

    return unwrap(
        req(
            lambda access_token: requests.put(
                url,
                json=workload,
                headers=headers(access_token),
            )
        )
    )


def delete_flow(name: str) -> Any:
    log.debug(f"Deleting flow: {name}")

    url = f"{config.carrier_endpoint}/flow/{name}"
    req = provision_req(config._token_api)

    return unwrap(
        req(
            lambda access_token: requests.delete(
                url,
                headers=headers(access_token),
            )
        )
    )

def deploy_coprocessor(
    tenant: str, 
    smart_pipe: SmartPipe, 
    coprocessor: Coprocessor, 
    schema: Dict[str, Any],
    secrets: List[Secret]
) -> None:
    delete_flow(coprocessor.id)


    save_result_coprocessor = schema["smartpipes"][smart_pipe.id]["io"].get("returns", None) == coprocessor.id
    
    save_result_coprocessor = schema["smartpipes"][smart_pipe.id]["io"].get("returns", None) == coprocessor.id
    copy_project_into_resource(coprocessor.id)
    create_coprocessor_docker_file(coprocessor)
    next_coprocessors = schema["smartpipes"][smart_pipe.id]["io"].get(coprocessor.id, None)

    if next_coprocessors is None:
        next_coprocessors = []

    workload = create_carrier_workload_file(tenant, smart_pipe.id, coprocessor, next_coprocessors)

    save_result_coprocessor = schema["smartpipes"][smart_pipe.id]["io"].get("returns", None) == coprocessor.id

    create_flow(coprocessor.id, workload)        
    secrets.append(Secret("COPROCESSOR_ID", coprocessor.id))
    secrets.append(Secret("SAVE_RESULT_COPROCESSOR", str(save_result_coprocessor)))
    add_secrets(coprocessor.id, secrets)

    log.info(f"Deploy for coprocessor {coprocessor.id} done")


def deploy(coprocessor_id: Optional[str] = None) -> None:    
    schema = build()
    tenant = TokenAPI(config).get_tenant()
    tenant_db = tenant_database()
    secrets = get_secrets(config) 

    secrets.append(Secret("SMARTPIPES_PRODUCTION", "true"))        
    secrets.append(Secret("SEAPLANE_TENANT_DB__DATABASE", tenant_db.name))
    secrets.append(Secret("SEAPLANE_TENANT_DB_USERNAME", tenant_db.username))
    secrets.append(Secret("SEAPLANE_TENANT_DB_PASSWORD", tenant_db.password))

    if coprocessor_id is not None and coprocessor_id != "entry_point":
        for sm in context.smart_pipes:
            for c in sm.coprocessors:
                if c.id == coprocessor_id:
                    deploy_coprocessor(tenant, sm, c, schema, secrets[:])
    elif coprocessor_id is not None and coprocessor_id == "entry_point":
        log.info("Deploying entry points...")

        copy_project_into_resource("http")
        create_http_api_entry_point_docker_file()
    else:  # deploy everything
        for sm in context.smart_pipes:
            delete_stream(sm.id)
            create_stream(sm.id)

            for c in sm.coprocessors:
                deploy_coprocessor(tenant, sm, c, schema, secrets[:])

        copy_project_into_resource("http")
        create_http_api_entry_point_docker_file()

    log.info("Deployment complete")


def destroy() -> None:
    build()

    for sm in context.smart_pipes:
        delete_stream(sm.id)

        for c in sm.coprocessors:
            delete_flow(c.id)
