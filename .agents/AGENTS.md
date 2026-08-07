# ATS Project Rules

## RULE 1: Self-Learning Loop — Read Before Acting, Learn After Every Correction

### Before ANY task:
1. **ALWAYS** read `C:\Users\CORTEC\Desktop\ATS\myself\lessons_learned.txt` FIRST, before writing any CV, cover letter, or making any edits.
2. Internalize every rule, mistake, and candidate profile data in that file.
3. Apply all lessons proactively — do not repeat any documented mistake.

### After ANY correction from the user:
1. **IMMEDIATELY** update `C:\Users\CORTEC\Desktop\ATS\myself\lessons_learned.txt` with the new lesson.
2. Add the lesson under the appropriate section, or create a new section if needed.
3. Write the lesson in the same format: what happened, why it was wrong, rule for the future.
4. Increment the mistake number and update the "Last Updated" date at the top.
5. This is NOT optional — every user correction is a lesson that must be permanently recorded.

### The lessons file is a living journal:
- The AI talks to itself in this file — it is a self-directed learning log.
- Every new pattern, preference, or correction discovered during a session gets written there.
- The file grows over time and becomes the AI's institutional memory for this project.
- When in doubt about any decision (merging, language level, claims, formatting), check the lessons file first.

### What counts as a lesson:
- Any time the user corrects a factual claim (e.g., language level, program names)
- Any time the user rejects a design choice (e.g., merging entries, removing a project)
- Any time a reviewer provides feedback that changes the output
- Any formatting or structural preference the user expresses
- Any new candidate data (new programs, projects, skills, certifications)

---

## RULE 2: Candidate Data Integrity

- The user's personal data lives in `C:\Users\CORTEC\Desktop\ATS\myself\`
- NEVER invent experiences, skills, projects, or qualifications not found in this directory.
- ALWAYS cross-reference claims against actual project files and data.
- When unsure about a detail, check the source files — do not guess.

---

## RULE 3: CV & Cover Letter Standards

- Internship/entry-level CVs must be exactly 1 page — verify with pdflatex output.
- Cover letters must be exactly 1 page.
- Always compile both LaTeX and Markdown versions.
- Verify all GitHub links are live before finalizing.
- Check tense against event dates before choosing present vs. past tense.

---

## RULE 4: MANDATORY PRE-SUBMISSION VERIFICATION CHECKLIST (FORCED CONDITION)

Before delivering ANY CV to the user, the AI **MUST** systematically verify ALL 19 conditions of the checklist below.

### 🛑 CRITICAL VERIFICATION PROTOCOL:
1. The AI MUST perform a full checklist verification before giving the CV to the user.
2. If **EVEN ONE** condition fails or is not respected, the AI **MUST NOT** present the CV.
3. The AI MUST automatically fix the non-compliant item, recompile/re-generate, and re-run the entire checklist.
4. Only when **100% of conditions pass** can the CV be presented to the user.

### 📋 The 19 Mandatory Verification Checklist Conditions:

- [ ] **1. Fits target length**: Exactly 1 page for internship/early-career (verified via `pdflatex` output log).
- [ ] **2. Single-column layout**: No tables, text boxes, sidebars, or graphics carrying information.
- [ ] **3. Standard section headings**: Use exact standard terms ("Summary", "Education", "Skills", "Projects", "Experience").
- [ ] **4. Text-selectable PDF**: Must be compiled text-selectable PDF (not a scanned image).
- [ ] **5. Strict Filename**: `Benouali_Abdelkader_yahia_zakaria_CV.pdf` (and `Benouali_Abdelkader_yahia_zakaria_Cover_Letter.pdf`).
- [ ] **6. Contact info in body**: Name and contact details placed in body text, not header/footer zones.
- [ ] **7. Summary as Value Proposition**: 2–4 lines (30–50 words) value proposition; NO first-person pronouns ("I am"), NO objective statements.
- [ ] **8. Action-Verb Bullet Formula**: Every bullet follows `Action Verb + Task/Context + Tool/Method + Quantified Result`.
- [ ] **9. Quantification Target**: Numbers/metrics present in 60–70%+ of bullets.
- [ ] **10. Natural Keyword Matching**: Key job-posting keywords appear naturally in Skills + Experience; acronyms spelled out on first use.
- [ ] **11. Categorized Skills**: Skills organized into clean categories (8–15 total skills).
- [ ] **12. Strong Projects Portfolio**: 2–4 strongest projects with tech stack + verifiable outcomes included.
- [ ] **13. Zero Typos**: Thorough spellcheck and grammar check completed.
- [ ] **14. Consistent Tense & Dates**: Past tense for past events, present tense ("Building") ONLY for active events; consistent date formats.
- [ ] **15. Market-Appropriate Info**: No unnecessary personal info (no photo/DOB/marital status unless required).
- [ ] **16. Working Hyperlinks**: All links (LinkedIn, GitHub, Behance, project repos) tested and active.
- [ ] **17. Job-Specific Tailoring**: Custom-tailored to the target job description (not generic).
- [ ] **18. Visual Consistency**: Font (Times/Mathptmx or Arial), font sizes (Name 16-20pt, Headings 12-13pt, Body 10-11.5pt), line spacing (1.0-1.15) consistent throughout.
- [ ] **19. Top-Third Breathability**: White space allows top third of Page 1 to breathe for the 5-second scan.
