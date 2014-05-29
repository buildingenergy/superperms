from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)


# Role Levels
ROLE_VIEWER = 0
ROLE_MEMBER = 10
ROLE_OWNER  = 20

ROLE_LEVEL_CHOICES = (
    (ROLE_VIEWER, 'Viewer'),
    (ROLE_MEMBER, 'Member'),
    (ROLE_OWNER, 'Owner'),
)


# Invite status
STATUS_PENDING  = 'pending'
STATUS_ACCEPTED = 'accepted'
STATUS_REJECTED = 'rejected'

STATUS_CHOICES = (
    (STATUS_PENDING, 'Pending'),
    (STATUS_ACCEPTED, 'Accepted'),
    (STATUS_REJECTED, 'Rejected'),
)


class ExportableField(models.Model):
    """Tracks which model fields are exportable."""
    class Meta:
        unique_together = ('field_model', 'name', 'organization')
        ordering = ['organization', 'name']

    # For relating to the model-type whose fields we're exporting.
    field_model = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    organization = models.ForeignKey('Organization')


class OrganizationUser(models.Model):
    class Meta:
        ordering = ['organization', '-role_level']

    user = models.ForeignKey(USER_MODEL)
    organization = models.ForeignKey('Organization')
    status = models.CharField(default=STATUS_PENDING, choices=STATUS_CHOICES)
    role_level = models.IntegerField(
        default=ROLE_VIEWER, choices=ROLE_LEVEL_CHOICES
    )


class Organization(models.Model):
    """A group of people that optionally contains another sub group."""
    class Meta:
        ordering = ['name']

    users = models.ManyToManyField(
        USER_MODEL,
        through=OrganizationUser,
        related_name='organizations'
    )
        
    child_org = models.ForeignKey(
        'Organization', blank=True, null=True, related_name='parent_org'
    )
    exportable_fields = models.ManyToManyField(
        'ExportableField', blank=True, null=True
    )

    # If below this threshold, we don't show results from this Org
    # in exported views of its data.
    query_threshold = models.IntegerField(max_length=4, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Perform checks before saving."""
        # There can only be one.
        if self.self.parent_org and self.child_org:
            raise TooManyNestedSeedOrgs

        super(Organization, self).save(*args, **kwargs)

    def get_exportable_fields(self):
        """Default to parent definition of exportable fields."""
        if self.parent_org is not None:
            return self.parent_org.exportable_fields.all()
        return self.exportable_fields.all()


    def get_query_threshold(self):
        """Default to parent definition of query threshold."""
        if self.parent_org is not None:
            return self.parent_org.query_threshold
        return self.query_threshold

    @property
    def is_parent(self):
        return self.child_org is not None
