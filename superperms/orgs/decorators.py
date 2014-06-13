import json
from functools import wraps

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


def is_parent_org_owner(org_user):
    """Only allow owners of parent orgs to view child org perms."""
    return (
        org_user.role_level >= ROLE_OWNER and
        not org_user.organization.parent_org
    )


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
            body = json.loads(request.body)
            try:
                org = Organization.objects.get(pk=body.get('organization_id'))
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
