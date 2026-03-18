TREND_NARRATIVE_PROMPT = """
You are a creative strategist at Dr.Jart+.

Based on these trend signals identified this week:
{sources_summary}

And this anchor product:
{product_context}

Return a JSON object with exactly these three fields:

primary_trend:
  One sentence naming the dominant trend this week
  that is most relevant to Cicapair.

trend_summary:
  2-3 sentences explaining the trend landscape
  and why it matters for Cicapair right now.

campaign_angle:
  One sentence recommending the specific creative angle
  that connects this trend to Cicapair most powerfully.
  This will become the unifying theme for all four
  campaign assets in Phase 2.

Return ONLY valid JSON. No preamble.
"""