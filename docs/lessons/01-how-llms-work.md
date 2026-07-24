# Lesson 01 — How an LLM Actually Works (the honest version)

Goal: by the end you can explain, to a friend, what a Large Language Model *is* — no magic.

## 1. The one-sentence truth
> An LLM is a program that, given some text, predicts the **next chunk of text** — over and over.

That's it. "Write me a poem" works because the most probable continuation of that request *is* a poem. It's autocomplete that got extremely good.

## 2. Tokens — the LLM's alphabet
Models don't see letters or words. They see **tokens** — pieces of words.
- `"voice"` might be 1 token. `"assistant"` might be 2 (`assist` + `ant`).
- Rough rule: **1 token ≈ 4 characters ≈ ¾ of a word.**

Why you care as a MERN dev: **you pay per token** (input + output). Token count = your bill. Cost control = token control.

## 3. Next-token prediction (the actual mechanism)
Given the tokens so far, the model outputs a **probability for every possible next token**:

```
Input: "The sky is"
        →  " blue"  : 71%
           " clear" : 12%
           " grey"  : 6%
           " the"   : 0.01%
           ...(50,000+ options each with a probability)
```

It picks one (usually a likely one), appends it, and repeats. A whole paragraph is just this loop running hundreds of times.

- Turning those raw scores into probabilities that sum to 100% is done by a function called **softmax** (we'll do the math in Phase 1).
- **Temperature** = a knob on that step: low = always pick the safest/most likely token (boring, consistent); high = allow riskier picks (creative, random). We'll feel this live in Phase 1.

## 4. Where the "intelligence" comes from
During its (one-time, giant, done-by-the-vendor) training, the model read a huge chunk of the internet and adjusted billions of internal numbers ("weights") so its next-token guesses match real text. Those weights quietly encode grammar, facts, reasoning patterns. **We never touch that training** — we *use* the finished model and steer it (prompts, RAG, light fine-tuning).

## 5. Mapping to what you already know (MERN)
| MERN thing | LLM equivalent |
|---|---|
| `fetch(url, { body })` | calling the model API |
| Request body JSON | your prompt + settings |
| Response JSON | the generated text |
| Rate limits / bill by request | billed by **tokens** |
| Stateless HTTP | LLM is stateless too — it only knows what you send each call (why we resend history for "memory") |

That last row is huge: **the model has no memory between calls.** "Conversation memory" is us re-sending the past messages every time. You'll build that in Phase 1–2.

## 6. Check your understanding
1. What is the model fundamentally doing at each step?
2. Why does token count matter to a business?
3. If the model is stateless, how do we make it "remember" the conversation?

(Answers we'll confirm together — just take a guess before Phase 1.)

## Next
→ Get an Anthropic API key (`console.anthropic.com`), put it in `.env`, then Phase 1: we make our first real API call and watch tokens + temperature in action.
