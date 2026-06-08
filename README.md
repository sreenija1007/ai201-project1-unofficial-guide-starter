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

**Chunk size:** 300 tokens for official pages and news articles, 150 for yelp, reddit, and niche reviews

**Overlap:** 50 tokens for long documents, 20 for reviews

**Why these choices fit your documents:** Reviews are short and self-contained so I chunk them whole or close to it. Splitting a yelp review mid-sentence loses the whole point of that review. The official pages are longer and sometimes a key detail like late night hours is buried in the middle of a paragraph, so the overlap helps make sure that context doesn't get cut off at a chunk boundary. I used LangChain's RecursiveCharacterTextSplitter so it tries to break at paragraphs first before falling back to sentences.

**Final chunk count:** 46 chunks

## Embedding Model

**Model used:** sentence-transformers/all-MiniLM-L6-v2

**Production tradeoff reflection:** I went with MiniLM because it's free and runs locally, no API key needed. It works well enough for short review text. If I were actually deploying this I'd probably try OpenAI's embedding models since they tend to be more accurate especially for weird or informal phrasing, but they cost money. I'd also think about whether I need multilingual support since UCLA has students from all over who might not be writing reviews in perfect standard English. The 256 token limit is fine for most of my chunks but a few of the longer official page chunks might lose some quality at the edges.

## Sample Chunks

**Chunk 1** (source: 12_dining_portal.txt)
```
UCLA Dining Portal
UCLA Dining provides a range of dining options for students, faculty, staff, and guests. During the academic school year we offer four all-you-care-to-eat residential restaurants and multiple quick-service locations.
Residential Restaurants (All-You-Care-To-Eat)
Bruin Plate - Sunset Village - Healthy and sustainable eating, locally sourced ingredients
```

**Chunk 2** (source: 09_yelp_bruin_plate.txt)
```
4 stars - Best option for vegetarians
As a vegetarian Bruin Plate is the only dining hall where I feel like I have real choices. The plant-based options are creative and filling not just a sad salad. The grain bowls and flatbreads are excellent. Highly recommend for anyone with dietary restrictions.
```

**Chunk 3** (source: 01_dining_locations.txt)
```
Quick Service Locations
Bruin Cafe: coffee, pastries, grab and go items
The Study at Hedrick: artisan bakery, coffee bar, open 24 hours
Rendezvous: Asian and Latin cuisine
Epicuria at Ackerman: Mediterranean food in the student union
Bruin Bowl: custom bowls, healthy options
```

**Chunk 4** (source: 07_reddit_mealplan.txt)
```
Post: Breaking down the UCLA meal plan cost - is it worth it?
Comment: Did the math last quarter. Meal plan works out to about 14 dollars per meal if you use every single swipe. You can eat off campus in Westwood for less than that at a lot of places. The only advantage is convenience and not having to think about food.
```

**Chunk 5** (source: 03_asucla_guide.txt)
```
Bruin Plate is known as the healthy dining hall that serves seasonal fresh dishes. Some popular items include roasted herb chicken, arugula-topped flatbread, baked potatoes and yams, tuna poke bowls and more. This UCLA dining hall does not serve soda but rather fruit-infused water such as pineapple, lime or strawberry water.
```

## Grounded Generation

**System prompt grounding instruction:** "You are an assistant that answers questions about UCLA campus dining. Use ONLY the documents provided below to answer. Do not use any outside knowledge. If the documents do not contain enough information to answer confidently, say exactly: I don't have enough information in my documents to answer that. For every claim in your answer, say which document it came from using the label like (Document 1) or (Document 3)."

**How source attribution is surfaced in the response:** Every response ends with a sources section listing the URL for each document that was actually used. Chunks with a similarity distance above 0.7 are filtered out before being passed to the model. The model is also instructed to label each claim with the document it came from inline in the answer itself.

## Retrieval Test Results

**Query 1: "What dining hall is known for healthy food at UCLA?"**

Top results:
- Result 1 (distance=0.473, source: 04_best_nation_2023.txt) — News article about UCLA dining rankings, mentions Bruin Plate emphasizing healthy eating
- Result 2 (distance=0.520, source: 02_discover_dining.txt) — Official dining overview mentioning Bruin Plate champions healthy eating with locally sourced produce
- Result 3 (distance=0.539, source: 11_yelp_epicuria.txt) — Yelp review of Epicuria, not directly relevant to healthy food

Results 1 and 2 are relevant because they both describe Bruin Plate in the context of healthy eating. Result 3 is a weaker match. The distance scores on results 1 and 2 are below 0.55 which indicates solid retrieval for this query.

**Query 2: "What is De Neve Late Night and when does it run?"**

Top results:
- Result 1 (distance=0.851, source: 10_yelp_de_neve.txt) — Yelp review specifically describing De Neve Late Night, says it runs until 2am
- Result 2 (distance=0.977, source: 10_yelp_de_neve.txt) — Another De Neve review mentioning late night after 10pm
- Result 3 (distance=1.075, source: 10_yelp_de_neve.txt) — De Neve Late Night during finals, open until 2am

The content is relevant and the right source is being retrieved. However the distance scores are high, all above 0.85, which means the semantic match is weaker than ideal. This is because the question uses "De Neve Late Night" as a proper noun which MiniLM doesn't treat as a special entity. The system still returns the right documents but confidence is lower.

**Query 3: "Is the UCLA meal plan worth it for off campus students?"**

Top results:
- Result 1 (distance=0.240, source: 07_reddit_mealplan.txt) — Reddit comment breaking down cost at 14 dollars per meal, says convenience is the only advantage
- Result 2 (distance=0.308, source: 07_reddit_mealplan.txt) — Student saying they kept the plan second year and regretted it
- Result 3 (distance=0.319, source: 07_reddit_mealplan.txt) — Student saying "Honestly no" if you live off The Hill

This is the best retrieval of the three queries. Distance scores are very low, all under 0.35, meaning strong semantic matches. All top results come from the dedicated meal plan reddit thread which is exactly the right source.

## Example Responses

**Response 1 — working well**

Query: "What dining hall at UCLA is known for healthy food?"

Response: According to the ASUCLA dining guide (Document 1), Bruin Plate is known as the healthy dining hall at UCLA. It serves seasonal fresh dishes including roasted herb chicken, tuna poke bowls, and arugula flatbread. It does not serve soda, offering fruit-infused water instead. The official dining overview (Document 2) also describes Bruin Plate as championing healthy eating with locally sourced produce, organic options, and sustainable seafood.

Sources: https://housing.ucla.edu/discover-dining-2025, https://asucla.ucla.edu/ucla/ucla-dining-hall

**Response 2 — working well**

Query: "Is the UCLA meal plan worth it for off campus students?"

Response: Based on student opinions (Document 1), most off-campus students find the meal plan hard to justify. One student calculated it works out to about 14 dollars per meal, and notes you can eat cheaper in Westwood. Another student said they kept it second year and regretted it after unused swipes expired. The general consensus is the plan makes more sense if you live in the dorms where access is easy (Document 2).

Sources: https://www.reddit.com/r/ucla/search/?q=meal+plan+worth+it&sort=top

**Out-of-scope refusal**

Query: "What are UCLA gym hours?"

Response: I don't have enough information in my documents to answer that.

## Query Interface

The interface is a Gradio web app running at http://localhost:7860. There is one text input field where you type your question and an Ask button. The answer appears in a text box below and the sources used are listed underneath.

Sample interaction transcript:

User: Which dining hall should I go to for vegetarian options?

System: According to a Yelp review (Document 1), Bruin Plate is described as the only dining hall where vegetarians feel like they have real choices. The plant-based options are creative and filling, with grain bowls and flatbreads highlighted as excellent. The ASUCLA guide (Document 2) also confirms Bruin Plate has expanded vegetarian and vegan options and does not serve soda.

Sources: https://www.yelp.com/biz/bruin-plate-los-angeles, https://asucla.ucla.edu/ucla/ucla-dining-hall

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What dining hall at UCLA is known for healthy food options? | Bruin Plate, local produce, organic, no soda | Correctly identified Bruin Plate with locally sourced produce, sustainable seafood, organic options, vegetarian and vegan dishes. Cited Documents 2 and 4 | Relevant | Accurate |
| 2 | What is De Neve Late Night and when does it run? | Extended hours at De Neve after dinner for meal plan students, runs until 2am | System said it does not have enough information to answer. The documents contain relevant Yelp reviews about late night but the distance scores were too high and chunks were filtered out | Partially relevant | Inaccurate |
| 3 | How is Epicuria different from De Neve? | Epicuria is Mediterranean, De Neve is American style | Partially correct. Said Epicuria has more limited menu variety than De Neve but did not mention the cuisine difference specifically. Missed that De Neve is American style and Epicuria is Mediterranean | Partially relevant | Partially accurate |
| 4 | How many times has UCLA been ranked number 1 for college food? | Nine out of the last ten years as of 2025 | Returned 7 times instead of 9. Retrieved an older news article from 2023 which cited 7 times rather than the 2025 article with the updated count | Partially relevant | Partially accurate |
| 5 | What do students say about the meal plan if you live off campus? | Mixed, most say hard to justify | Good answer. Correctly captured that off-campus students can only use the plan for breakfast and lunch, cost works out to 12-15 dollars per meal, but noted one student found it worth it for convenience during midterms | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target
**Response accuracy:** Accurate / Partially accurate / Inaccurate

## Failure Case Analysis

**Question that failed:** What is De Neve Late Night and when does it run?

**What the system returned:** "I don't have enough information in my documents to answer that." The documents do contain Yelp reviews describing De Neve Late Night running until 2am but the system refused to answer.

**Root cause (tied to a specific pipeline stage):** This is a retrieval filtering failure. The distance scores for De Neve Late Night queries were all above 0.85 which triggered the 0.7 distance filter in query.py, causing all chunks to be dropped before reaching the LLM. The embedding model did not create a strong semantic match between the query phrase "De Neve Late Night" as a proper noun and the review text describing it. With only 46 chunks in the store there were not enough similar documents to produce a confident match. The filter that was meant to remove irrelevant results ended up removing all results for this query.

**What you would change to fix it:** Lower the distance threshold from 0.7 to 0.9 so that moderately relevant chunks still reach the LLM rather than being dropped entirely. Also add more dedicated documents about De Neve specifically so there are more chunks for the embedding model to match against. The 46 total chunk count is much lower than planned which hurts retrieval confidence across the board.

## Spec Reflection

**One way the spec helped you during implementation:** Having the two chunk sizes written down before coding made chunk.py straightforward to write. I didn't have to figure out the logic while coding, I just implemented what the spec said. It also helped me catch that review content and official content needed different treatment before writing a single line.

**One way your implementation diverged from the spec, and why:** I estimated about 280 chunks but ended up with only 46. The yelp and reddit pages had much less text than expected once cleaned, and several of the official pages were shorter than anticipated. This is significantly fewer chunks than planned which explains why some distance scores are high — there simply are not enough similar documents in the store for every query to find a strong match.

## AI Usage

**Instance 1**

- What I gave the AI: The Chunking Strategy section from planning.md and a sample HTML file from the UCLA Housing dining page
- What it produced: A scrape.py script using BeautifulSoup that grabbed the main content and stripped nav and footer, saved to txt with a metadata header
- What I changed or overrode: The selector it used worked on the Housing pages but broke on the Adminvc news pages which have a different HTML structure. I had to look at the news page HTML manually and update the selector for those pages specifically

**Instance 2**

- What I gave the AI: The Retrieval Approach section and an example chunk file showing the format with metadata fields
- What it produced: ingest.py that embedded all chunks and stored them in ChromaDB with the right metadata
- What I changed or overrode: It tried to embed everything in one batch call and my laptop ran out of memory. I changed it to process 50 chunks at a time instead which fixed the issue
