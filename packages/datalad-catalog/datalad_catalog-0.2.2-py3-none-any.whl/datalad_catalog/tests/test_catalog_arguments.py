import pytest
from datalad.support.exceptions import InsufficientArgumentsError
from datalad.tests.utils_pytest import (
    assert_in_results,
    assert_raises,
)
from datalad_catalog.catalog import Catalog


def test_catalog_no_argument():
    """
    Test if error is raised when no argument is supplied
    """
    ctlg = Catalog()
    assert_raises(TypeError, ctlg)


def test_catalog_wrong_action_argument():
    """
    Test if error is raised when wrong action argument is supplied
    """
    ctlg = Catalog()
    assert_raises(ValueError, ctlg, "wrong_action")


def test_catalog_no_path_argument():
    """
    Test if error is raised when -c/--catalog_dir argument is not supplied
    """
    ctlg = Catalog()
    assert_in_results(
        ctlg("create", on_failure="ignore"),
        action="catalog_create",
        status="impossible",
        message=(
            "Datalad catalog %s requires a path to operate on. "
            "Forgot -c, --catalog_dir?",
            "create",
        ),
        path=None,
    )


def test_catalog_nonexisting_noncreate(tmp_path):
    """
    Test if error is raised when non-create action is used on a non-existing catalog
    """
    catalog_path = tmp_path / "test_catalog"
    ctlg = Catalog()
    assert_in_results(
        ctlg("add", catalog_dir=catalog_path, on_failure="ignore"),
        action="catalog_add",
        status="impossible",
        message=(
            "Catalog does not exist: datalad catalog '%s' can only "
            "operate on an existing catalog, please supply a path "
            "to an existing directory with the catalog argument: "
            "-c, --catalog_dir.",
            "add",
        ),
        path=catalog_path,
    )
