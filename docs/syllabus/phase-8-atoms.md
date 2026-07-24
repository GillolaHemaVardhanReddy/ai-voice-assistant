# Phase 8 — FINE-TUNING & HUGGING FACE (train your own)

Goal: customize a *pretrained* model on your own examples — the practical, affordable kind of "training." Now that you understand the internals (Phase 7), this makes full sense. 🔧 = open-the-hood atom.

| Atom | Idea you'll learn | What you'll do | You'll end up with |
|------|-------------------|----------------|--------------------|
| **8.0** | What fine-tuning is (and isn't) | See where it beats prompting/RAG | A clear decision rule |
| **8.1 🔧** | What fine-tuning actually changes (weights nudged) | Connect to Phase 7 training | The real picture |
| **8.2** | The Hugging Face ecosystem | Tour `transformers`, `datasets`, `tokenizers` | The toolkit |
| **8.3** | Run a pretrained model locally | Load + generate with a small model | HF working on your machine |
| **8.4** | Build a small dataset | Make ~100 example pairs | Training data |
| **8.5** | Fine-tune it | Run a fine-tune with `Trainer` | A customized model |
| **8.6 🔧** | **LoRA/PEFT** — cheap, efficient fine-tuning | Fine-tune with LoRA | The affordable way |
| **8.7** | Evaluate it | Measure before vs after | Proof it improved |
| **8.8** | Wrap it up | A model tuned for your assistant | **Your own trained model** |
