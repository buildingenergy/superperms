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

    def setUp(self):
        super(TestDecorators, self).setUp()
        self.fake_org = Organization.objects.create(name='fake org')
        self.fake_member = User.objects.create(
            email='fake_member@asdf.com'
        )
        self.fake_owner = User.objects.create(
            email='fake_owner@asdf.com'
        )
        self.fake_viewer = User.objects.create(
            email='fake_viewer@asdf.com'
        )
        self.fake_owner_org_user = OrganizationUser.objects.create(
            user=self.fake_owner, organization=self.fake_org
        )
        self.fake_member_org_user = OrganizationUser.objects.create(
            user=self.fake_member, organization=self.fake_org
        )
        self.fake_viewer_org_user = OrganizationUser.objects.create(
            user=self.fake_viewer, organization=self.fake_org
        )

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
