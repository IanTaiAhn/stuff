# Basically a place where I can access my stuff from anywhere since that's what I need.

Very solid url with career advice and such.

https://github.com/fractal-bootcamp/bootcamp-monorepo/tree/main/advice/career

Well I'm in a pickle with what I want to do and say about my rag pipeline...

Should I just make a post about the "live website"?
Even though it's just a static website and it makes calls to a backend fast api that does the rag stuff there.

I had fun with playing around with a local rag pipeline I thought maybe it'd also be fun to try to host it completely for free.

While I did find a "working" solution there were a couple of cavets to my completely "Free" and hosted rag pipeline.

Hugging Face deprecated their embedding/reranker api endpoints in Sept. 2025 so I had to pivot to another free option, Jina API.
This became the biggest limitation since my Jina Api key would only last for one session of frequent use, and then once my free tier of Render powered down Jina API would throttle the key.

I was working with 512MB and 0.1 CPU of processing power on Render (free tier limitations) and I thought maybe I could get away with using sentence_transformers for embeddings/rernaking, but unfortuneatyl, torch is quite large(version I used was 350mb).

The LLM (text generator) was easy since Groq api endpoints are free as long as you don't spam their endpoints.

In the end the hosted Rag pipeline worked faster than my locally hosted rag pipeline, and competely for free, albeit that one slight caveat of it only working once before Jina API key would be throttled and I would need to regenerate a new Jina API key to add into my Render's environment variables.

This prototype showed me how expensive live production is and made me appreciate my covered access to Gemeni Enterprise a little more.
Overall, this was a fun learnign experience and the constraints put on this live rag pipeline prototype made me think outside the box than if I had all the required resources needed right off the bat. 
I really trimmed the fat off of my requirements.txt to have it fit on Render's free tier, and leveraged "free" api endpoints so that my rag pipeline would run.

Refined version:

I was playing around with a local RAG pipeline and thought
"What if I tried to host it completely for free?"

TL;DR: it worked albeit with some caveats.

Since Hugging Face deprecated their embedding/reranking APIs in Sept 2025, I had to pivot to Jina. At first it was my key to hosting this for free, but then it became the biggest bottleneck. My Jina API key only survived a single session of heavy use, and once Render’s free tier powered down, the key would get throttled.

I was also limited to 512MB RAM and 0.1 CPU on Render. I considered running sentence-transformers locally, but Torch alone (~350MB) made that unrealistic.

The LLM side was easy and Groq’s free API worked great as long as I didn’t spam it.

In the end:

The hosted RAG pipeline was faster than my local one
It cost $0
But it only worked once before I had to regenerate a Jina API key and redeploy the backend on Render

This little experiment made me:

Appreciate how expensive “real” production actually is
Value enterprise tools (like Gemini Enterprise) a lot more
Think more creatively under constraints

I trimmed the fat off my requirements.txt and stitched together only "free" APIs to make it work.
Fun project overall and you can check out the static frontend website here and the source code here. (backend will definitely be broken unless you personally message me so that I can regenerate a Jina API key for you XD)