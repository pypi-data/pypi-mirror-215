import logging
import sys
from pathlib import Path  # , PurePath

from django import setup as django_setup
from django.conf import settings
from django_listview_filters.__init__ import __version__

# from sphinx.util import logging

logger = logging.getLogger(__name__)

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

sys.path.insert(0, str(Path("../").resolve()))

logger.debug(f"Full path: {sys.path}")

settings.configure()

django_setup()

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Django ListView Filters"
copyright = "2023, Karl Wooster"
author = "Karl Wooster"
# release = "0.0.1b0.dev1"
version = __version__
print(f"Version: {version}")
release = version

# rst_epilog = """
# .. |ProjectVersion| replace:: version...{version}
# """.format(version = version)

substitutions = [
    ("|ProjectVersion|", version),
]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "docs.custom_extensions.extensions",
    "sphinx.ext.autosectionlabel",
]

autosectionlabel_prefix_document = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
# html_static_path = ["_static"]
