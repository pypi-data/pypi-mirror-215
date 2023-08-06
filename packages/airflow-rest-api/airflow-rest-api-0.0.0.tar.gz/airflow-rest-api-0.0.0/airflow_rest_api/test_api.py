# -*- coding: utf-8 -*-
import os
from collections import Counter
from asyncio import gather
import pytest
from airflow_rest_api.tests_fixtures import client_session, templates_repository, ara, default_kw


def test_load(ara):
    assert len(ara.templates) > 0


def test_show_templates(ara):
    errors = ara.show_templates()
    assert errors is None


@pytest.mark.asyncio
async def test_http_methods(ara, client_session):
    df = (
        await ara.execute(
            session=client_session,
            template_id=0,
            **{"params": {"limit": 10}}
        )
    ).to_df("connections")
    assert df.shape[0] == 10

    payload = {"connection_id": "0", "conn_type": "0", "description": "0", "host": "0",
               "login": "0", "schema": "0", "port": 0, "password": "pa$$word", "extra": "0"}
    data = (
        await ara.execute(
            session=client_session,
            template_id=1,
            **{"json": payload}
        )
    )
    assert {**payload, **data.raw} == payload, data

    payload_new = {"description": "1", "schema": "1"}
    data = (
        await ara.execute(
            session=client_session,
            method=ara.get_template(11).method,
            url=ara.render_url(template_id=11, connection_id="0"),
            **{"json": payload_new, "params": {"update_mask": ",".join(payload_new.keys())}}
        )
    )
    assert {**payload, **data.raw} == {**payload, **payload_new}, data

    data = (
        await ara.execute(
            session=client_session,
            method=ara.get_template(12).method,
            url=ara.render_url(template_id=12, connection_id="0")
        )
    )
    assert data.status == 204, data


@pytest.mark.asyncio
async def test_brute_force_get(ara, client_session, templates_repository, default_kw):
    tasks = []
    for _id in templates_repository.ids:
        tmpl = templates_repository.get_template(_id)
        if tmpl.method == "GET":
            tasks.append(
                ara.execute(
                    session=client_session,
                    method=tmpl.method,
                    url=ara.render_url(template_id=_id, **default_kw)
                )
            )
    c = Counter(map(lambda resp: resp.status, (await gather(*tasks))))
    assert c == Counter({200: 35, 404: 5, 403: 1})
