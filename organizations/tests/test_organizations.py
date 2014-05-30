from django.contrib.auth.models import User
from django.utils.unittest import TestCase

from organizations.exceptions import TooManyNestedOrgs
from organizations.models import (
    ROLE_VIEWER,
    ROLE_MEMBER,
    ROLE_OWNER,
    STATUS_PENDING,
    STATUS_ACCEPTED,
    STATUS_REJECTED,
    ExportableField,
    Organization,
    OrganizationUser,
)

class TestOrganization(TestCase):

    def setUp(self, *args, **kwargs):
        self.user = User.objects.create(email='asdf@asdf.com')
        super(TestOrganization, self).setUp(*args, **kwargs)

    def tearDown(self, *args, **kwargs):
        """WTF Django test case?"""
        User.objects.all().delete()
        OrganizationUser.objects.all().delete()
        Organization.objects.all().delete()
        ExportableField.objects.all().delete()
        super(TestOrganization, self).tearDown(*args, **kwargs)

    def test_add_user_to_org(self):
        """Test that a user is associated with an org using through table."""
        org = Organization.objects.create()

        # Ensure we don't have any users associated yet.
        self.assertEqual(org.users.all().count(), 0)

        # Just link a user and an org, leave defaults
        org_user = OrganizationUser.objects.create(
            user=self.user, organization=org
        )

        self.assertEqual(org_user.role_level, ROLE_VIEWER) # Default
        self.assertEqual(org_user.status, STATUS_PENDING)

        self.assertEqual(
            org.users.all()[0], self.user
        )

    def test_exportable_fields(self):
        """We can set a list of fields to be exportable for an org."""
        org = Organization.objects.create()
        exportable_fields = [
            ExportableField.objects.create(
                name='test-{0}'.format(x),
                organization=org,
                field_model='FakeModel'
            ) for x in range(10)
        ]

        self.assertListEqual(
            list(org.exportable_fields.all()), exportable_fields
        )

    def test_one_level_org_nesting(self):
        """Make sure we can save one level of organization."""
        parent_org = Organization.objects.create(name='Big Daddy')
        child_org = Organization.objects.create(name='Little Sister')

        parent_org.child_org = child_org
        parent_org.save()

        refreshed_parent = Organization.objects.get(pk=parent_org.pk)
        refreshed_child = Organization.objects.get(pk=child_org.pk)
        self.assertEqual(refreshed_parent.child_org, refreshed_child)
        self.assertEqual(refreshed_child.parent_org.all()[0], refreshed_parent)

    def test_multi_level_org_nesting(self):
        """Make sure we raise exception if a child tries to make a child."""
        parent_org = Organization.objects.create(name='Big Daddy')
        child_org = Organization.objects.create(name='Little Sister')
        baby_org = Organization.objects.create(name='Baby Sister')

        parent_org.child_org = child_org
        parent_org.save()

        child_org.child_org = baby_org # Double nesting
        self.assertRaises(TooManyNestedOrgs, child_org.save)


    def test_get_exportable_fields(self):
        """Make sure we use parent exportable_fields."""
        parent_org = Organization.objects.create(name='Parent')
        parent_fields = [
            ExportableField.objects.create(
                name='parent-{0}'.format(x),
                organization=parent_org,
                field_model='FakeModel'
            ) for x in range(10)
        ]

        child_org = Organization.objects.create(name='Child')
        child_fields = [
            ExportableField.objects.create(
                name='child-{0}'.format(x),
                organization=child_org,
                field_model='FakeModel'
            ) for x in range(10)
        ]

        self.assertListEqual(
            list(child_org.get_exportable_fields()), child_fields
        )

        parent_org.child_org = child_org
        parent_org.save()

        self.assertListEqual(
            list(child_org.get_exportable_fields()), parent_fields
        )

    def test_get_query_threshold(self):
        """Make sure we use the parent's query threshold."""
        parent_org = Organization.objects.create(
            name='Parent', query_threshold=10
        )

        child_org = Organization.objects.create(
            name='Child', query_threshold=9
        )

        self.assertEqual(child_org.get_query_threshold(), 9)

        parent_org.child_org = child_org
        parent_org.save()

        self.assertEqual(child_org.get_query_threshold(), 10)
