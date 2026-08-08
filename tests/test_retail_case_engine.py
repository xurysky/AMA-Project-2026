import unittest
from datetime import timedelta

from src.retail_case_engine import CaseConflict, RetailCaseEngine, utc_now


class RetailCaseEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = RetailCaseEngine()
        self.engine.seed()

    def test_atp_excludes_reserved_safety_blocked_and_transfer_out(self):
        atp = self.engine.calculate_atp(
            physical_on_hand=100,
            soft_reserved=12,
            safety_stock=20,
            blocked_or_quarantined=5,
            pending_transfer_out=8,
            eligible_confirmed_inbound=10,
        )
        self.assertEqual(atp, 65)

    def test_seed_cases_use_dynamic_agent_participation(self):
        case = self.engine.get_case("CASE-SH-001")
        decisions = {item["agent"]: item for item in case["agent_decisions"]}
        self.assertEqual(decisions["Inventory Agent"]["role"], "lead")
        self.assertEqual(decisions["Marketing Agent"]["status"], "NO_CAMPAIGN")
        self.assertEqual(case["inventory"]["sellable_atp"], 29)
        self.assertNotEqual(case["inventory"]["physical_on_hand"], case["inventory"]["sellable_atp"])

    def test_low_confidence_case_pauses_then_reassesses_after_cycle_count(self):
        case_id = "CASE-SH-002"
        action_id = "ACT-SH-002-01"
        initial = self.engine.get_case(case_id)
        self.assertEqual(initial["status"], "WAITING_FOR_STORE_CONFIRMATION")

        accepted = self.engine.accept_action(case_id, action_id, "Store Manager")
        self.assertEqual(accepted["actions"][0]["status"], "READY")

        reassessed = self.engine.execute_action(case_id, action_id, "Store Manager", observed_count=58)
        self.assertEqual(reassessed["status"], "WAITING_FOR_APPROVAL")
        self.assertEqual(reassessed["inventory"]["physical_on_hand"], 58)
        self.assertEqual(reassessed["inventory"]["inventory_confidence"], 0.98)
        self.assertEqual(reassessed["decision_packet"]["version"], 2)
        self.assertTrue(any(a["action_id"] == "ACT-SH-002-02" for a in reassessed["actions"]))

    def test_approval_requires_authorized_role(self):
        with self.assertRaises(CaseConflict):
            self.engine.approve_packet("CASE-SH-001", "Store Manager", "Store Manager", "Approve")

        approved = self.engine.approve_packet(
            "CASE-SH-001",
            "Regional Ops",
            "Regional Operations Manager",
            "Evidence reviewed",
        )
        self.assertEqual(approved["status"], "READY_FOR_EXECUTION")
        self.assertTrue(all(a["status"] == "APPROVED" for a in approved["actions"]))

    def test_expired_packet_requires_reassessment(self):
        self.engine._cases["CASE-SH-001"]["decision_packet"]["expires_at"] = (
            utc_now() - timedelta(minutes=1)
        ).isoformat()
        with self.assertRaises(CaseConflict):
            self.engine.approve_packet(
                "CASE-SH-001",
                "Regional Ops",
                "Regional Operations Manager",
                "Too late",
            )
        case = self.engine.get_case("CASE-SH-001")
        self.assertEqual(case["status"], "REASSESS_REQUIRED")
        self.assertEqual(case["decision_packet"]["status"], "EXPIRED")

    def test_failed_execution_records_compensation_then_retries(self):
        case_id = "CASE-SH-003"
        transfer_id = "ACT-SH-003-01"
        voucher_id = "ACT-SH-003-02"
        self.engine.approve_packet(case_id, "Merch Lead", "Merchandise Manager", "Approved")

        failed = self.engine.execute_action(case_id, transfer_id, "Operations Console")
        self.assertEqual(failed["status"], "PARTIALLY_EXECUTED")
        self.assertEqual(failed["execution_receipts"][-1]["status"], "FAILED")
        self.assertIsNotNone(failed["execution_receipts"][-1]["compensation_action"])

        retried = self.engine.execute_action(case_id, transfer_id, "Operations Console")
        self.assertEqual(retried["execution_receipts"][-1]["status"], "COMPLETED")
        self.assertEqual(retried["actions"][0]["attempts"], 2)

        completed = self.engine.execute_action(case_id, voucher_id, "CRM Manager")
        self.assertEqual(completed["status"], "COMPLETED")
        self.assertEqual(completed["kpi_observations"]["measurement_type"], "demo_observed")


if __name__ == "__main__":
    unittest.main()
