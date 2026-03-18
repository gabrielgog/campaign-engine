VIDEO_SCRIPT_PROMPT = """
{system_prompt}

{few_shots}

---

## GENERATION TASK: VIDEO SCRIPT

Trend Context: {trend_context}
Campaign Brief: {campaign_brief}

Generate a compelling video script for social media short-form video (20-90 seconds).

The script must:
- Open with the skin concern (redness, sensitivity, barrier damage)
- Explain the product's instant color correction
- Reference Centella Asiatica and its benefits
- Include at least one clinical claim
- End with brand sign-off or clear CTA
- Feel natural when read aloud
- Weave in the campaign angle naturally

CRITICAL: You MUST include ALL 6 fields in your JSON response:
1. hook
2. body
3. cta
4. full_script
5. estimated_duration_seconds
6. trend_reference

Return ONLY a valid JSON object. No markdown formatting.
No preamble. No explanation. Just valid JSON with all 6 fields.

{{
  "hook": "...",
  "body": "...",
  "cta": "...",
  "full_script": "...",
  "estimated_duration_seconds": 45,
  "trend_reference": "..."
}}
"""