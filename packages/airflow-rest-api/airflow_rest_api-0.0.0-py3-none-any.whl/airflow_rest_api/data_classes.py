# -*- coding: utf-8 -*-
import re
from dataclasses import dataclass, asdict, field
from typing import FrozenSet, Dict, List
from pandas import DataFrame


__all__ = ("Template", "Response")

expr_path_variables = re.compile(r"\{([A-Za-z0-9_]+)\}")


@dataclass
class Template:
    """Data class for template
    """
    id: int
    path: str
    method: str
    description: str
    tag: str
    filter_key: str
    query_params: List
    path_variables: FrozenSet = field(init=False)

    def __post_init__(self):
        """Post init attrs
        """
        self.path_variables = {*expr_path_variables.findall(self.path)}

    def dict(self):
        data = asdict(self)
        del data["tag"], data["filter_key"], data["query_params"], data["path_variables"]
        return data


@dataclass
class Response:
    """Data class wrapper for json response
    """
    status: int
    raw: Dict

    def to_df(self, filter_key=None):
        """Convert dict to dataframe

        Parameters
        ----------
        filter_key : str, optional
            Key from dict for select, by default None

        Returns
        -------
        pandas.core.frame.DataFrame
            Converted dataframe
        """
        if self.raw is None:
            return
        try:
            return DataFrame(self.raw[filter_key] if filter_key else self.raw)
        except (ValueError, KeyError):
            return
