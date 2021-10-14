# coding=utf-8
r"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /
"""

from tests import IntegrationTestCase
from tests.holodeck import Request
from twilio.base import serialize
from twilio.base.exceptions import TwilioException
from twilio.http.response import Response


class SinkTestCase(IntegrationTestCase):

    def test_fetch_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.events.v1.sinks("DGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").fetch()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://events.twilio.com/v1/Sinks/DGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        ))

    def test_fetch_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "status": "initialized",
                "sink_configuration": {
                    "arn": "arn:aws:kinesis:us-east-1:111111111:stream/test",
                    "role_arn": "arn:aws:iam::111111111:role/Role",
                    "external_id": "1234567890"
                },
                "description": "A Sink",
                "sid": "DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "date_created": "2015-07-30T20:00:00Z",
                "sink_type": "kinesis",
                "date_updated": "2015-07-30T20:00:00Z",
                "url": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "links": {
                    "sink_test": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Test",
                    "sink_validate": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Validate"
                }
            }
            '''
        ))

        actual = self.client.events.v1.sinks("DGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").fetch()

        self.assertIsNotNone(actual)

    def test_create_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.events.v1.sinks.create(description="description", sink_configuration={}, sink_type="kinesis")

        values = {
            'Description': "description",
            'SinkConfiguration': serialize.object({}),
            'SinkType': "kinesis",
        }

        self.holodeck.assert_has_request(Request(
            'post',
            'https://events.twilio.com/v1/Sinks',
            data=values,
        ))

    def test_create_response(self):
        self.holodeck.mock(Response(
            201,
            '''
            {
                "status": "initialized",
                "sink_configuration": {
                    "arn": "arn:aws:kinesis:us-east-1:111111111:stream/test",
                    "role_arn": "arn:aws:iam::111111111:role/Role",
                    "external_id": "1234567890"
                },
                "description": "My Kinesis Sink",
                "sid": "DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "date_created": "2015-07-30T20:00:00Z",
                "sink_type": "kinesis",
                "date_updated": "2015-07-30T20:00:00Z",
                "url": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "links": {
                    "sink_test": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Test",
                    "sink_validate": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Validate"
                }
            }
            '''
        ))

        actual = self.client.events.v1.sinks.create(description="description", sink_configuration={}, sink_type="kinesis")

        self.assertIsNotNone(actual)

    def test_delete_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.events.v1.sinks("DGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").delete()

        self.holodeck.assert_has_request(Request(
            'delete',
            'https://events.twilio.com/v1/Sinks/DGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        ))

    def test_delete_response(self):
        self.holodeck.mock(Response(
            204,
            None,
        ))

        actual = self.client.events.v1.sinks("DGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").delete()

        self.assertTrue(actual)

    def test_list_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.events.v1.sinks.list()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://events.twilio.com/v1/Sinks',
        ))

    def test_read_empty_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "sinks": [],
                "meta": {
                    "page": 0,
                    "page_size": 10,
                    "first_page_url": "https://events.twilio.com/v1/Sinks?PageSize=10&Page=0",
                    "previous_page_url": null,
                    "url": "https://events.twilio.com/v1/Sinks?PageSize=10&Page=0",
                    "next_page_url": null,
                    "key": "sinks"
                }
            }
            '''
        ))

        actual = self.client.events.v1.sinks.list()

        self.assertIsNotNone(actual)

    def test_read_results_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "sinks": [
                    {
                        "status": "initialized",
                        "sink_configuration": {
                            "arn": "arn:aws:kinesis:us-east-1:111111111:stream/test",
                            "role_arn": "arn:aws:iam::111111111:role/Role",
                            "external_id": "1234567890"
                        },
                        "description": "A Sink",
                        "sid": "DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "date_created": "2015-07-30T19:00:00Z",
                        "sink_type": "kinesis",
                        "date_updated": "2015-07-30T19:00:00Z",
                        "url": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "links": {
                            "sink_test": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Test",
                            "sink_validate": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Validate"
                        }
                    },
                    {
                        "status": "initialized",
                        "sink_configuration": {
                            "arn": "arn:aws:kinesis:us-east-1:222222222:stream/test",
                            "role_arn": "arn:aws:iam::111111111:role/Role",
                            "external_id": "1234567890"
                        },
                        "description": "ANOTHER Sink",
                        "sid": "DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab",
                        "date_created": "2015-07-30T20:00:00Z",
                        "sink_type": "kinesis",
                        "date_updated": "2015-07-30T20:00:00Z",
                        "url": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab",
                        "links": {
                            "sink_test": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab/Test",
                            "sink_validate": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab/Validate"
                        }
                    },
                    {
                        "status": "active",
                        "sink_configuration": {
                            "destination": "http://example.org/webhook",
                            "method": "POST",
                            "batch_events": true
                        },
                        "description": "A webhook Sink",
                        "sid": "DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac",
                        "date_created": "2015-07-30T21:00:00Z",
                        "sink_type": "webhook",
                        "date_updated": "2015-07-30T21:00:00Z",
                        "url": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac",
                        "links": {
                            "sink_test": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac/Test",
                            "sink_validate": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac/Validate"
                        }
                    }
                ],
                "meta": {
                    "page": 0,
                    "page_size": 20,
                    "first_page_url": "https://events.twilio.com/v1/Sinks?PageSize=20&Page=0",
                    "previous_page_url": null,
                    "url": "https://events.twilio.com/v1/Sinks?PageSize=20&Page=0",
                    "next_page_url": null,
                    "key": "sinks"
                }
            }
            '''
        ))

        actual = self.client.events.v1.sinks.list()

        self.assertIsNotNone(actual)

    def test_read_results_in_use_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "sinks": [
                    {
                        "status": "initialized",
                        "sink_configuration": {
                            "arn": "arn:aws:kinesis:us-east-1:111111111:stream/test",
                            "role_arn": "arn:aws:iam::111111111:role/Role",
                            "external_id": "1234567890"
                        },
                        "description": "A Sink",
                        "sid": "DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "date_created": "2015-07-30T19:00:00Z",
                        "sink_type": "kinesis",
                        "date_updated": "2015-07-30T19:00:00Z",
                        "url": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "links": {
                            "sink_test": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Test",
                            "sink_validate": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Validate"
                        }
                    },
                    {
                        "status": "initialized",
                        "sink_configuration": {
                            "arn": "arn:aws:kinesis:us-east-1:222222222:stream/test",
                            "role_arn": "arn:aws:iam::111111111:role/Role",
                            "external_id": "1234567890"
                        },
                        "description": "ANOTHER Sink",
                        "sid": "DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab",
                        "date_created": "2015-07-30T20:00:00Z",
                        "sink_type": "kinesis",
                        "date_updated": "2015-07-30T20:00:00Z",
                        "url": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab",
                        "links": {
                            "sink_test": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab/Test",
                            "sink_validate": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab/Validate"
                        }
                    },
                    {
                        "status": "active",
                        "sink_configuration": {
                            "destination": "http://example.org/webhook",
                            "method": "POST",
                            "batch_events": true
                        },
                        "description": "A webhook Sink",
                        "sid": "DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac",
                        "date_created": "2015-07-30T21:00:00Z",
                        "sink_type": "webhook",
                        "date_updated": "2015-07-30T21:00:00Z",
                        "url": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac",
                        "links": {
                            "sink_test": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac/Test",
                            "sink_validate": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac/Validate"
                        }
                    }
                ],
                "meta": {
                    "page": 0,
                    "page_size": 20,
                    "first_page_url": "https://events.twilio.com/v1/Sinks?InUse=True&PageSize=20&Page=0",
                    "previous_page_url": null,
                    "url": "https://events.twilio.com/v1/Sinks?InUse=True&PageSize=20&Page=0",
                    "next_page_url": null,
                    "key": "sinks"
                }
            }
            '''
        ))

        actual = self.client.events.v1.sinks.list()

        self.assertIsNotNone(actual)

    def test_read_results_status_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "sinks": [
                    {
                        "status": "active",
                        "sink_configuration": {
                            "destination": "http://example.org/webhook",
                            "method": "POST",
                            "batch_events": true
                        },
                        "description": "A webhook Sink",
                        "sid": "DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac",
                        "date_created": "2015-07-30T21:00:00Z",
                        "sink_type": "webhook",
                        "date_updated": "2015-07-30T21:00:00Z",
                        "url": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac",
                        "links": {
                            "sink_test": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac/Test",
                            "sink_validate": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaac/Validate"
                        }
                    }
                ],
                "meta": {
                    "page": 0,
                    "page_size": 20,
                    "first_page_url": "https://events.twilio.com/v1/Sinks?Status=active&PageSize=20&Page=0",
                    "previous_page_url": null,
                    "url": "https://events.twilio.com/v1/Sinks?Status=active&PageSize=20&Page=0",
                    "next_page_url": null,
                    "key": "sinks"
                }
            }
            '''
        ))

        actual = self.client.events.v1.sinks.list()

        self.assertIsNotNone(actual)

    def test_update_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.events.v1.sinks("DGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").update(description="description")

        values = {'Description': "description", }

        self.holodeck.assert_has_request(Request(
            'post',
            'https://events.twilio.com/v1/Sinks/DGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
            data=values,
        ))

    def test_update_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "status": "initialized",
                "sink_configuration": {
                    "arn": "arn:aws:kinesis:us-east-1:111111111:stream/test",
                    "role_arn": "arn:aws:iam::111111111:role/Role",
                    "external_id": "1234567890"
                },
                "description": "My Kinesis Sink",
                "sid": "DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "date_created": "2015-07-30T20:00:00Z",
                "sink_type": "kinesis",
                "date_updated": "2015-07-30T20:00:00Z",
                "url": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "links": {
                    "sink_test": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Test",
                    "sink_validate": "https://events.twilio.com/v1/Sinks/DGaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Validate"
                }
            }
            '''
        ))

        actual = self.client.events.v1.sinks("DGXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").update(description="description")

        self.assertIsNotNone(actual)