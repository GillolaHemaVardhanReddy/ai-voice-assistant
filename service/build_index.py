import numpy as np
from pathlib import Path
from .embedder import encode


NOTES_DIR = Path(__file__).parent / "notes"
files = sorted(str(p) for p in NOTES_DIR.glob("*.txt"))
print(files)

chunks = []
embed_texts = []
sources=[]
for file in files:
    text = open(file, "r").read()
    section = ""
    for block in text.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        if block.startswith("#"):
            section = block.lstrip("# ").strip()
        else:
            chunks.append(block)
            embed_texts.append(f"{section}: {block}")
            sources.append(file.split("/")[-1])

assert len(chunks) == len(embed_texts) == len(sources)
print(len(files), "files →", len(chunks), "chunks")

vecs = encode(embed_texts).astype(np.float32)

np.savez(Path(__file__).parent / "index.npz", vecs=vecs, chunks=chunks, sources=sources)
print("saved", vecs.shape)