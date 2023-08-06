from pytest_bdd import when
from qashared.fixtures import *
from merchantsapi.fixtures import * 
from mandsapplicationform.fixtures import * 

@when('I complete the application')
def complete_application(application_form_page: ApplicationFormPage, application_context: DividoSimpleNamespace):    
    application_form_page.navigate(application_context.application.data.token)
    application_form_page.select_years()
    application_form_page.select_residential_status()
    application_form_page.select_nationality()
    application_form_page.click_next_button()

    application_form_page.select_employment_status()
    application_form_page.select_occupation()
    application_form_page.enter_income()
    application_form_page.choose_circumstance_radio()
    application_form_page.click_next_button()

    application_form_page.enter_account_holder_name()
    application_form_page.enter_sortcode()
    application_form_page.enter_account_number()
    application_form_page.click_next_button()

    application_form_page.click_next_button("Review & submit")

    application_form_page.wait_for_approval()
    application_form_page.click_next_button()

    application_form_page.click_next_button()

    application_form_page.scroll_credit_agreement()
    application_form_page.accept_agreement()
    application_form_page.click_next_button()

    application_form_page.choose_repayment()
    application_form_page.confirm_veracity()
    application_form_page.click_next_button()

    application_form_page.choose_credit_increase()
    application_form_page.click_next_button()
    application_form_page.wait_for_approval("Congratulations! Welcome to Sparks Pay")
