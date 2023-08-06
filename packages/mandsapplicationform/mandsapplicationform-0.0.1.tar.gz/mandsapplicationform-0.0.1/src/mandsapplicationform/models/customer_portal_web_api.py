from qashared.models.base.api.api import Api
from qashared.models.base.api.route import Route
from qashared.models.extensions.divido_simple_namespace import DividoSimpleNamespace


class CustomerPortalWebApi(Api):
    def __init__(self, playwright, config: DividoSimpleNamespace):
        config.verify_attributes(['base_url', 'api_key', 'account_number'], 'CustomerPortalWebApi config was missing the following required attributes')
        super().__init__(base_url=config.base_url, headers={"X-DIVIDO-API-KEY": config.api_key})

        self.context = next(self.get_context(playwright))
        self.account_number = config.account_number
        self.tokens = TokensRoute(self.context, self.account_number)

class TokensRoute(Route):
    def __init__(self, context, account_number):
        self.context = context
        self.account_number = account_number
        self.required_attributes = ['token']
 
    def create(self) -> DividoSimpleNamespace:
        return self.send_request(self.context.post, "/api/generate-token", data={'account_number': self.account_number})
    