Settings
========

These are the settings that can be set in the Django project ``settings.py`` file.

.. note::
    Defaults are shown.

.. _show_all_setting:

Set whether an ``All`` option is shown in list in sidebar.

.. code-block:: python

    FILTERVIEW_SHOW_ALL = True

.. _show_unused_setting:

Set whether filters with no matches are shown in sidebar.

.. code-block:: python

    FILTERVIEW_SHOW_UNUSED_FILTERS = True

.. _page_var_setting:

Set parameter in URL for page.

.. code-block:: python
    
    FILTERVIEW_PAGE_VAR = 'page'

.. _search_var_setting:

Set parameter in URL for search.

.. code-block:: python

    FILTERVIEW_SEARCH_VAR = 'search'

.. _error_var_setting:

Set parameter in URL for errors.

.. code-block:: python

    FILTERVIEW_ERROR_VAR = 'error'

.. _extra_ignored_params_setting:

Add extra parameters to be ignored by filtering as a list.

.. code-block:: python

    FILTERVIEW_EXTRA_IGNORED_PARAMS = None

*Example:*

.. code-block:: python

    FILTERVIEW_EXTRA_IGNORED_PARAMS = [
        'foo',
        'bar',
    ]
