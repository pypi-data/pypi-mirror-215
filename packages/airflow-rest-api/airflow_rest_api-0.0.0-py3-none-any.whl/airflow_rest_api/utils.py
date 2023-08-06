# -*- coding: utf-8 -*-
from functools import wraps
from airflow_rest_api.exceptions import TemplateSearchError


def raise_search_error(func):
    """Decorate funcion

    Parameters
    ----------
    func : function
        Wrapped function

    Returns
    -------
    function
        Function wrapper

    Raises
    ------
    TemplateSearchError
        Template's id doesn't exist
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Raise error if didn't find template's id in repository

        Returns
        -------
        Anu
            Function result

        Raises
        ------
        TemplateSearchError
            Template's id doesn't exist
        """
        try:
            return func(*args, **kwargs)
        except KeyError as exc:
            raise TemplateSearchError(exc) from exc
    return wrapper
