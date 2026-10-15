import unittest
from unittest.mock import patch

import workflow
import storage


class WorkflowTests(unittest.TestCase):

    def setUp(self):
        self.original_requests = storage.requests

        storage.requests = {}

        self.request = storage.create_request(
            "STU100",
            "student"
        )

    def tearDown(self):
        storage.requests = self.original_requests

    def test_new_request_is_requested(self):
        self.assertEqual(
            self.request["status"],
            "requested"
        )

    def test_cannot_issue_before_approval(self):
        before = self.request.copy()

        with self.assertRaises(ValueError):
            workflow.issue_card(self.request["id"])

        self.assertEqual(self.request, before)

    def test_cannot_approve_with_empty_staff_id(self):
        before = self.request.copy()

        with self.assertRaises(ValueError):
            workflow.approve_request(
                self.request["id"],
                "   "
            )

        self.assertEqual(self.request, before)

    def test_complete_workflow(self):
        request_id = self.request["id"]

        workflow.approve_request(request_id, "M01")
        self.assertEqual(self.request["status"], "approved")
        self.assertEqual(self.request["approved_by"], "M01")

        workflow.issue_card(request_id)
        self.assertEqual(self.request["status"], "issued")

        workflow.return_card(request_id)
        self.assertEqual(self.request["status"], "returned")

    def test_cannot_return_twice(self):
        request_id = self.request["id"]

        workflow.approve_request(request_id, "M01")
        workflow.issue_card(request_id)
        workflow.return_card(request_id)

        before = self.request.copy()

        with self.assertRaises(ValueError):
            workflow.return_card(request_id)

        self.assertEqual(self.request, before)


if __name__ == "__main__":
    unittest.main()