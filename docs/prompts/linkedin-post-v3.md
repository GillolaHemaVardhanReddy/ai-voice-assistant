<!-- Commentary for SHARING the v3 article as a post (use LinkedIn's own share flow on
     the published article — the article card + cover image attach automatically).
     Do NOT put the link in a comment: that rule is for EXTERNAL links. A LinkedIn
     article is internal, carries no reach penalty, and a comment link would not
     render the cover card at all.
     Rewritten 19 Aug on his brief: short, explains the article, asks two real
     questions, freelance offer before the tags. -->

I asked my own AI assistant which company I work for.

"I don't have that information." The answer was in its notes. Five times.

I spent a day adding reranking to the RAG bot on my portfolio. Almost nothing went the way the guides said it would:

→ My retrieval score didn't move at all. MRR 0.93 before, 0.93 after.
→ My relevance cutoff, calibrated on clean test documents, turned out to be 3x too low the moment it met real data.
→ But it fixed the failure above, and it finally let the bot say "I don't know" instead of inventing something.

I wrote up all of it, with the actual numbers, including the parts where I was wrong.

Two things I'd genuinely like answers to:

1. Is a reranker actually worth it on a small corpus? Mine is 6 files, 127 chunks. Or did I just pay latency and cost for an abstention feature I could have built some cheaper way?

2. If you work with RAG — tell me what I got wrong. I'm learning this by building it, so blind spots are guaranteed. I would much rather hear it than keep shipping it.

I'm currently looking to build one RAG chat model for someone, absolutely free. If that's useful to you, email or DM me — gillolahemavardhanreddy@gmail.com

#RAG #AI #LLM #MachineLearning #BuildInPublic #BackendEngineering
