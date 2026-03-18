GOOGLE_ADS_PROMPT = """
{system_prompt}

{few_shots}

---

## GENERATION TASK: GOOGLE ADS

Trend Context: {trend_context}
Campaign Brief: {campaign_brief}

Generate a complete Google Ads set with 3 headlines and 3 descriptions.

Requirements:
- Each headline: 30 characters max, no end punctuation
- Each description: 90 characters max
- At least one clinical stat across headlines/descriptions
- At least one ingredient mention
- Lead with benefit not brand name
- Speak empathetically to redness/sensitivity
- All 6 fields must feel unified in tone and message

CRITICAL: You MUST include ALL 8 fields in your JSON response:
1. headline_1 (with text and character_count)
2. headline_2 (with text and character_count)
3. headline_3 (with text and character_count)
4. description_1 (with text and character_count)
5. description_2 (with text and character_count)
6. description_3 (with text and character_count)
7. display_url
8. campaign_theme

Return ONLY a valid JSON object. No markdown formatting.
No preamble. No explanation. Just valid JSON with all 8 fields.

{{
  "headline_1": {{"text": "...", "character_count": 28}},
  "headline_2": {{"text": "...", "character_count": 30}},
  "headline_3": {{"text": "...", "character_count": 29}},
  "description_1": {{"text": "...", "character_count": 88}},
  "description_2": {{"text": "...", "character_count": 90}},
  "description_3": {{"text": "...", "character_count": 85}},
  "display_url": "drjart.com/cicapair",
  "campaign_theme": "..."
}}
"""