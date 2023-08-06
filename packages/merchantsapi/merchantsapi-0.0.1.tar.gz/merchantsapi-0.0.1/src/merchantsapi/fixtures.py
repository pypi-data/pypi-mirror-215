import pytest
from merchantsapi.models.merchants_api import MerchantsApi
from playwright.sync_api import Playwright
from qashared.models.extensions.divido_simple_namespace import DividoSimpleNamespace
from qashared.helpers import * 


@pytest.fixture
def application_context():
    return DividoSimpleNamespace()

@pytest.fixture
def merchants_api(playwright: Playwright, config):
    return MerchantsApi(playwright, config.merchants_api)