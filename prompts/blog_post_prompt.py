BLOG_POST_PROMPT = """
{system_prompt}

{few_shots}

---

## GENERATION TASK: BLOG POST

Trend Context: {trend_context}
Campaign Brief: {campaign_brief}

Generate a complete blog post anchored to Cicapair and this trend.

Requirements:
- Minimum 800 words
- SEO title with primary keyword
- Meta description ≤155 characters
- H1 matching or close to title
- At least 2 H2 subheadings
- Educate and validate reader's concern
- Explain Centella Asiatica for new readers
- Include at least one clinical claim with context
- Final paragraph CTA
- Markdown formatted

CRITICAL: You MUST include ALL 8 fields in your JSON response:
1. seo_title
2. meta_description
3. h1
4. primary_keyword
5. secondary_keywords (array of 3)
6. body (full blog content)
7. word_count (integer, ~800 minimum)
8. cta (final call to action paragraph)

Return ONLY a valid JSON object. No markdown formatting around JSON.
No preamble. No explanation. Just valid JSON with all 8 fields.

Example structure:
{{
  "seo_title": "...",
  "meta_description": "...",
  "h1": "...",
  "primary_keyword": "...",
  "secondary_keywords": ["...", "...", "..."],
  "body": "...",
  "word_count": 850,
  "cta": "..."
}}
"""