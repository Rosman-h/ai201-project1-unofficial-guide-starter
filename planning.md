# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

## Domain

Off-campus housing experiences for Howard University students and DC renters.
This knowledge is valuable because official Howard channels don't tell you
which apartments have noise issues, broken AC, or predatory management —
students have to find that out the hard way or from each other.
Off-campus housing near Howard University is one of the most stressful parts of the college experience, but Howard's official channels offer almost no guidance on which specific apartments are worth it.This system makes that scattered student knowledge searchable in one place.

## Documents

1. The Oliver — Google Reviews (maps.google.com)
2. The Avenue Apartments — Google Reviews (maps.google.com)
3. Trellis House — Google Reviews (maps.google.com)
4. Trellis House — ApartmentRatings.com
5. Mazza GrandMarc — Google Reviews (maps.google.com)
6. Clover at The Parks — Google Reviews (maps.google.com)
7. r/HowardUniversity — "how does off campus housing work?" thread
8. r/GradAdmissions — "Grad student rent in DC" thread
9. r/washingtondc — "cheaper apartments available in May/June?" thread
10. r/washingtondc — "intern housing DC fall semester" thread

## Chunking Strategy

Documents are a mix of short reviews (1–5 sentences) and Reddit
comment threads (conversational, variable length).

Chunk size: ~300 characters with 50-character overlap.

Rationale: Most reviews express one complete thought in 2–4 sentences.
A 300-character chunk captures a full opinion without merging unrelated
reviews together. Overlap ensures that a key fact near a chunk boundary
(e.g. "AC broken for 3 weeks" split across two chunks) appears in at
least one complete chunk. Reddit comments are similarly short, so the
same size fits both source types.

## Retrieval Approach

Embedding model: all-MiniLM-L6-v2 (sentence-transformers, runs locally)
Top-k: 5 chunks per query

Rationale: 5 chunks gives the LLM enough context to synthesize
multiple opinions without drowning it in loosely related text.

Production tradeoffs I'd consider: text-embedding-3-large (OpenAI) for
higher accuracy but adds API cost and latency; multilingual models if
serving international students; a longer context model if reviews were
much longer.

## Evaluation Plan

1. Q: What do students say about noise at Trellis House?
   A: Multiple reviewers mention thin walls, loud neighbors,
   and footsteps from above. Management rarely resolves complaints.

2. Q: How do Howard students afford off-campus housing?
   A: Through refund checks, part-time jobs, parental support,
   or loans (though loans are discouraged).

3. Q: Is Mazza GrandMarc a good option for Howard students?
   A: Mixed — affordable and close to Howard, but inconsistent
   management, broken gym equipment, and AC issues reported.

4. Q: What is the realistic rent range for a studio in DC?
   A: Roughly $1,200–$1,600/month for a studio; under $1,000
   requires sharing a room with roommates.

5. Q: How far in advance should I look for DC housing as an intern?
   A: About 2 months in advance; furnished finder and university
   Facebook groups are recommended for short-term leases.

## Anticipated Challenges

1. Chunk boundary splits: A negative review like "the AC has been
   broken for 3 weeks" might get split mid-sentence, making
   retrieval miss the complaint entirely.
2. Review noise: Many reviews are generic praise ("great staff!")
   with no specific information. These chunks will get retrieved
   for almost any query and dilute useful responses.

## AI Tool Plan

- Ingestion + chunking: I'll share my Documents section and
  Chunking Strategy with Claude and ask it to write ingest.py
  that loads .txt files, cleans boilerplate (owner responses,
  ad text, photo references), and chunks at ~300 chars with
  50-char overlap.
- Embedding + retrieval: I'll share my Retrieval Approach section
  and ask Claude to write embed.py that uses all-MiniLM-L6-v2
  and stores chunks in ChromaDB with source metadata.
- Generation: I'll ask Claude to write query.py with a Groq prompt
  that enforces grounding and outputs source attribution.
- Interface: I'll ask Claude to scaffold a Gradio app.py using
  the example from the project spec.

## Architecture

Document Ingestion (.txt files)
↓
Cleaning (remove owner responses, ads, photo tags)
↓
Chunking (~300 chars, 50 overlap)
↓
Embedding (all-MiniLM-L6-v2, sentence-transformers)
↓
Vector Store (ChromaDB, local)
↓
Retrieval (top-5 semantic search)
↓
Generation (Groq llama-3.3-70b-versatile, grounded prompt)
↓
Gradio Interface (query input → answer + sources)

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
