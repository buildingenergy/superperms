from django.contrib.auth.models import User
from django.utils.unittest import TestCase

from superperms.orgs.exceptions import (
    UserNotInOrganization, InsufficientPermission 
)
from superperms.orgs.models import (
    ROLE_VIEWER,
    ROLE_MEMBER,
    ROLE_OWNER,
    Organization,
    OrganizationUser,
)

class TestDecorators(TestCase):

    #
    ## Test has_perm in various permutations.
    ###

    def test_has_perm_w_no_perm_name(self):
        """Default to false if an undefined perm is spec'ed"""
        pass

    #
    ## Test boolean functions for permission logic. 
    ###

    def test_can_remove_org(self):
        pass

    def test_can_create_sub_org(self):
        pass

    def test_can_invite_member(self):
        pass

    def test_can_remove_member(self):
        pass

    def test_can_modify_query_threshold(self):
        pass

    def test_can_view_sub_org_settings(self):
        pass

    def test_can_view_sub_org_fields(self):
        pass
