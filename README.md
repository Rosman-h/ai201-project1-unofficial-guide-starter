# Howard University Off-Campus Housing: Unofficial Guide

## Domain

Off-campus housing near Howard University is one of the most stressful parts of the college experience, but Howard's official channels offer almost no guidance on which specific apartments are worth it.This system makes that scattered student knowledge searchable in one place.

## Document Sources

1. The Oliver - Google Reviews
2. The Avenue Apartments - Google Reviews
3. Trellis House - Google Reviews
4. Trellis House - ApartmentRatings.com
5. Mazza GrandMarc - Google Reviews
6. Clover at The Parks - Google Reviews
7. r/HowardUniversity - "how does off campus housing work?"
8. r/GradAdmissions - "Grad student rent in DC"
9. r/washingtondc - "cheaper apartments in May/June?"
10. r/washingtondc - "intern housing DC fall semester"

## Chunking Strategy

Documents were split by paragraph with a maximum chunk size of 500
characters. This approach was chosen because documents consist of
short reviews and Reddit comments — each paragraph represents one
complete opinion. Fixed character splitting was avoided because it
would cut sentences mid-thought. Overlap was not used since each
review is already a self-contained unit.

## Sample Chunks

**Chunk 1** (avenue_google_reviews.txt)
"Two thumbs down. WE WANT MRS. BLOUNT BACK!!! Throwback the new bring
back the experience with dignity, pride, respect, helpful, intelligence,
and humanity!!! Overall the apartment building is nice. The tenants are
friendly. It's been 1 year since residing here. I'm satisfied."

**Chunk 2** (clover_google_reviews.txt)
"Common Clover is not a good place to rent. They are charging very high
prices, advertising that they will do maintenance and cleaning of the
apartments once a week, but when they come, they do so for a few minutes
and the apartment is left dirty. Living at Common Clover was the best
solution to my senior year of college I never thought I'd find."

**Chunk 3** (reddit_dc_apartments_seasonal.txt)
"Response: People tend to move more in the spring and early summer so yes
availability will be up but so will prices. Moving in the dead of winter
is much less desirable and prices reflect the lower foot traffic.
Apartments that become available in fall and winter will stay empty for
several months so landlords offer lower rents to get tenants in."

**Chunk 4** (trellis_apartmentratings.txt)
"Nice and safe facility with spacious living spaces. Location easily
accessible. Well maintained. Staff are very accommodating. Parking is
plentiful. The only thing that hasn't been great was the front desk
staff — sometimes they can be rude. Also the gym equipment needs to
be fixed and it gets hot in there."

**Chunk 5** (mazza_google_reviews.txt)
"I've had a pretty good experience living at Mazza. The office is filled
with students so it's hard to get your questions answered properly
sometimes. The gym is bad, a lot of the equipment doesn't work. I do
feel safe here and the rent is affordable."

## Embedding Model

Model used: all-MiniLM-L6-v2 (sentence-transformers, runs locally)

For a production deployment I would consider:

- text-embedding-3-large (OpenAI) for higher accuracy but adds
  API cost and latency
- A multilingual model if serving international students
- A domain-specific model fine-tuned on housing reviews for
  better semantic matching

## Retrieval Test Results

**Query 1:** What do students say about noise at Trellis House?
Top chunks retrieved:

- trellis_google_reviews.txt (distance: 0.956): "Trellis House Apartments —
  I live here for more than 5 years. This spectacular place has amenities..."
- trellis_google_reviews.txt (distance: 0.966): "I've now been at Trellis
  House for six years, and from the moment I moved in, it's always felt
  like home..."
- trellis_google_reviews.txt (distance: 1.012): "If you would like to sleep
  and live in peace and quiet I strongly suggest not living here. The
  materials used are not great from a sound perspective..."

Relevance: Partially accurate. The most relevant chunk (noise complaint)
ranked 3rd behind generic positive reviews. The correct source was
retrieved but distance scores were high (0.95+) indicating weak semantic
matching between "noise" and "peace and quiet."

**Query 2:** How do Howard students afford off campus housing?
Top chunks retrieved:

- reddit_howard_offcampus.txt (distance: 0.366): "Question: How does off
  campus housing work at Howard?..."
- reddit_howard_offcampus.txt (distance: 0.567): "Response: I can attest
  to each of the comments so far being true. My mom paid my rent using
  the refund checks..."
- reddit_howard_offcampus.txt (distance: 0.700): "Response: Personally I
  work part time to cover rent. Some people have their parents pay..."

Relevance: Accurate. All top chunks came from the correct source with
low distance scores. The retrieval correctly identified the Reddit thread
as the most relevant document.

**Query 3:** Is Mazza a good place to live for Howard students?
Top chunks retrieved:

- mazza_google_reviews.txt (distance: 0.396): "Mazza has been a nice place
  to live as a Howard student. If they had shuttles I would live here
  again..."
- mazza_google_reviews.txt (distance: 0.578): "Living here at Mazza has
  been great. The rooms and amenities make the place more fun..."
- mazza_google_reviews.txt (distance: 0.581): "I am a Howard student
  currently leasing with Mazza. I have had the pleasure to be here for
  my Junior year..."

Relevance: Accurate. All top chunks came from the correct source with
low distance scores. Retrieval correctly prioritized Howard student
perspectives on Mazza.

## Grounded Generation

Grounding is enforced through the system prompt in query.py, which
explicitly instructs the model to answer ONLY from the retrieved
documents and to say "I don't have enough information on that" if
the documents don't cover the question. Source attribution is
collected programmatically from chunk metadata and appended to
every response.

## Example Responses

**Example 1 — grounded response with source citation:**

Question: What do students say about noise at Trellis House?

Answer: Students say that Trellis House is very loud, with thin walls
that allow them to hear their neighbors as if they are right next to
them. They also mention that the footsteps from the upstairs neighbors
can be heard, and some have had issues with noise from neighbors,
particularly those who live on the west side of the building near
Sherman Avenue, a big commuter road. One student warned that if you
want to sleep and live in peace and quiet, you should not live at
Trellis House. Despite this, one student had a different experience
and found their neighbors to be respectful and pleasant.

Sources: trellis_google_reviews.txt, oliver_google_reviews.txt

**Example 2 — grounded response with source citation:**

Question: How do Howard students afford off campus housing?

Answer: Howard students afford off-campus housing in several ways:

1. Some take out loans to pay for rent.
2. Others use their refund checks from scholarships or financial aid
   that exceed their school balance.
3. Some students work part-time to cover rent.
4. Some have their parents or family members pay for rent.
   It is also noted that taking out loans for rent is not recommended.

Sources: reddit_howard_offcampus.txt, trellis_apartmentratings.txt,
reddit_grad_rent_dc.txt

**Out-of-scope query — system declines to answer:**

Question: What are the best neighborhoods in Los Angeles for students?

Answer: I don't have enough information on that in my sources.

Sources: (none relevant)

## Query Interface

The interface is built with Gradio and runs at http://127.0.0.1:7860.
Input: a plain text question typed into a textbox.
Output: a grounded answer and a list of source documents it drew from.
To run: python app.py

## Evaluation Report

| #   | Question                                                      | Expected Answer                                                                           | System Response                                                                            | Accuracy           |
| --- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------ |
| 1   | What do students say about noise at Trellis House?            | Thin walls, loud neighbors, footsteps, Sherman Ave noise, management unresponsive         | Correctly identified thin walls, Sherman Ave, upstairs neighbors, noted dissenting opinion | Accurate           |
| 2   | How do Howard students afford off campus housing?             | Refund checks, part-time work, parental support, loans (not recommended)                  | Listed all 4 methods correctly, noted loans not recommended                                | Accurate           |
| 3   | Is Mazza a good option for Howard students?                   | Mixed — affordable and close to Howard but inconsistent management, broken gym, AC issues | Correctly gave balanced mixed response citing both positives and negatives                 | Accurate           |
| 4   | What is the realistic rent range for a studio in DC?          | Roughly $1,200-$1,600/month for a studio                                                  | Correctly stated $1,200-$1,600 range with specific examples                                | Accurate           |
| 5   | How far in advance should I look for DC housing as an intern? | About 2 months in advance                                                                 | Correctly said 2 months in advance                                                         | Partially Accurate |

**Notes:**

- Question 5 was marked partially accurate because trellis_apartmentratings.txt
  was retrieved as a source despite containing no relevant information about
  intern housing timelines. This is a retrieval noise issue.
- All 5 questions were answered using only retrieved documents with no
  hallucination detected.

## Failure Case

**Query:** What do students say about noise at Trellis House?

**What went wrong:** The retrieval returned high distance scores (0.95+)
for all chunks, and the most relevant chunk — the one explicitly
complaining about noise — ranked 3rd behind two generic positive reviews.

**Why it happened:** The query used the word "noise" but the actual
complaint in the document used the phrase "peace and quiet" and "you can
hear all your neighbors." The embedding model did not closely match these
semantically related but differently worded phrases, resulting in weak
retrieval scores across all chunks.

**Pipeline stage:** Retrieval (embed.py) — the embedding model failed to
bridge the semantic gap between the query vocabulary and the document
vocabulary.

**How it could be fixed:** Hybrid search combining semantic search with
keyword (BM25) search would have caught "noise" as a keyword match even
when the semantic similarity was weak. This is listed as a stretch feature
in the project spec.

## Spec Reflection

**One way the spec helped:** Writing the chunking strategy in planning.md
before touching any code forced me to think about the structure of my
documents first. When the initial fixed character chunking produced
fragments like "tenants are friendly." with no context, I already had a
clear rationale in my spec for why paragraph-based chunking fit my
documents better. That made the fix obvious rather than a guess.

**One way implementation diverged from the spec:** My planning.md specified
a chunk size of 300 characters with 50 character overlap. During
implementation I switched to paragraph-based chunking with a 500 character
maximum and no overlap. This was because my documents are structured as
one review per paragraph, so splitting by paragraph boundaries produced
more meaningful chunks than splitting by character count. The spec was
updated to reflect this change.

## AI Usage

**Instance 1: ingest.py**
I gave Claude my chunking strategy from planning.md and asked it to write
the ingestion script. It generated fixed character chunking which produced
fragments. I caught this by inspecting the sample chunks and told Claude
to switch to paragraph-based splitting instead.

**Instance 2: embed.py**
I asked Claude to implement the embedding and retrieval code. It worked
but crashed silently on the second query because it reloaded the model
every time retrieve() was called. I identified the issue and directed
Claude to load the model once at the module level instead.

**Instance 3: query.py**
I asked Claude to write the grounded prompt template. I reviewed it and
tested it with an out-of-scope question to confirm the system declined
to answer rather than making something up.
