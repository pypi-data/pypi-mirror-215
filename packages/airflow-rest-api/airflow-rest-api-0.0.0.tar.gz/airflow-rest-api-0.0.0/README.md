<p align="center">
    <a href="https://bit.ly/airflow-ra"><img src="https://bit.ly/ara-logo" alt="ARA"></a>
</p>
<p align="center">
    <a href="https://pypi.org/project/airflow-rest-api"><img src="https://img.shields.io/pypi/v/airflow-rest-api.svg?style=flat-square&logo=appveyor" alt="Version"></a>
    <a href="https://pypi.org/project/airflow-rest-api"><img src="https://img.shields.io/pypi/l/airflow-rest-api.svg?style=flat-square&logo=appveyor&color=blueviolet" alt="License"></a>
    <a href="https://pypi.org/project/airflow-rest-api"><img src="https://img.shields.io/pypi/pyversions/airflow-rest-api.svg?style=flat-square&logo=appveyor" alt="Python"></a>
    <a href="https://pypi.org/project/airflow-rest-api"><img src="https://img.shields.io/pypi/status/airflow-rest-api.svg?style=flat-square&logo=appveyor" alt="Status"></a>
    <a href="https://pypi.org/project/airflow-rest-api"><img src="https://img.shields.io/pypi/format/airflow-rest-api.svg?style=flat-square&logo=appveyor&color=yellow" alt="Format"></a>
    <a href="https://pypi.org/project/airflow-rest-api"><img src="https://img.shields.io/pypi/wheel/airflow-rest-api.svg?style=flat-square&logo=appveyor&color=red" alt="Wheel"></a>
    <a href="https://pypi.org/project/airflow-rest-api"><img src="https://img.shields.io/bitbucket/pipelines/deploy-me/airflow-rest-api/master?style=flat-square&logo=appveyor" alt="Build"></a>
    <a href="https://pypi.org/project/airflow-rest-api"><img src="https://bit.ly/ara-cov" alt="Coverage"></a>
    <a href="https://pepy.tech/project/airflow-rest-api"><img src="https://static.pepy.tech/personalized-badge/airflow-rest-api?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" alt="Downloads"></a>
    <br><br><br>
</p>

# AIRFLOW-REST-API

Async wrapper for [Airflow REST API](https://bit.ly/ara-docs). See more in [documentation](https://deploy-me.bitbucket.io/airflow-rest-api/index.html)

## INSTALL

```bash
pip install airflow-rest-api
```

## USAGE

```python
import asyncio
import os
import aiohttp
from airflow_rest_api.api import AirflowRestApi

AIRFLOW_HOST = os.environ.get("AIRFLOW_HOST", "http://127.0.0.1:8080")
AIRFLOW_USER = os.environ.get("AIRFLOW_USER", "admin")
AIRFLOW_PASSWORD = os.environ.get("AIRFLOW_PASSWORD", "admin")


async def main(ara):
    for template in ara.find_template("/dags"):
        template_id = template.id
        break
    auth = aiohttp.BasicAuth(AIRFLOW_USER, AIRFLOW_PASSWORD)
    async with aiohttp.ClientSession(auth=auth) as session:
        airflow_tasks = await ara.execute(session=session, template_id=template_id)
        if airflow_tasks.status == 200:
            file_token = airflow_tasks.raw["dags"][0]["file_token"]
            template_id = 360
            dag_source_code = (
                await ara.execute(
                    session=session,
                    method=ara.get_template(template_id).method,
                    url=ara.render_url(template_id=template_id, file_token=file_token)
                    )
                ).raw
            print(dag_source_code)


ara = AirflowRestApi(airflow_host=AIRFLOW_HOST)
ara.show_templates()

loop = asyncio.get_event_loop()
loop.run_until_complete(main(ara))
```
