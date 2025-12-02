import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = "deepseek-reasoner"  # best reasoning model


# ---------------------------------------------------------
# Initialize client
# ---------------------------------------------------------
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_BASE)


# ---------------------------------------------------------
# Build the curated + NO_IMPACT logic prompt
# ---------------------------------------------------------
def build_analysis_prompt(
    article_title: str, article_content: str, reference_articles: List[dict]
) -> str:

    reference_block = ""
    if reference_articles:
        parts = []
        for ref in reference_articles:
            block = f"Title: {ref['title']}\nContent: {ref['content']}"
            parts.append(block)
        reference_block = "\n\n-----\n".join(parts)
    else:
        reference_block = "No similar articles found."

    return f"""
You are an expert crypto market analyst. Your goal is to evaluate the following news
article and determine whether it has real impact on cryptocurrency prices.

-----------------------------------------
NEW ARTICLE:
Title: {article_title}

Content:
{article_content}
-----------------------------------------

REFERENCE HISTORICAL ARTICLES (context for comparison):
{reference_block}
-----------------------------------------

### CRITICAL INSTRUCTIONS (READ CAREFULLY):

1. Determine if this news will realistically influence crypto markets.
2. If the event does NOT meaningfully impact ANY crypto price:
   → Respond ONLY with the word: NO_IMPACT
   → Do NOT provide explanations.
   → Do NOT continue the analysis.

3. If the event DOES have meaningful impact, provide a structured analysis:
   ### Summary
   (2–3 sentence overview)

   ### Impact on Coins
   - Coin 1: expected movement + explanation  
   - Coin 2: expected movement + explanation  

   ### Market Sentiment
   (Bullish / Bearish / Neutral)

   ### Risk Factors
   (Possible uncertainties)

Make sure you strictly follow this classification rule.
Begin your evaluation below:
"""


# ---------------------------------------------------------
# Run DeepSeek Reasoner call
# ---------------------------------------------------------
async def run_deepseek(prompt: str) -> str:
    """
    Sends the final prompt to DeepSeek Reasoner.
    """
    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a highly factual and responsible crypto analyst.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=900,
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("DeepSeek Error:", e)
        return f"DeepSeek Error: {str(e)}"


# ---------------------------------------------------------
# FULL PIPELINE (Used by Router)
# ---------------------------------------------------------
async def analyze_article_with_deepseek(article: dict, similar_articles: List[dict]):
    """
    Full process:
    1. Build prompt
    2. Send to DeepSeek
    3. Return AI output
    """
    final_prompt = build_analysis_prompt(
        article_title=article["title"],
        article_content=article["content"],
        reference_articles=similar_articles,
    )

    ai_output = await run_deepseek(final_prompt)

    return ai_output
