"""
Tests for views in the `enterprise_data` module.
"""

import os
from unittest import mock
from uuid import UUID, uuid4

import ddt
from pytest import mark
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase

from enterprise_data.api.v1.serializers import EnterpriseOfferSerializer
from enterprise_data.models import EnterpriseLearnerEnrollment, EnterpriseOffer
from enterprise_data.tests.mixins import JWTTestMixin
from enterprise_data.tests.test_utils import (
    EnterpriseLearnerEnrollmentFactory,
    EnterpriseLearnerFactory,
    EnterpriseOfferFactory,
    UserFactory,
    get_dummy_enterprise_api_data,
)
from enterprise_data_roles.constants import ENTERPRISE_DATA_ADMIN_ROLE
from enterprise_data_roles.models import EnterpriseDataFeatureRole, EnterpriseDataRoleAssignment


@ddt.ddt
@mark.django_db
class TestEnterpriseLearnerEnrollmentViewSet(JWTTestMixin, APITransactionTestCase):
    """
    Tests for EnterpriseLearnerEnrollmentViewSet.
    """

    def setUp(self):
        super().setUp()
        self.user = UserFactory(is_staff=True)
        role, __ = EnterpriseDataFeatureRole.objects.get_or_create(name=ENTERPRISE_DATA_ADMIN_ROLE)
        self.role_assignment = EnterpriseDataRoleAssignment.objects.create(
            role=role,
            user=self.user
        )
        self.client.force_authenticate(user=self.user)

        mocked_get_enterprise_customer = mock.patch(
            'enterprise_data.filters.EnterpriseApiClient.get_enterprise_customer',
            return_value=get_dummy_enterprise_api_data()
        )

        self.mocked_get_enterprise_customer = mocked_get_enterprise_customer.start()
        self.addCleanup(mocked_get_enterprise_customer.stop)
        self.enterprise_id = 'ee5e6b3a-069a-4947-bb8d-d2dbc323396c'
        self.set_jwt_cookie()

    def tearDown(self):
        super().tearDown()
        EnterpriseLearnerEnrollment.objects.all().delete()

    def test_filter_by_offer_id(self):
        enterprise_learner = EnterpriseLearnerFactory(
            enterprise_customer_uuid=self.enterprise_id
        )

        offer_1_id = '1234'
        offer_2_id = '2ThisIsmyOfferId'

        learner_enrollment_1 = EnterpriseLearnerEnrollmentFactory(
            offer_id=offer_1_id,
            enterprise_customer_uuid=self.enterprise_id,
            is_consent_granted=True,
            enterprise_user_id=enterprise_learner.enterprise_user_id
        )
        EnterpriseLearnerEnrollmentFactory(
            offer_id=offer_2_id,
            enterprise_customer_uuid=self.enterprise_id,
            is_consent_granted=True,
            enterprise_user_id=enterprise_learner.enterprise_user_id
        )

        url = reverse('v1:enterprise-learner-enrollment-list', kwargs={'enterprise_id': self.enterprise_id})
        response = self.client.get(url, data={'offer_id': offer_1_id})
        results = response.json()['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['enrollment_id'], learner_enrollment_1.enrollment_id)

    def test_filter_by_ignore_null_course_list_price(self):
        enterprise_learner = EnterpriseLearnerFactory(
            enterprise_customer_uuid=self.enterprise_id
        )

        EnterpriseLearnerEnrollmentFactory(
            course_list_price=None,
            enterprise_customer_uuid=self.enterprise_id,
            is_consent_granted=True,
            enterprise_user_id=enterprise_learner.enterprise_user_id
        )
        learner_enrollment_with_price = EnterpriseLearnerEnrollmentFactory(
            enterprise_customer_uuid=self.enterprise_id,
            is_consent_granted=True,
            enterprise_user_id=enterprise_learner.enterprise_user_id
        )

        url = reverse('v1:enterprise-learner-enrollment-list', kwargs={'enterprise_id': self.enterprise_id})
        response = self.client.get(url, data={'ignore_null_course_list_price': True})
        results = response.json()['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['enrollment_id'], learner_enrollment_with_price.enrollment_id)

    def test_get_course_product_line(self):
        """ Test that the course product line information is returned correctly """
        enterprise_learner = EnterpriseLearnerFactory(
            enterprise_customer_uuid=self.enterprise_id
        )
        learner_enrollment_executive_ed = EnterpriseLearnerEnrollmentFactory(
            enterprise_customer_uuid=self.enterprise_id,
            is_consent_granted=True,
            enterprise_user_id=enterprise_learner.enterprise_user_id,
            course_product_line='Executive Education'
        )
        EnterpriseLearnerEnrollmentFactory(
            enterprise_customer_uuid=self.enterprise_id,
            is_consent_granted=True,
            enterprise_user_id=enterprise_learner.enterprise_user_id,
            course_product_line='OCM'
        )

        url = reverse('v1:enterprise-learner-enrollment-list', kwargs={'enterprise_id': self.enterprise_id})
        response = self.client.get(url, data={'course_product_line': 'Executive Education'})
        results = response.json()['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['enrollment_id'], learner_enrollment_executive_ed.enrollment_id)

    def test_get_subsidy_flag(self):
        """ Test that the subsidy information is returned correctly """
        enterprise_learner = EnterpriseLearnerFactory(
            enterprise_customer_uuid=self.enterprise_id
        )
        learner_enrollment_subsidized = EnterpriseLearnerEnrollmentFactory(
            enterprise_customer_uuid=self.enterprise_id,
            is_consent_granted=True,
            enterprise_user_id=enterprise_learner.enterprise_user_id,
            is_subsidy=True
        )
        EnterpriseLearnerEnrollmentFactory(
            enterprise_customer_uuid=self.enterprise_id,
            is_consent_granted=True,
            enterprise_user_id=enterprise_learner.enterprise_user_id,
            is_subsidy=False
        )

        url = reverse('v1:enterprise-learner-enrollment-list', kwargs={'enterprise_id': self.enterprise_id})
        response = self.client.get(url, data={'is_subsidy': True})
        results = response.json()['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['enrollment_id'], learner_enrollment_subsidized.enrollment_id)


@ddt.ddt
@mark.django_db
class TestEnterpriseOffersViewSet(JWTTestMixin, APITransactionTestCase):
    """
    Tests for EnterpriseOfferViewSet.
    """

    def setUp(self):
        super().setUp()
        self.user = UserFactory(is_staff=True)
        role, __ = EnterpriseDataFeatureRole.objects.get_or_create(name=ENTERPRISE_DATA_ADMIN_ROLE)
        self.role_assignment = EnterpriseDataRoleAssignment.objects.create(
            role=role,
            user=self.user
        )
        self.client.force_authenticate(user=self.user)

        self.enterprise_customer_uuid_1 = uuid4()
        self.enterprise_offer_1_offer_id = str(uuid4())
        self.enterprise_offer_1 = EnterpriseOfferFactory(
            offer_id=self.enterprise_offer_1_offer_id.replace('-', ''),
            enterprise_customer_uuid=self.enterprise_customer_uuid_1
        )

        self.enterprise_customer_2_uuid = uuid4()
        self.enterprise_offer_2_offer_id = '11111'
        self.enterprise_offer_2 = EnterpriseOfferFactory(
            offer_id=self.enterprise_offer_2_offer_id,
            enterprise_customer_uuid=self.enterprise_customer_2_uuid
        )

        self.set_jwt_cookie()

    def tearDown(self):
        super().tearDown()
        EnterpriseOffer.objects.all().delete()

    def test_list_offers(self):
        enterprise_id = self.enterprise_offer_1.enterprise_customer_uuid
        url = reverse(
            'v1:enterprise-offers-list',
            kwargs={'enterprise_id': enterprise_id}
        )

        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        expected_results = [EnterpriseOfferSerializer(self.enterprise_offer_1).data]
        response_json = response.json()
        results = response_json['results']
        assert results == expected_results

    def test_retrieve_offers_uuid(self):
        """
        Make sure that EnterpriseOffer objects that store UUID values inside offer_id return a hyphenated UUID.
        """
        enterprise_id = self.enterprise_offer_1.enterprise_customer_uuid
        url = os.path.join(
            reverse(
                'v1:enterprise-offers-list',
                kwargs={'enterprise_id': enterprise_id}
            ),
            self.enterprise_offer_1_offer_id + "/",
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response_json = response.json()
        results = response_json
        assert results['offer_id'] == str(UUID(self.enterprise_offer_1_offer_id))

    def test_retrieve_offer_offer_id_int(self):
        """
        Make sure that EnterpriseOffer objects that store integer values inside offer_id return the value verbatim.
        """
        enterprise_id = self.enterprise_offer_2.enterprise_customer_uuid
        url = os.path.join(
            reverse(
                'v1:enterprise-offers-list',
                kwargs={'enterprise_id': enterprise_id}
            ),
            self.enterprise_offer_2_offer_id + "/",
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK

        response_json = response.json()
        results = response_json
        assert results['offer_id'] == self.enterprise_offer_2_offer_id
