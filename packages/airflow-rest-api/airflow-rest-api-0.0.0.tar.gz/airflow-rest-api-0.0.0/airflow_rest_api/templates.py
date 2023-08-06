# -*- coding: utf-8 -*-
import re
from pathlib import Path
from types import MappingProxyType

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files

from pandas import read_json

from airflow_rest_api.data_classes import Template
from airflow_rest_api.exceptions import TemplateRenderError
from airflow_rest_api.utils import raise_search_error


class TemplatesRepository:
    """Templates Repository
    """

    def __init__(self):
        """Init params
        """
        self.__df = self.__load_df()
        self._data = self._convert_df2dict(self.__df)

    def __repr__(self):
        """Return templates repository representation

        Returns
        -------
        str
            Templates repository representation
        """
        return f"{self}(ids={self.ids})"

    def __str__(self):
        """Str method

        Returns
        -------
        str
            String representation
        """
        return self.__class__.__name__

    def __iter__(self):
        """Yield templates

        Yields
        ------
        generator
            Tuple of template id and template dataclass
        """
        for t_id, template in self._data.items():
            yield t_id, template

    @staticmethod
    def __load_df(df_path=None):
        """Load json data

        Parameters
        ----------
        df_path : str, optional
            Json path, by default None

        Returns
        -------
        pandas.core.frame.DataFrame
            Loaded dataframe
        """
        if df_path is None:
            try:
                df_path = files("airflow_rest_api") / ".data"
            except ModuleNotFoundError:
                df_path = Path(__file__).parent / ".data"
        with open(df_path, "rb") as f:
            return read_json(f, orient="records", compression="gzip")

    @staticmethod
    def _convert_df2dict(df):
        """Convert dataframe to dict

        Parameters
        ----------
        df : pandas.core.frame.DataFrame
            Dataframe

        Returns
        -------
        types.MappingProxyType
            Template storage
        """
        _data = {}
        tmpl_rows = df.T.to_dict().values()
        for tmpl_row in tmpl_rows:
            tmpl = Template(**tmpl_row)
            _data[tmpl.id] = tmpl
        return MappingProxyType(_data)

    @property
    def df_md(self):
        """Get markdown table

        Returns
        -------
        str
            Markdown table
        """
        return self.__df[
            ["id", "path", "method", "description"]
            ].to_markdown(tablefmt="grid", index=False)

    @df_md.setter
    def df_md(self):
        """Protect access
        """

    @property
    def ids(self):
        """Return set of templates identifieres

        Returns
        -------
        set
            Templates identifieres
        """
        return {i for i, _ in self}

    @raise_search_error
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
        return self._data[template_id]

    def render_template(self, template_id, **template_vars):
        """Render template

        Parameters
        ----------
        template_id : int
            Template's identifier

        Returns
        -------
        str
            Rendered template
        """
        template = self.get_template(template_id)
        diff = template.path_variables.difference({*template_vars.keys()})
        if diff:
            raise TemplateRenderError(','.join(diff), template.path)
        return template.path.format(**template_vars)

    def find_template_id(self, pattern):
        """Find templates by pattern

        Parameters
        ----------
        search_pattern : str
            Regex or usual string

        Yields
        ------
        Template
            Dataclass
        """
        for _, template in self:
            if re.search(pattern, template.path):
                yield template
