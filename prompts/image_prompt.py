IMAGE_PROMPT_TEMPLATE = """
{system_prompt}

{few_shots}

---

## GENERATION TASK: IMAGE PROMPT

Trend Context: {trend_context}
Campaign Brief: {campaign_brief}

Generate a detailed image generation prompt optimized for Midjourney v6.

The prompt must:
- Lead with the skin result (calm, even-toned skin) not the product
- Specify color palette (sage green, warm beige, clinical but warm)
- Include lighting direction (soft morning light, golden hour, etc.)
- Reference editorial/lifestyle/clinical style
- Show Cicapair product placement
- Include technical parameters (--ar 4:5, --style raw, --v 6)
- Avoid copyrighted references or real person names
- Feel premium and Korean beauty editorial

CRITICAL: You MUST include ALL 9 fields in your JSON response:
1. subject
2. setting
3. lighting
4. color_palette
5. style_reference
6. product_placement
7. technical_parameters
8. full_prompt
9. optimised_for

Return ONLY a valid JSON object. No markdown formatting.
No preamble. No explanation. Just valid JSON with all 9 fields.

{{
  "subject": "...",
  "setting": "...",
  "lighting": "...",
  "color_palette": "...",
  "style_reference": "...",
  "product_placement": "...",
  "technical_parameters": "...",
  "full_prompt": "...",
  "optimised_for": "Midjourney v6"
}}
"""