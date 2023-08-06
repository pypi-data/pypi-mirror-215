import pytest
from mandsapplicationform.models.application_form import ApplicationFormPage
from mandsapplicationform.models.customer_portal import CustomerPortalPage
from mandsapplicationform.models.customer_portal_web_api import CustomerPortalWebApi
from qashared.helpers import * 
from playwright.sync_api import Playwright

@pytest.fixture
def application_form_page(page, config, test_data):
    return ApplicationFormPage(page, config.application_form.base_url, test_data.applicant.as_object)

@pytest.fixture
def customer_portal_page(page, config):
    return CustomerPortalPage(page, config.customer_portal_web.base_url)

@pytest.fixture(scope="session")
def customer_portal_token(playwright: Playwright, config):
    api = CustomerPortalWebApi(playwright, config.customer_portal_web)
    return api.tokens.create().token