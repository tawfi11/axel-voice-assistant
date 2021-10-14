# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from tests import IntegrationTestCase
from tests.holodeck import Request
from twilio.base.exceptions import TwilioException
from twilio.http.response import Response


class BrandRegistrationTestCase(IntegrationTestCase):

    def test_fetch_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.messaging.v1.brand_registrations("BNXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").fetch()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://messaging.twilio.com/v1/a2p/BrandRegistrations/BNXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        ))

    def test_fetch_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "sid": "BN0044409f7e067e279523808d267e2d85",
                "account_sid": "AC78e8e67fc0246521490fb9907fd0c165",
                "customer_profile_bundle_sid": "BU3344409f7e067e279523808d267e2d85",
                "a2p_profile_bundle_sid": "BU3344409f7e067e279523808d267e2d85",
                "date_created": "2021-01-27T14:18:35Z",
                "date_updated": "2021-01-27T14:18:36Z",
                "status": "PENDING",
                "tcr_id": "BXXXXXX",
                "failure_reason": "Registration error",
                "url": "https://messaging.twilio.com/v1/a2p/BrandRegistrations/BN0044409f7e067e279523808d267e2d85",
                "brand_score": 42
            }
            '''
        ))

        actual = self.client.messaging.v1.brand_registrations("BNXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").fetch()

        self.assertIsNotNone(actual)

    def test_list_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.messaging.v1.brand_registrations.list()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://messaging.twilio.com/v1/a2p/BrandRegistrations',
        ))

    def test_read_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "meta": {
                    "page": 0,
                    "page_size": 50,
                    "first_page_url": "https://messaging.twilio.com/v1/a2p/BrandRegistrations?PageSize=50&Page=0",
                    "previous_page_url": null,
                    "next_page_url": null,
                    "key": "data",
                    "url": "https://messaging.twilio.com/v1/a2p/BrandRegistrations?PageSize=50&Page=0"
                },
                "data": [
                    {
                        "sid": "BN0044409f7e067e279523808d267e2d85",
                        "account_sid": "AC78e8e67fc0246521490fb9907fd0c165",
                        "customer_profile_bundle_sid": "BU3344409f7e067e279523808d267e2d85",
                        "a2p_profile_bundle_sid": "BU3344409f7e067e279523808d267e2d85",
                        "date_created": "2021-01-27T14:18:35Z",
                        "date_updated": "2021-01-27T14:18:36Z",
                        "status": "APPROVED",
                        "tcr_id": "BXXXXXX",
                        "failure_reason": "Registration error",
                        "url": "https://messaging.twilio.com/v1/a2p/BrandRegistrations/BN0044409f7e067e279523808d267e2d85",
                        "brand_score": 42
                    }
                ]
            }
            '''
        ))

        actual = self.client.messaging.v1.brand_registrations.list()

        self.assertIsNotNone(actual)

    def test_create_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.messaging.v1.brand_registrations.create(customer_profile_bundle_sid="BUXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", a2p_profile_bundle_sid="BUXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

        values = {
            'CustomerProfileBundleSid': "BUXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            'A2PProfileBundleSid': "BUXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        }

        self.holodeck.assert_has_request(Request(
            'post',
            'https://messaging.twilio.com/v1/a2p/BrandRegistrations',
            data=values,
        ))

    def test_create_response(self):
        self.holodeck.mock(Response(
            201,
            '''
            {
                "sid": "BN0044409f7e067e279523808d267e2d85",
                "account_sid": "AC78e8e67fc0246521490fb9907fd0c165",
                "customer_profile_bundle_sid": "BU0000009f7e067e279523808d267e2d90",
                "a2p_profile_bundle_sid": "BU1111109f7e067e279523808d267e2d85",
                "date_created": "2021-01-28T10:45:51Z",
                "date_updated": "2021-01-28T10:45:51Z",
                "status": "PENDING",
                "tcr_id": "BXXXXXX",
                "failure_reason": "Registration error",
                "url": "https://messaging.twilio.com/v1/a2p/BrandRegistrations/BN0044409f7e067e279523808d267e2d85",
                "brand_score": 42
            }
            '''
        ))

        actual = self.client.messaging.v1.brand_registrations.create(customer_profile_bundle_sid="BUXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", a2p_profile_bundle_sid="BUXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

        self.assertIsNotNone(actual)
