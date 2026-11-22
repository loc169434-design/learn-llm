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
2. Read `ai_research_lab/PROGRESS_TRACKER.md` and `ai_research_lab/README.md` to check the user's daily self-trained AI & theory-first research lab progress (`day01` -> `day14`, modeled on TS. Bùi Thanh Hùng's papers in `research_thay_hung/`).
3. Read `docs/INTERVIEW_PLAYBOOK.md` for recent Android + AI interview notes.
4. Check the latest `lesson*.py` and `ai_research_lab/day*/lab*.py` files to see whether the user has finished the current `# TODO`s.

## Teaching Style & Strict Study Rules (User-Defined)
Always strictly follow these 3 classroom rules in every lesson/lab:
1. **Classroom Teacher Pacing (Chậm, cặn kẽ từng nửa bài):** Teach like a dedicated university professor at the whiteboard — explain *why* every concept/formula exists from first principles and intuition before code. Break each day into bite-sized halves (Tiết 1 / Tiết 2) rather than dumping everything at once.
2. **Interactive 5–7 MCQ Check:** After each theory section, embed a compact interactive HTML quiz widget (`5–7` multiple-choice questions with instant explanations) via `generative_ui` so the user verifies conceptual mastery before coding.
3. **15-Minute Independent Struggle Rule (Chỉ chỉ hướng, KHÔNG đưa code giải ngay):**
   - When assigning coding exercises (`# TODO`), give **ONLY directional hints** (problem goal, input/output, high-level logical steps, edge cases to watch for) — **NEVER give full copy-paste solution code upfront**!
   - Note the start time (15-minute focus window). During those 15 minutes, the user tries coding independently.
   - If the user asks for hints before 15 minutes are up without sharing their own attempt, gently remind them of the 15-minute rule and offer at most a tiny Socratic nudge. Only review/debug their code or reveal detailed implementation patterns after they share their own code attempt OR after 15 minutes of independent effort!

## Workflow When the User Says "ôn bài" / "học tiếp" / "làm bài tập"

### Step 1: Daily Interactive Review Widget (inside Antigravity Chat)
- Always read the built-in `generative_ui` skill first if not yet read in the conversation.
- Create an inline interactive HTML quiz artifact (`daily_review_quiz.html`) in the conversation's artifact directory (`<appDataDir>/brain/<conversation-id>/daily_review_quiz.html`) using `write_file` with `UserFacing: true` and `RequestFeedback: false`, and embed it inline using `<agent-embed>`.
- Keep the widget compact (`<= 450px` tall), themed with Antigravity CSS variables (`--foreground`, `--card`, `--card-border`, `--primary`, `--success`, `--error`, `--link`), and containing **3 questions**:
  1. **Câu 1 (MCQ):** AI / Backend / RAG interview question from the previous 1–3 lessons.
  2. **Câu 2 (MCQ):** Android Senior / Automation (`DriveSafeAI`) trade-off or internals question.
  3. **Câu 3 (Code Fill-in-the-Blank):** Fill 2 missing Python/Kotlin keywords in a realistic snippet.

### Step 2: Check Code & Guide Next Lesson / Research Lab Day
- Check both the active `ai_research_lab/dayXX_*/` lab and any active `lesson*.py`:
  - Explain **underlying theory first from intuition & math fundamentals** (`THEORY_DAYXX.md`), connecting directly to TS. Bùi Thanh Hùng's papers (`research_thay_hung/`).
  - If the current `labXX_*.py` (or `lesson*.py`) still has `NotImplementedError` (`# TODO`), guide the user and verify once done.
  - Once completed and verified, record empirical metrics into `ai_research_lab/PROGRESS_TRACKER.md`, scaffold the next `dayXX_*/` folder (`THEORY_DAYXX.md` + `labXX_*.py` with clear `# TODO`s), and update `STUDY_LOG.md` so the user can commit & push across machines.
