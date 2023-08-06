from playwright.sync_api import expect
from qashared.models.base.ui.page import Page

class CustomerPortalPage(Page):
    def __init__(self, page, base_url):
        super().__init__(page, base_url)
        
        self.tabs = page.locator('nav.web-tabs')
        self.header = page.locator('div.web-header')
        self.transactions_button = page.get_by_role("button", name="Transactions")
        self.statements_button = page.get_by_role("button", name="Statements")
        self.my_account_button = page.get_by_role("button", name="My Account")
        self.payments_button = page.get_by_role("button", name="Payments")
        self.credit_label = page.locator('span.web-item__label')
        self.account_updates_header = page.get_by_role("heading", name="Account updates")
        self.direct_debit_header = page.get_by_role("heading", name="Direct Debit")
        self.current_balance = page.locator('div.web-item').filter(has_text="Current balance").locator('p')
        self.balance_available = page.locator('div.web-item').filter(has_text="Available to spend").locator('p')
        self.due_payment = page.locator('div.web-item').filter(has_text="Minimum payment due").locator('p')
        self.sparks_pay_balance = page.locator('div.web-item').filter(has_text="Sparks Pay balance").locator('p')
        self.table = page.locator('table.web-table')
        
    def navigate(self, token):
        self.page.goto(f"{self.base_url}?token={token}")
        
    def wait_for_header_text(self, text):
        expect(self.header).to_contain_text(text)
        
    def click_transactions_button(self):
        self.transactions_button.click()
        
    def click_statements_button(self):
        self.statements_button.click()
    
    def click_my_account_button(self):
        self.my_account_button.click()
        
    def click_payments_button(self):
        self.payments_button.click()
        
    def wait_for_account_info_to_be_visible(self):
        expect(self.account_updates_header).to_be_visible()
        
    def wait_for_payment_info_to_be_visible(self):
        expect(self.direct_debit_header).to_be_visible()
        expect(self.due_payment).to_contain_text('£')
        expect(self.sparks_pay_balance).to_contain_text('£')

    def wait_for_balances(self):
        expect(self.current_balance).to_contain_text('£')
        expect(self.balance_available).to_contain_text('£')
        
    def wait_for_table_data(self):
        with self.page.expect_response("**/api/*s"):
            pass
        
        expect(self.table).to_be_visible()
        expect(self.table).not_to_contain_text('unable to display')
        