# -*- coding: utf-8 -*-
from json.decoder import JSONDecodeError
from aiohttp.client_exceptions import ContentTypeError

from airflow_rest_api.data_classes import Response
from airflow_rest_api.templates import TemplatesRepository


__all__ = ("AirflowRestApi", )


class AirflowRestApi:
    """API interface for Airflow REST API
    """

    def __init__(self, airflow_host, airflow_api="/api/v1"):
        """Init params

        Parameters
        ----------
        airflow_host : str
            Airflow host
        airflow_api : str, optional
            Airflow api path, by default "/api/v1"
        """
        self.__templates_repository = TemplatesRepository()
        self.default_kwargs = {
            "airflow_host": airflow_host, "airflow_api": airflow_api}

    def __repr__(self):
        """Return AirflowRestApi representation

        Returns
        -------
        str
            AirflowRestApi representation
        """
        return f"{self}(templates={self.templates})"

    def __str__(self):
        """Str method

        Returns
        -------
        str
            String representation
        """
        return self.__class__.__name__

    @property
    def templates(self):
        """Return set of templates identifieres

        Returns
        -------
        set
            Templates identifieres
        """
        return self.__templates_repository.ids

    def render_url(self, template_id, **template_vars):
        """Render url

        Parameters
        ----------
        template_id : int
            Template's identifier

        Returns
        -------
        str
            Rendered url
        """
        return self.__templates_repository.render_template(
            template_id, **{**self.default_kwargs, **template_vars}
            )

    def find_template(self, search_pattern):
        """Find templates by pattern

        Parameters
        ----------
        search_pattern : str
            Regex or usual string

        Returns
        -------
        generator
            Templates generator
        """
        return self.__templates_repository.find_template_id(search_pattern)

    def get_template(self, template_id):
        """Get template by template identifier

        Parameters
        ----------
        template_id : int
            Template's identifier

        Returns
        -------
        Template
            Template dataclass
        """
        return self.__templates_repository.get_template(template_id)

    def get_template_default_method(self, template_id):
        """Get template's HTTP method

        Parameters
        ----------
        template_id : int
            Template's identifier

        Returns
        -------
        str
            HTTP method
        """
        return self.__templates_repository.get_template(template_id).methods[0]

    def show_templates(self):
        """Print markdown table with templates
        """
        print(self.__templates_repository.df_md)

    async def execute(self, session, url=None, method=None, template_id=None, **kwargs):
        """Call requested uri

        Parameters
        ----------
        session : aiohttp.ClientSession
            Client session
        url : str, optional
            Api url, by default None
        method : str, optional
            HTTP method, by default None
        template_id : int, optional
            Template's identifier, by default None

        Returns
        -------
        airflow_rest_api.data_classes.Response
            Dataclass instance
        """
        if url is None:
            url = self.render_url(template_id=template_id)
        if method is None:
            method = self.get_template(template_id).method
        async with session.request(method, url, **kwargs) as resp:
            status = resp.status
            try:
                raw = await resp.json()
            except (ContentTypeError, JSONDecodeError):
                raw = await resp.text()
            return Response(status=status, raw=raw)
