import unittest

from dbsnap_verify.state_doc import (
    state_doc_s3_key,
    get_or_create_state_doc_in_s3,
    current_state,
)

import json

import boto3
s3 = boto3.client("s3")

import mock

with open('./tests/fixtures/example_state_doc.json') as state_doc_file:
    EXAMPLE_STATE_DOC = json.load(state_doc_file)

mock_state_doc = mock.Mock(return_value=EXAMPLE_STATE_DOC)
mock_no_such_key_exception = mock.Mock(side_effect=s3.exceptions.NoSuchKey({}, ""))
mock_none = mock.Mock(return_value=None)


@mock.patch('dbsnap_verify.state_doc.upload_state_doc', mock_none)
class Tests(unittest.TestCase):

    @mock.patch('dbsnap_verify.state_doc.download_state_doc', mock_state_doc)
    def setUp(self):
        # mock the static json config in the Cloudwatch event rule trigger.
        # an AWS Lambda always accepts `event` as its first argument.
        self.event = {
            "database" : "test-db-instance",
            "state_doc_bucket" : "bucket-to-hold-state-documents",
            "snapshot_region" : "us-east-1",
        }
        self.state_doc = get_or_create_state_doc_in_s3(self.event)

    def test_state_doc_s3_key(self):
        self.assertEqual(
            state_doc_s3_key(self.event["database"]),
            "state-doc-test-db-instance.json"
        )

    @mock.patch('dbsnap_verify.state_doc.download_state_doc', mock_no_such_key_exception)
    def test_get_or_create_state_doc_in_s3_missing_key(self):
        """Returns a new state_doc when one is not found in s3"""
        state_doc = get_or_create_state_doc_in_s3(self.event)
        self.assertEqual(state_doc["database"], "test-db-instance")
        self.assertEqual(state_doc["state_doc_bucket"], "bucket-to-hold-state-documents")
        self.assertEqual(state_doc["snapshot_region"], "us-east-1")
        self.assertEqual(state_doc["states"][-1]["state"], "wait")

    def test_get_or_create_state_doc_in_s3_doc_found_in_s3(self):
        print(self.state_doc)
        self.assertEqual(self.state_doc["database"], "test-db-instance")
        self.assertEqual(self.state_doc["snapshot_region"], "us-east-1")
        self.assertGreater(len(self.state_doc["states"]), 5)
        self.assertEqual(self.state_doc["states"][-1]["state"], "wait")

    def test_current_state(self):
        self.assertEqual(current_state(self.state_doc), "wait")


