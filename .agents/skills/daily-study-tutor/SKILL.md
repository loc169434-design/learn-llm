---
name: daily-study-tutor
description: >-
  Use this skill whenever the user opens the learn-llm workspace on any machine and
  asks to continue studying ("học tiếp", "ôn bài", "làm bài tập", "review", "kiểm tra bài cũ"),
  or asks for their interactive daily quiz widget.
---

# Daily Study Tutor & Interactive Quiz Workflow (`learn-llm`)

This skill keeps the user's learning progress, daily interactive review quizzes, and interview prep synchronized across machines via Git.

## Context Files to Read First
1. Read `STUDY_LOG.md` to check the latest completed lessons (`lesson*.py`) and current module status.
2. Read `docs/INTERVIEW_PLAYBOOK.md` for recent Android + AI interview notes.
3. Check the latest `lesson*.py` files in the workspace root (`ls lesson*.py`) to see whether the user has finished the current `# TODO`s.

## Workflow When the User Says "ôn bài" / "học tiếp" / "làm bài tập"

### Step 1: Daily Interactive Review Widget (inside Antigravity Chat)
- Always read the built-in `generative_ui` skill first if not yet read in the conversation.
- Create an inline interactive HTML quiz artifact (`daily_review_quiz.html`) in the conversation's artifact directory (`<appDataDir>/brain/<conversation-id>/daily_review_quiz.html`) using `write_file` with `UserFacing: true` and `RequestFeedback: false`, and embed it inline using `<agent-embed>`.
- Keep the widget compact (`<= 450px` tall), themed with Antigravity CSS variables (`--foreground`, `--card`, `--card-border`, `--primary`, `--success`, `--error`, `--link`), and containing **3 questions**:
  1. **Câu 1 (MCQ):** AI / Backend / RAG interview question from the previous 1–3 lessons.
  2. **Câu 2 (MCQ):** Android Senior / Automation (`DriveSafeAI`) trade-off or internals question.
  3. **Câu 3 (Code Fill-in-the-Blank):** Fill 2 missing Python/Kotlin keywords in a realistic snippet.

### Step 2: Check Code & Guide Next Lesson
- If the current `lesson*.py` still has `NotImplementedError` (`# TODO`), briefly remind the user what to implement and verify it once done.
- If the current lesson is completed and passes when run with `uv run python ...` / `uv run pytest`, scaffold the next lesson (`lessonXX.py`) with clear `# TODO`s, Kotlin analogies, and update `STUDY_LOG.md` (plus `docs/INTERVIEW_PLAYBOOK.md` if applicable) so the user can commit & push before switching computers.
