# Spidy v1 — article figures

Five hand-authored SVGs for `/spidy/v1`. **Paste them inline** (not as `<img>`) so `currentColor`
picks up your article's text colour in both themes.

**One thing to set**, once, anywhere in your stylesheet:

```css
:root                                  { --fig-accent: #2B4FD4; }  /* light */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"])      { --fig-accent: #6D8CF0; }  /* dark  */
}
:root[data-theme="dark"]               { --fig-accent: #6D8CF0; }
```

Both accents were validated for lightness band and contrast against their surfaces. Everything
else in the figures is `currentColor`, so it themes itself.

Each `<svg>` already carries `role="img"` and an `aria-label`. Wrap in `<figure>` with the caption
given, and give the svg `max-width:100%; height:auto`. Figures 2 and 5 are charts — they carry
their own value labels, so no legend and no axis ticks are needed.


---

## Figure 1 — The ratio

**Caption:** <b>190 kilobytes of data behind 1.8 gigabytes of machinery.</b> The grey bar is what the container shipped in order to produce the vectors. At the same scale the vectors themselves would be <b>0.09 pixels wide</b> — so they are not drawn as a bar, because drawing them would be a lie.

```html
<svg viewBox="0 0 900 212" role="img" aria-label="A full-width grey bar represents 1.8 gigabytes of runtime and libraries. The 190 kilobytes of actual vector data would be 0.09 pixels wide at the same scale, marked by a hairline at the far left.">
  <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" fill="currentColor">
    <text x="40" y="40" font-size="12" opacity="0.6">WHAT THE CONTAINER SHIPPED, TO SCALE</text>
    <rect x="40" y="72" width="820" height="54" rx="3" fill="currentColor" opacity="0.16"/>
    <text x="852" y="105" text-anchor="end" font-size="15" font-weight="700" opacity="0.85">1.8 GB</text>
    <text x="852" y="63" text-anchor="end" font-size="11.5" opacity="0.6">torch · onnxruntime · sympy · a symbolic-algebra engine</text>
    <line x1="41" y1="66" x2="41" y2="132" stroke="var(--fig-accent, #2B4FD4)" stroke-width="2.5"/>
    <path d="M 41 140 L 41 156 L 66 156" fill="none" stroke="var(--fig-accent, #2B4FD4)" stroke-width="1.5"/>
    <text x="74" y="161" font-size="14" font-weight="700" fill="var(--fig-accent, #2B4FD4)">190 KB — the vectors. The entire point.</text>
    <text x="74" y="186" font-size="11.5" opacity="0.6">127 chunks &#215; 384 dimensions &#215; 4 bytes. At this scale: 0.09 px wide — thinner than the line marking it.</text>
  </g>
</svg>
```


---

## Figure 2 — The shrink

**Caption:** Two measures, two panels, two scales — <b>never one chart with two axes.</b> Disk size fell 5.6&#215;; runtime memory fell 9.9&#215; and, crucially, crossed under the ceiling that made the free tier possible at all. Same 127 chunks, same answers — all 12 retrieval scores verified identical to three decimals first.

```html
<svg viewBox="0 0 900 268" role="img" aria-label="Two panels. Left: container image on disk falls from 1.95 gigabytes to 751 megabytes to 347 megabytes. Right: runtime memory falls from 625 megabytes to 63.4 megabytes, crossing under Render's 512 megabyte limit.">
  <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" fill="currentColor">

    <text x="20" y="26" font-size="12" opacity="0.6">IMAGE ON DISK</text>
    <line x1="110" y1="44" x2="110" y2="228" stroke="currentColor" stroke-width="1" opacity="0.25"/>
    <text x="100" y="76" text-anchor="end" font-size="11.5" opacity="0.6">first build</text>
    <rect x="110" y="56" width="292" height="30" rx="3" fill="currentColor" opacity="0.28"/>
    <text x="412" y="76" font-size="13" font-weight="600" opacity="0.85">1.95 GB</text>
    <text x="100" y="131" text-anchor="end" font-size="11.5" opacity="0.6">torch dropped</text>
    <rect x="110" y="111" width="113" height="30" rx="3" fill="currentColor" opacity="0.28"/>
    <text x="233" y="131" font-size="13" font-weight="600" opacity="0.85">751 MB</text>
    <text x="100" y="186" text-anchor="end" font-size="11.5" opacity="0.6">model removed</text>
    <rect x="110" y="166" width="52" height="30" rx="3" fill="var(--fig-accent, #2B4FD4)"/>
    <text x="172" y="186" font-size="13" font-weight="700" fill="var(--fig-accent, #2B4FD4)">347 MB</text>

    <line x1="452" y1="20" x2="452" y2="240" stroke="currentColor" stroke-width="1" opacity="0.18"/>

    <text x="482" y="26" font-size="12" opacity="0.6">MEMORY AT RUNTIME (RSS)</text>
    <line x1="590" y1="44" x2="590" y2="228" stroke="currentColor" stroke-width="1" opacity="0.25"/>
    <text x="580" y="76" text-anchor="end" font-size="11.5" opacity="0.6">measured</text>
    <rect x="590" y="56" width="268" height="30" rx="3" fill="currentColor" opacity="0.28"/>
    <text x="850" y="46" text-anchor="end" font-size="13" font-weight="600" opacity="0.85">625 MB</text>
    <text x="580" y="131" text-anchor="end" font-size="11.5" opacity="0.6">shipped</text>
    <rect x="590" y="111" width="27" height="30" rx="3" fill="var(--fig-accent, #2B4FD4)"/>
    <text x="627" y="131" font-size="13" font-weight="700" fill="var(--fig-accent, #2B4FD4)">63.4 MB</text>
    <line x1="810" y1="48" x2="810" y2="176" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 4" opacity="0.6"/>
    <text x="806" y="196" text-anchor="end" font-size="11" opacity="0.65">Render free tier</text>
    <text x="806" y="211" text-anchor="end" font-size="11" opacity="0.65">512 MB ceiling</text>
    <text x="590" y="256" font-size="11.5" opacity="0.6">The first build did not fit. That is the whole story of this version.</text>
  </g>
</svg>
```


---

## Figure 3 — Pipeline strip — v1

**Caption:** Design D's own component, for v1. <b>Three of five stages lit, two dark.</b> Don't let anyone &ldquo;fix&rdquo; the dark ones — a v1 whose empty stages get filled in by later versions is exactly what makes the series read as one system growing rather than twelve unrelated posts.

```html
<svg viewBox="0 0 1000 142" role="img" aria-label="Five pipeline stages. Question, Retrieve and Generate are lit as built in version 1. Rerank and Context are dark, arriving in later versions.">
  <defs><marker id="pa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" fill="currentColor">
    <rect x="20" y="34" width="168" height="72" rx="3" fill="none" stroke="var(--fig-accent, #2B4FD4)" stroke-width="2"/>
    <text x="34" y="55" font-size="10" fill="var(--fig-accent, #2B4FD4)" opacity="0.8">01 · QUESTION</text>
    <text x="34" y="78" font-size="13" font-weight="600" fill="var(--fig-accent, #2B4FD4)">What they typed</text>
    <text x="34" y="96" font-size="10" fill="var(--fig-accent, #2B4FD4)" opacity="0.7">new in v1</text>

    <rect x="218" y="34" width="168" height="72" rx="3" fill="var(--fig-accent, #2B4FD4)" fill-opacity="0.1" stroke="var(--fig-accent, #2B4FD4)" stroke-width="3"/>
    <text x="232" y="55" font-size="10" fill="var(--fig-accent, #2B4FD4)" opacity="0.8">02 · RETRIEVE</text>
    <text x="232" y="78" font-size="13" font-weight="700" fill="var(--fig-accent, #2B4FD4)">vecs @ q, top-k</text>
    <text x="232" y="96" font-size="10" fill="var(--fig-accent, #2B4FD4)" opacity="0.7">new in v1 · primary</text>

    <rect x="416" y="34" width="168" height="72" rx="3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 4" opacity="0.35"/>
    <text x="430" y="55" font-size="10" opacity="0.4">03 · RERANK</text>
    <text x="430" y="78" font-size="13" font-weight="600" opacity="0.4">&#8212;</text>
    <text x="430" y="96" font-size="10" opacity="0.4">not yet</text>

    <rect x="614" y="34" width="168" height="72" rx="3" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 4" opacity="0.35"/>
    <text x="628" y="55" font-size="10" opacity="0.4">04 · CONTEXT</text>
    <text x="628" y="78" font-size="13" font-weight="600" opacity="0.4">&#8212;</text>
    <text x="628" y="96" font-size="10" opacity="0.4">arrives in v2</text>

    <rect x="812" y="34" width="168" height="72" rx="3" fill="none" stroke="var(--fig-accent, #2B4FD4)" stroke-width="2"/>
    <text x="826" y="55" font-size="10" fill="var(--fig-accent, #2B4FD4)" opacity="0.8">05 · GENERATE</text>
    <text x="826" y="78" font-size="13" font-weight="600" fill="var(--fig-accent, #2B4FD4)">Answer + citations</text>
    <text x="826" y="96" font-size="10" fill="var(--fig-accent, #2B4FD4)" opacity="0.7">new in v1</text>

    <g stroke="currentColor" stroke-width="1.5" opacity="0.45" color="currentColor">
      <line x1="192" y1="70" x2="212" y2="70" marker-end="url(#pa)"/>
      <line x1="390" y1="70" x2="410" y2="70" marker-end="url(#pa)"/>
      <line x1="588" y1="70" x2="608" y2="70" marker-end="url(#pa)"/>
      <line x1="786" y1="70" x2="806" y2="70" marker-end="url(#pa)"/>
    </g>
  </g>
</svg>
```


---

## Figure 4 — v1 architecture

**Caption:** The half most RAG diagrams leave out is the top one. <b>Chunking and embedding happen offline, once</b> — changing them means rebuilding <code>index.npz</code>, not editing a request handler. The two halves touch at exactly one point: the index is loaded into memory at startup, and every question reads it.

```html
<svg viewBox="0 0 1000 320" role="img" aria-label="Version 1 architecture in two halves. Index time, offline: notes are chunked, embedded and written to index.npz. Query time, online: question, encode, search, LLM, answer. The index is loaded once at startup.">
  <defs><marker id="aa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" fill="currentColor">
    <rect x="0" y="8" width="1000" height="118" rx="5" fill="currentColor" opacity="0.04"/>
    <text x="18" y="28" font-size="11" opacity="0.6">INDEX TIME &#8212; offline, once, when the notes change. <tspan opacity="0.75">build_index.py</tspan></text>

    <rect x="85"  y="42" width="170" height="54" rx="3" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.55"/>
    <text x="170" y="65" text-anchor="middle" font-size="12.5" font-weight="600">6 .txt notes</text>
    <text x="170" y="83" text-anchor="middle" font-size="10" opacity="0.6">written by hand</text>

    <rect x="305" y="42" width="170" height="54" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <text x="390" y="65" text-anchor="middle" font-size="12.5" font-weight="600">chunk</text>
    <text x="390" y="83" text-anchor="middle" font-size="10" opacity="0.6">127 pieces</text>

    <rect x="525" y="42" width="170" height="54" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <text x="610" y="65" text-anchor="middle" font-size="12.5" font-weight="600">embed</text>
    <text x="610" y="83" text-anchor="middle" font-size="10" opacity="0.6">1536-d each</text>

    <rect x="745" y="42" width="170" height="54" rx="3" fill="none" stroke="var(--fig-accent, #2B4FD4)" stroke-width="2"/>
    <text x="830" y="65" text-anchor="middle" font-size="12.5" font-weight="700" fill="var(--fig-accent, #2B4FD4)">index.npz</text>
    <text x="830" y="83" text-anchor="middle" font-size="10" fill="var(--fig-accent, #2B4FD4)" opacity="0.8">949 KB &#183; float32</text>

    <g stroke="currentColor" stroke-width="1.5" color="currentColor">
      <line x1="257" y1="69" x2="301" y2="69" marker-end="url(#aa)"/>
      <line x1="477" y1="69" x2="521" y2="69" marker-end="url(#aa)"/>
      <line x1="697" y1="69" x2="741" y2="69" marker-end="url(#aa)"/>
    </g>

    <g stroke="var(--fig-accent, #2B4FD4)" stroke-width="1.5" stroke-dasharray="5 4" fill="none" color="var(--fig-accent, #2B4FD4)">
      <path d="M 830 98 L 830 142 L 500 142 L 500 196" marker-end="url(#aa)"/>
    </g>
    <text x="672" y="136" text-anchor="middle" font-size="10.5" fill="var(--fig-accent, #2B4FD4)" opacity="0.85">np.load once, at server startup</text>

    <rect x="0" y="162" width="1000" height="146" rx="5" fill="currentColor" opacity="0.04"/>
    <text x="18" y="182" font-size="11" opacity="0.6">QUERY TIME &#8212; online, every question. <tspan opacity="0.75">POST /ask</tspan></text>

    <rect x="30"  y="198" width="160" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.55"/>
    <text x="110" y="222" text-anchor="middle" font-size="12.5" font-weight="600">question</text>
    <text x="110" y="240" text-anchor="middle" font-size="10" opacity="0.6">raw text</text>

    <rect x="225" y="198" width="160" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <text x="305" y="222" text-anchor="middle" font-size="12.5" font-weight="600">encode</text>
    <text x="305" y="240" text-anchor="middle" font-size="10" opacity="0.6">1536-d vector</text>

    <rect x="420" y="198" width="160" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <text x="500" y="222" text-anchor="middle" font-size="12.5" font-weight="600">search</text>
    <text x="500" y="240" text-anchor="middle" font-size="10" opacity="0.6">top-k of 127</text>

    <rect x="615" y="198" width="160" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <text x="695" y="222" text-anchor="middle" font-size="12.5" font-weight="600">LLM</text>
    <text x="695" y="240" text-anchor="middle" font-size="10" opacity="0.6">answer from CONTEXT</text>

    <rect x="810" y="198" width="160" height="56" rx="3" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.55"/>
    <text x="890" y="222" text-anchor="middle" font-size="12.5" font-weight="600">answer</text>
    <text x="890" y="240" text-anchor="middle" font-size="10" opacity="0.6">+ [sources]</text>

    <g stroke="currentColor" stroke-width="1.5" color="currentColor">
      <line x1="192" y1="226" x2="221" y2="226" marker-end="url(#aa)"/>
      <line x1="387" y1="226" x2="416" y2="226" marker-end="url(#aa)"/>
      <line x1="582" y1="226" x2="611" y2="226" marker-end="url(#aa)"/>
      <line x1="777" y1="226" x2="806" y2="226" marker-end="url(#aa)"/>
    </g>
    <text x="500" y="288" text-anchor="middle" font-size="11" opacity="0.55">Retrieval is one matrix multiply. That is the whole of it.</text>
  </g>
</svg>
```


---

## Figure 5 — What retrieval actually returns

**Caption:** Real measured output for <b>&ldquo;Does he have experience in MongoDB?&rdquo;</b> — the five nearest chunks and their cosine scores. The right chunk doesn't just win, <b>it wins by 0.128 while the runners-up sit within 0.02 of each other.</b> That gap is the signal; without it you have five plausible chunks and no way to tell.

```html
<svg viewBox="0 0 900 296" role="img" aria-label="Bar chart of the five nearest chunks for the question does he have experience in MongoDB. The MongoDB chunk from boundaries.txt scores 0.620; the next four score 0.492, 0.483, 0.474 and 0.472.">
  <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" fill="currentColor">
    <text x="20" y="26" font-size="12" opacity="0.6">COSINE SCORE &#183; TOP 5 OF 127 CHUNKS</text>
    <line x1="300" y1="44" x2="300" y2="262" stroke="currentColor" stroke-width="1" opacity="0.25"/>

    <text x="290" y="72" text-anchor="end" font-size="11.5" font-weight="700">boundaries.txt</text>
    <text x="290" y="87" text-anchor="end" font-size="10" opacity="0.6">the MongoDB chunk</text>
    <rect x="300" y="54" width="461" height="34" rx="3" fill="var(--fig-accent, #2B4FD4)"/>
    <text x="771" y="77" font-size="14" font-weight="700" fill="var(--fig-accent, #2B4FD4)">0.620</text>

    <text x="290" y="119" text-anchor="end" font-size="11.5" opacity="0.75">skills.txt</text>
    <text x="290" y="133" text-anchor="end" font-size="10" opacity="0.5">Redis</text>
    <rect x="300" y="102" width="366" height="34" rx="3" fill="currentColor" opacity="0.24"/>
    <text x="676" y="125" font-size="13" opacity="0.7">0.492</text>

    <text x="290" y="167" text-anchor="end" font-size="11.5" opacity="0.75">boundaries.txt</text>
    <text x="290" y="181" text-anchor="end" font-size="10" opacity="0.5">production ops</text>
    <rect x="300" y="150" width="359" height="34" rx="3" fill="currentColor" opacity="0.24"/>
    <text x="669" y="173" font-size="13" opacity="0.7">0.483</text>

    <text x="290" y="215" text-anchor="end" font-size="11.5" opacity="0.75">skills.txt</text>
    <text x="290" y="229" text-anchor="end" font-size="10" opacity="0.5">Node &amp; Express</text>
    <rect x="300" y="198" width="352" height="34" rx="3" fill="currentColor" opacity="0.24"/>
    <text x="662" y="221" font-size="13" opacity="0.7">0.474</text>

    <text x="290" y="263" text-anchor="end" font-size="11.5" opacity="0.75">boundaries.txt</text>
    <text x="290" y="277" text-anchor="end" font-size="10" opacity="0.5">Java vs Node</text>
    <rect x="300" y="246" width="351" height="34" rx="3" fill="currentColor" opacity="0.24"/>
    <text x="661" y="269" font-size="13" opacity="0.7">0.472</text>
  </g>
</svg>
```

---

## Figure 6 — The retriever going blind (v2 article)

**Caption:** Same 127 chunks, same retriever, two questions one turn apart. Drop the keyword and the best match lands nearer the measured noise floor than the answer.

```html
<svg viewBox="0 0 900 250" role="img" aria-label="A cosine similarity scale. The keyword question scores 0.620 and finds the right chunk. The pronoun follow-up scores 0.344 on the wrong chunk. The measured noise floor for unrelated words is 0.186.">
  <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" fill="currentColor">
    <text x="40" y="34" font-size="12" opacity="0.6">BEST MATCH FOUND, SAME 127 CHUNKS, SAME RETRIEVER</text>
    <line x1="60" y1="150" x2="840" y2="150" stroke="currentColor" stroke-width="2" opacity="0.3"/>
    <text x="60" y="176" font-size="11" opacity="0.5">0.0</text>
    <text x="840" y="176" text-anchor="end" font-size="11" opacity="0.5">0.7</text>

    <g opacity="0.55">
      <line x1="267" y1="140" x2="267" y2="160" stroke="currentColor" stroke-width="2" stroke-dasharray="3 3"/>
      <text x="267" y="200" text-anchor="middle" font-size="11.5">0.186</text>
      <text x="267" y="217" text-anchor="middle" font-size="10.5">noise floor</text>
      <text x="267" y="232" text-anchor="middle" font-size="10.5">(unrelated words)</text>
    </g>

    <g>
      <line x1="443" y1="122" x2="443" y2="160" stroke="currentColor" stroke-width="2.5"/>
      <circle cx="443" cy="150" r="6" fill="currentColor"/>
      <text x="443" y="112" text-anchor="middle" font-size="15" font-weight="700">0.344</text>
      <text x="443" y="92" text-anchor="middle" font-size="11.5" opacity="0.75">&#8220;so he knows it?&#8221;</text>
      <text x="443" y="76" text-anchor="middle" font-size="10.5" opacity="0.6">&#8212; and it is the WRONG chunk.</text>
      <text x="443" y="60" text-anchor="middle" font-size="10.5" opacity="0.6">MongoDB is not in the top 5 at all.</text>
    </g>

    <g>
      <line x1="751" y1="122" x2="751" y2="160" stroke="var(--fig-accent, #2B4FD4)" stroke-width="2.5"/>
      <circle cx="751" cy="150" r="7" fill="var(--fig-accent, #2B4FD4)"/>
      <text x="751" y="112" text-anchor="middle" font-size="16" font-weight="700" fill="var(--fig-accent, #2B4FD4)">0.620</text>
      <text x="751" y="92" text-anchor="middle" font-size="11.5" fill="var(--fig-accent, #2B4FD4)" opacity="0.85">&#8220;does he know MongoDB?&#8221;</text>
      <text x="751" y="76" text-anchor="middle" font-size="10.5" fill="var(--fig-accent, #2B4FD4)" opacity="0.7">the right chunk, rank 1</text>
    </g>

    <text x="40" y="224" font-size="11.5" opacity="0.6">Drop one keyword and the search lands nearer to</text>
    <text x="40" y="240" font-size="11.5" opacity="0.6">random noise than to the answer.</text>
  </g>
</svg>
```

---

## Figure 7 — What query rewriting changes (v2 article)

**Caption:** The same follow-up down two pipelines. The user types four identical words either way; one extra call before retrieval decides whether the system can answer at all.

```html
<svg viewBox="0 0 980 300" role="img" aria-label="Two paths for the same follow-up question. Without the rewriter, the search misses and the bot says it lacks context. With the rewriter, the question is rewritten to name MongoDB, the search hits, and the answer is correct.">
  <defs><marker id="ra" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" fill="currentColor">
    <text x="20" y="26" font-size="12" opacity="0.6">THE SAME FOLLOW-UP, TWO PIPELINES</text>

    <text x="20" y="70" font-size="11" opacity="0.5">WITHOUT THE REWRITER</text>
    <rect x="20" y="82" width="200" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.5"/>
    <text x="120" y="106" text-anchor="middle" font-size="12.5">&#8220;so he knows it?&#8221;</text>
    <text x="120" y="123" text-anchor="middle" font-size="10" opacity="0.6">no keyword to embed</text>
    <rect x="290" y="82" width="200" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.5"/>
    <text x="390" y="106" text-anchor="middle" font-size="12.5">search</text>
    <text x="390" y="123" text-anchor="middle" font-size="10" opacity="0.6">MongoDB chunk absent</text>
    <rect x="560" y="82" width="400" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.5"/>
    <text x="580" y="106" font-size="12">&#8220;I don&#8217;t have enough context to answer</text>
    <text x="580" y="123" font-size="12">what &#8216;it&#8217; refers to.&#8221;</text>
    <g stroke="currentColor" stroke-width="1.5" opacity="0.45" color="currentColor">
      <line x1="222" y1="108" x2="286" y2="108" marker-end="url(#ra)"/>
      <line x1="492" y1="108" x2="556" y2="108" marker-end="url(#ra)"/>
    </g>

    <line x1="20" y1="164" x2="960" y2="164" stroke="currentColor" stroke-width="1" opacity="0.18"/>

    <text x="20" y="196" font-size="11" fill="var(--fig-accent, #2B4FD4)" opacity="0.8">WITH THE REWRITER</text>
    <rect x="20" y="208" width="200" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.5"/>
    <text x="120" y="232" text-anchor="middle" font-size="12.5">&#8220;so he knows it?&#8221;</text>
    <text x="120" y="249" text-anchor="middle" font-size="10" opacity="0.6">identical question</text>
    <rect x="290" y="208" width="270" height="52" rx="3" fill="var(--fig-accent, #2B4FD4)" fill-opacity="0.1" stroke="var(--fig-accent, #2B4FD4)" stroke-width="2.5"/>
    <text x="425" y="230" text-anchor="middle" font-size="12" font-weight="700" fill="var(--fig-accent, #2B4FD4)">&#8220;Does Hemavardhan have</text>
    <text x="425" y="247" text-anchor="middle" font-size="12" font-weight="700" fill="var(--fig-accent, #2B4FD4)">knowledge of MongoDB?&#8221;</text>
    <rect x="630" y="208" width="150" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <text x="705" y="232" text-anchor="middle" font-size="12.5">search</text>
    <text x="705" y="249" text-anchor="middle" font-size="10" opacity="0.6">right chunk, rank 1</text>
    <rect x="810" y="208" width="150" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <text x="885" y="232" text-anchor="middle" font-size="12.5">correct answer</text>
    <text x="885" y="249" text-anchor="middle" font-size="10" opacity="0.6">+ [boundaries.txt]</text>
    <g stroke="currentColor" stroke-width="1.5" color="currentColor">
      <line x1="222" y1="234" x2="286" y2="234" marker-end="url(#ra)"/>
      <line x1="562" y1="234" x2="626" y2="234" marker-end="url(#ra)"/>
      <line x1="782" y1="234" x2="806" y2="234" marker-end="url(#ra)"/>
    </g>
    <text x="20" y="288" font-size="11.5" opacity="0.6">One extra call, before retrieval. The user types the same four words either way.</text>
  </g>
</svg>
```
