import pytest
import json
import sys
from unittest.mock import MagicMock, patch
from models.schemas import (
    SourcingOutput,
    AssetBundle,
    VideoScript,
    ImagePrompt,
    GoogleAdsSet,
    GoogleAdsHeadline,
    GoogleAdsDescription,
    BlogPost,
    TrendSource,
    BundleScoreReport,
    AssetScore,
    DimensionScore,
    PassStatus,
    AssetType,
)


@pytest.fixture
def mock_trend_source():
    """Sample TrendSource for testing."""
    return TrendSource(
        source_url="https://example.com/article",
        publish_date="2026-03-10",
        headline="Centella Asiatica: The Trending Ingredient",
        summary="Centella is gaining traction in skincare routines.",
        relevance_score=0.85,
        trend_signal="Centella Asiatica trending",
        product_connection="Cicapair's hero ingredient",
        sentiment="positive"
    )


@pytest.fixture
def mock_sourcing_output(mock_trend_source):
    """Sample SourcingOutput for testing."""
    return SourcingOutput(
        cycle_trigger="Weekly scheduled cycle",
        primary_trend="Centella Asiatica barrier repair trend",
        trend_summary="Consumers increasingly seek ingredient-focused skincare",
        campaign_angle="Position Cicapair as the science-backed Centella solution",
        sources=[mock_trend_source],
        top_sources=[mock_trend_source],
        synthetic_content_used=False,
        synthetic_content_note=None
    )


@pytest.fixture
def mock_video_script():
    """Sample VideoScript for testing."""
    return VideoScript(
        hook="You know that moment when your skin betrays you",
        body="Redness, irritation, compromised barrier",
        cta="Dr.Jart+ Cicapair. Try it.",
        full_script="You know that moment... Dr.Jart+ Cicapair. Try it.",
        estimated_duration_seconds=45,
        trend_reference="Barrier repair trend"
    )


@pytest.fixture
def mock_image_prompt():
    """Sample ImagePrompt for testing."""
    return ImagePrompt(
        subject="Close-up of calm, even-toned skin",
        setting="Soft morning light",
        lighting="Golden hour diffused",
        color_palette="Sage green, warm beige",
        style_reference="Korean beauty editorial",
        product_placement="Cicapair jar in foreground",
        technical_parameters="--ar 4:5 --style raw --v 6",
        full_prompt="Close-up of calm skin in morning light...",
        optimised_for="Midjourney v6"
    )


@pytest.fixture
def mock_google_ads():
    """Sample GoogleAdsSet for testing."""
    return GoogleAdsSet(
        headline_1=GoogleAdsHeadline(text="Redness Corrected Instantly", character_count=27),
        headline_2=GoogleAdsHeadline(text="Cicapair Barrier Repair", character_count=23),
        headline_3=GoogleAdsHeadline(text="96% See Instant Results", character_count=23),
        description_1=GoogleAdsDescription(
            text="Green-to-beige color corrector. Centella Asiatica powered. Repairs barrier.",
            character_count=73
        ),
        description_2=GoogleAdsDescription(
            text="12-hour coverage, SPF 30, dermatologist tested. For sensitive, rosacea-prone skin.",
            character_count=81
        ),
        description_3=GoogleAdsDescription(
            text="Shop Cicapair at drjart.com. One dime-size amount. Soothe, correct, repair.",
            character_count=76
        ),
        display_url="drjart.com/cicapair",
        campaign_theme="Redness solution through barrier repair"
    )


@pytest.fixture
def mock_blog_post():
    """Sample BlogPost for testing."""
    return BlogPost(
        seo_title="Why Your Redness Isn't Going Away: Centella Asiatica Solution",
        meta_description="Learn why redness persists and how Centella Asiatica repairs skin barrier.",
        h1="Why Your Redness Isn't Going Away (And What Centella Asiatica Does About It)",
        primary_keyword="centella asiatica redness",
        secondary_keywords=["skin barrier repair", "rosacea skincare", "korean skincare"],
        body="If you've tried everything... [blog content]",
        word_count=850,
        cta="Ready to try Cicapair? Shop now at drjart.com/cicapair"
    )


@pytest.fixture
def mock_asset_bundle(mock_sourcing_output, mock_video_script, mock_image_prompt,
                      mock_google_ads, mock_blog_post):
    """Sample AssetBundle for testing."""
    return AssetBundle(
        trend_context=mock_sourcing_output.trend_summary,
        campaign_angle=mock_sourcing_output.campaign_angle,
        video_script=mock_video_script,
        image_prompt=mock_image_prompt,
        google_ads=mock_google_ads,
        blog_post=mock_blog_post,
        generation_attempt=1
    )


@pytest.fixture
def mock_asset_score():
    """Sample AssetScore for testing."""
    return AssetScore(
        asset_type=AssetType.VIDEO_SCRIPT,
        brand_alignment=DimensionScore(
            score=32,
            reasoning="Strong brand voice",
            issues=[]
        ),
        format_compliance=DimensionScore(
            score=33,
            reasoning="All 6 fields present",
            issues=[]
        ),
        trend_alignment=DimensionScore(
            score=33,
            reasoning="Trend naturally woven",
            issues=[]
        ),
        composite_score=98,
        pass_status=PassStatus.PASS,
        regeneration_instructions=None,
        attempt_number=1
    )


@pytest.fixture
def mock_bundle_score_report(mock_asset_score):
    """Sample BundleScoreReport for testing."""
    return BundleScoreReport(
        video_script_score=mock_asset_score,
        image_prompt_score=mock_asset_score,
        google_ads_score=mock_asset_score,
        blog_post_score=mock_asset_score,
        all_passed=True,
        cycle_complete=True
    )


@pytest.fixture
def mock_serper_api():
    """Mock Serper API response."""
    return {
        "organic": [
            {
                "position": 1,
                "title": "Article Title",
                "link": "https://example.com/article",
                "snippet": "Article snippet...",
                "date": "2026-03-10"
            }
        ]
    }


@pytest.fixture
def mock_claude_response_sources():
    """Mock Claude response for source scoring."""
    return [
        {
            "source_url": "https://example.com/article",
            "publish_date": "2026-03-10",
            "headline": "Centella Trend",
            "summary": "Summary text",
            "relevance_score": 0.85,
            "trend_signal": "Centella trending",
            "product_connection": "Related to Cicapair",
            "sentiment": "positive"
        }
    ]


@pytest.fixture
def mock_claude_response_synthetic():
    """Mock Claude response for synthetic sources."""
    return [
        {
            "source_url": "synthetic://trend-1",
            "publish_date": "2026-03-01",
            "headline": "Synthetic trend headline",
            "summary": "Synthetic trend summary",
            "relevance_score": 0.8,
            "trend_signal": "Synthetic trend signal",
            "product_connection": "Connected to Cicapair",
            "sentiment": "positive"
        }
    ] * 5


@pytest.fixture
def mock_claude_response_narrative():
    """Mock Claude response for trend narrative."""
    return {
        "primary_trend": "Centella Asiatica barrier repair trend",
        "trend_summary": "Consumers are increasingly aware of skin barrier importance",
        "campaign_angle": "Position Cicapair as the barrier repair solution"
    }


@pytest.fixture
def mock_claude_response_assets():
    """Mock Claude response for asset generation."""
    return {
        "video_script": {
            "hook": "You know that moment",
            "body": "When your skin betrays you",
            "cta": "Cicapair",
            "full_script": "You know that moment... Cicapair",
            "estimated_duration_seconds": 45,
            "trend_reference": "Barrier repair"
        },
        "image_prompt": {
            "subject": "Calm skin",
            "setting": "Morning light",
            "lighting": "Soft",
            "color_palette": "Sage green",
            "style_reference": "Editorial",
            "product_placement": "Cicapair jar",
            "technical_parameters": "--ar 4:5",
            "full_prompt": "Detailed prompt",
            "optimised_for": "Midjourney v6"
        },
        "google_ads": {
            "headline_1": {"text": "Headline 1", "character_count": 10},
            "headline_2": {"text": "Headline 2", "character_count": 10},
            "headline_3": {"text": "Headline 3", "character_count": 10},
            "description_1": {"text": "Desc 1", "character_count": 6},
            "description_2": {"text": "Desc 2", "character_count": 6},
            "description_3": {"text": "Desc 3", "character_count": 6},
            "display_url": "drjart.com",
            "campaign_theme": "Theme"
        },
        "blog_post": {
            "seo_title": "Title",
            "meta_description": "Meta desc",
            "h1": "H1",
            "primary_keyword": "keyword",
            "secondary_keywords": ["kw1", "kw2", "kw3"],
            "body": "Blog body content",
            "word_count": 850,
            "cta": "CTA text"
        }
    }


@pytest.fixture
def mock_claude_response_scoring():
    """Mock Claude response for scoring."""
    return {
        "asset_type": "video_script",
        "scores": {
            "brand_alignment": {
                "score": 32,
                "reasoning": "Strong brand voice",
                "issues": []
            },
            "format_compliance": {
                "score": 33,
                "reasoning": "All fields present",
                "issues": []
            },
            "trend_alignment": {
                "score": 33,
                "reasoning": "Trend naturally woven",
                "issues": []
            }
        },
        "composite_score": 98,
        "pass": True,
        "regeneration_instructions": None
    }
