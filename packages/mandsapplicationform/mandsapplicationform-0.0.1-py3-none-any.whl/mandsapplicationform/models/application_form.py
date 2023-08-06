from playwright.sync_api import expect
from qashared.models.base.ui.page import Page
from qashared.models.base.ui.component import Component

class ApplicationFormPage(Page):
    def __init__(self, page, base_url, applicant):
        super().__init__(page, base_url)
        self.applicant = applicant
        
        self.cookies_accept = page.locator("button.cm-btn-success")
        self.years_dropdown = page.locator("[id='select.addresses.0.months_at_address_years']")
        self.residential_status_dropdown = page.locator("select[aria-labelledby='occupancy_status-label']")
        self.nationality_dropdown = page.locator("select[aria-labelledby='nationality-label']")
        self.employment_status_dropdown = page.locator("select[aria-labelledby='employment_status-label']")
        self.occupation_dropdown = page.locator("select[aria-labelledby='employment_branch-label']")
        self.income_input = page.locator("input[aria-labelledby='income.gross_income-label']")
        self.account_holder_name_input = page.locator("input[aria-labelledby='bank.account_holder_name-label']")
        self.sortcode_input = page.locator("input[aria-labelledby='bank.sort_code-label']")
        self.account_number_input = page.locator("input[aria-labelledby='bank.account_number-label']")
        self.circumstances_radio = page.locator("span[for='radio.change_circumstances-false']")
        self.agreement_checkbox = page.locator("span.chakra-checkbox__control.css-1p5rec5")
        self.veracity_confirm_checkbox = page.locator("span.chakra-checkbox__control.css-1p5rec5")
        self.full_amount_checkbox = page.locator("span[for='radio.minimum_monthly_repayment-false']")
        self.accept_credit_limit_increases_checkbox = page.locator("span[for='radio.apply_credit_limit_increases_automatically-true']")
        self.next_button = page.locator("button.chakra-button.css-itfxvl")
        self.header = page.locator("h1")

    def navigate(self, token):
        self.page.goto(f"{self.base_url}?token={token}")

    def accept_cookies(self):
        self.cookies_accept.click()
        
    def select_years(self):
        self.years_dropdown.select_option(str(self.applicant.years))

    def select_residential_status(self):
        self.residential_status_dropdown.select_option(self.applicant.residential_status)
         
    def select_nationality(self):
        self.nationality_dropdown.select_option(self.applicant.nationality)
   
    def select_employment_status(self):
        self.employment_status_dropdown.select_option(self.applicant.employment_status)
    
    def select_occupation(self):
        self.occupation_dropdown.select_option(self.applicant.occupation)

    def enter_income(self):
        self.income_input.fill(str(self.applicant.income))

    def enter_sortcode(self):
        self.sortcode_input.type(str(self.applicant.sort_code))

    def enter_account_number(self):
        with self.page.expect_response("**/api/validate/bank-account?**"):
            self.account_number_input.type(str(self.applicant.account_number))

    def enter_account_holder_name(self):
        self.account_holder_name_input.type(self.applicant.account_holder_name)

    def choose_circumstance_radio(self):
        self.circumstances_radio.check()

    def accept_agreement(self):
        self.agreement_checkbox.check()

    def choose_repayment(self):
        self.full_amount_checkbox.check()

    def confirm_veracity(self):
        self.veracity_confirm_checkbox.check()

    def choose_credit_increase(self):
        self.accept_credit_limit_increases_checkbox.check()

    def scroll_credit_agreement(self):
        expect(self.agreement_checkbox).to_be_visible(timeout=15000)
        self.page.evaluate("document.querySelector(\"div[aria-label='Credit agreement scroll window'] > iframe\").contentDocument.childNodes[0].scroll(0, 99999)")

    def click_next_button(self, text = ''):
        expect(self.next_button).to_contain_text(text)
        self.next_button.click()
    
    def wait_for_approval(self, message = 'Congratulations'):
        expect(self.header).to_be_visible(timeout=15000)
        expect(self.header).to_contain_text(message)