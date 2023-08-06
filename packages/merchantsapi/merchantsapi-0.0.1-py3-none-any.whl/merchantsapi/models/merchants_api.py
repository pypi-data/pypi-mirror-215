from qashared.models.base.api.api import Api
from qashared.models.base.api.route import Route
from qashared.models.extensions.divido_simple_namespace import DividoSimpleNamespace


class MerchantsApi(Api):
    def __init__(self, playwright, config: DividoSimpleNamespace):
        config.verify_attributes(['base_url', 'api_key'], 'MerchantsApi config was missing the following required attributes')
        super().__init__(base_url=config.base_url, headers={"X-DIVIDO-API-KEY": config.api_key})

        self.context = next(self.get_context(playwright))
        self.applications = ApplicationsRoute(self.context)

class ApplicationsRoute(Route):
    def __init__(self, context):
        self.context = context
        self.required_attributes = ['data', 'data.id', 'data.token', 'data.current_status']
 
    def create(self, application) -> DividoSimpleNamespace:
        return self.send_request(self.context.post, "/applications", data=application)

    def get(self, id) -> DividoSimpleNamespace:
        return self.send_request(self.context.get, f"/applications/{id}")
    