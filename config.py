import os
from dotenv import load_dotenv

load_dotenv()


ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "drjart-campaign")



GENERATION_MODEL = "claude-sonnet-4-20250514"
SCORING_MODEL = "claude-sonnet-4-20250514"

GENERATION_TEMPERATURE = 0.7
SCORING_TEMPERATURE = 0.1
JSON_OUTPUT_TEMPERATURE = 0.0

PASS_THRESHOLD = 85
NEAR_PASS_THRESHOLD = 80
MAX_REGENERATION_ATTEMPTS = 3


ANCHOR_PRODUCT = {
    "name": "Cicapair Soothing Color Correcting Treatment SPF 30",
    "brand": "Dr.Jart+",
    "hero_ingredient": "Centella Asiatica Extracts (Cica Complex)",
    "key_benefits": [
        "Instantly corrects visible redness",
        "Repairs skin barrier over time",
        "12-hour coverage",
        "SPF 30 protection",
        "Green-to-beige color transformation",
        "Fragrance free and dermatologist tested",
        "National Rosacea Society accepted"
    ],
    "target_skin": [
        "Sensitive skin",
        "Rosacea-prone skin",
        "Acne-prone skin",
        "Redness-prone skin"
    ],
    "clinical_claims": [
        "96% said it instantly corrects visible redness",
        "91% said it conceals the look of blemishes",
        "97% showed skin barrier repair",
        "97% showed improved moisture levels",
        "Reduces visible redness by 22% after one use",
        "Repairs skin barrier by 36% in one hour"
    ],
    "product_url": "https://www.drjart.com/cicapair"
}

MAX_RAW_SOURCES = 20
TOP_SOURCES_COUNT = 5
MIN_RELEVANCE_SCORE = 0.6
MAX_SOURCE_AGE_DAYS = 30

SEARCH_QUERIES = [
    "centella asiatica skincare trend 2026",
    "sensitive skin redness TikTok trend 2026",
    "Korean skincare redness treatment trending",
    "rosacea skincare routine trend",
    "skin barrier repair trend 2026",
    "no makeup makeup look trend skincare",
    "Dr Jart Cicapair TikTok viral 2026",
    "cica skincare ingredient trending",
]

ASSET_CONSTRAINTS = {
    "google_ads": {
        "headline_max_chars": 30,
        "description_max_chars": 90,
        "headline_count": 3,
        "description_count": 3,
    },
    "blog_post": {
        "min_word_count": 800,
        "meta_description_max_chars": 155,
    },
    "video_script": {
        "min_duration_seconds": 20,
        "max_duration_seconds": 90,
    },
    "image_prompt": {
        "optimised_for": "Midjourney v6",
        "default_aspect_ratio": "4:5",
    }
}


OUTPUT_DIR = "output"
BUNDLE_FILENAME = "campaign_bundle.json"