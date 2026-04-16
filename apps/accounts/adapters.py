from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):
    role_redirect_map = {
        "citizen": "reports:index",
        "seller": "suppliers:index",
        "collector": "missions:index",
        "center": "sorting_center:index",
        "buyer": "buyers:index",
        "partner": "partners:index",
        "admin": "dashboard:index",
    }

    def get_login_redirect_url(self, request):
        user = request.user
        role = getattr(user, "role", "")
        return self.get_url(self.role_redirect_map.get(role, "accounts:profile"))
