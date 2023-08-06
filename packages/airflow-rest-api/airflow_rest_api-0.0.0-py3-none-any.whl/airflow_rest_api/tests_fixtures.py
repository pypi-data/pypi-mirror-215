# -*- coding: utf-8 -*-
import os
import pytest
from aiohttp import ClientSession, BasicAuth
from airflow_rest_api.api import AirflowRestApi
from airflow_rest_api.templates import TemplatesRepository

# pytestmark = pytest.mark.asyncio
AIRFLOW_HOST = os.environ.get("AIRFLOW_HOST", "http://127.0.0.1:8080")
AIRFLOW_USER = os.environ.get("AIRFLOW_USER", "admin")
AIRFLOW_PASSWORD = os.environ.get("AIRFLOW_PASSWORD", "admin")


@pytest.fixture
async def client_session():
    auth = BasicAuth(AIRFLOW_USER, AIRFLOW_PASSWORD)
    async with ClientSession(auth=auth) as session:
        yield session


@pytest.fixture
def templates_repository():
    return TemplatesRepository()


@pytest.fixture
def ara():
    return AirflowRestApi(airflow_host=AIRFLOW_HOST)


@pytest.fixture
def default_kw():
    return {
        "airflow_host": AIRFLOW_HOST,
        "airflow_api": "/api/v1",
        "connection_id": "airflow_db",
        "dag_id": "dag_example",
        "task_id": "task_example",
        "dag_run_id": "scheduled__2023-06-25T00:00:00+00:00",
        "event_log_id": 1,
        "import_error_id": 1,
        "pool_name": "default_pool",
        "map_index": -1,
        "variable_key": "example_variable",
        "xcom_key": "example_variable",
        "task_try_number": 0,
        "file_token": "Ii1vcHQvYWlyZmxvdy9kYWdzL1RhZ13leGFtcGxlLnB4Ig.kNJgo7GtCCoF8Y6n_oJfZMyx_zo",
        "uri": "some_uri",
        "role_name": "Admin",
        "username": "admin"
    }
