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


class ParticipantTestCase(IntegrationTestCase):

    def test_fetch_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.insights.v1.rooms("RMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                   .participants("PAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").fetch()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://insights.twilio.com/v1/Video/Rooms/RMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Participants/PAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
        ))

    def test_fetch_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "publisher_info": {},
                "edge_location": "ashburn",
                "join_time": "2015-07-30T20:00:00Z",
                "leave_time": "2015-07-30T20:00:00Z",
                "end_reason": "disconnected_via_api",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "error_code": 0,
                "media_region": "us1",
                "properties": {},
                "room_sid": "RMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "error_code_url": "error_code_url",
                "participant_sid": "PAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "codecs": [
                    "VP8"
                ],
                "status": "in_progress",
                "duration_sec": 50000000,
                "participant_identity": "participant_identity",
                "url": "https://insights.twilio.com/v1/Video/Rooms/RMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Participants/PAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            }
            '''
        ))

        actual = self.client.insights.v1.rooms("RMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                        .participants("PAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX").fetch()

        self.assertIsNotNone(actual)

    def test_list_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.insights.v1.rooms("RMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                   .participants.list()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://insights.twilio.com/v1/Video/Rooms/RMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Participants',
        ))

    def test_read_empty_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "meta": {
                    "url": "https://insights.twilio.com/v1/Video/Rooms/RMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Participants?PageSize=50&Page=0",
                    "key": "participants",
                    "first_page_url": "https://insights.twilio.com/v1/Video/Rooms/RMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Participants?PageSize=50&Page=0",
                    "page_size": 50,
                    "next_page_url": null,
                    "page": 0,
                    "previous_page_url": null
                },
                "participants": []
            }
            '''
        ))

        actual = self.client.insights.v1.rooms("RMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                        .participants.list()

        self.assertIsNotNone(actual)

    def test_read_full_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "meta": {
                    "url": "https://insights.twilio.com/v1/Video/Rooms/RMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Participants?PageSize=50&Page=0",
                    "key": "participants",
                    "first_page_url": "https://insights.twilio.com/v1/Video/Rooms/RMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Participants?PageSize=50&Page=0",
                    "page_size": 50,
                    "next_page_url": null,
                    "page": 0,
                    "previous_page_url": null
                },
                "participants": [
                    {
                        "publisher_info": {},
                        "edge_location": "ashburn",
                        "join_time": "2015-07-30T20:00:00Z",
                        "leave_time": "2015-07-30T20:00:00Z",
                        "end_reason": "disconnected_via_api",
                        "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "error_code": 53205,
                        "media_region": "us1",
                        "properties": {},
                        "room_sid": "RMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "error_code_url": "error_code_url",
                        "participant_sid": "PAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "codecs": [
                            "VP8"
                        ],
                        "status": "in_progress",
                        "duration_sec": 50000000,
                        "participant_identity": "participant_identity",
                        "url": "https://insights.twilio.com/v1/Video/Rooms/RMaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Participants/PAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                    }
                ]
            }
            '''
        ))

        actual = self.client.insights.v1.rooms("RMXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX") \
                                        .participants.list()

        self.assertIsNotNone(actual)