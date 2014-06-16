import json
from functools import wraps

from django.conf import settings
from django.http import HttpResponseBadRequest

from superperms.orgs.exceptions import (
    InsufficientPermission, UserNotInOrganization
)
from superperms.orgs.models import (
    ROLE_OWNER,
    ROLE_MEMBER,
    ROLE_VIEWER,
    Organization,
    OrganizationUser
)


# Allow Super Users to ignore permissions.
ALLOW_SUPER_USER_PERMS = getattr(settings, 'ALLOW_SUPER_USER_PERMS', True)


def is_parent_org_owner(org_user):
    """Only allow owners of parent orgs to view child org perms."""
    return (
        org_user.role_level >= ROLE_OWNER and
        not org_user.organization.parent_org
    )


def is_owner(org_user):
    """Owners, and only owners have owner perms."""
    return org_user.role_level >= ROLE_OWNER


def is_member(org_user):
    """Members and owners are considered to have member perms."""
    return org_user.role_level >= ROLE_MEMBER


def is_viewer(org_user):
    """Everybody is considered to have viewer perms."""
    return org_user.role_level >= ROLE_VIEWER


def can_create_sub_org(org_user):
    return is_parent_org_owner(org_user)


def can_remove_org(org_user):
    return is_parent_org_owner(org_user)


def can_invite_member(org_user):
    return org_user.role_level >= ROLE_OWNER


def can_remove_member(org_user):
    return org_user.role_level >= ROLE_OWNER


def can_modify_query_thresh(org_user):
    return is_parent_org_owner(org_user)


def can_view_sub_org_settings(org_user):
    return org_user.role_level >= ROLE_OWNER


def can_view_sub_org_fields(org_user):
    return is_parent_org_owner(org_user)


def can_modify_data(org_user):
    return org_user.role_level >= ROLE_MEMBER


def can_view_data(org_user):
    return org_user.role_level >= ROLE_VIEWER


PERMS = {
    'is_parent_org_owner': is_parent_org_owner,
    'is_owner': is_owner,
    'is_member': is_member,
    'is_viewer': is_viewer,
    'can_create_sub_org': can_create_sub_org,
    'can_remove_org': can_remove_org,
    'can_invite_member': can_invite_member,
    'can_remove_member': can_remove_member,
    'can_modify_query_thresh': can_modify_query_thresh,
    'can_view_sub_org_settings': can_view_sub_org_settings,
    'can_view_sub_org_fields': can_view_sub_org_fields,
    'can_modify_data': can_modify_data,
    'can_view_data': can_view_data
}


def has_perm(perm_name):
    """Proceed if user from request has ``perm_name``."""
    def decorator(fn):
        @wraps(fn)
        def _wrapped(request, *args, **kwargs):
            # Skip perms checks if settings allow super_users to bypass.
            if request.user.is_superuser and ALLOW_SUPER_USER_PERMS:
                return fn(request, *args, **kwargs)

            # Extract the org_id
            if request.method in ['GET' or 'DELETE']:
                org_id = request.GET.get('organization_id')
            else:
                org_id = json.loads(request.body).get('organization_id')

            try:
                org = Organization.objects.get(pk=org_id)
            except Organization.DoesNotExist:

                return HttpResponseBadRequest()

            try:
                org_user = OrganizationUser.objects.get(
                    user=request.user, organization=org
                )
            except OrganizationUser.DoesNotExist:
                raise UserNotInOrganization

            if not PERMS.get(perm_name, lambda x: False)(org_user):
                raise InsufficientPermission

            # Logic to see if person has permission required.
            return fn(request, *args, **kwargs)

        return _wrapped

    return decorator
