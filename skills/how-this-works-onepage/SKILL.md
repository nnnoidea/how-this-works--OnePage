---
name: how-this-works-onepage
description: "Understand and explain projects, repositories, codebases, libraries, frameworks, Skills, and documentation through a source-backed visual OnePage. Use when the user asks to explain a project, understand a repository, learn how it works, get oriented in unfamiliar source code, map its architecture, understand design choices or key mechanisms, or judge what it can do and whether it fits a need. Applies to GitHub links and local projects, including requests for project walkthroughs, architecture overviews, and visual explanations. Activate for project-learning intent even when the user does not mention HTML, a webpage, visualization, or OnePage. Also use when explicitly asked for HTW or How This Works. Keep isolated bug fixes and implementation tasks outside this scope unless project understanding is requested."
---

# How This Works — OnePage

Produce a source-backed OnePage explanation of the requested project, in the user's language. The Agent handles research; this package supplies presentation and validation. No separate Answer Me with HTML installation is needed.

The result should let a reader unfamiliar with the project understand what it is, its purpose and boundaries, main capabilities, how its parts cooperate, and the relevant design choices and limits. Identify the studied project and source version in the explanation.

## Plan a connected reading path

Before drafting, plan the page's questions together along this progression: **definition → uses and capability scope → external relationships → internal architecture → selected mechanisms → a representative collaboration scenario**. Let each answer prepare the reader for the next:

1. **Define the project.** Briefly name its concrete form and main responsibility, establishing what kind of thing the reader is looking at.
2. **Show its uses and capability scope as a whole.** Connect complete user needs to supported outcomes, adoption conditions, and work the user must still supply. Choose complementary needs that reveal different sides of suitability or delivery, with perspectives and number determined by the material. Distinguish built-in capabilities, integrations, and user configuration. This locates the project within its category; a feature list or examples that merely change the input domain do not establish that scope.
3. **Show external relationships.** Use the [project boundary template](references/visual-format.md#project-boundary-template): one explicit box named for the studied project, its outward-facing responsibilities inside, and users and collaborating systems outside. Label the exchanges across that box. These responsibility boundaries complement the capability scope; expand internal architecture in the next part.
4. **Explain internal architecture.** Open the project boundary to show its main parts, their responsibilities, and their connections. Give the reader an overall structure in which to place the subsequent details, organized by how the system works.
5. **Develop selected mechanisms where useful.** Expand mechanisms that support a main use, explain an important design choice, or clarify behavior that affects results. Explain their purpose, operation, and relevant conditions. Give architecture and mechanisms enough space to make the design understandable; their depth follows the project.
6. **Bring the parts together in a representative scenario.** Trace an input or task through the architecture and mechanisms already introduced to its result. Connect the external exchanges to the internal handoffs, showing how the parts cooperate. Use this walkthrough to consolidate the explanation rather than substitute for the architecture.

Use this as a reading progression, with sections merged or expanded to suit the material. Research remains flexible, and planning can stay internal. Keep each section focused on a coherent question; do not bundle unrelated leftover topics. Ground scope and limits in the sources rather than inventing exclusions or uniqueness claims.

Use **one-page understanding as the default** for a general project explanation. Focus research on the project's scope, architecture, meaningful mechanisms, their cooperation, and conditions that affect suitability. Read further wherever uncertainty could change a central conclusion. Deliver one readable page with enough explanation for that objective; exhaustive implementation catalogues and peripheral options can remain for follow-up. Readers can use the draft and sources to ask an Agent further questions. Let the material set the depth and length, without a file whitelist or fixed word or panel quota.

## Create or extend the study

Write the planned explanation as editable Markdown with source citations. Use [Visual format](references/visual-format.md) for the bundled components. Keep the draft alongside its HTML. Existing drafts can be clarified or locally revised.

**Explain each substantive point visually by default, including in onepage studies.** Show the objects and relationships, participants and exchanges, or inputs and changes that make the point understandable. Use prose to explain the visual and supply conditions, evidence, and limits. Related points can share a visual when it explains their relationships; choose the number and types from the material. Give mechanisms their own visual explanation where the overview leaves them unexplained. Boxes of paragraphs and before/after text tables are not substitutes for showing relationships or changes. Keep a point primarily textual only when visualization would not help, and briefly explain the exception in the delivery notes. Preserve material points and ground every visual relationship in evidence; do not invent behavior to fill a diagram. Label illustrative examples as such.

Render each draft with Node.js 20+:

```sh
node SKILL_DIR/scripts/render.mjs DRAFT.md OUTPUT.html --source-dir SOURCE_CHECKOUT
```

Replace `SKILL_DIR` with this folder's absolute path. `--source-dir` selects the local files for embedded code; omit it when no code is embedded or the working directory is already correct. It does not verify the checkout's revision. The bundled renderer needs no dependency installation, browser launch, or update check. Reuse output paths when revising. Read rendering diagnostics; layout and syntax are handled by the renderer, not hand-written HTML/CSS/SVG.

## Write for quick understanding

Adapt Answer Me with HTML's STE100-inspired writing principles for project explanations; this is not full ASD-STE100 conformance.

- Name sections with concrete objects and familiar actions so readers can anticipate the content. Use a question or a statement that matches what the section explains; keep internal planning terminology out of reader-facing titles. Lead with the answer or concrete question, then develop it.
- Keep sentences that add understanding. Remove preambles, promotional claims, research narration, and closing summaries that add no information.
- Give each sentence one main point. Prefer a named actor and a direct verb: “The runner calls the model,” not “Model invocation is performed.” Keep conditions close to the behavior they qualify.
- Use familiar words. Explain necessary technical terms on first use, then use the same name in prose and diagrams. Replace vague abstractions with who does what to which object.
- Make paragraphs develop one idea. Split overloaded sentences while preserving causal links, prerequisites, and limits.
- Let prose explain what the reader should understand from the diagram, including why a relationship matters, rather than recounting each node and arrow.
- State uncertainty precisely: separate observed implementation, author claims, illustrative examples, and unverified behavior. Put shared study limitations together rather than repeating them in each section.
- Keep diagram labels short and concrete, with essential conditions next to the relevant relationship. Treat renderer writing warnings as revision hints, not a score to optimize or a reason to delete meaning. Adapt to the output language rather than enforcing English word limits on Chinese.

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
