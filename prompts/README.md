# Prompt Layer

Keep prompts as versioned files, separate from provider SDK code.

Recommended future files:
- system_teacher.md
- context_analyzer.md
- presentation_planner.md
- explanation_composer.md
- verifier.md

Rules:
- prompts must not hard-code volatile model names;
- prompts must not assume a specific provider;
- prompt changes require benchmark runs;
- use compact, explicit output contracts;
- never ask the model for pixel-perfect page layout.
