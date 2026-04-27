"""Compatibility facade for save-file hex editing.

The legacy implementation still lives in the top-level ``hexedit.py`` module.
New GUI code should import this module instead so the implementation can be
moved behind the logic package incrementally without changing UI call sites.
"""

from hexedit import *  # noqa: F401,F403
