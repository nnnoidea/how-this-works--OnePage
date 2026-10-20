---
name: how-this-works-onepage
description: Explain a code, Skill, or documentation project in one source-backed visual page for a developer encountering it for the first time. Connect its purpose, main capabilities, cooperation and adoption conditions using an integrated renderer and source-validation tools.
---

# How This Works — OnePage

Produce a source-backed OnePage explanation of the requested project, in the user's language. The Agent handles research; this package supplies presentation and validation. No separate Answer Me with HTML installation is needed.

The result should let a reader unfamiliar with the project understand its purpose, main capabilities, how its parts cooperate, and the relevant design choices and limits. Identify the studied project and source version in the explanation. These are delivery outcomes, not prescribed research steps or a fixed page outline.

Use **one-page understanding as the default** for a general project explanation. Bound the learning objective to purpose, main capabilities, their cooperation in a representative use, and choices or conditions that materially affect suitability. Internal implementation catalogues, exhaustive options, and peripheral branches are outside that objective unless they change a central conclusion. This bounds the research depth, not just the length of the final prose. Any source remains available for resolving consequential uncertainty; do not impose a file whitelist or omit a major capability. Deliver one readable overview page, without a fixed word or panel quota. Readers can use the draft and sources to ask an Agent follow-up questions; the first page need not explain every implementation detail.

## Create or extend the study

Write the explanation as editable Markdown with source citations. Use [Visual format](references/visual-format.md) for the bundled components; let the material determine the structure. Keep the draft alongside its HTML. Do not cut substantive content merely to fit a panel count. Existing drafts can be clarified or locally revised without rebuilding a research database.

**Explain each substantive point visually by default, including in onepage studies.** Show the objects and relationships, participants and exchanges, or inputs and changes that make the point understandable. Use prose to explain the visual and supply conditions, evidence, and limits. Clear prose alone is not a reason to omit a visual. Several related points can share a visual; there is no diagram count or type quota. A single overview flow does not cover other mechanisms merely mentioned in prose. Boxes of paragraphs and before/after text tables are not substitutes for showing the relationships or changes. Keep a point primarily textual only when it genuinely cannot be usefully visualized, and briefly explain that exception in the delivery notes. Do not drop a material point to avoid visualizing it or invent relationships, order, quantities, or outcomes to fill a diagram. Label illustrative examples as such.

Render each draft with Node.js 20+:

```sh
node SKILL_DIR/scripts/render.mjs DRAFT.md OUTPUT.html --source-dir SOURCE_CHECKOUT
```

Replace `SKILL_DIR` with this folder's absolute path. `--source-dir` selects the local files for embedded code; omit it when no code is embedded or the working directory is already correct. It does not verify the checkout's revision. The bundled renderer needs no dependency installation, browser launch, or update check. Reuse output paths when revising. Read rendering diagnostics; layout and syntax are handled by the renderer, not hand-written HTML/CSS/SVG.

## Validate the result

Checks use Python 3.9+; source checks also require Git with `--no-lazy-fetch`. For GitHub source links in one or more Markdown drafts:

```sh
python3 SKILL_DIR/scripts/check_sources.py DRAFT.md --repo OWNER/NAME GIT_DIR
```

Repeat `--repo` for multiple repositories. It checks fixed commits, paths, and line bounds offline, including citations from separate branches. It does not establish whether cited versions support the account or verify a local repository's remote provenance. Add `--evidence-url 'CITATION_URL'` for selected source excerpts, repeating it as needed; all supported source links are still checked. `--evidence` exports every excerpt when wanted. Whole-file and commit links have no line excerpt. Other source formats need direct verification.

After rendering the study's pages, check their local links and anchors:

```sh
python3 SKILL_DIR/scripts/check_pages.py OUTPUT_DIRECTORY --entry index.html
```

This also lists pages unreachable through verified links from the entry. Root-relative links are unverified without deployment context. Point it at the study being delivered, not a directory of archived experiments. External links and JavaScript interactions are not checked. Script `--help` describes available arguments.

Check whether sources support the explanations and diagrams and whether the result omits something material to the user's request. Exercise the rendered reading route and links. Distinguish incorrect explanations, inaccurate citations, omissions, and presentation issues; fix supported findings and recheck the affected parts. Script success does not certify meaning, completeness, or usability.

Review each substantive explanation point against the rendered visuals: can the reader see the relationship or change being explained, and does the visual help them follow it? Check the reasons for any text-only points. Do not substitute prose polish, diagram counts, or component variety for this review; a diagram that merely repeats labels or implies unsupported behavior does not meet the requirement.

Deliver the page link, editable draft, and material limitations.
