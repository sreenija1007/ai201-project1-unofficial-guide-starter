# Project 1 Planning: The Unofficial Guide

## Domain

UCLA Campus Dining

UCLA dining gets ranked number 1 in the country basically every year which sounds great but doesn't really tell you anything useful. Like which dining hall is actually worth going to at 7pm on a weekday? Is the meal plan worth it if you're not living on the Hill? The official site just has menus and hours, it doesn't tell you the stuff that actually matters day to day.

The knowledge exists, it's just scattered across reddit threads and yelp reviews and nowhere is it all in one place you can actually search through.

## Documents

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | UCLA Housing Dining Locations | official hours and meal plan info | https://housing.ucla.edu/dining-locations |
| 2 | UCLA Housing Discover Dining 2025 | overview of all the dining spots | https://housing.ucla.edu/discover-dining-2025 |
| 3 | ASUCLA Dining Hall Guide | student-written breakdown of each hall | https://asucla.ucla.edu/ucla/ucla-dining-hall |
| 4 | UCLA Adminvc Dining Best in Nation 2023 | ranking article with hall descriptions | https://adminvc.ucla.edu/news-views/fall-2023/ucla-dining-named-best-nation-seventh-time |
| 5 | UCLA Adminvc Dining Number 1 2025 | 2025 update on rankings | https://adminvc.ucla.edu/news-views/summer-2025/ucla-dining-remains-no-1-nation |
| 6 | Reddit r/UCLA dining hall threads | actual student opinions on each hall | https://www.reddit.com/r/ucla/search/?q=dining+hall&sort=top |
| 7 | Reddit r/UCLA meal plan threads | is the meal plan worth it debate | https://www.reddit.com/r/ucla/search/?q=meal+plan+worth+it&sort=top |
| 8 | Niche.com UCLA food reviews | aggregated student ratings | https://www.niche.com/colleges/university-of-california-los-angeles/reviews/?topic=food |
| 9 | Yelp Bruin Plate | reviews of the healthy dining hall | https://www.yelp.com/biz/bruin-plate-los-angeles |
| 10 | Yelp De Neve | reviews including late night | https://www.yelp.com/biz/de-neve-dining-los-angeles |
| 11 | Yelp Epicuria at Covel | reviews of the mediterranean hall | https://www.yelp.com/biz/epicuria-at-covel-los-angeles |
| 12 | UCLA Dining Portal | menus, allergen info, pricing | https://dining.ucla.edu |

## Chunking Strategy

**Chunk size:** 300 tokens for the official pages and news articles, 150 for reviews and reddit comments

**Overlap:** 50 tokens for long documents, 20 for the short review stuff

**Reasoning:** The yelp and reddit content is already pretty short, each comment or review is basically one complete thought so I don't want to split those up. The official pages are longer and info can spill across paragraphs so I need some overlap there or I'll lose context at the boundaries. If chunks are too small I'll get fragments that don't make sense on their own. Too large and a chunk about Bruin Plate ends up mixed with Epicuria content which confuses retrieval.

**Final chunk count:** around 280

## Retrieval Approach

**Embedding model:** sentence-transformers/all-MiniLM-L6-v2

**Top-k:** 5

**Production tradeoff reflection:** I'm using MiniLM because it runs locally and doesn't need an API key which is convenient for this project. If this were a real deployed thing I'd probably look at OpenAI's embedding models for better accuracy, but that costs money per token. MiniLM also has a 256 token limit which is fine for reviews but could be a problem for longer chunks from the official pages. For a real product I'd also think about multilingual support since UCLA has a lot of international students who might search in other languages.

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What dining hall at UCLA is known for healthy food options? | Bruin Plate, it's described as the health focused hall with local produce, organic options, no soda |
| 2 | What is De Neve Late Night and when does it run? | It's extended hours at De Neve after regular dinner, for meal plan students, runs late into the evening |
| 3 | How is Epicuria different from De Neve? | Epicuria is Mediterranean food, pasta and pizza. De Neve is American style, burgers, chili, fried chicken |
| 4 | How many times has UCLA been ranked number 1 for college food? | Nine out of the last ten years as of 2025 per Niche.com |
| 5 | What do students say about the meal plan if you live off campus? | Mixed, most say it's hard to justify the cost since you can't use it for dinner at the residential halls unless you live there |

## Anticipated Challenges

1. Reddit and yelp reviews sometimes completely contradict each other. One person loves Bruin Plate, another says it runs out of food by 7. The LLM might just pick one side and present it as fact which would be wrong.

2. Some of the sources are from 2021 or 2022 and dining hours and prices change. There's no way for the system to know if a review is outdated without checking manually.

## Architecture

```
[Documents]          [Chunking]             [Embedding + Store]
requests +     -->   LangChain          -->  all-MiniLM-L6-v2
BeautifulSoup        RecursiveCharacter       ChromaDB (local)
                     TextSplitter
12 sources           reviews: 150 tok        metadata stored:
official pages       official: 300 tok       source_type
reddit threads       overlap: 20-50          dining_hall
yelp reviews                                 fetch_date

[Retrieval]          [Generation]
ChromaDB        -->  Groq API
top-k = 5            llama-3.3-70b-versatile

user types query     answer with citations
embed query          via query.py CLI
similarity search
return top 5 chunks
```

## AI Tool Plan

**Milestone 3 Ingestion and chunking:**
I'll give Claude the Documents section and Chunking Strategy from this file plus a sample HTML page from UCLA Housing. I want it to write scrape.py that fetches each URL, strips the nav and footer junk, and saves clean txt files. Also chunk.py using RecursiveCharacterTextSplitter with the sizes above. I'll check it worked by looking at a few chunks manually to make sure reviews aren't getting cut in weird places.

**Milestone 4 Embedding and retrieval:**
I'll give Claude the Retrieval Approach section and show it what the chunk output looks like. I want ingest.py that embeds everything and loads it into ChromaDB with the right metadata. I'll test it by running a quick query directly against the database before hooking up the LLM.

**Milestone 5 Generation and interface:**
I'll give Claude the whole planning doc and the 5 evaluation questions. I want query.py that takes a question, grabs top 5 chunks, builds a prompt, calls Groq, and returns an answer with sources. I'll run all 5 test questions and compare to my expected answers.
