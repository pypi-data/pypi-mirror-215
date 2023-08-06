# -*- coding: utf-8 -*-
import pytest
from pandas import DataFrame
from airflow_rest_api.data_classes import Response


@pytest.fixture
def resp_empty():
    return Response(status=0, raw=None)


@pytest.fixture
def resp_not_empty():
    return Response(
        status=0,
        raw={"some_key": {"columns": ["some_column"], "data": [["some_value"]]}}
        )


def test_resp_empty_to_df(resp_empty):
    assert resp_empty.to_df() is None
    assert resp_empty.to_df("some_key") is None


def test_resp_not_empty_to_df(resp_not_empty):
    assert isinstance(resp_not_empty.to_df(), DataFrame)
    assert resp_not_empty.to_df("some_key_not_exists") is None
