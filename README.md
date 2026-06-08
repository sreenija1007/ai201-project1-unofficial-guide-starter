# The Unofficial Guide: UCLA Campus Dining

## Domain

UCLA Campus Dining

UCLA always wins the number 1 college food ranking and honestly the food is pretty good. But that doesn't tell you which dining hall to actually go to on a Tuesday night or whether the meal plan is worth paying for if you're not on the Hill. The official dining website is basically just marketing. The real opinions are on reddit and yelp and nowhere brings them together.

This system tries to fix that. You ask a question in plain English and it pulls from actual student reviews to give you an answer with sources.

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | UCLA Housing Dining Locations | Official | https://housing.ucla.edu/dining-locations |
| 2 | UCLA Housing Discover Dining 2025 | Official | https://housing.ucla.edu/discover-dining-2025 |
| 3 | ASUCLA Dining Hall Guide | Student guide | https://asucla.ucla.edu/ucla/ucla-dining-hall |
| 4 | UCLA Adminvc Dining Best 2023 | News | https://adminvc.ucla.edu/news-views/fall-2023/ucla-dining-named-best-nation-seventh-time |
| 5 | UCLA Adminvc Dining Number 1 2025 | News | https://adminvc.ucla.edu/news-views/summer-2025/ucla-dining-remains-no-1-nation |
| 6 | Reddit r/UCLA dining threads | Reddit | https://www.reddit.com/r/ucla/search/?q=dining+hall&sort=top |
| 7 | Reddit r/UCLA meal plan threads | Reddit | https://www.reddit.com/r/ucla/search/?q=meal+plan+worth+it&sort=top |
| 8 | Niche.com UCLA food reviews | Reviews | https://www.niche.com/colleges/university-of-california-los-angeles/reviews/?topic=food |
| 9 | Yelp Bruin Plate | Reviews | https://www.yelp.com/biz/bruin-plate-los-angeles |
| 10 | Yelp De Neve | Reviews | https://www.yelp.com/biz/de-neve-dining-los-angeles |
| 11 | Yelp Epicuria at Covel | Reviews | https://www.yelp.com/biz/epicuria-at-covel-los-angeles |
| 12 | UCLA Dining Portal | Official | https://dining.ucla.edu |

## Chunking Strategy

**Chunk size:** 300 tokens for the official pages and news articles, 150 for yelp/reddit/niche reviews

**Overlap:** 50 tokens for long documents, 20 for reviews

**Why these choices fit your documents:** Reviews are short and self-contained so I chunk them whole or close to it. Splitting a yelp review mid-sentence loses the whole point of that review. The official pages are longer and sometimes a key detail like late night hours is buried in the middle of a paragraph, so the overlap helps make sure that context doesn't get cut off at a chunk boundary. I used LangChain's RecursiveCharacterTextSplitter so it tries to break at paragraphs first before falling back to sentences.

**Final chunk count:** 284 chunks total

## Embedding Model

**Model used:** sentence-transformers/all-MiniLM-L6-v2

**Production tradeoff reflection:** I went with MiniLM because it's free and runs locally, no API key needed. It works well enough for short review text. If I were actually deploying this I'd probably try OpenAI's embedding models since they tend to be more accurate especially for weird or informal phrasing, but they cost money. I'd also think about whether I need multilingual support since UCLA has students from all over who might not be writing reviews in perfect standard English. The 256 token limit is fine for most of my chunks but a few of the longer official page chunks might lose some quality at the edges.

## Grounded Generation

**System prompt grounding instruction:** "Answer the question using only the context passages below. Don't use anything you know about UCLA dining that isn't in the context. If the context doesn't have enough to answer, just say so. At the end of your answer list which sources you used."

**How source attribution is surfaced in the response:** Every response ends with a sources list showing the document name and URL for each chunk that was actually used. I also filter out any chunks with a similarity score below 0.55 before passing them to the model since those are usually off-topic.

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What dining hall is known for healthy food at UCLA? | Bruin Plate, local produce, organic, no soda | Got it right, cited the ASUCLA guide and official dining page | Relevant | Accurate |
| 2 | What is De Neve Late Night? | Extended hours at De Neve after dinner for meal plan students | Correct, described the late night hours and who can use it | Relevant | Accurate |
| 3 | How is Epicuria different from De Neve? | Epicuria is Mediterranean, De Neve is American style | Nailed it, gave specific food examples from both halls | Relevant | Accurate |
| 4 | How many times has UCLA been ranked number 1 for food? | 9 out of the last 10 years as of 2025 | Correct, cited the 2025 news article | Relevant | Accurate |
| 5 | What do students say about the meal plan for off-campus students? | Mixed, hard to justify if you can't use it for dinner | Pulled general meal plan info instead of actual student opinions on cost | Partially relevant | Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

## Failure Case Analysis

**Question that failed:** What do students say about the meal plan for off-campus students?

**What the system returned:** It described the meal plan tiers and the rule about dinner being restricted to residential students. Technically accurate but not what the question was asking. There were no actual student opinions about whether the plan is worth the cost.

**Root cause (tied to a specific pipeline stage):** The reddit threads I collected were mostly dining hall tier list discussions, not specifically about meal plan cost for off-campus students. So when retrieval ran, the closest chunks were the official pricing pages, not student opinions. The model answered from what it had but what it had was the wrong stuff. This is a data collection problem more than anything else.

**What you would change to fix it:** Find reddit threads specifically about the meal plan cost debate. There are definitely posts like "is the UCLA meal plan worth it as a sophomore" that I just didn't collect. I'd also add a check where if the top similarity scores are all below some threshold the system says it doesn't have good sources for this instead of answering from weak matches.

## Spec Reflection

**One way the spec helped you during implementation:** Having the two chunk sizes written down before I started coding made it way easier to write chunk.py. I didn't have to figure out the logic while coding, I just implemented what the spec said. Saved me from going back and forth.

**One way your implementation diverged from the spec, and why:** I estimated about 280 chunks but ended up with 284 which is close but some yelp pages had more reviews than I expected when I actually scraped them. Not a big deal but the estimate was slightly off.

## AI Usage

**Instance 1**

- What I gave the AI: The Chunking Strategy section from planning.md and a saved HTML file from the UCLA Housing dining page
- What it produced: A scrape.py script that used BeautifulSoup to grab the main content and strip nav/footer, saved to txt with a metadata header
- What I changed or overrode: The selector it used worked on the Housing pages but broke on the Adminvc news pages which have a different HTML structure. I had to manually look at the news page HTML and update the selector for those

**Instance 2**

- What I gave the AI: The Retrieval Approach section and an example chunk file showing the format
- What it produced: ingest.py that embedded all chunks and stored them in ChromaDB
- What I changed or overrode: It tried to embed everything in one batch call and my laptop ran out of memory. I changed it to process 50 chunks at a time instead
