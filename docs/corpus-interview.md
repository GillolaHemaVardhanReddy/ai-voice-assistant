# Spidy corpus interview — 112 questions

**Purpose:** grow `service/notes/` from 3,853 words (127 chunks) to ~15,000 words (~495 chunks)
of true, retrievable information about Hemavardhan, so Spidy can answer a real recruiter
without guessing.

**Created 19 Aug 2026 (S22), after Atom 2.11 calibrated the relevance cutoff at 0.18.**

---

## ⚠️ HOW TO ANSWER — the format matters as much as the content

Today's experiment proved this. Two chunks containing the same fact scored **0.41** and **0.07**
depending only on how they were framed. So:

1. **Third person, always.** "He owns…", never "I own…". Matches the existing notes and the
   voice Spidy answers in.
2. **Give every answer a `#` heading that names what it is about.** The heading is what the
   reranker reads first. `# Notice period, availability and when he can start` scored 0.41.
   A heading naming the wrong topic scored *lower than no heading at all* — so name the
   topic a recruiter would ask about, not the topic you feel like writing about.
3. **Self-contained sentences.** Chunks get split apart. A sentence starting with "It also…"
   is useless alone. Repeat the subject: "The Vedamandir payments subsystem also…".
4. **Numbers, names, versions, dates.** `5.2 crore`, `ClickHouse`, `50 migrations`, `2023`.
   Exact tokens are what BM25 (Atom 2.12) will index and what recruiters actually search for.
5. **Honest negatives belong in the corpus.** "He has not worked with Kubernetes" scored
   **0.834** — the reranker's highest score all session. Saying no is answering.
6. **~150 words per answer.** Shorter is fine if that's the whole truth. Don't pad — padding
   creates near-duplicate chunks that compete with each other and both lose.

**Where answers go:** existing files where they fit; new files where a topic is big enough
(suggested new files listed per section). Then rebuild: `python -m service.build_index`.

---

## 1. Identity, education, logistics  → `faq.txt`

1. Full name, and how it should be written/pronounced in a professional context?
2. Where did he study, what degree, what years, and what was the result?
3. Any coursework, projects or subjects from college that actually matter to his work today?
4. Current city, willingness to relocate, and to which cities specifically?
5. Remote / hybrid / onsite — what does he actually want, and what will he accept?
6. Work authorisation: passport, visa status, any constraints on working abroad?

## 2. Current role  → `about.txt`

7. Company name, his exact title, team size, and who he reports to?
8. When did he join, and what was the role when he joined vs now?
9. What does a normal working week actually look like, hour by hour?
10. What is he single-handedly responsible for — where does the buck stop with him?
11. What did he inherit vs what did he build from zero at this job?
12. What would break, and how fast, if he stopped working tomorrow?

## 3. Career history  → new file `career.txt`

13. Every role before this one: company, title, dates, why he left?
14. First paid programming work — what was it and what did it teach him?
15. Any internships, and what real work came out of them?
16. The single biggest step-change in his ability — when, and what caused it?
17. Has he ever been rejected, laid off, or failed an interview badly? What happened?
18. How did he get his current job — the actual process, not the polished version?

## 4. Payments & fintech — his stated edge  → new file `payments.txt`

19. Which payment gateways has he integrated, and what differs between them?
20. Describe the payments subsystem's architecture end to end: request → money moved.
21. How does he guarantee no double-charge? The actual mechanism, not the intent.
22. Idempotency: where are the keys generated, stored, and expired?
23. Webhooks: ordering, retries, duplicates, signature verification — how is each handled?
24. Refunds, partial refunds, chargebacks, failed settlements — what has he actually built?
25. Reconciliation: how does he prove the ledger matches the gateway?
26. The worst payments bug he has personally shipped, and how it was found and fixed?
27. What is the 5.2 crore figure measured over — timeframe, volume, average ticket?
28. What in the payments system does he consider not good enough yet?

## 5. Databases  → `skills.txt`

29. MySQL: the hardest schema he has designed, and why it was hard?
30. An index he added that changed a real query's timing — before/after numbers?
31. His migration process step by step: writing, reviewing, dry-run, deploy, rollback?
32. A migration that went wrong, and what changed in the process afterwards?
33. ClickHouse: why it was chosen, what it replaced, what it is bad at?
34. Redis: exactly what is cached, what the TTLs are, how invalidation works?
35. A cache-invalidation bug he has debugged?
36. When would he refuse to add another datastore?

## 6. Backend & architecture  → new file `architecture.txt`

37. The full request path of the most complex endpoint he owns?
38. Multi-tenancy: how is tenant isolation actually enforced?
39. How are background jobs / queues handled, and what happens when one fails?
40. An architectural decision he made that he now thinks was wrong?
41. An architectural decision he defended against pushback and was right about?
42. How does he decide between "fix it properly" and "ship the patch"?
43. What does his error handling and logging strategy look like in practice?
44. How does he handle API versioning and breaking changes for existing clients?

## 7. Production operations  → `skills.txt`

45. Describe the deploy pipeline from `git push` to live?
46. What are the deploy-order safety gates, and what incident caused them?
47. PM2 clustering: how many processes, on what hardware, and why that number?
48. CloudFront: what is cached, and how does automated invalidation trigger?
49. The worst production incident he has handled — timeline, decisions, outcome?
50. What is monitored today, what alerts him, and what does he wish he had?
51. Has he ever been on call? What did that look like?

## 8. Engineering standards & tooling  → new file `standards.txt`

52. What exactly do the commit-message enforcement rules require, and why?
53. What is the pre-push drift check checking for?
54. What does he look for in a code review, in priority order?
55. What has he built in-house that another engineer uses daily?
56. How does he onboard a new engineer into his codebase?
57. What documentation does he actually write, and what does he refuse to write?

## 9. Open source  → `projects.txt`

58. Both published tools: what problem does each solve, for whom?
59. Why did he build each one instead of using something existing?
60. Install numbers, stars, issues, real users — the honest figures?
61. Has anyone else contributed, and how did he handle it?
62. What would he change about each tool today?

## 10. Projects in depth  → `projects.txt`

63. Vedamandir: the product, the users, the scale, his exact contribution?
64. The analytics platform: what question does it answer, for whom, how fast?
65. The customer-recovery work: what does it do and what did it recover?
66. The internal tools: what existed before them, what changed after?
67. Any project he started and abandoned, and why?
68. Which single project is he proudest of, and why that one?

## 11. AI & the current learning  → new file `ai-journey.txt`

69. What is he building in the AI voice assistant project, and how far has he got?
70. What has he implemented from scratch vs called an API for?
71. What does he now understand about embeddings that he didn't three months ago?
72. What is RAG, in his own words, to a non-technical hiring manager?
73. Which parts of ML still feel genuinely unclear to him?
74. What is the end goal — a job, a product, both?
75. How does he study: sources, hours per week, how he decides what's next?

## 12. Languages & tools  → `skills.txt`

76. JavaScript/TypeScript: what does he know that a 2-year dev typically doesn't?
77. Python: what has he actually built with it, honestly?
78. C and C++: where did those come from and does he still use them?
79. Which frameworks/libraries does he know deeply vs has merely used?
80. What is his editor/terminal/daily setup, and has he customised it?
81. What tool does he reach for that most engineers he knows don't?

## 13. Boundaries — what he has NOT done  → `boundaries.txt`

82. Which popular technologies has he never touched? Name them explicitly.
83. What scale has he not operated at?
84. Has he led a team? Managed anyone formally? Owned a hiring decision?
85. Has he worked in a large company, or only startups?
86. What kind of work would he be genuinely bad at today?
87. What is he most likely to be over-estimated on by a recruiter reading his CV?

## 14. Collaboration & communication  → new file `working-style.txt`

88. How does he work with product/design when a spec is ambiguous?
89. How does he handle disagreeing with someone more senior?
90. Has he mentored anyone, and what specifically did they learn from him?
91. How does he prefer to receive feedback?
92. How does he communicate a slipping deadline?
93. What kind of teammate frustrates him?

## 15. Product & business sense  → `preferences.txt`

94. Has he ever pushed back on building a feature, and won?
95. How does he think about the cost of what he builds?
96. Has he ever talked to an actual end user of his software?
97. What does he think Vedamandir's business actually needs next?

## 16. Failures & lessons  → new file `lessons.txt`

98. The most expensive mistake he has made in production?
99. Something he believed strongly two years ago and no longer believes?
100. A time he was the blocker on a project?
101. What does he do when he is completely stuck on a bug?
102. A skill he tried to learn and gave up on?

## 17. What he wants next  → `preferences.txt`

103. The ideal next role, described concretely — team, stack, scope, size?
104. What would make him say no to an otherwise good offer?
105. Where does he want to be technically in two years?
106. Does he want to keep coding long-term or move toward architecture/leadership?
107. Startup vs scale-up vs enterprise — genuine preference, with reasoning?

## 18. Compensation & process  → `faq.txt`

108. Current CTC — fixed, variable, and what he'd share with a recruiter?
109. What is negotiable besides base salary?
110. How many interview rounds is he willing to do, and what does he refuse?
111. Does he do take-home assignments? Time limit?
112. What are his references, and who would speak for him?
