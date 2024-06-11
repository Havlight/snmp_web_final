from ninja_extra import api_controller, route
from django.contrib import auth
from ninja import Schema


class InUSerSchema(Schema):
    username: str
    password: str


@api_controller('/accounts', auth=None, tags=['accounts'])
class Accounts:
    @route.post('/login')
    def user_login(self, request, data: InUSerSchema):
        user = auth.authenticate(username=data.username, password=data.password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return 200, {"meaasge": "login success"}
        else:
            return 404, {"message": "login fail"}

    @route.get('/logout')
    def user_logout(self, request):
        auth.logout(request)
        return 200
