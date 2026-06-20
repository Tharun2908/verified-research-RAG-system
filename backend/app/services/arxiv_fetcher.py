"""
backend/app/services/arxiv_fetcher.py

Phase A (M8): fetch real ML/NLP paper abstracts from the public arXiv API and write
them to a clean JSON file in the same shape as sample_papers.json, so the existing
ingestion can consume them.

arXiv API notes:
  - Public, no API key. Endpoint: http://export.arxiv.org/api/query
  - Returns Atom XML (an RSS-like feed). We parse it with the stdlib (xml.etree).
  - Be polite: the API asks for <=1 request every ~3 seconds. We page in batches
    of 100 with a delay between pages.
  - Query by category with `cat:cs.CL OR cat:cs.IR`, sorted by most recent.

Output: backend/data/arxiv_papers.json  -> [{title, authors, year, abstract, arxiv_id}]
"""

from __future__ import annotations

import time
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ARXIV_API = "http://export.arxiv.org/api/query"
# Atom XML namespaces used in arXiv responses.
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def _fetch_page(search_query: str, start: int, page_size: int) -> str:
    """Fetch one page of results as raw XML text."""
    params = {
        "search_query": search_query,
        "start": start,
        "max_results": page_size,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "verified-rag-system/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def _parse_entries(xml_text: str) -> list[dict]:
    """Parse one XML page into a list of paper dicts."""
    root = ET.fromstring(xml_text)
    papers = []
    for entry in root.findall("atom:entry", NS):
        title = entry.findtext("atom:title", default="", namespaces=NS).strip()
        summary = entry.findtext("atom:summary", default="", namespaces=NS).strip()
        published = entry.findtext("atom:published", default="", namespaces=NS).strip()
        # id looks like http://arxiv.org/abs/2401.01234v1 -> take the tail
        raw_id = entry.findtext("atom:id", default="", namespaces=NS).strip()
        arxiv_id = raw_id.rsplit("/", 1)[-1] if raw_id else ""

        authors = [
            a.findtext("atom:name", default="", namespaces=NS).strip()
            for a in entry.findall("atom:author", NS)
        ]
        authors_str = ", ".join(authors[:5])  # cap to first 5 for brevity
        year = int(published[:4]) if len(published) >= 4 and published[:4].isdigit() else None

        # collapse internal whitespace/newlines in title + abstract
        title = " ".join(title.split())
        summary = " ".join(summary.split())

        # skip entries with no usable abstract
        if not summary:
            continue

        papers.append({
            "title": title,
            "authors": authors_str,
            "year": year,
            "abstract": summary,
            "arxiv_id": arxiv_id,
        })
    return papers


def fetch_arxiv(
    categories: list[str],
    total: int = 250,
    page_size: int = 100,
    delay_seconds: float = 3.0,
    out_path: str = "data/arxiv_papers.json",
) -> int:
    """Fetch `total` abstracts across the given categories; write JSON. Returns count."""
    # query: (cat:cs.CL OR cat:cs.IR) AND (topic keywords in abstract)
    cat_clause = " OR ".join(f"cat:{c}" for c in categories)
    topic_terms = [
        "hallucination",
        "retrieval",
        "retrieval-augmented",
        "faithfulness",
        "grounding",
        "RAG",
        "factuality",
    ]
    topic_clause = " OR ".join(f'abs:"{t}"' for t in topic_terms)
    search_query = f"({cat_clause}) AND ({topic_clause})"

    all_papers: list[dict] = []
    seen_ids: set[str] = set()

    start = 0
    while len(all_papers) < total:
        xml_text = _fetch_page(search_query, start=start, page_size=page_size)
        page = _parse_entries(xml_text)
        if not page:
            break  # no more results

        for p in page:
            if p["arxiv_id"] in seen_ids:
                continue
            seen_ids.add(p["arxiv_id"])
            all_papers.append(p)
            if len(all_papers) >= total:
                break

        start += page_size
        print(f"  fetched {len(all_papers)}/{total}...")
        if len(all_papers) < total:
            time.sleep(delay_seconds)  # be polite to the API

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_papers, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(all_papers)} papers to {out_path}")
    return len(all_papers)


if __name__ == "__main__":
    fetch_arxiv(categories=["cs.CL", "cs.IR"], total=250)
