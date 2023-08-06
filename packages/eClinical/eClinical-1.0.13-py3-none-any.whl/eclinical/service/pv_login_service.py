
import cjen

from eclinical.environment.environment import Environment
from eclinical.service._sponsor_login_service import _SponsorLoginService


class PVLoginService(_SponsorLoginService):
    @cjen.context.add(content=dict(system="PV"))
    def __init__(self, environment: Environment = None):
        super().__init__(environment)
        self.sponsor_auth()

    @cjen.http.post_mapping(uri="pv/auth")
    @cjen.jwt(key="Authorization", json_path="$.payload.token")
    def sponsor_auth(self, resp=None, **kwargs):
        ...