import json
import os
import re
from typing import List
from dotenv import load_dotenv
from openai import OpenAI

# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------
load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1")
DEEPSEEK_MODEL = "deepseek-reasoner"

# ---------------------------------------------------------
# Initialize client
# ---------------------------------------------------------
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_BASE)


# ---------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------
def build_analysis_prompt(
    article_title: str,
    article_summary: str,
    reference_articles: List[dict],
) -> str:

    if reference_articles:
        reference_block = "\n".join(
            f"- Title: {ref.get('title', '')}\n  Summary: {ref.get('summary', '')}"
            for ref in reference_articles
        )
    else:
        reference_block = "None"
    return f"""
You are a professional crypto market analyst writing concise research analyses
for traders and investors.

All articles are already crypto-related.
Your task is to assess **how much this news is likely to impact the crypto market**.

IMPORTANT CONCEPT:
- Some news is relevant but has **low or negligible market impact**.
- In such cases, clearly state that impact is limited and assign a low score.
- Do NOT exaggerate impact where none exists.

========================
NEWS ARTICLE
Title: {article_title}

Summary:
{article_summary}
========================

REFERENCE CONTEXT (background only):
{reference_block}
========================

OUTPUT FORMAT (FOLLOW EXACTLY):

ANALYSIS (KEY POINTS):
- <Why this news matters OR why its market impact is limited>
- <Expected effect on behavior, sentiment, or liquidity (if any)>

IMPACT STRENGTH (0–100):
<single integer only>

IMPACT SCORING GUIDANCE:
- 0–20  : Informational; unlikely to affect prices or sentiment
- 20–40 : Minor or indirect impact; limited to niche participants
- 40–60 : Moderate impact; sector-specific or narrative-driven
- 60–80 : Strong impact; likely to influence prices or sentiment
- 80–100: High impact; broadly market-moving

TIME HORIZON:
<Short-term (0–7 days) | Medium-term (7–30 days) | Long-term (30–90 days)>

MARKET SENTIMENT:
<Bullish | Bearish | Neutral>

PRICE EFFECT:
<Likely Up | Likely Down | Likely Volatile | Neutral>

SECTORS AFFECTED (choose 1–3 only):
- <Sector>: <short justification>
- <Sector>: <short justification>

COINS AFFECTED (if any):
- <SYMBOL>: <short reason>
- <SYMBOL>: <short reason>
(If none, write: None)

RISK FACTORS / LIMITATIONS:
- <Why this news may not materially move the market>
- <Key uncertainty or dependency>

RULES:
- No long paragraphs or storytelling.
- Do not force impact where none exists.
- Base conclusions strictly on the article and context.

END.
"""


# ---------------------------------------------------------
# Run DeepSeek
# ---------------------------------------------------------
async def run_deepseek(prompt: str) -> dict:
    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a crypto market analyst.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=900,
            temperature=0.3,
        )

        # 🔑 THIS IS THE KEY LINE
        full_response_text = json.dumps(
            response.model_dump(),
            ensure_ascii=False,
            indent=2,
        )

        return {
            "status": "RAW",
            "prediction": full_response_text,
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "prediction": str(e),
        }


# ---------------------------------------------------------
# Full pipeline
# ---------------------------------------------------------
async def analyze_article_with_deepseek(
    article: dict,
    similar_articles: List[dict],
):
    final_prompt = build_analysis_prompt(
        article_title=article["title"],
        article_summary=article["summary"],
        reference_articles=similar_articles,
    )

    ai_output = await run_deepseek(final_prompt)
    return ai_output
