import unittest

from fastapi.testclient import TestClient

from src.api import app


class RetailCaseApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        response = self.client.post("/api/v1/cases/reset")
        self.assertEqual(response.status_code, 200)

    def test_workflow_serves_new_operations_console(self):
        response = self.client.get("/workflow")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Retail Merchandise Intelligence &amp; Operations", response.text)
        self.assertIn("Retail Decision Copilot", response.text)
        self.assertIn("Human–AI workflow", response.text)
        self.assertIn("function renderHome", response.text)
        self.assertIn("function renderCaseWorkspace", response.text)
        self.assertIn("function renderExecutiveHome", response.text)
        self.assertIn("function renderRoleActionPanel", response.text)
        self.assertIn('value="executive"', response.text)
        self.assertNotIn("Human in the loop · 当前由你处理", response.text)
        self.assertNotIn("为什么需要人：", response.text)
        self.assertIn("function startTour", response.text)
        self.assertIn("Exception Queue", response.text)
        self.assertIn("SKU Portfolio", response.text)
        self.assertIn("Scenario Lab", response.text)
        self.assertNotIn("Proven to drive <strong>+40%", response.text)

        home = self.client.get("/")
        self.assertEqual(home.status_code, 200)
        self.assertIn("/api/v1/platform-context", home.text)

        legacy = self.client.get("/legacy")
        self.assertEqual(legacy.status_code, 200)
        self.assertIn("Agent Orchestrator", legacy.text)

    def test_platform_context_integrates_legacy_capabilities(self):
        payload = self.client.get("/api/v1/platform-context").json()
        self.assertEqual(payload["operating_model"], "Retail Decision Case")
        self.assertEqual(len(payload["core_agents"]), 5)
        self.assertIn("Orchestrator", payload["shared_controls"])
        self.assertIn("Policy and Compliance", payload["shared_controls"])
        self.assertEqual(len(payload["seasons"]), 4)
        self.assertGreaterEqual(len(payload["data_sources"]), 7)
        self.assertEqual(payload["boundaries"]["production"].split()[0], "Only")

        regions = self.client.get("/api/v1/regions").json()["regions"]
        self.assertEqual(set(regions), {"china", "japan", "southeast_asia", "korea"})
        self.assertTrue(all(region["business_risk"] for region in regions.values()))

    def test_case_list_and_health(self):
        health = self.client.get("/health").json()
        self.assertEqual(health["status"], "healthy")
        self.assertEqual(health["active_cases"], 3)
        payload = self.client.get("/api/v1/cases").json()
        self.assertEqual(payload["summary"]["total"], 3)
        self.assertEqual(len(payload["cases"]), 3)

    def test_decision_intelligence_is_read_only_and_business_facing(self):
        payload = self.client.get(
            "/api/v1/cases/CASE-SH-003/decision-intelligence"
        ).json()
        self.assertEqual(payload["mode"], "READ_ONLY_DECISION_SUPPORT")
        self.assertEqual(payload["brief"]["recommended_scenario"], "transfer_member_15")
        self.assertEqual(len(payload["forecast"]["recommended"]), 7)
        self.assertEqual(len(payload["discount_sensitivity"]), 5)
        self.assertEqual(len(payload["agent_trace"]), 5)
        self.assertTrue(any(item["status"] == "POLICY_BLOCKED" for item in payload["scenarios"]))
        self.assertTrue(any(item["channel"] == "WeChat member offer" for item in payload["channel_supply_plan"]))

        case = self.client.get("/api/v1/cases/CASE-SH-003").json()
        self.assertEqual(case["status"], "WAITING_FOR_APPROVAL")

    def test_store_confirmation_and_approval_api(self):
        case_id = "CASE-SH-002"
        action_id = "ACT-SH-002-01"
        accepted = self.client.post(
            f"/api/v1/cases/{case_id}/actions/{action_id}/accept",
            json={"actor": "Store Manager"},
        )
        self.assertEqual(accepted.status_code, 200)
        executed = self.client.post(
            f"/api/v1/cases/{case_id}/actions/{action_id}/execute",
            json={"actor": "Store Manager", "observed_count": 58},
        )
        self.assertEqual(executed.status_code, 200)
        self.assertEqual(executed.json()["status"], "WAITING_FOR_APPROVAL")

        approved = self.client.post(
            f"/api/v1/cases/{case_id}/approve",
            json={
                "actor": "Regional Ops",
                "role": "Regional Operations Manager",
                "comment": "Verified after cycle count",
            },
        )
        self.assertEqual(approved.status_code, 200)
        self.assertEqual(approved.json()["status"], "READY_FOR_EXECUTION")

    def test_execution_requires_packet_approval(self):
        response = self.client.post(
            "/api/v1/cases/CASE-SH-001/actions/ACT-SH-001-01/execute",
            json={"actor": "Operations Console"},
        )
        self.assertEqual(response.status_code, 409)


if __name__ == "__main__":
    unittest.main()
