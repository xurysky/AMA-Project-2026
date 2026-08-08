"""Retail merchandise decision cases for the Project 46 operational demo.

The case engine keeps deterministic retail calculations separate from LLM
explanations. It models the workflow a store and regional operations team can
actually execute: evidence snapshot, domain decisions, approval, action, and
receipt.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().isoformat()


def iso_after(hours: int) -> str:
    return (utc_now() + timedelta(hours=hours)).isoformat()


class ProductVariant(BaseModel):
    style_id: str
    color_id: str
    size_id: str
    variant_id: str
    gtin: str
    product_name: str
    color_name: str
    lifecycle: str
    category: str
    unit_cost_cny: float
    current_price_cny: float
    margin_floor_pct: float
    master_data_version: str = "MDM-2026.07.31"


class InventorySnapshot(BaseModel):
    physical_on_hand: int
    soft_reserved: int
    safety_stock: int
    blocked_or_quarantined: int
    pending_transfer_out: int = 0
    eligible_confirmed_inbound: int = 0
    returned_pending_inspection: int = 0
    sellable_atp: int
    future_atp: int
    future_atp_at: Optional[str] = None
    demand_units_per_day: float
    days_of_supply: float
    inventory_confidence: float
    as_of_time: str
    freshness_minutes: int


class EvidenceItem(BaseModel):
    source: str
    observed_at: str
    summary: str
    quality: str = "verified"


class DomainDecision(BaseModel):
    agent: str
    role: str
    status: str
    recommendation: str
    evidence_refs: List[str]
    confidence: float
    model_version: str = "rules+retail-ops-v1"
    rule_version: str = "retail-policy-2026.08"
    prompt_version: Optional[str] = None
    blockers: List[str] = Field(default_factory=list)


class ProposedAction(BaseModel):
    action_id: str
    action_type: str
    title: str
    owner_role: str
    target_system: str
    status: str
    quantity: Optional[int] = None
    due_at: str
    requires_approval: bool = False
    required_approval_role: Optional[str] = None
    requires_store_acceptance: bool = False
    idempotency_key: str
    retryable: bool = True
    attempts: int = 0
    failure_mode: Optional[str] = None
    rejection_reason: Optional[str] = None


class DecisionPacket(BaseModel):
    packet_id: str
    version: int
    status: str
    recommendation: str
    rationale: List[str]
    alternatives: List[str]
    blockers: List[str]
    expires_at: str
    policy_version: str
    proposed_action_ids: List[str]
    required_approval_roles: List[str]


class ApprovalRecord(BaseModel):
    approval_id: str
    packet_id: str
    actor: str
    role: str
    decision: str
    comment: str
    decided_at: str


class ExecutionReceipt(BaseModel):
    receipt_id: str
    action_id: str
    target_system: str
    status: str
    attempt: int
    requested_at: str
    completed_at: str
    external_reference: Optional[str] = None
    error_code: Optional[str] = None
    detail: str
    compensation_action: Optional[str] = None


class AuditEvent(BaseModel):
    time: str
    actor: str
    action: str
    detail: str


class RetailCase(BaseModel):
    case_id: str
    document_type: str = "retail_case"
    case_type: str
    dedupe_key: str
    title: str
    status: str
    severity: str
    region: str
    city: str
    store_id: str
    store_name: str
    store_cluster: str
    owner_role: str
    lead_agent: str
    sla_due_at: str
    created_at: str
    updated_at: str
    as_of_time: str
    planning_policy_version: str
    consent_policy_version: str
    variant: ProductVariant
    inventory: InventorySnapshot
    return_disposition: Dict[str, int]
    store_constraints: Dict[str, Any]
    evidence: List[EvidenceItem]
    agent_decisions: List[DomainDecision]
    decision_packet: DecisionPacket
    actions: List[ProposedAction]
    approvals: List[ApprovalRecord] = Field(default_factory=list)
    execution_receipts: List[ExecutionReceipt] = Field(default_factory=list)
    audit_log: List[AuditEvent] = Field(default_factory=list)
    kpi_observations: Dict[str, Any] = Field(default_factory=dict)


class CaseConflict(ValueError):
    """Raised when a requested transition violates the case state machine."""


class RetailCaseEngine:
    def __init__(self) -> None:
        self._cases: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def calculate_atp(
        physical_on_hand: int,
        soft_reserved: int,
        safety_stock: int,
        blocked_or_quarantined: int,
        pending_transfer_out: int = 0,
        eligible_confirmed_inbound: int = 0,
    ) -> int:
        return max(
            0,
            physical_on_hand
            - soft_reserved
            - safety_stock
            - blocked_or_quarantined
            - pending_transfer_out
            + eligible_confirmed_inbound,
        )

    def seed(self, replace: bool = False) -> List[Dict[str, Any]]:
        if self._cases and not replace:
            return self.list_cases()["cases"]
        self._cases = {case["case_id"]: case for case in self._build_seed_cases()}
        return self.list_cases()["cases"]

    def load(self, cases: List[Dict[str, Any]]) -> None:
        for case in cases:
            if case.get("document_type") == "retail_case" and case.get("case_id"):
                self._cases[case["case_id"]] = case

    def list_cases(
        self,
        status: Optional[str] = None,
        case_type: Optional[str] = None,
        severity: Optional[str] = None,
    ) -> Dict[str, Any]:
        cases = list(self._cases.values())
        if status:
            cases = [case for case in cases if case["status"] == status]
        if case_type:
            cases = [case for case in cases if case["case_type"] == case_type]
        if severity:
            cases = [case for case in cases if case["severity"] == severity]
        cases.sort(key=lambda case: (self._severity_rank(case["severity"]), case["sla_due_at"]))
        return {
            "cases": deepcopy(cases),
            "summary": self.summary(),
        }

    def summary(self) -> Dict[str, Any]:
        cases = list(self._cases.values())
        return {
            "total": len(cases),
            "critical": sum(case["severity"] == "critical" for case in cases),
            "waiting_for_store": sum(case["status"] == "WAITING_FOR_STORE_CONFIRMATION" for case in cases),
            "waiting_for_approval": sum(case["status"] == "WAITING_FOR_APPROVAL" for case in cases),
            "execution_attention": sum(case["status"] in {"PARTIALLY_EXECUTED", "EXECUTION_FAILED"} for case in cases),
            "completed": sum(case["status"] == "COMPLETED" for case in cases),
        }

    def get_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        case = self._cases.get(case_id)
        return deepcopy(case) if case else None

    def approve_packet(self, case_id: str, actor: str, role: str, comment: str) -> Dict[str, Any]:
        case = self._require_case(case_id)
        packet = case["decision_packet"]
        if case["status"] != "WAITING_FOR_APPROVAL":
            raise CaseConflict("Case is not waiting for approval")
        if datetime.fromisoformat(packet["expires_at"]) <= utc_now():
            case["status"] = "REASSESS_REQUIRED"
            packet["status"] = "EXPIRED"
            self._audit(case, "Policy Engine", "PACKET_EXPIRED", packet["packet_id"])
            raise CaseConflict("Decision packet expired; reassessment is required")
        required_roles = packet["required_approval_roles"]
        if required_roles and role not in required_roles:
            raise CaseConflict(f"Approval requires one of: {', '.join(required_roles)}")
        approval = ApprovalRecord(
            approval_id=f"APR-{len(case['approvals']) + 1:03d}",
            packet_id=packet["packet_id"],
            actor=actor,
            role=role,
            decision="APPROVED",
            comment=comment,
            decided_at=iso_now(),
        ).model_dump()
        case["approvals"].append(approval)
        packet["status"] = "APPROVED"
        for action in case["actions"]:
            if action["status"] == "PENDING_APPROVAL":
                action["status"] = "APPROVED"
        case["status"] = "READY_FOR_EXECUTION"
        case["updated_at"] = iso_now()
        self._audit(case, actor, "PACKET_APPROVED", f"{packet['packet_id']} by {role}: {comment}")
        return deepcopy(case)

    def reject_packet(self, case_id: str, actor: str, role: str, comment: str) -> Dict[str, Any]:
        case = self._require_case(case_id)
        if case["status"] != "WAITING_FOR_APPROVAL":
            raise CaseConflict("Case is not waiting for approval")
        case["approvals"].append(
            ApprovalRecord(
                approval_id=f"APR-{len(case['approvals']) + 1:03d}",
                packet_id=case["decision_packet"]["packet_id"],
                actor=actor,
                role=role,
                decision="REJECTED",
                comment=comment,
                decided_at=iso_now(),
            ).model_dump()
        )
        case["decision_packet"]["status"] = "REJECTED"
        for action in case["actions"]:
            if action["status"] in {"PENDING_APPROVAL", "APPROVED"}:
                action["status"] = "REJECTED"
                action["rejection_reason"] = comment
        case["status"] = "REJECTED"
        case["updated_at"] = iso_now()
        self._audit(case, actor, "PACKET_REJECTED", f"{role}: {comment}")
        return deepcopy(case)

    def accept_action(self, case_id: str, action_id: str, actor: str) -> Dict[str, Any]:
        case, action = self._require_action(case_id, action_id)
        if action["status"] != "WAITING_FOR_STORE_ACCEPTANCE":
            raise CaseConflict("Action is not waiting for store acceptance")
        action["status"] = "READY"
        case["updated_at"] = iso_now()
        self._audit(case, actor, "STORE_TASK_ACCEPTED", action_id)
        return deepcopy(case)

    def reject_action(self, case_id: str, action_id: str, actor: str, reason: str) -> Dict[str, Any]:
        case, action = self._require_action(case_id, action_id)
        if action["status"] not in {"WAITING_FOR_STORE_ACCEPTANCE", "READY"}:
            raise CaseConflict("Action can no longer be rejected")
        action["status"] = "REJECTED"
        action["rejection_reason"] = reason
        case["status"] = "REASSESS_REQUIRED"
        case["updated_at"] = iso_now()
        self._audit(case, actor, "STORE_TASK_REJECTED", f"{action_id}: {reason}")
        return deepcopy(case)

    def execute_action(
        self,
        case_id: str,
        action_id: str,
        actor: str,
        observed_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        case, action = self._require_action(case_id, action_id)
        allowed = {"APPROVED", "READY", "FAILED"}
        if action["status"] not in allowed:
            raise CaseConflict(f"Action status {action['status']} cannot be executed")
        if action["requires_approval"] and action["status"] != "APPROVED" and action["attempts"] == 0:
            raise CaseConflict("Approve the decision packet before execution")
        action["attempts"] += 1
        requested_at = iso_now()

        should_fail = action.get("failure_mode") == "fail_first_attempt" and action["attempts"] == 1
        if should_fail:
            action["status"] = "FAILED"
            receipt = ExecutionReceipt(
                receipt_id=f"RCP-{len(case['execution_receipts']) + 1:03d}",
                action_id=action_id,
                target_system=action["target_system"],
                status="FAILED",
                attempt=action["attempts"],
                requested_at=requested_at,
                completed_at=iso_now(),
                error_code="WMS_CAPACITY_WINDOW_CLOSED",
                detail="The requested pick wave missed the current warehouse cut-off.",
                compensation_action="Release the temporary transfer allocation before retry.",
            ).model_dump()
            case["execution_receipts"].append(receipt)
            case["status"] = "PARTIALLY_EXECUTED"
            self._audit(case, "Execution Orchestrator", "ACTION_FAILED", f"{action_id}: WMS_CAPACITY_WINDOW_CLOSED")
            self._audit(case, "Execution Orchestrator", "COMPENSATION_RECORDED", f"Released allocation for {action_id}")
        else:
            action["status"] = "COMPLETED"
            receipt = ExecutionReceipt(
                receipt_id=f"RCP-{len(case['execution_receipts']) + 1:03d}",
                action_id=action_id,
                target_system=action["target_system"],
                status="COMPLETED",
                attempt=action["attempts"],
                requested_at=requested_at,
                completed_at=iso_now(),
                external_reference=f"{action['target_system']}-{case_id[-4:]}-{action['attempts']}",
                detail=self._execution_detail(action, observed_count),
            ).model_dump()
            case["execution_receipts"].append(receipt)
            self._audit(case, actor, "ACTION_COMPLETED", action_id)
            if action["action_type"] == "STORE_CYCLE_COUNT":
                self._apply_cycle_count(case, observed_count)
            else:
                self._refresh_case_execution_status(case)
        case["updated_at"] = iso_now()
        return deepcopy(case)

    def reset(self) -> List[Dict[str, Any]]:
        return self.seed(replace=True)

    def _apply_cycle_count(self, case: Dict[str, Any], observed_count: Optional[int]) -> None:
        actual = int(observed_count if observed_count is not None else 58)
        inventory = case["inventory"]
        inventory["physical_on_hand"] = actual
        inventory["inventory_confidence"] = 0.98
        inventory["freshness_minutes"] = 2
        inventory["as_of_time"] = iso_now()
        inventory["sellable_atp"] = self.calculate_atp(
            actual,
            inventory["soft_reserved"],
            inventory["safety_stock"],
            inventory["blocked_or_quarantined"],
            inventory["pending_transfer_out"],
        )
        inventory["future_atp"] = inventory["sellable_atp"] + inventory["eligible_confirmed_inbound"]
        inventory["days_of_supply"] = round(inventory["sellable_atp"] / max(inventory["demand_units_per_day"], 1), 1)
        case["evidence"].append(
            EvidenceItem(
                source="Store RFID cycle count",
                observed_at=iso_now(),
                summary=f"Store confirmed {actual} physical units; inventory confidence raised to 98%.",
                quality="verified",
            ).model_dump()
        )
        inventory_decision = next(d for d in case["agent_decisions"] if d["agent"] == "Inventory Agent")
        inventory_decision.update(
            {
                "status": "COMPLETED",
                "recommendation": "RFID count confirmed a broken-size stockout. Transfer 72 M/L units from SH-018.",
                "confidence": 0.96,
                "blockers": [],
            }
        )
        packet = case["decision_packet"]
        packet.update(
            {
                "version": packet["version"] + 1,
                "status": "PENDING_APPROVAL",
                "recommendation": "Approve a 72-unit inter-store transfer after the verified cycle count.",
                "rationale": [
                    "Verified ATP covers less than one day of M/L demand.",
                    "SH-018 has eligible sellable ATP and can release 72 units.",
                    "No customer campaign will run until receiving is confirmed.",
                ],
                "blockers": [],
                "expires_at": iso_after(4),
                "proposed_action_ids": ["ACT-SH-002-02"],
                "required_approval_roles": ["Regional Operations Manager"],
            }
        )
        if not any(a["action_id"] == "ACT-SH-002-02" for a in case["actions"]):
            case["actions"].append(
                ProposedAction(
                    action_id="ACT-SH-002-02",
                    action_type="TRANSFER_REQUEST",
                    title="Transfer 72 AIRism M/L units from SH-018",
                    owner_role="Regional Operations Manager",
                    target_system="ERP_TRANSFER",
                    status="PENDING_APPROVAL",
                    quantity=72,
                    due_at=iso_after(8),
                    requires_approval=True,
                    required_approval_role="Regional Operations Manager",
                    idempotency_key=f"{case['case_id']}:ACT-SH-002-02",
                ).model_dump()
            )
        case["status"] = "WAITING_FOR_APPROVAL"
        self._audit(case, "Inventory Agent", "CASE_REASSESSED", "Cycle count removed the inventory-confidence blocker")

    def _refresh_case_execution_status(self, case: Dict[str, Any]) -> None:
        actionable = [a for a in case["actions"] if a["status"] != "BLOCKED"]
        if actionable and all(a["status"] in {"COMPLETED", "REJECTED"} for a in actionable):
            case["status"] = "COMPLETED"
            case["kpi_observations"]["case_cycle_minutes"] = 18
            case["kpi_observations"]["measurement_type"] = "demo_observed"
            self._audit(case, "System", "CASE_COMPLETED", "All approved actions have execution receipts")
        elif any(a["status"] == "FAILED" for a in actionable):
            case["status"] = "PARTIALLY_EXECUTED"
        else:
            case["status"] = "IN_EXECUTION"

    @staticmethod
    def _execution_detail(action: Dict[str, Any], observed_count: Optional[int]) -> str:
        if action["action_type"] == "STORE_CYCLE_COUNT":
            return f"Cycle count completed with {observed_count if observed_count is not None else 58} physical units."
        if action["action_type"] == "TRANSFER_REQUEST":
            return f"Transfer request accepted for {action.get('quantity', 0)} units."
        if action["action_type"] == "REPLENISHMENT_REQUEST":
            return f"Warehouse replenishment created for {action.get('quantity', 0)} units."
        if action["action_type"] == "MEMBER_VOUCHER_DRAFT":
            return "Consent-filtered CRM campaign draft created; no messages were sent."
        return "Action completed and acknowledged by the target system."

    def _require_case(self, case_id: str) -> Dict[str, Any]:
        case = self._cases.get(case_id)
        if not case:
            raise KeyError(case_id)
        return case

    def _require_action(self, case_id: str, action_id: str) -> tuple[Dict[str, Any], Dict[str, Any]]:
        case = self._require_case(case_id)
        for action in case["actions"]:
            if action["action_id"] == action_id:
                return case, action
        raise KeyError(action_id)

    @staticmethod
    def _audit(case: Dict[str, Any], actor: str, action: str, detail: str) -> None:
        case["audit_log"].append(AuditEvent(time=iso_now(), actor=actor, action=action, detail=detail).model_dump())

    @staticmethod
    def _severity_rank(severity: str) -> int:
        return {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(severity, 9)

    def _build_seed_cases(self) -> List[Dict[str, Any]]:
        return [self._broken_size_case(), self._low_confidence_case(), self._overstock_case()]

    def _broken_size_case(self) -> Dict[str, Any]:
        now = iso_now()
        physical, reserved, safety, blocked = 74, 18, 24, 3
        atp = self.calculate_atp(physical, reserved, safety, blocked)
        case_id = "CASE-SH-001"
        actions = [
            ProposedAction(
                action_id="ACT-SH-001-01",
                action_type="TRANSFER_REQUEST",
                title="Transfer 160 AIRism M/L units from SH-021 and SH-033",
                owner_role="Regional Operations Manager",
                target_system="ERP_TRANSFER",
                status="PENDING_APPROVAL",
                quantity=160,
                due_at=iso_after(6),
                requires_approval=True,
                required_approval_role="Regional Operations Manager",
                idempotency_key=f"{case_id}:ACT-SH-001-01",
            ),
            ProposedAction(
                action_id="ACT-SH-001-02",
                action_type="REPLENISHMENT_REQUEST",
                title="Replenish 420 units from East China DC",
                owner_role="Supply Chain Planner",
                target_system="WMS_PICK",
                status="PENDING_APPROVAL",
                quantity=420,
                due_at=iso_after(10),
                requires_approval=True,
                required_approval_role="Regional Operations Manager",
                idempotency_key=f"{case_id}:ACT-SH-001-02",
            ),
        ]
        case = RetailCase(
            case_id=case_id,
            case_type="BROKEN_SIZE_STOCKOUT",
            dedupe_key="BROKEN_SIZE_STOCKOUT:SH-001:AIR-M-BLK:2026-08-01-AM",
            title="AIRism black M/L broken-size risk",
            status="WAITING_FOR_APPROVAL",
            severity="critical",
            region="china",
            city="Shanghai",
            store_id="SH-001",
            store_name="Shanghai Huaihai Road Flagship",
            store_cluster="urban_flagship",
            owner_role="Regional Operations Manager",
            lead_agent="Inventory Agent",
            sla_due_at=iso_after(3),
            created_at=now,
            updated_at=now,
            as_of_time=now,
            planning_policy_version="MERCH-SUMMER-2026.07",
            consent_policy_version="PIPL-MKT-2026.02",
            variant=ProductVariant(
                style_id="AIR-TEE-2026",
                color_id="BLK",
                size_id="M-L",
                variant_id="AIR-TEE-2026-BLK-ML",
                gtin="06912345670018",
                product_name="AIRism Cotton Crew Neck T-Shirt",
                color_name="Black",
                lifecycle="seasonal_core",
                category="mens_tops",
                unit_cost_cny=42,
                current_price_cny=99,
                margin_floor_pct=45,
            ),
            inventory=InventorySnapshot(
                physical_on_hand=physical,
                soft_reserved=reserved,
                safety_stock=safety,
                blocked_or_quarantined=blocked,
                returned_pending_inspection=5,
                sellable_atp=atp,
                future_atp=atp + 420,
                future_atp_at=iso_after(36),
                demand_units_per_day=46,
                days_of_supply=round(atp / 46, 1),
                inventory_confidence=0.94,
                as_of_time=now,
                freshness_minutes=8,
            ),
            return_disposition={"pending_inspection": 5, "sellable": 0, "quarantined": 0},
            store_constraints={"backroom_capacity_units": 620, "receiving_window": "14:00-17:00", "task_load_minutes": 75, "task_capacity_minutes": 180},
            evidence=[
                EvidenceItem(source="POS", observed_at=now, summary="M/L sell-through accelerated to 46 units/day after three heatwave days."),
                EvidenceItem(source="RFID", observed_at=now, summary="Physical count variance is within tolerance; inventory is decision-ready."),
                EvidenceItem(source="OMS", observed_at=now, summary="18 units are already reserved for pickup and cannot be reallocated."),
            ],
            agent_decisions=[
                DomainDecision(agent="Inventory Agent", role="lead", status="COMPLETED", recommendation="Transfer 160 units now and replenish 420 units from the DC.", evidence_refs=["POS", "RFID", "OMS"], confidence=0.94),
                DomainDecision(agent="Pricing Agent", role="support", status="COMPLETED", recommendation="Protect the in-season price; no markdown or broad voucher.", evidence_refs=["MERCH-SUMMER-2026.07"], confidence=0.97),
                DomainDecision(agent="Customer Understanding Agent", role="optional", status="SKIPPED", recommendation="No audience build until inventory receiving is confirmed.", evidence_refs=["PIPL-MKT-2026.02"], confidence=1.0),
                DomainDecision(agent="Personalization Agent", role="support", status="COMPLETED", recommendation="Recommend available colors or nearby-store pickup; block unavailable M/L promises.", evidence_refs=["OMS", "ATP"], confidence=0.92),
                DomainDecision(agent="Marketing Agent", role="optional", status="NO_CAMPAIGN", recommendation="Do not launch a campaign while ATP is below one day of demand.", evidence_refs=["ATP"], confidence=0.99),
            ],
            decision_packet=DecisionPacket(
                packet_id="DP-SH-001-V1",
                version=1,
                status="PENDING_APPROVAL",
                recommendation="Approve the inter-store transfer and DC replenishment; keep price protected and marketing blocked.",
                rationale=[
                    "Sellable ATP is 29 units after reservations, safety stock, and blocked stock.",
                    "Current ATP covers only 0.6 days of M/L demand.",
                    "Low-selling stores can release stock before the DC shipment arrives.",
                ],
                alternatives=["Show substitute colors and nearby-store pickup only.", "Take no inventory action and accept the stockout risk."],
                blockers=["Broad customer campaign blocked until receiving is confirmed."],
                expires_at=iso_after(4),
                policy_version="retail-policy-2026.08",
                proposed_action_ids=[a.action_id for a in actions],
                required_approval_roles=["Regional Operations Manager"],
            ),
            actions=actions,
            audit_log=[AuditEvent(time=now, actor="Case Formation Service", action="CASE_CREATED", detail="Broken-size threshold breached with verified inventory")],
            kpi_observations={"decision_packet_minutes": 7, "blocked_unfulfillable_recommendations": 4, "measurement_type": "demo_observed"},
        )
        return case.model_dump()

    def _low_confidence_case(self) -> Dict[str, Any]:
        now = iso_now()
        physical, reserved, safety, blocked = 96, 8, 20, 0
        atp = self.calculate_atp(physical, reserved, safety, blocked)
        case_id = "CASE-SH-002"
        action = ProposedAction(
            action_id="ACT-SH-002-01",
            action_type="STORE_CYCLE_COUNT",
            title="Verify AIRism white M/L physical stock",
            owner_role="Store Manager",
            target_system="STORE_TASK",
            status="WAITING_FOR_STORE_ACCEPTANCE",
            due_at=iso_after(1),
            requires_store_acceptance=True,
            idempotency_key=f"{case_id}:ACT-SH-002-01",
        )
        case = RetailCase(
            case_id=case_id,
            case_type="BROKEN_SIZE_STOCKOUT",
            dedupe_key="BROKEN_SIZE_STOCKOUT:SH-009:AIR-WHT-ML:2026-08-01-AM",
            title="AIRism white M/L inventory mismatch",
            status="WAITING_FOR_STORE_CONFIRMATION",
            severity="high",
            region="china",
            city="Shanghai",
            store_id="SH-009",
            store_name="Shanghai Wujiaochang Store",
            store_cluster="urban_standard",
            owner_role="Store Manager",
            lead_agent="Inventory Agent",
            sla_due_at=iso_after(1),
            created_at=now,
            updated_at=now,
            as_of_time=now,
            planning_policy_version="MERCH-SUMMER-2026.07",
            consent_policy_version="PIPL-MKT-2026.02",
            variant=ProductVariant(
                style_id="AIR-TEE-2026",
                color_id="WHT",
                size_id="M-L",
                variant_id="AIR-TEE-2026-WHT-ML",
                gtin="06912345670025",
                product_name="AIRism Cotton Crew Neck T-Shirt",
                color_name="White",
                lifecycle="seasonal_core",
                category="mens_tops",
                unit_cost_cny=42,
                current_price_cny=99,
                margin_floor_pct=45,
            ),
            inventory=InventorySnapshot(
                physical_on_hand=physical,
                soft_reserved=reserved,
                safety_stock=safety,
                blocked_or_quarantined=blocked,
                sellable_atp=atp,
                future_atp=atp,
                demand_units_per_day=39,
                days_of_supply=round(atp / 39, 1),
                inventory_confidence=0.54,
                as_of_time=now,
                freshness_minutes=42,
            ),
            return_disposition={"pending_inspection": 0, "sellable": 0, "quarantined": 0},
            store_constraints={"backroom_capacity_units": 380, "receiving_window": "10:00-12:00", "task_load_minutes": 135, "task_capacity_minutes": 180},
            evidence=[
                EvidenceItem(source="ERP", observed_at=now, summary="Book inventory reports 96 units.", quality="stale"),
                EvidenceItem(source="RFID", observed_at=now, summary="Only 61 tags were observed; variance exceeds the 10% policy threshold.", quality="low_confidence"),
            ],
            agent_decisions=[
                DomainDecision(agent="Inventory Agent", role="lead", status="BLOCKED", recommendation="Run a store cycle count before transfer or promotion decisions.", evidence_refs=["ERP", "RFID"], confidence=0.54, blockers=["Inventory confidence below 80%"]),
                DomainDecision(agent="Pricing Agent", role="optional", status="NOT_INVOKED", recommendation="Wait for verified inventory.", evidence_refs=[], confidence=1.0),
                DomainDecision(agent="Customer Understanding Agent", role="optional", status="NOT_INVOKED", recommendation="Wait for verified inventory.", evidence_refs=[], confidence=1.0),
                DomainDecision(agent="Personalization Agent", role="support", status="BLOCKED", recommendation="Block local pickup promise for this variant.", evidence_refs=["RFID"], confidence=0.98, blockers=["Inventory confidence below 80%"]),
                DomainDecision(agent="Marketing Agent", role="optional", status="NO_CAMPAIGN", recommendation="No campaign while inventory is unverified.", evidence_refs=["RFID"], confidence=1.0),
            ],
            decision_packet=DecisionPacket(
                packet_id="DP-SH-002-V1",
                version=1,
                status="BLOCKED_PENDING_CONFIRMATION",
                recommendation="Ask the store to complete a cycle count before making a commercial decision.",
                rationale=["ERP and RFID differ by more than the policy threshold.", "Marketing or transfer based on uncertain stock can create oversell."],
                alternatives=["Temporarily hide local pickup for this variant."],
                blockers=["Store physical count required."],
                expires_at=iso_after(2),
                policy_version="retail-policy-2026.08",
                proposed_action_ids=[action.action_id],
                required_approval_roles=[],
            ),
            actions=[action],
            audit_log=[AuditEvent(time=now, actor="Policy Engine", action="CASE_PAUSED", detail="Inventory confidence 54%; store confirmation required")],
            kpi_observations={"stale_data_blocked": True, "measurement_type": "demo_observed"},
        )
        return case.model_dump()

    def _overstock_case(self) -> Dict[str, Any]:
        now = iso_now()
        physical, reserved, safety, blocked = 1180, 40, 60, 80
        atp = self.calculate_atp(physical, reserved, safety, blocked)
        case_id = "CASE-SH-003"
        actions = [
            ProposedAction(
                action_id="ACT-SH-003-01",
                action_type="TRANSFER_REQUEST",
                title="Transfer 320 light jackets to two outlet stores",
                owner_role="Regional Operations Manager",
                target_system="WMS_TRANSFER",
                status="PENDING_APPROVAL",
                quantity=320,
                due_at=iso_after(18),
                requires_approval=True,
                required_approval_role="Merchandise Manager",
                idempotency_key=f"{case_id}:ACT-SH-003-01",
                failure_mode="fail_first_attempt",
            ),
            ProposedAction(
                action_id="ACT-SH-003-02",
                action_type="MEMBER_VOUCHER_DRAFT",
                title="Create a consent-filtered 15% member voucher draft",
                owner_role="CRM Manager",
                target_system="CRM_CAMPAIGN_DRAFT",
                status="PENDING_APPROVAL",
                due_at=iso_after(20),
                requires_approval=True,
                required_approval_role="Merchandise Manager",
                idempotency_key=f"{case_id}:ACT-SH-003-02",
            ),
            ProposedAction(
                action_id="ACT-SH-003-03",
                action_type="MARKDOWN",
                title="Apply a 30% chain-wide markdown",
                owner_role="Pricing Manager",
                target_system="PRICING",
                status="BLOCKED",
                due_at=iso_after(24),
                requires_approval=True,
                required_approval_role="Finance Controller",
                idempotency_key=f"{case_id}:ACT-SH-003-03",
                retryable=False,
                rejection_reason="Projected margin falls below the approved floor.",
            ),
        ]
        case = RetailCase(
            case_id=case_id,
            case_type="SEASONAL_OVERSTOCK",
            dedupe_key="SEASONAL_OVERSTOCK:SH-014:SPR-JKT-BE-SM:2026-W31",
            title="Spring light jacket overstock",
            status="WAITING_FOR_APPROVAL",
            severity="high",
            region="china",
            city="Shanghai",
            store_id="SH-014",
            store_name="Shanghai Qibao Store",
            store_cluster="suburban_family",
            owner_role="Merchandise Manager",
            lead_agent="Inventory Agent",
            sla_due_at=iso_after(8),
            created_at=now,
            updated_at=now,
            as_of_time=now,
            planning_policy_version="MERCH-SPRING-EXIT-2026.07",
            consent_policy_version="PIPL-MKT-2026.02",
            variant=ProductVariant(
                style_id="SPR-JKT-2026",
                color_id="BEG",
                size_id="S-M",
                variant_id="SPR-JKT-2026-BEG-SM",
                gtin="06912345671015",
                product_name="Pocketable UV Protection Parka",
                color_name="Beige",
                lifecycle="clearance",
                category="womens_outerwear",
                unit_cost_cny=92,
                current_price_cny=249,
                margin_floor_pct=38,
            ),
            inventory=InventorySnapshot(
                physical_on_hand=physical,
                soft_reserved=reserved,
                safety_stock=safety,
                blocked_or_quarantined=blocked,
                returned_pending_inspection=65,
                sellable_atp=atp,
                future_atp=atp,
                demand_units_per_day=28,
                days_of_supply=round(atp / 28, 1),
                inventory_confidence=0.91,
                as_of_time=now,
                freshness_minutes=15,
            ),
            return_disposition={"pending_inspection": 65, "sellable": 18, "quarantined": 7, "return_to_vendor": 4},
            store_constraints={"backroom_capacity_units": 760, "backroom_utilization_pct": 92, "display_capacity_units": 84, "task_load_minutes": 160, "task_capacity_minutes": 180},
            evidence=[
                EvidenceItem(source="POS", observed_at=now, summary="Four-week rate of sale fell to 28 units/day after the season transition."),
                EvidenceItem(source="Returns", observed_at=now, summary="65 returned units await inspection and are excluded from ATP."),
                EvidenceItem(source="Store Task", observed_at=now, summary="Backroom utilization is 92%; additional inbound stock is blocked."),
            ],
            agent_decisions=[
                DomainDecision(agent="Inventory Agent", role="lead", status="COMPLETED", recommendation="Transfer 320 units to outlet demand before deeper markdown.", evidence_refs=["POS", "Returns", "Store Task"], confidence=0.91),
                DomainDecision(agent="Pricing Agent", role="required", status="COMPLETED", recommendation="Allow a targeted 15% voucher; block a 30% chain-wide markdown.", evidence_refs=["MERCH-SPRING-EXIT-2026.07"], confidence=0.95),
                DomainDecision(agent="Customer Understanding Agent", role="support", status="COMPLETED", recommendation="Build only a consented audience with recent light-outerwear intent.", evidence_refs=["PIPL-MKT-2026.02"], confidence=0.96),
                DomainDecision(agent="Personalization Agent", role="support", status="COMPLETED", recommendation="Recommend only sellable S/M variants at stores with confirmed ATP.", evidence_refs=["ATP", "Returns"], confidence=0.93),
                DomainDecision(agent="Marketing Agent", role="optional", status="DRAFT_ONLY", recommendation="Create a limited member-voucher draft; do not send before approval.", evidence_refs=["PIPL-MKT-2026.02", "ATP"], confidence=0.92),
            ],
            decision_packet=DecisionPacket(
                packet_id="DP-SH-003-V1",
                version=1,
                status="PENDING_APPROVAL",
                recommendation="Transfer 320 units first and prepare a targeted 15% member voucher; block the 30% markdown.",
                rationale=[
                    "Sellable ATP is 1,000 units and backroom utilization is 92%.",
                    "Returned units pending inspection are excluded from sellable supply.",
                    "A 30% markdown breaches the current margin floor.",
                ],
                alternatives=["Transfer only and reassess after seven days.", "Take no action and accept space and aging-stock cost."],
                blockers=["Chain-wide 30% markdown blocked by margin policy."],
                expires_at=iso_after(12),
                policy_version="retail-policy-2026.08",
                proposed_action_ids=[a.action_id for a in actions],
                required_approval_roles=["Merchandise Manager"],
            ),
            actions=actions,
            audit_log=[AuditEvent(time=now, actor="Case Formation Service", action="CASE_CREATED", detail="Aging stock and store-space thresholds breached")],
            kpi_observations={"decision_packet_minutes": 11, "blocked_margin_breach": True, "measurement_type": "demo_observed"},
        )
        return case.model_dump()

