import re
from app.services.deepseek_client.deepseek_client import client, DEEPSEEK_MODEL

"""
DeepSeek-powered, high-quality summarizer.

This version produces concise, information-dense summaries without forcing
sentence count. It aggressively ignores irrelevant or non-impactful content,
and extracts only the core facts needed for downstream crypto impact analysis.
"""


async def summarize_with_deepseek(text: str, published_at: str = None) -> str:
    """
    High-signal summary generator using DeepSeek.
    Includes published date explicitly to help downstream automated analysis.
    """

    if not text or len(text.strip()) < 30:
        return text.strip()

    # Format date block for LLM consumption
    date_block = ""
    if published_at:
        date_block = (
            f"This article was originally published on: {published_at}.\n\n"
            "IMPORTANT: Always use this exact date in the summary. "
            "Do NOT convert it into phrases like '2 days ago' or 'recent'. "
            "The summary is used for automated analysis and semantic search, "
            "so including the exact ISO date is essential.\n\n"
        )

    prompt = f"""
{date_block}
Provide a concise, high-signal summary of the following news article.

CRITICAL SUMMARY REQUIREMENTS:

- Include the exact published date clearly inside the summary.
- Do NOT use vague time references such as "2 days ago", "yesterday",
  "last week", "recently", etc.
- Summaries will be processed by automated systems and semantic search models,
  so they must contain clear, explicit information without ambiguity.
- Include ONLY essential factual developments that matter for regulatory,
  institutional, economic, market-structure, tokenization, exchange,
  liquidity, ETF, or other crypto-relevant implications.
- Remove ALL filler, disclaimers, ads, author comments, intros, outros,
  or background fluff.
- The length should be ADAPTIVE: longer for high-information articles and
  shorter when fewer important details exist.
- Do NOT add opinions, speculation, or interpretation.
- Tone must be precise, neutral, and information-dense.

Article:
{text}

Return ONLY the clean, refined summary — nothing else.
"""

    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You produce high-precision summaries for automated analysis. "
                        "Your goal is to retain only the highest-signal facts."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=500,
        )

        summary = response.choices[0].message.content.strip()
        summary = re.sub(r"\s+", " ", summary).strip()

        return summary

    except Exception as e:
        print("DeepSeek summarization error:", e)
        return text[:400].strip()


# ------------------------------------------------------------------------------------
# Public API for the rest of pipeline
# ------------------------------------------------------------------------------------


async def generate_summary(text: str, published_at: str = None) -> str:
    """
    Public interface for generating high-quality summaries.
    Includes published_at to help LLM produce time-aware summaries.
    """
    try:
        cleaned = text.strip().replace("\n", " ")
        return await summarize_with_deepseek(cleaned, published_at=published_at)
    except Exception:
        # Fallback to a truncated preview
        return text[:400].strip()
