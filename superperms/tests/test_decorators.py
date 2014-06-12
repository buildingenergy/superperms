import json

from django.contrib.auth.models import User
from django.utils.unittest import TestCase
from django.http import HttpResponse, HttpResponseBadRequest

from superperms.orgs import decorators
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

#
## Copied wholesale from django-brake's tests
## https://github.com/gmcquillan/django-brake/blob/master/brake/tests/tests.py
###

class FakeRequest(object):
    """A simple request stub."""
    __name__ = 'FakeRequest'
    method = 'POST'
    META = {'REMOTE_ADDR': '127.0.0.1'}
    path = 'fake_login_path'
    body = None

    def __init__(self, headers=None):
        if headers:
            self.META.update(headers)


class FakeClient(object):
    """An extremely light-weight test client."""

    def _gen_req(self, view_func, data, headers, method='POST', **kwargs):
        request = FakeRequest(headers)
        if 'user' in kwargs:
            request.user = kwargs.get('user')
        if callable(view_func):
            setattr(request, method, data)
            request.body = json.dumps(data)
            return view_func(request)

        return request

    def get(self, view_func, data, headers=None, **kwargs):
        return self._gen_req(view_func, data, headers, method='GET', **kwargs)

    def post(self, view_func, data, headers=None, **kwargs):
        return self._gen_req(view_func, data, headers, **kwargs)


#
## These are test functions wrapped in decorators.
###

@decorators.has_perm('derp')
def _fake_view_no_perm_name(request):
    return HttpResponse()


@decorators.has_perm('can_invite_member')
def _fake_invite_user(request):
    return HttpResponse()


class TestDecorators(TestCase):

    def setUp(self):
        super(TestDecorators, self).setUp()
        self.client = FakeClient()
        self.fake_org = Organization.objects.create(name='fake org')
        self.fake_member = User.objects.create(
            username='fake_member',
            email='fake_member@asdf.com'
        )
        self.fake_owner = User.objects.create(
            username='fake_owner',
            email='fake_owner@asdf.com'
        )
        self.fake_viewer = User.objects.create(
            username='fake_viewer',
            email='fake_viewer@asdf.com'
        )
        self.fake_owner_org_user = OrganizationUser.objects.create(
            user=self.fake_owner,
            organization=self.fake_org,
            role_level=ROLE_OWNER
        )
        self.fake_member_org_user = OrganizationUser.objects.create(
            user=self.fake_member,
            organization=self.fake_org,
            role_level=ROLE_MEMBER
        )
        self.fake_viewer_org_user = OrganizationUser.objects.create(
            user=self.fake_viewer,
            organization=self.fake_org,
            role_level=ROLE_VIEWER
        )

    def tearDown(self):
        """WTF DJANGO."""
        User.objects.all().delete()
        Organization.objects.all().delete()
        OrganizationUser.objects.all().delete()
        super(TestDecorators, self).tearDown()
    #
    ## Test has_perm in various permutations.
    ###

    def test_has_perm_w_no_org(self):
        """We should return BadRequest if there's no org."""
        self.client.user = User.objects.create(username='f', email='d@d.com')
        resp = self.client.post(
            _fake_view_no_perm_name,
            {'organization_id': 0},
            user=self.client.user
        )

        self.assertEqual(resp.__class__, HttpResponseBadRequest)

    def test_has_perm_user_not_in_org(self):
        """We should reject requests from a user not in this org."""
        self.client.user = User.objects.create(username='f', email='d@d.com')
        self.assertRaises(
            UserNotInOrganization,
            self.client.post,
            _fake_view_no_perm_name,
            {'organization_id': self.fake_org.pk},
            user=self.client.user
        )

    def test_has_perm_w_no_perm_name(self):
        """Default to false if an undefined perm is spec'ed"""
        self.client.user = self.fake_member
        self.assertRaises(
            InsufficientPermission,
            self.client.post,
            _fake_view_no_perm_name,
            {'organization_id': self.fake_org.pk},
            user=self.fake_member
        )

    def test_has_perm_good_case(self):
        """Test that we actually allow people through."""
        self.client.user = self.fake_owner
        resp = self.client.post(
            _fake_invite_user,
            {'organization_id': self.fake_org.pk},
            user = self.fake_owner
        )

        self.assertEqual(resp.__class__, HttpResponse)

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
