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


class SampleTestCase(IntegrationTestCase):

    def test_fetch_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.autopilot.v1.assistants("UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                    .tasks("UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                    .samples("UFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").fetch()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://autopilot.twilio.com/v1/Assistants/UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Tasks/UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Samples/UFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        ))

    def test_fetch_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "url": "https://autopilot.twilio.com/v1/Assistants/UAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Tasks/UDaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Samples/UFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "task_sid": "UDaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "sid": "UFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "assistant_sid": "UAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "date_created": "2015-07-30T20:00:00Z",
                "language": "language",
                "tagged_text": "tagged_text",
                "date_updated": "2015-07-30T20:00:00Z",
                "source_channel": null
            }
            '''
        ))

        actual = self.client.autopilot.v1.assistants("UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                         .tasks("UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                         .samples("UFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").fetch()

        self.assertIsNotNone(actual)

    def test_list_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.autopilot.v1.assistants("UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                    .tasks("UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                    .samples.list()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://autopilot.twilio.com/v1/Assistants/UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Tasks/UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Samples',
        ))

    def test_read_empty_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "samples": [],
                "meta": {
                    "first_page_url": "https://autopilot.twilio.com/v1/Assistants/UAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Tasks/UDaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Samples?Language=language&PageSize=50&Page=0",
                    "previous_page_url": null,
                    "key": "samples",
                    "next_page_url": null,
                    "url": "https://autopilot.twilio.com/v1/Assistants/UAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Tasks/UDaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Samples?Language=language&PageSize=50&Page=0",
                    "page": 0,
                    "page_size": 50
                }
            }
            '''
        ))

        actual = self.client.autopilot.v1.assistants("UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                         .tasks("UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                         .samples.list()

        self.assertIsNotNone(actual)

    def test_read_full_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "samples": [
                    {
                        "url": "https://autopilot.twilio.com/v1/Assistants/UAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Tasks/UDaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Samples/UFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "task_sid": "UDaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "sid": "UFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "assistant_sid": "UAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "date_created": "2015-07-30T20:00:00Z",
                        "language": "language",
                        "tagged_text": "tagged_text",
                        "date_updated": "2015-07-30T20:00:00Z",
                        "source_channel": "sms"
                    }
                ],
                "meta": {
                    "first_page_url": "https://autopilot.twilio.com/v1/Assistants/UAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Tasks/UDaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Samples?Language=language&PageSize=50&Page=0",
                    "previous_page_url": null,
                    "key": "samples",
                    "next_page_url": null,
                    "url": "https://autopilot.twilio.com/v1/Assistants/UAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Tasks/UDaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Samples?Language=language&PageSize=50&Page=0",
                    "page": 0,
                    "page_size": 50
                }
            }
            '''
        ))

        actual = self.client.autopilot.v1.assistants("UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                         .tasks("UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                         .samples.list()

        self.assertIsNotNone(actual)

    def test_create_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.autopilot.v1.assistants("UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                    .tasks("UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                    .samples.create(language="language", tagged_text="tagged_text")

        values = {'Language': "language", 'TaggedText': "tagged_text", }

        self.holodeck.assert_has_request(Request(
            'post',
            'https://autopilot.twilio.com/v1/Assistants/UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Tasks/UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Samples',
            data=values,
        ))

    def test_create_response(self):
        self.holodeck.mock(Response(
            201,
            '''
            {
                "url": "https://autopilot.twilio.com/v1/Assistants/UAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Tasks/UDaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Samples/UFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "task_sid": "UDaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "sid": "UFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "assistant_sid": "UAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "date_created": "2015-07-30T20:00:00Z",
                "language": "language",
                "tagged_text": "tagged_text",
                "date_updated": "2015-07-30T20:00:00Z",
                "source_channel": "alexa"
            }
            '''
        ))

        actual = self.client.autopilot.v1.assistants("UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                         .tasks("UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                         .samples.create(language="language", tagged_text="tagged_text")

        self.assertIsNotNone(actual)

    def test_update_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.autopilot.v1.assistants("UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                    .tasks("UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                    .samples("UFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").update()

        self.holodeck.assert_has_request(Request(
            'post',
            'https://autopilot.twilio.com/v1/Assistants/UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Tasks/UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Samples/UFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        ))

    def test_update_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "url": "https://autopilot.twilio.com/v1/Assistants/UAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Tasks/UDaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Samples/UFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "task_sid": "UDaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "sid": "UFaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "assistant_sid": "UAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "date_created": "2015-07-30T20:00:00Z",
                "language": "language",
                "tagged_text": "tagged_text",
                "date_updated": "2015-07-30T20:00:00Z",
                "source_channel": "alexa"
            }
            '''
        ))

        actual = self.client.autopilot.v1.assistants("UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                         .tasks("UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                         .samples("UFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").update()

        self.assertIsNotNone(actual)

    def test_delete_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.autopilot.v1.assistants("UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                    .tasks("UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                    .samples("UFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").delete()

        self.holodeck.assert_has_request(Request(
            'delete',
            'https://autopilot.twilio.com/v1/Assistants/UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Tasks/UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Samples/UFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        ))

    def test_delete_response(self):
        self.holodeck.mock(Response(
            204,
            None,
        ))

        actual = self.client.autopilot.v1.assistants("UAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                         .tasks("UDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                         .samples("UFXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").delete()

        self.assertTrue(actual)
