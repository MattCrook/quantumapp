from .permissions import BasePermission
from .authentication import JSONWebTokenAuthentication
from .blacklist.models import BlacklistedToken
from .compat import gettext_lazy as _


class IsNotBlacklisted(BasePermission):
    message = _('You have been blacklisted.')

    def has_permission(self, request, view):
        return not BlacklistedToken.objects.filter(
            token=JSONWebTokenAuthentication.get_token_from_request(request)
        ).exists()
