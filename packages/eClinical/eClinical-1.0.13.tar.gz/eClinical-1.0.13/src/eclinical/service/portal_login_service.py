import cjen

from eclinical.environment.environment import Environment
from eclinical.service._login_service import _LoginService


class PortalLoginService(_LoginService):
    @cjen.context.add(content=dict(system="ADMIN"))
    def __init__(self, environment: Environment = None):
        super(PortalLoginService, self).__init__(environment)
        self.auth(data=self.user_pwd())
        self.entry_portal(data=dict(companyId=self.context["workForCompanyId"]))

    @cjen.http.post_mapping(uri="admin/user/entry/portal")
    def entry_portal(self, data ,resp=None, **kwargs): ...
