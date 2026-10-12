# Interactive demo upgrade

PromiseTrap remains on `promisetrap`. No commits, pushes, branch changes, PRs or submissions were performed during this upgrade.

The Investigation Gallery offers **12 interactive fictional cases, 8 newly added**, with **35 source documents** available as authored text and readable PNGs. The original internship, scholarship, optional-service and deadline scenario IDs remain supported. The scholarship now includes a separate eligibility document; the deadline case now contains three explicitly dated notices.

## Implemented experience

- A prominent searchable gallery with category filters, fictional badges, actual source previews, a flagship case and two negative controls.
- Separate authored walkthrough and Gemma image-analysis actions. Walkthrough claims run through the retained PromiseGraph engine. Image mode contains no authored claims and explicitly requests Gemma; it never falls back to Ollama. Explicit Ollama selection remains available.
- Contextual actions and an optional tour with Next, Back, Skip, Exit and Finish. Actions navigate existing tabs, actual findings and original sources. Tour checkmarks mean opened, not independently verified. Modal layout reserves space for tour controls.
- Backend-persisted confirmations of actual analysis operations, including cache reuse. No invented completion percentages or model streams.
- Clickable current-state finding counters, recent activity, linked conditions, and eligibility outcomes with supporting clauses.
- Promise Journey displays actual before/after quotations. Undated material remains labeled Document Sequence.
- PromiseLab offers applicable optional-certificate and guarantee-to-conditional presets, editable fields, explicit before/after field differences, and Decimal calculations for the hypothetical pair. Original evidence is preserved. New edits clear stale results; controls prevent concurrent sandbox edits during a request.
- Source metadata and claim saves show confirmations. Unavailable providers are explained; unavailable live challenges and analysis are disabled.
- Graph selection emphasizes relationships, with evidence navigation, filters, Zoom to fit and Reset view.
- Offline clarification generation, editing and copy confirmation; actual report and receipt downloads provide preparation/error feedback.

## Verification

- **105 backend/engine tests passed**; only existing upstream deprecation warnings remain.
- **8 frontend decision tests passed** (`npm run test --workspace apps/web`). These exercise the shared gallery filtering, contextual availability, real navigation targets and readable field-difference logic.
- **TypeScript and production build passed**.
- All 12 independent expected-result fixtures passed real FastAPI/PromiseGraph evaluation; results are in `evaluation-results.json`.
- Real Chrome checks: all 12 authored gallery launches, category/search/empty filters, flagship evidence and original image preview, acceptance/rejection/unresolved reviews with notes, tour navigation, calculator, fee and guarantee presets, Reset, stale-result removal, graph selection/filter/fit/reset, unknown/unmet/satisfied eligibility with supporting clause, metadata saving, claim confirmation/correction, offline draft generation/copy, provider-unavailable image launch, and safe restart.
- PDF, Markdown, JSON and receipt files were actually downloaded and confirmed present in Downloads. All report formats also passed API tests for each case. The browser download-event notification timed out; filesystem verification confirmed the saved files.
- Mobile gallery and PromiseLab checked at 390 × 844, with document width 390 and no horizontal page overflow. Temporary viewport override was reset. Screenshots are in `screenshots/demo-*.jpg`.
- Both controls produce **zero contradictions**: free registration with an optional INR 200 printed certificate, and the completely consistent offer. Historical average salary is not treated as a guaranteed individual salary; monthly/annual billing units do not create a numeric contradiction; equal deposits do not create a fee conflict.

## Limits

Live Gemma inference is **not verified**: this backend has no `GEMINI_API_KEY`. The live gallery action visibly reports the configuration error while retaining only original images and no claims. Existing mocked-provider tests remain separate from genuine cloud inference. Images require visual evidence review after real extraction.

Browser automation could not upload the comparison copy because the ChatGPT Chrome extension does not have file URL access. No extension settings were changed. API tests independently verify byte-identical/different-byte comparisons, original hashes and PDF raster navigation. This is an automation limitation, not evidence of a failed application upload.

The browser checks cover the controls listed above; they do not claim exhaustive testing of every existing ingestion permutation, operating system or external provider. Financial subtotals may exclude disputed obligations; a zero subtotal does not prove free participation. Matching hashes establish byte identity, not source authenticity.

## Modified files

- Backend: `apps/api/app/advanced_samples.py`, `apps/api/app/main.py`, `apps/api/tests/test_advanced_api.py`.
- Frontend: `apps/web/app/page.tsx`, `apps/web/app/globals.css`, `apps/web/components/InvestigationTools.tsx`, `apps/web/components/EvidenceGraph.tsx`, new `InvestigationGallery.tsx` and `InvestigationExperience.tsx`, `apps/web/lib/types.ts`, new `apps/web/lib/demo.ts`, new `apps/web/tests/demo.test.cjs`, `apps/web/package.json`.
- Samples: `scripts/generate_samples.py`, generated PNG/TXT sources and `examples/advanced/expected.json`.
- Documentation: `README.md`, `docs/evaluation.md`, `docs/demo-script.md`, `docs/evaluation-results.json`, this audit and four demo screenshots.

## Run locally

From the repository root, in two terminals:

```bash
.venv/bin/python -m uvicorn app.main:app --app-dir apps/api --host 127.0.0.1 --port 8000 --reload
```

```bash
npm run dev
```

Open http://127.0.0.1:3000. Both servers are running at the end of the implementation session. Walkthroughs require no model credentials. For live Gemma, set `GEMINI_API_KEY` in the backend environment and restart; do not relabel authored fixtures as model output.
