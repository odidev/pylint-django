"""Common Django module."""
import re
from pylint.checkers.base import NameChecker
from pylint.checkers.variables import VariablesChecker
from pylint_plugin_utils import get_checker

from pylint_django.checkers import register_checkers

# we want to import the transforms to make sure they get added to the astroid manager,
# however we don't actually access them directly, so we'll disable the warning
from pylint_django import transforms  # noqa, pylint: disable=unused-import
from pylint_django import compat


def load_configuration(linter):
    """
    Amend existing checker config.
    """
    name_checker = get_checker(linter, NameChecker)
    name_checker.config.good_names += ('qs', 'urlpatterns', 'register', 'app_name', 'handler500')

    # We want to ignore the unused-argument warning for arguments named `request`. The signature of Django view
    # functions require the request argument but it is okay if the request is not used in the function.
    # https://github.com/PyCQA/pylint-django/issues/155
    variables_checker = get_checker(linter, VariablesChecker)
    old_ignored_argument_names_pattern = variables_checker.config.ignored_argument_names.pattern
    new_ignored_argument_names_pattern = "request"
    if old_ignored_argument_names_pattern:
        new_ignored_argument_names_pattern = old_ignored_argument_names_pattern + "|request"

    variables_checker.config.ignored_argument_names = re.compile(new_ignored_argument_names_pattern)

    # we don't care about South migrations
    linter.config.black_list += ('migrations', 'south_migrations')


def register(linter):
    """
    Registering additional checkers.
    """
    # add all of the checkers
    register_checkers(linter)

    # register any checking fiddlers
    try:
        # pylint: disable=import-outside-toplevel
        from pylint_django.augmentations import apply_augmentations
        apply_augmentations(linter)
    except ImportError:
        # probably trying to execute pylint_django when Django isn't installed
        # in this case the django-not-installed checker will kick-in
        pass

    if not compat.LOAD_CONFIGURATION_SUPPORTED:
        load_configuration(linter)
