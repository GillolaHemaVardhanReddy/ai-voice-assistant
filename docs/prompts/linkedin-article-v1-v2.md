<!-- Spidy v1->v2 LinkedIn article. Rendered copy: paste from the artifact page, not from here. -->

# My AI assistant worked great. Until someone asked a follow-up question.

I'm a MERN developer. For the last few months I've been learning AI by actually building something instead of watching tutorials.

The thing is **Spidy**, an assistant on my portfolio that answers questions about my work. It's live now. Getting there took two versions and I got a lot wrong on the way, which is most of what this post is about.


## Why I built it

First I just asked a normal LLM some questions about myself, to see what would happen.

It didn't make up a fake resume. That's what I expected and it didn't do it. What it actually did was politely say it didn't know, and then tell the visitor to go check my LinkedIn.

So it wasn't lying. It just had nothing to work with. Its own answer said it: **"not in my context."**

That's the whole problem. The model didn't need to be smarter. It needed my notes.


## v1: giving it my files

The technique is called **RAG**, retrieval-augmented generation. The name sounds heavier than the idea.

I wrote six plain text files about my work. A script cuts them into 127 short pieces and turns each piece into a list of numbers that represents what it means. When someone asks a question, the question becomes numbers the same way, and I find the pieces whose numbers point in a similar direction. Those pieces go into the prompt with one instruction: answer only from this, and say so if the answer isn't here.

That's it. **The search itself is one matrix multiply.** No framework, no library, around forty lines.


![The top half is the part most RAG diagrams skip. Chunking and embedding happen offline, once. Only the bottom row runs when someone asks something.](~/Desktop/spidy-figures/04-arch.png)
*The top half is the part most RAG diagrams skip. Chunking and embedding happen offline, once. Only the bottom row runs when someone asks something.*

Every answer ends with the files it used, like `[boundaries.txt]`. I wanted people to be able to check where an answer came from instead of trusting it.


![Real scores for "Does he have experience in MongoDB?" The right piece wins by 0.128. The next four are all within 0.02 of each other.](~/Desktop/spidy-figures/05-hits.png)
*Real scores for "Does he have experience in MongoDB?" The right piece wins by 0.128. The next four are all within 0.02 of each other.*


## The hard part had nothing to do with AI

The retrieval was the easy part. The hard part was getting it to fit in **512 MB of memory**, which is what the free hosting tier gives you.

My first Docker image was **1.95 GB**.

At some point I sat down and did this multiplication:


> **127 chunks × 384 dimensions × 4 bytes = 190 kilobytes**

190 KB. That's the actual data. I had shipped 1.8 GB of libraries to produce it. **Basically I built a whole factory to deliver one envelope.**


![At this scale the real data would be 0.09 pixels wide, so I didn't draw it as a bar.](~/Desktop/spidy-figures/01-ratio.png)
*At this scale the real data would be 0.09 pixels wide, so I didn't draw it as a bar.*

Fixing that taught me more than the AI part did.

**A model is not a runtime.** The weights were about 90 MB. Everything wrapped around them was 1.8 GB. In my head those had been one thing.

**Removing a dependency once doesn't mean it's gone.** I took a big library out of `requirements.txt` and it came straight back in through the Dockerfile.

**Check inside the container, not the manifest.** I found a 57 MB symbolic algebra library sitting in a web service that does no algebra. It came in as somebody else's dependency. I only found it by running `du` inside the running container.

**Build time is not run time.** Those 127 pieces never change between requests. I was re-cutting and re-embedding all of them every time the server started, for no reason. That moved offline into a file the server just loads.

Where it ended up: **1.95 GB down to 347 MB on disk, and 625 MB of memory down to 63.4 MB.** Same 127 pieces, same answers. I saved all twelve retrieval scores before I started and checked them again after, matching to three decimals, before I believed any of it.


![Two different measurements, so two panels. The dashed line is the limit the first build couldn't get under.](~/Desktop/spidy-figures/02-shrink.png)
*Two different measurements, so two panels. The dashed line is the limit the first build couldn't get under.*


## The bug that actually worried me

Early on, Spidy answered in first person. _"I built the analytics platform."_

Nothing in the prompt had told it who it was, so it just assumed it was me. It was speaking as me, on my own site, and nothing about it looked broken. The fix was one paragraph in the system prompt saying you are Spidy, you are not Hemavardhan, always speak in third person.

That one stayed with me more than the 1.9 GB did. **It wasn't a crash. It ran perfectly and did the wrong thing**, and I could easily have not noticed.


## v2: it couldn't follow a conversation

v1 treated every question like it was the first thing you'd ever said. Ask _"does he know MongoDB?"_ and it answers properly. Ask _"so he knows it?"_ right after and it has no idea what "it" is.

Obvious fix, send the conversation history along with the question. That half works straight away, the model can see the earlier turn now.

But there's a second half I completely missed. **The search doesn't get the conversation.** It only ever gets the sentence you just typed. So on that follow-up my system was searching 127 pieces of text for the phrase _"so he knows it?"_

I measured how bad that is.


![Same 127 pieces, same search, two questions one turn apart. The MongoDB piece doesn't come fifth on the follow-up. It doesn't show up at all.](~/Desktop/spidy-figures/06-blind.png)
*Same 127 pieces, same search, two questions one turn apart. The MongoDB piece doesn't come fifth on the follow-up. It doesn't show up at all.*

Best match on the follow-up: **0.344**. Best match on the proper question: **0.620**. And when I checked what five completely unrelated words score against my notes, that came out at **0.186**.

So the follow-up landed closer to random noise than to the answer.

The part that bothered me more: **it still returned five results, confidently.** Top-k always returns k. There's no way for it to say "I found nothing."

The fix is to rewrite the question before searching. Turn _"so he knows it?"_ into _"Does Hemavardhan have knowledge of MongoDB?"_ and search for that instead.


![Same four words typed by the user either way. One extra call before the search decides whether the thing can answer at all.](~/Desktop/spidy-figures/07-rewrite.png)
*Same four words typed by the user either way. One extra call before the search decides whether the thing can answer at all.*

Took me four tries.

First attempt came back as _"Here's the rewritten question:"_ followed by the question and then an unsolicited answer, and all of that went into the search. Second attempt quietly pulled a fact out of the previous answer and changed what was being asked. I added a line to the prompt telling it not to change the meaning. Still failed.

What finally fixed it wasn't a better instruction. It was giving the input **structure**, labelled sections so the model could see where the conversation ended and the question started. Three prompt rewrites, beaten by one heading.


> **You can't fix a structural problem by adding adjectives.**


## What I got out of it

The technical stuff is in any tutorial. These weren't.

**Measure your instrument before you measure your change.** Early on I decided the memory feature worked because the answers looked different with it turned on. Then I ran the same question three times with nothing changed at all, and the wording came out different every time. My proof was noise. Now the first thing I build for any change is the measurement of changing nothing.

**If both options pass, you didn't test anything.** My first memory test used a follow-up that happened to contain its own keyword, so the search found the right answer without needing any history at all. Both versions passed. I nearly shipped on that.

**Know what you're actually shipping.** 190 KB inside 1.8 GB. No build log tells you that ratio, you have to go and divide it yourself.

**The failures that matter don't crash.** The bot speaking as me. A rewritten question that quietly narrowed itself. Search returning five confident wrong results. All of them returned 200.


## What's next

v2 is live. It remembers, and it can follow a pronoun.

It still can't tell an exact product name from a general topic. It still takes whatever five pieces are nearest without checking if they're any good. It still takes a few seconds to answer.

All of those have names and known fixes and I'll write them up as I build them. The next one is the least interesting and the most useful: a set of real questions with the file that should answer each one, so that from here every change gets a number instead of my opinion.

Spidy is on my portfolio if you want to try it. It'll also tell you what I haven't done. I wrote those notes on purpose.

---

## The share-post (separate from the article)

Post this Tuesday or Wednesday, 9–10 AM IST. **Article link goes in the first comment, not the
post body** — LinkedIn suppresses posts with external links in them.

```
My portfolio assistant answered "does he know MongoDB?" perfectly.

Then: "so he knows it?"

No idea what "it" meant.

The obvious fix is to send the conversation history along. That's only half of it, and the other half took me a while to see:

The model gets the conversation. The search doesn't.

It only ever sees the sentence you just typed. So on that follow-up, my system was searching 127 documents for the literal phrase "so he knows it?"

The numbers:

0.620 — the proper question
0.344 — the follow-up
0.186 — five completely unrelated words

It landed closer to noise than to the answer. And it still returned five confident results, because this kind of search has no way to say "I found nothing."

I wrote up both versions of the thing. What RAG actually is under the acronym, why my first container was 1.95 GB to ship 190 KB of data, the bug where it started speaking as me, and the four tries it took to fix the follow-up.

Written for anyone learning this by building instead of watching tutorials.

Link in comments 👇

#RAG #AI #LLM #MachineLearning #SoftwareEngineering
```

### Shorter variant

```
My portfolio assistant answered "does he know MongoDB?" perfectly.

Then someone asked "so he knows it?" and it had no idea what "it" meant.

I sent it the conversation history. Still broken. It took me a while to see why:

The model gets the conversation. The search doesn't.

It only ever sees the sentence you just typed — so it was searching 127 documents for the phrase "so he knows it?"

Proper question: 0.620
Follow-up: 0.344
Five unrelated words: 0.186

Closer to noise than to the answer.

I wrote up how I found it and the four attempts it took to fix. For anyone learning this by building rather than watching tutorials.

Link in comments 👇

#RAG #AI #LLM #SoftwareEngineering
```

**First hour matters.** Reply to every comment — LinkedIn weights early engagement heavily, and
replies count.
