SYNTHETIC_SOURCES_PROMPT = """
You are a senior trend analyst at a Korean beauty
marketing agency. Based on your knowledge of the
skincare industry and the Cicapair product:

Anchor product context:
{product_context}

Generate 5 realistic, logically grounded synthetic
trend data points that would be relevant to a
Cicapair campaign right now in 2026.

These should represent plausible current trends in:
- Sensitive skin and redness conversations
- Korean skincare adoption globally
- Ingredient-led skincare (Centella Asiatica)
- No-makeup makeup looks
- Skin barrier repair category

CRITICAL: Each synthetic source MUST have ALL 8 fields:
1. source_url: "synthetic://trend-[number]"
2. publish_date: a recent 2026 date (ISO format)
3. headline: a realistic article or post headline
4. summary: 2-3 sentences describing this trend
5. relevance_score: float between 0.7 and 0.95
6. trend_signal: the specific trend
7. product_connection: how it connects to Cicapair
8. sentiment: "positive" OR "neutral" OR "negative"

Return ONLY a valid JSON array with 5 objects.
No markdown formatting. No preamble. No explanation.

Example structure:
[
  {{
    "source_url": "synthetic://trend-1",
    "publish_date": "2026-03-01",
    "headline": "...",
    "summary": "...",
    "relevance_score": 0.85,
    "trend_signal": "...",
    "product_connection": "...",
    "sentiment": "positive"
  }}
]
"""