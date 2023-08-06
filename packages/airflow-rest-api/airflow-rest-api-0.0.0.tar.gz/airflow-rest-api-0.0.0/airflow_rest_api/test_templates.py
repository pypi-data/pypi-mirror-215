# -*- coding: utf-8 -*-
from types import MappingProxyType
import pytest

from airflow_rest_api.data_classes import Template
from airflow_rest_api.exceptions import TemplateSearchError, TemplateRenderError
from airflow_rest_api.tests_fixtures import templates_repository


@pytest.fixture
def bad_id():
    return 2023


@pytest.fixture
def good_id():
    return 0


def test_load_data(templates_repository):
    assert isinstance(templates_repository._data, MappingProxyType)
    assert len(templates_repository.ids) > 0


def test_df_md(templates_repository):
    assert isinstance(templates_repository.df_md, str)
    assert len(templates_repository.df_md) > 0


def test_get_template(templates_repository):
    template = templates_repository.get_template(10)
    assert isinstance(template, Template)


def test_get_template_bad_id(templates_repository, bad_id):
    with pytest.raises(TemplateSearchError):
        templates_repository.get_template(bad_id)


def test_render_template(templates_repository, good_id):
    url = templates_repository.render_template(
        good_id, airflow_host="http://airflow.ru", airflow_api="/api/v1")
    assert url == "http://airflow.ru/api/v1/connections", url


def test_render_template_bad_id(templates_repository, bad_id):
    with pytest.raises(TemplateSearchError):
        templates_repository.render_template(bad_id, some_arg="some_value")


def test_render_template_without_vars(templates_repository, good_id):
    with pytest.raises(TemplateRenderError):
        templates_repository.render_template(good_id)


def test_find_template_not_exist(templates_repository):
    with pytest.raises(StopIteration):
        next(templates_repository.find_template_id("/SOME-VALUE"))


def test_find_template_id(templates_repository):
    template = templates_repository.find_template_id("/dags/")
    assert next(template) is not None
