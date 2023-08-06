import importlib
import pytest


class TestImport:
    """Double check that this package is importable."""
    def test_import_root_package(self):
        assert importlib.import_module("merchantsapi")

    @pytest.mark.parametrize(
        "sub_module", (
            # FIXME: Change to dynamically pull in sub-modules.
            "steps",
            "fixtures",
            "models",
        )
    )
    def test_import_sub_modules(self, sub_module):
        assert importlib.import_module(f"merchantsapi.{sub_module}")