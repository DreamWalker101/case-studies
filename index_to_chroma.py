#!/usr/bin/env python3
"""
index_to_chroma.py — Index all case studies into ChromaDB for agent access.
Collection: "ahmed-context"

Chunks each case study into meaningful sections (## headings) so queries
like "how does the pipeline handle VRAM?" return the right section, not
the entire document.

Usage:
  python3 index_to_chroma.py           # index/reindex everything
  python3 index_to_chroma.py --query "how does triage work"
"""

import sys
import os
import re
import httpx
import chromadb
from pathlib import Path

CHROMA_DB_PATH   = os.path.expanduser("~/.claude-pipeline/chroma_db")
COLLECTION       = "ahmed-context"
OLLAMA_HOST      = "http://localhost:11434"
EMBED_MODEL      = "nomic-embed-text"
CASE_STUDIES_DIR = Path(__file__).parent


def get_embedding(text: str) -> list[float]:
    r = httpx.post(
        f"{OLLAMA_HOST}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=30
    )
    r.raise_for_status()
    return r.json()["embedding"]


def chunk_markdown(content: str, source_file: str) -> list[dict]:
    """
    Split markdown into chunks at ## headings.
    Each chunk gets metadata: file, section, project.
    """
    chunks = []
    project = Path(source_file).parent.name

    # Split on ## headings (keep the heading with its content)
    parts = re.split(r'\n(?=## )', content)

    for part in parts:
        part = part.strip()
        if not part or len(part) < 50:
            continue

        # Extract section title
        first_line = part.splitlines()[0].strip()
        section = re.sub(r'^#+\s*', '', first_line) if first_line.startswith('#') else "Overview"

        chunks.append({
            "text": part[:4000],  # nomic-embed-text max
            "metadata": {
                "project": project,
                "file": Path(source_file).name,
                "section": section,
                "source_path": str(source_file),
                "type": "case_study" if "CASE_STUDY" in source_file else "context",
            }
        })

    return chunks


def index_all():
    os.makedirs(CHROMA_DB_PATH, exist_ok=True)
    client     = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(COLLECTION)

    # Find all markdown files in case-studies
    md_files = list(CASE_STUDIES_DIR.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files")

    all_ids, all_embeddings, all_docs, all_metas = [], [], [], []

    for md_file in md_files:
        content = md_file.read_text()
        chunks  = chunk_markdown(content, str(md_file))
        print(f"  {md_file.relative_to(CASE_STUDIES_DIR)}: {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            doc_id = f"{md_file.stem}::{chunk['metadata']['section']}::{i}"
            try:
                embedding = get_embedding(chunk["text"])
            except Exception as e:
                print(f"    ⚠️  Embedding failed for chunk {i}: {e}")
                continue

            all_ids.append(doc_id)
            all_embeddings.append(embedding)
            all_docs.append(chunk["text"][:1500])
            all_metas.append(chunk["metadata"])

    if all_ids:
        collection.upsert(
            ids=all_ids,
            embeddings=all_embeddings,
            documents=all_docs,
            metadatas=all_metas
        )
        print(f"\n✅ Indexed {len(all_ids)} chunks into '{COLLECTION}' collection")
    else:
        print("No chunks to index")


def query(q: str, n: int = 5):
    client     = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(COLLECTION)

    embedding = get_embedding(q)
    results   = collection.query(
        query_embeddings=[embedding],
        n_results=n,
        include=["documents", "metadatas", "distances"]
    )

    print(f"\nQuery: {q}\n{'─'*50}")
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        print(f"\n📄 [{meta['project']}] {meta['section']} ({meta['file']})  score={1-dist:.2f}")
        print(doc[:400])
        print()


if __name__ == "__main__":
    if "--query" in sys.argv:
        idx = sys.argv.index("--query")
        q   = " ".join(sys.argv[idx+1:])
        query(q)
    else:
        index_all()
