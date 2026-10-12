"""Explicit fictional structured fixtures. Never presented as Gemma output."""
import json
from datetime import date
from pathlib import Path

from promisegraph.advanced.matching import analyze
from promisegraph.advanced.provenance import fingerprint
from promisegraph.advanced.schemas import Claim, Criterion, Investigation, Scope, Source, Stage, now
from promisegraph.advanced.verification import validate_anchor


SAMPLES = Path(__file__).resolve().parents[3] / "examples" / "advanced"


def scope(purpose="registration", stage="registration"):
    return Scope(program="fictional nova 2026", audience="all registered applicants", purpose=purpose, period="2026 intake", application_stage=stage, contractual_condition="nova 2026 terms", qualifying_event="registration")


def spec(text, category, subject, predicate, **kwargs):
    return {"original_text": text, "normalized_statement": text, "category": category, "subject": subject, "predicate": predicate, "uncertainty": "low", **kwargs}


DATASETS = {
    "internship": [
        {"name": "internship-advertisement", "stage": "advertisement", "title": "Nova Internship • Advertisement", "claims": [
            spec("Registration is completely free.", "fee", "registration", "cost", amount="0", currency="INR", unit="one_time", modality="guaranteed", value_kind="exact", financial_role="fee"),
            spec("Guaranteed stipend ₹20,000 per month.", "compensation", "stipend", "payment", amount="20000", currency="INR", unit="month", modality="guaranteed", value_kind="exact", financial_role="compensation", scope=scope("stipend", "participation").model_dump()),
            spec("Certificate guaranteed to all registered applicants.", "certificate", "certificate", "issuance", modality="guaranteed", scope=scope("certificate", "completion").model_dump())]},
        {"name": "internship-registration", "stage": "registration", "title": "Nova Internship • Registration", "claims": [
            spec("A mandatory processing fee of ₹499 is due upfront for registration.", "fee", "registration", "cost", amount="499", currency="INR", unit="one_time", modality="mandatory", value_kind="exact", financial_role="fee", payment_timing="upfront")]},
        {"name": "internship-offer", "stage": "offer", "title": "Nova Internship • Offer terms", "claims": [
            spec("Stipend up to ₹20,000 per month, subject to performance evaluation.", "compensation", "stipend", "payment", amount="20000", currency="INR", unit="month", modality="conditional", value_kind="maximum", conditions=["Performance evaluation"], financial_role="compensation", scope=scope("stipend", "participation").model_dump()),
            spec("Certificates issued only after successful evaluation and 80% attendance.", "certificate", "certificate", "issuance", modality="conditional", conditions=["Successful evaluation", "80% attendance"], scope=scope("certificate", "completion").model_dump())]}],
    "scholarship": [
        {"name": "scholarship-advertisement", "stage": "advertisement", "title": "Nova Scholarship • Advertisement", "claims": [spec("Guaranteed 100% tuition coverage for all registered applicants.", "scholarship", "tuition", "coverage", amount="100", unit="percent", modality="guaranteed", value_kind="exact", scope=scope("tuition", "award").model_dump())]},
        {"name": "scholarship-terms", "stage": "agreement", "title": "Nova Scholarship • Terms", "claims": [
            spec("Tuition coverage is capped at ₹100,000; applicable course tuition is ₹150,000.", "scholarship", "tuition", "coverage", amount="100000", currency="INR", unit="one_time", applicable_cost="150000", modality="conditional", value_kind="maximum", conditions=["Funding cap ₹100,000"], financial_role="coverage", scope=scope("tuition", "award").model_dump()),
            spec("Applicants must be in year 4 of their degree.", "eligibility", "applicant", "year", modality="mandatory", criteria=[Criterion(field="year_of_study", operator="equals", value="4").model_dump()], conditions=["Year 4 of degree"])]}],
    "optional": [
        {"name": "optional-advertisement", "stage": "advertisement", "title": "Nova Workshop • Advertisement", "claims": [spec("Registration is free.", "fee", "registration", "cost", amount="0", currency="INR", unit="one_time", modality="guaranteed", value_kind="exact", financial_role="fee")]},
        {"name": "optional-terms", "stage": "agreement", "title": "Nova Workshop • Optional extras", "claims": [spec("An optional printed certificate costs ₹200.", "fee", "printed certificate", "cost", amount="200", currency="INR", unit="one_time", modality="optional", value_kind="exact", financial_role="fee", scope=scope("printed certificate", "completion").model_dump())]}],
    "deadline": [
        {"name": "deadline-v1", "stage": "advertisement", "date": "2026-10-01", "title": "Nova announcement • Version 1", "claims": [spec("Application deadline is October 15, 2026.", "deadline", "application", "deadline", date_value="2026-10-15", modality="mandatory")]},
        {"name": "deadline-v2", "stage": "advertisement", "date": "2026-10-05", "title": "Nova announcement • Version 2", "claims": [spec("Application deadline is October 20, 2026.", "deadline", "application", "deadline", date_value="2026-10-20", modality="mandatory")]}],
}


# Catalog metadata describes questions to investigate, never computed findings.
CATALOG = {
    "internship": {"title": "The Internship That Wasn't Free", "domain": "Recruitment", "summary": "A free application becomes a paid commitment, and two guarantees acquire conditions.", "issues": ["Mandatory payment", "Conditional stipend", "Certificate requirements"], "capability": "Promise Journey + PromiseLab", "featured": True},
    "scholarship": {"title": "The Scholarship With a Hidden Cap", "domain": "Education", "summary": "Full tuition coverage meets a funding ceiling and a final-year eligibility rule.", "issues": ["Coverage cap", "Eligibility"], "capability": "FinePrint Radar + Personal Reality"},
    "subscription": {"title": "The Lifetime Subscription That Expires", "domain": "Technology", "summary": "Lifetime access, upgrades and refunds receive precise restrictions in the contract.", "issues": ["Access expiry", "Paid upgrades", "Refund conditions"], "capability": "ConditionChain"},
    "placement": {"title": "The Guaranteed Placement Promise", "domain": "Education", "summary": "Placement assistance and historic salary averages require careful interpretation.", "issues": ["Placement guarantee", "Historical average", "Eligibility"], "capability": "ScopeGuard + Personal Reality"},
    "event": {"title": "The Event That Changed Its Rules", "domain": "Events", "summary": "A fictional showcase adds an entry fee and narrows certificate eligibility.", "issues": ["Entry fee", "Winner-only certificates", "Eligibility"], "capability": "Evidence Lens + Promise Journey"},
    "deadline": {"title": "The Moving Application Deadline", "domain": "Recruitment", "summary": "Three dated notices document revisions rather than simultaneous contradictions.", "issues": ["Version ordering", "Updated deadline"], "capability": "Promise Drift"},
    "deposit": {"title": "The Refundable Deposit Dispute", "domain": "Contracts", "summary": "A refundable reservation deposit meets cancellation windows and exclusions.", "issues": ["Refund exclusions", "Cancellation window"], "capability": "Reality Calculator + FinePrint Radar"},
    "software": {"title": "The Software Plan With Unexpected Limits", "domain": "Technology", "summary": "An unlimited plan introduces request limits and separately billed exports.", "issues": ["Usage limits", "Feature charges", "Billing units"], "capability": "ScopeGuard + Reality Calculator"},
    "job": {"title": "The Job Offer With Changing Compensation", "domain": "Recruitment", "summary": "Fixed pay and a joining bonus turn into base pay and conditional incentives.", "issues": ["Fixed vs variable pay", "Conditional bonus", "Work arrangement"], "capability": "Promise Journey + Devil’s Advocate"},
    "price": {"title": "The Promotional Price Trap", "domain": "Consumer services", "summary": "A final advertised price differs from checkout, while optional extras remain separate.", "issues": ["Final payable total", "Discount eligibility", "Optional extras"], "capability": "Financial comparison + ScopeGuard"},
    "optional": {"title": "The Apparently Contradictory Workshop", "domain": "Control cases", "summary": "Free registration and an optional printed certificate concern different services.", "issues": ["Optional vs mandatory", "Service scope"], "capability": "ScopeGuard negative control", "control": True},
    "consistent": {"title": "The Completely Consistent Offer", "domain": "Control cases", "summary": "Three documents agree on registration, certificate terms and the deadline.", "issues": ["Aligned commitments"], "capability": "Evidence-backed consistency", "control": True},
}


def scoped(text, category, subject, predicate, purpose=None, **kwargs):
    kwargs.setdefault("scope", scope(purpose or subject, "participation").model_dump())
    return spec(text, category, subject, predicate, **kwargs)


def money(text, subject, amount, modality="mandatory", category="fee", **kwargs):
    kwargs.setdefault("value_kind", "exact")
    kwargs.setdefault("financial_role", "compensation" if category == "compensation" else "fee")
    kwargs.setdefault("unit", "one_time")
    return scoped(text, category, subject, "payment", amount=amount, currency="INR", modality=modality, **kwargs)


def doc(name, stage, title, claims, **metadata):
    return {"name": name, "stage": stage, "title": title, "claims": claims, **metadata}


# Retain all original scenario IDs. Add an eligibility document and a dated notice.
criteria = DATASETS["scholarship"][1]["claims"].pop()
DATASETS["scholarship"].insert(1, doc("scholarship-eligibility", "selection", "Nova Scholarship • Eligibility", [criteria]))
DATASETS["deadline"].append(doc("deadline-notice", "agreement", "Nova announcement • Official update", [spec("Application deadline is October 25, 2026.", "deadline", "application", "deadline", date_value="2026-10-25", modality="mandatory")], date="2026-10-09"))

DATASETS.update({
    "subscription": [
        doc("subscription-ad", "advertisement", "Nova Studio • Lifetime pass", [
            scoped("Lifetime access is guaranteed with no expiry.", "access", "studio access", "availability", modality="guaranteed"),
            scoped("All future upgrades are guaranteed to be included.", "access", "upgrades", "inclusion", modality="guaranteed"),
            scoped("A full refund is guaranteed at any time.", "other", "subscription refund", "refund", modality="guaranteed")]),
        doc("subscription-plan", "registration", "Nova Studio • Plan details", [
            scoped("Studio access is conditional on an active pass and expires on December 31, 2027.", "access", "studio access", "availability", modality="conditional", conditions=["Active pass", "Expires December 31, 2027"]),
            money("Major-version upgrades cost INR 1200 and are optional.", "upgrades", "1200", "optional")]),
        doc("subscription-terms", "agreement", "Nova Studio • Refund and upgrade terms", [
            scoped("Major upgrades are included only if the upgrade payment is made.", "access", "upgrades", "inclusion", modality="conditional", conditions=["Upgrade payment"]),
            scoped("A refund is available only within 14 days and before activation.", "other", "subscription refund", "refund", modality="conditional", conditions=["Within 14 days", "Before activation"])])],
    "placement": [
        doc("placement-ad", "advertisement", "Nova Academy • Career programme", [
            scoped("Placement is guaranteed for every enrolled applicant.", "placement", "placement", "outcome", modality="guaranteed"),
            money("Historical average salary was INR 600000 per year; individual pay is not guaranteed.", "historic salary", "600000", "possible", category="compensation", unit="year", value_kind="unspecified")]),
        doc("placement-enrollment", "registration", "Nova Academy • Enrollment agreement", [
            scoped("Placement assistance is subject to assessment; employment is not guaranteed.", "placement", "placement", "outcome", modality="conditional", conditions=["Assessment", "Employer selection"]),
            scoped("Applicants must have academic score at least 70.", "eligibility", "applicant score", "eligibility", modality="mandatory", conditions=["Academic score at least 70"], criteria=[Criterion(field="academic_score", operator="at_least", value="70").model_dump()])]),
        doc("placement-policy", "agreement", "Nova Academy • Placement policy", [
            money("INR 600000 per year is a historical average only, subject to individual employer offers.", "historic salary", "600000", "conditional", category="compensation", unit="year", value_kind="unspecified", conditions=["Individual employer offer"]),
            scoped("Placement participation requires year 4 of study.", "eligibility", "applicant year", "eligibility", modality="mandatory", conditions=["Year 4"], criteria=[Criterion(field="year_of_study", operator="equals", value="4").model_dump()])])],
    "event": [
        doc("event-ad", "advertisement", "Nova Showcase • Invitation", [
            money("Entry is free with a final payable amount of INR 0.", "event entry", "0", "guaranteed"),
            scoped("Certificates are guaranteed to all participants.", "certificate", "event certificate", "issuance", modality="guaranteed")]),
        doc("event-registration", "registration", "Nova Showcase • Entry rules", [
            money("A mandatory entry payment of INR 350 is due upfront.", "event entry", "350", payment_timing="upfront")]),
        doc("event-terms", "agreement", "Nova Showcase • Participation terms", [
            scoped("Certificates are issued only to competition winners.", "certificate", "event certificate", "issuance", modality="conditional", conditions=["Competition winner"]),
            scoped("Participants must be in year 3 of study.", "eligibility", "event applicant", "eligibility", modality="mandatory", conditions=["Year 3"], criteria=[Criterion(field="year_of_study", operator="equals", value="3").model_dump()])])],
    "deposit": [
        doc("deposit-ad", "advertisement", "Nova Retreat • Reservation offer", [
            money("A mandatory deposit of INR 5000 is due upfront.", "reservation deposit", "5000", financial_role="deposit", payment_timing="upfront", refundable=True),
            scoped("The reservation deposit is guaranteed fully refundable at any time.", "other", "reservation refund", "refund", modality="guaranteed", refund_terms="fully refundable at any time")]),
        doc("deposit-payment", "registration", "Nova Retreat • Payment terms", [
            money("A mandatory deposit of INR 5000 is due upfront.", "reservation deposit", "5000", financial_role="deposit", payment_timing="upfront", refundable=True)]),
        doc("deposit-refund", "agreement", "Nova Retreat • Cancellation policy", [
            scoped("Deposit refunds are conditional on cancellation at least 7 days before arrival; no-shows are excluded.", "other", "reservation refund", "refund", modality="conditional", conditions=["Cancellation at least 7 days before arrival", "No-show excluded"], refund_terms="cancellation at least 7 days before arrival; no-shows are excluded")])],
    "software": [
        doc("software-plans", "advertisement", "Nova Cloud • Plan comparison", [
            scoped("Unlimited API access is guaranteed without usage restrictions.", "access", "api access", "availability", modality="guaranteed"),
            money("Data exports are included with a payable charge of INR 0.", "data export", "0", "guaranteed"),
            money("The plan costs INR 900 per month.", "plan price", "900", unit="month")]),
        doc("software-usage", "agreement", "Nova Cloud • Usage policy", [
            scoped("API access is conditional on the monthly limit of 10000 requests.", "access", "api access", "availability", modality="conditional", conditions=["10000 requests per month"])]),
        doc("software-billing", "registration", "Nova Cloud • Billing details", [
            money("Data exports require a mandatory payment of INR 300 upfront.", "data export", "300", payment_timing="upfront"),
            money("The annual plan costs INR 10800 per year.", "plan price", "10800", unit="year")])],
    "job": [
        doc("job-listing", "advertisement", "Nova Works • Analyst listing", [
            money("Fixed guaranteed compensation is INR 60000 per month.", "monthly pay", "60000", "guaranteed", category="compensation", unit="month"),
            money("A joining bonus of INR 50000 is guaranteed.", "joining bonus", "50000", "guaranteed", category="compensation"),
            scoped("Remote work is guaranteed for this role.", "other", "work arrangement", "location", modality="guaranteed")]),
        doc("job-recruiter", "selection", "Nova Works • Recruiter note", [
            money("Base compensation is INR 40000 per month; fixed and guaranteed.", "monthly pay", "40000", "guaranteed", category="compensation", unit="month"),
            money("Optional incentives up to INR 20000 per month are subject to sales targets.", "sales incentives", "20000", "conditional", category="compensation", unit="month", value_kind="maximum", conditions=["Sales targets"])]),
        doc("job-offer", "offer", "Nova Works • Offer letter", [
            money("The joining bonus of INR 50000 is subject to 6 months of continuous service.", "joining bonus", "50000", "conditional", category="compensation", conditions=["6 months continuous service"]),
            scoped("Remote work is conditional on manager approval; otherwise office attendance is required.", "other", "work arrangement", "location", modality="conditional", conditions=["Manager approval"])])],
    "price": [
        doc("price-ad", "advertisement", "Nova Market • Headphone offer", [
            money("The final payable price is guaranteed INR 999 including all mandatory charges.", "headphone final total", "999", "guaranteed")]),
        doc("price-checkout", "registration", "Nova Market • Checkout", [
            money("The final payable total is mandatory INR 1098 due upfront, including item price and handling; no other mandatory charge applies.", "headphone final total", "1098", payment_timing="upfront"),
            money("An optional gift-wrap service costs INR 50.", "gift wrap", "50", "optional")]),
        doc("price-conditions", "agreement", "Nova Market • Offer conditions", [
            scoped("The separate student discount requires year 4 of study; it does not change the documented undiscounted final total.", "eligibility", "student discount", "eligibility", modality="mandatory", criteria=[Criterion(field="year_of_study", operator="equals", value="4").model_dump()], conditions=["Year 4 of study"])])],
    "consistent": [doc("consistent-"+suffix, stage, "Nova Open Workshop • "+title, [
        spec("Registration is free.", "fee", "registration", "cost", amount="0", currency="INR", unit="one_time", modality="mandatory", value_kind="exact", financial_role="fee"),
        scoped("A digital certificate is guaranteed to all registered applicants.", "certificate", "digital certificate", "issuance", modality="guaranteed"),
        spec("Application deadline is October 30, 2026.", "deadline", "application", "deadline", date_value="2026-10-30", modality="mandatory")])
        for suffix, stage, title in [("ad", "advertisement", "Advertisement"), ("form", "registration", "Registration form"), ("terms", "agreement", "Terms")]],
})

# Independent expectations for the retained API engine (which omits consistent pairs).
EXPECTED = {
    "internship": ["contradiction"] * 3,
    "scholarship": ["contradiction"],
    "optional": [],
    "deadline": ["changed_term"] * 3,
    "subscription": ["contradiction"] * 3,
    "placement": ["contradiction", "material_qualification"],
    "event": ["contradiction"] * 2,
    "deposit": ["contradiction"],
    "software": ["contradiction", "contradiction", "insufficient_evidence"],
    "job": ["contradiction"] * 3,
    "price": ["contradiction"],
    "consistent": [],
}


def document(item):
    return "FICTIONAL SAMPLE — NOT A REAL ORGANIZATION OR OFFER\n\n" + item["title"] + ("\nPublished: "+item["date"] if item.get("date") else "") + "\n\n" + "\n\n".join(c["original_text"] for c in item["claims"]) + "\n\nScope: Nova 2026 program, all registered applicants, 2026 intake, Nova 2026 terms.\nUnless explicitly qualified above, all statements refer to the same qualifying event: registration.\nNo publication or effective date is claimed unless supplied in the sample metadata.\n"

