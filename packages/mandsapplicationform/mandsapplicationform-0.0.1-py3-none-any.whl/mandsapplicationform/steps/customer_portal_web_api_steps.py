from pytest_bdd import when, then
from qashared.fixtures import *
from merchantsapi.fixtures import * 
from mandsapplicationform.fixtures import * 
    
@when('I go to the customer portal')
def go_to_portal(customer_portal_token, customer_portal_page: CustomerPortalPage):    
    customer_portal_page.navigate(customer_portal_token)
    customer_portal_page.wait_for_header_text('Overview')

@when('I click the transactions button')
def go_to_transactions(customer_portal_page: CustomerPortalPage):
    customer_portal_page.click_transactions_button()
    customer_portal_page.wait_for_header_text('Transactions')
    
@when('I click the my account button')
def go_to_account(customer_portal_page: CustomerPortalPage):
    customer_portal_page.click_my_account_button()
    customer_portal_page.wait_for_header_text('My Account')
    
@when('I click the payments button')
def go_to_payments(customer_portal_page: CustomerPortalPage):
    customer_portal_page.click_payments_button()
    customer_portal_page.wait_for_header_text('Payments')

@when('I click the statements button')
def go_to_statements(customer_portal_page: CustomerPortalPage):
    customer_portal_page.click_statements_button()
    customer_portal_page.wait_for_header_text('Statements')
    
@then('The payment information is visible')
def payment_info_visible(customer_portal_page: CustomerPortalPage):
    customer_portal_page.wait_for_payment_info_to_be_visible()

@then('The overview is visible')
def payment_info_visible(customer_portal_page: CustomerPortalPage):
    customer_portal_page.wait_for_balances()

@then('The account information is visible')
def payment_info_visible(customer_portal_page: CustomerPortalPage):
    customer_portal_page.wait_for_account_info_to_be_visible()
    
@then('The table data is displayed')
def statements_load(customer_portal_page: CustomerPortalPage):
    customer_portal_page.wait_for_table_data()
