# With help from https://stackoverflow.com/questions/6498488/testing-admin-modeladmin-in-django

from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError

from tenant_schemas.test.cases import TenantTestCase
from tenant_schemas.utils import tenant_context

from tenant.models import Tenant
from tenant.admin import TenantAdmin, TenantAdminForm


class NonPublicTenantAdminTest(TenantTestCase):
    """For testing non-public tenants

    TenantTestCase comes with a `self.tenant`
    
    From docs: https://django-tenant-schemas.readthedocs.io/en/latest/test.html
        If you want a test to happen at any of the tenant’s domain, you can use the test case TenantTestCase. 
        It will automatically create a tenant for you, set the connection’s schema to tenant’s schema and 
        make it available at `self.tenant`

    """

    def test_nonpublic_tenant_admin_save_model(self):
        tenant_model_admin = TenantAdmin(model=Tenant, admin_site=AdminSite())

        # Can't create tenant outside the `public` schema. Current schema is `test`, so should throw exception
        with self.assertRaises(Exception):
            tenant_model_admin.save_model(obj=Tenant(), request=None, form=None, change=None)


class PublicTenantTestAdminPublic(TenantTestCase):
    """TenantTestCase comes with a tenant: tenant.test.com"""

    ###############################################################################
    # Not sure why this doesn't work, but seems like TenantTestCase is 
    # stops using the test databse and is looking for the real databse? or something...
    # So it fails on TravisCI where there is no database names `postgress` 
    ###############################################################################
    # fixtures = ['tenant/tenants.json']

    # # This doesn't seem to work when placed in SetUp, so make them class variables.
    # tenant_model_admin = TenantAdmin(model=Tenant, admin_site=AdminSite())
    # public_tenant = Tenant.objects.get(schema_name="public")

    # def test_public_tenant_exists(self):
    #     self.assertIsInstance(self.public_tenant, Tenant)
    #     self.assertEqual(self.public_tenant.domain_url, "localhost")
    #################################################################################

    def setUp(self):
        # create the public schema
        self.public_tenant = Tenant(
            domain_url='localhost',
            schema_name='public',
            name='public'
        )
        self.tenant_model_admin = TenantAdmin(model=Tenant, admin_site=AdminSite())

    def test_public_tenant_admin_save_model(self):

        with tenant_context(self.public_tenant):
            non_public_tenant = Tenant(name="Non-Public")  # Not a valid name, but not validated in this test
            # public tenant should be able to create new tenant/schemas
            self.tenant_model_admin.save_model(obj=non_public_tenant, request=None, form=None, change=None)
            self.assertIsInstance(non_public_tenant, Tenant)
            # schema names should be all lower case and dashes converted to underscores
            self.assertEqual(non_public_tenant.schema_name, "non_public")

        # oddly, seems to switch connections to the newly created "non_public" schema
        # so need to set context back to public to test more stuff
        with tenant_context(self.public_tenant):
            # tenant names with spaces should be rejected:
            with self.assertRaises(ValidationError):
                non_public_tenant_bad_name = Tenant(name="Non Public")
                self.tenant_model_admin.save_model(obj=non_public_tenant_bad_name, request=None, form=None, change=None)
            # also other alpha-numeric characters except dashes and underscores
            with self.assertRaises(ValidationError):
                non_public_tenant_bad_name = Tenant(name="Non*Public")
                self.tenant_model_admin.save_model(obj=non_public_tenant_bad_name, request=None, form=None, change=None)


class TenantAdminFormTest(TenantTestCase):

    def test_public_tenant_not_editable(self):
        form = TenantAdminForm({"name": "public"})
        self.assertFalse(form.is_valid())

    def test_new_non_public_tenant_valid(self):
        form = TenantAdminForm({"name": "non-public"})
        self.assertTrue(form.is_valid())

    def test_existing_non_public_tenant_valid(self):
        """ test tenant already exists as a part of the TenantTestCase """
        form = TenantAdminForm({"name": "test"})
        self.assertTrue(form.is_valid())

    def test_cant_change_existing_name(self):
        # test tenant already exists and is connected in TenantTestCase
        form = TenantAdminForm({"name": "nottest"})
        form.instance = Tenant.get()  # test tenant with schema 'test'
        self.assertFalse(form.is_valid())
