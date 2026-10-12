# PromiseTrap submission materials

Status: prepared; final organizer PR and MLH entry have not been submitted.

## Name and pitch

**PromiseTrap - Every promise deserves evidence.**

Investigate the gap between promises and fine print with multimodal AI, traceable evidence, and an original open-source comparison engine.

## Team

- Shoaib: https://github.com/shoaib2000857
- Omar: https://github.com/DevXOmar
- Jinal: https://github.com/jinaljpt
- Hansika: https://github.com/a-hansika

The team confirmed that the organizer-authorized build window had started. Development was assisted by Codex with GPT-6.1 Sol, as disclosed by the team.

## Links

- Public application: https://github.com/shoaib2000857/PromiseTrap
- MIT license: https://github.com/shoaib2000857/PromiseTrap/blob/main/LICENSE
- Frontend preview: https://promisetrap.vercel.app (frontend only; full investigations run locally)
- Screenshots: https://github.com/shoaib2000857/PromiseTrap/tree/main/docs/screenshots
- Original engine: https://github.com/shoaib2000857/PromiseTrap/tree/main/packages/promisegraph
- Live Gemma result: https://github.com/shoaib2000857/PromiseTrap/blob/main/docs/live-gemma-internship.json
- Demo video: not yet supplied; the team will add it.

## Description

Advertisements, registration forms, and offer letters often describe the same opportunity differently. PromiseTrap helps students, applicants, and consumers inspect those differences before committing money or time.

Upload original images, screenshots, PDFs, emails, or text. Gemma 4 extracts structured promises and conditions. Our original PromiseGraph engine normalizes monetary values, checks scope and optional services, compares claims, verifies quotations, and traces each finding to its evidence.

The investigation workspace offers side-by-side quotations, interactive evidence graphs, Promise Journey timelines, a Reality Calculator separating guaranteed and conditional compensation, condition dependencies, and analyst review. PromiseLab reruns comparisons against hypothetical structured changes without changing original evidence. Clarification drafts and hashed receipts support follow-up; dossiers export as PDF, Markdown, and JSON.

Findings investigate claims rather than people. Image-only quotations require visual review. Synthetic examples disclose authored extraction, and actual provider runs carry distinct provenance. An explicit Ollama option supports local inference without silently replacing Gemma 4.

## Technologies

Gemma 4 (gemma-4-26b-a4b-it), Gemini API, Google GenAI Python SDK, Ollama (gemma3:4b by default), Python, FastAPI, Pydantic, SQLite, Next.js, React, TypeScript, React Flow, Lucide, PyMuPDF, Pillow, ReportLab, pytest, and Vercel (frontend).

Runtime AI: Gemma and Ollama. Gemini API is the transport for the Gemma model; this application does not silently substitute a Gemini model.

AI coding tool: Codex. Coding model disclosed by the team: GPT-6.1 Sol.

## Category answers

### Best Use of Gemma 4

PromiseTrap uses gemma-4-26b-a4b-it through the Gemini API for structured extraction from text, images, and rendered PDF pages, and for bounded semantic review of ambiguous comparisons. A real run on 12 October 2026 at 14:53 IST processed three fictional PNG sources, extracted six claims, and produced three PromiseGraph findings; the actual result is published with image-evidence limitations.

### Best Open-Source AI Project

PromiseTrap combines open-weight AI with our original MIT-licensed PromiseGraph engine for scope-aware claim comparison, financial calculations, quotation verification, and provenance. The reusable engine runs independently of model credentials, and an explicit Ollama provider enables local inference.

## Validation and demo

77 engine/API tests passed after the enhancement pull. TypeScript checks and production builds passed. The recorded Gemma image run is actual provider extraction from fictional sources, not authored claims; it is one scenario and does not establish general accuracy. Image-only evidence remains approximate and needs review.

Follow the README to run the Python API and frontend locally. Use the real image scenario and [demo script](demo-script.md) for a full walkthrough. The Vercel link is a frontend preview only. TattvaDrishti inspired ingestion, batch analysis, source tracing, and descriptive pattern analysis; no supplied source code or weights were copied.

## Remaining submission actions

Add the team's demo video if available. Open the prepared submission-only branch as a PR to the organizer repository when ready; maintainers handle its merge. One team member must also submit the separate MLH platform form: https://www.mlh.com/events/hacktoberfest-hack-day-hyderabad-x-niat/submissions/new.

Announced form deadline: 13 October 2026, 7:30 PM IST. Final eligibility is determined by the organizers.
