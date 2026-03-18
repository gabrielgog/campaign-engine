from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum


class AssetType(str, Enum):
    VIDEO_SCRIPT = "video_script"
    IMAGE_PROMPT = "image_prompt"
    GOOGLE_ADS = "google_ads"
    BLOG_POST = "blog_post"


class PassStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    NEAR_PASS = "near_pass"
    HUMAN_REVIEW = "human_review"



class TrendSource(BaseModel):
    """Single sourced trend data point"""
    source_url: str = Field(
        description="Full URL of the source"
    )
    publish_date: str = Field(
        description="Publication date ISO format"
    )
    headline: str = Field(
        description="Title or headline of the content"
    )
    summary: str = Field(
        description="2-3 sentence summary of the content"
    )
    relevance_score: float = Field(
        ge=0.0, le=1.0,
        description="How relevant to Cicapair and current trends. 0-1"
    )
    trend_signal: str = Field(
        description="The specific trend this source signals"
    )
    product_connection: str = Field(
        description="How this trend connects to Cicapair specifically"
    )
    sentiment: str = Field(
        description="positive | neutral | negative"
    )


class SourcingOutput(BaseModel):
    """Phase 1 complete output"""
    cycle_trigger: str = Field(
        description="What triggered this content cycle"
    )
    anchor_product: str = Field(
        default="Cicapair Soothing Color Correcting Treatment SPF 30",
        description="Product all content is anchored to"
    )
    primary_trend: str = Field(
        description="The dominant trend identified this cycle"
    )
    trend_summary: str = Field(
        description="2-3 sentence summary of the trend landscape"
    )
    campaign_angle: str = Field(
        description="Recommended campaign angle connecting trend to Cicapair"
    )
    sources: list[TrendSource] = Field(
        description="All sourced data points"
    )
    top_sources: list[TrendSource] = Field(
        description="Top 3 highest relevance sources"
    )
    synthetic_content_used: bool = Field(
        default=False,
        description="Whether synthetic content was generated to fill gaps"
    )
    synthetic_content_note: Optional[str] = Field(
        default=None,
        description="Explanation if synthetic content was used"
    )




class VideoScript(BaseModel):
    """Video generation script asset"""
    hook: str = Field(
        description="Opening 1-2 sentences. Must address skin concern first"
    )
    body: str = Field(
        description="Main script body. 30-60 seconds when spoken aloud"
    )
    cta: str = Field(
        description="Closing call to action or brand sign-off"
    )
    full_script: str = Field(
        description="Complete script as one continuous piece"
    )
    estimated_duration_seconds: int = Field(
        ge=20, le=90,
        description="Estimated spoken duration in seconds"
    )
    trend_reference: str = Field(
        description="How the trend is woven into this script"
    )


class ImagePrompt(BaseModel):
    """Image generation prompt asset"""
    subject: str = Field(
        description="Who or what is the main subject"
    )
    setting: str = Field(
        description="Environment and context"
    )
    lighting: str = Field(
        description="Lighting direction and quality"
    )
    color_palette: str = Field(
        description="Specific colors present in the image"
    )
    style_reference: str = Field(
        description="Visual style - editorial, lifestyle, clinical etc"
    )
    product_placement: str = Field(
        description="How and where Cicapair appears in the image"
    )
    technical_parameters: str = Field(
        description="Aspect ratio, style, version flags for generator"
    )
    full_prompt: str = Field(
        description="Complete formatted prompt ready for image generator"
    )
    optimised_for: str = Field(
        default="Midjourney v6",
        description="Which image generator this is optimised for"
    )


class GoogleAdsHeadline(BaseModel):
    """Single Google Ads headline"""
    text: str = Field(
        description="Headline text. 30 characters maximum. No end punctuation"
    )
    character_count: int = Field(
        description="Exact character count"
    )

    @validator("character_count", always=True)
    def validate_character_count(cls, v, values):
        if "text" in values and len(values["text"]) > 30:
            raise ValueError(
                f"Headline exceeds 30 characters: {values['text']}"
            )
        return len(values.get("text", ""))


class GoogleAdsDescription(BaseModel):
    """Single Google Ads description"""
    text: str = Field(
        description="Description text. 90 characters maximum"
    )
    character_count: int = Field(
        description="Exact character count"
    )

    @validator("character_count", always=True)
    def validate_character_count(cls, v, values):
        if "text" in values and len(values["text"]) > 90:
            raise ValueError(
                f"Description exceeds 90 characters: {values['text']}"
            )
        return len(values.get("text", ""))


class GoogleAdsSet(BaseModel):
    """Complete Google Ads set"""
    headline_1: GoogleAdsHeadline
    headline_2: GoogleAdsHeadline
    headline_3: GoogleAdsHeadline
    description_1: GoogleAdsDescription
    description_2: GoogleAdsDescription
    description_3: GoogleAdsDescription
    display_url: str = Field(
        default="drjart.com/cicapair",
        description="Display URL for the ad"
    )
    campaign_theme: str = Field(
        description="The unifying theme across all 6 fields"
    )


class BlogPost(BaseModel):
    """Complete blog post asset"""
    seo_title: str = Field(
        description="SEO optimised title with primary keyword"
    )
    meta_description: str = Field(
        description="Meta description. 155 characters maximum"
    )
    h1: str = Field(
        description="H1 heading — matches or is close to SEO title"
    )
    primary_keyword: str = Field(
        description="Target SEO keyword for this post"
    )
    secondary_keywords: list[str] = Field(
        description="Supporting keywords naturally used in body"
    )
    body: str = Field(
        description="Full blog post body in markdown. Minimum 800 words"
    )
    word_count: int = Field(
        description="Approximate word count of body"
    )
    cta: str = Field(
        description="Final paragraph call to action"
    )


class AssetBundle(BaseModel):
    """Phase 2 complete output — all four draft assets"""
    trend_context: str = Field(
        description="The trend narrative all assets are built around"
    )
    campaign_angle: str = Field(
        description="The unifying campaign angle across all assets"
    )
    video_script: VideoScript
    image_prompt: ImagePrompt
    google_ads: GoogleAdsSet
    blog_post: BlogPost
    generation_attempt: int = Field(
        default=1,
        description="Which generation attempt this is. Max 3"
    )


# PHASE 3 — SCORING SCHEMAS

class DimensionScore(BaseModel):
    """Score for a single dimension"""
    score: int = Field(
        description="Numeric score for this dimension"
    )
    reasoning: str = Field(
        description="Explanation of this score"
    )
    issues: list[str] = Field(
        default=[],
        description="Specific issues found. Empty if none"
    )


class AssetScore(BaseModel):
    """Complete score for a single asset"""
    asset_type: AssetType
    brand_alignment: DimensionScore = Field(
        description="Score out of 34"
    )
    format_compliance: DimensionScore = Field(
        description="Score out of 33"
    )
    trend_alignment: DimensionScore = Field(
        description="Score out of 33"
    )
    composite_score: int = Field(
        description="Sum of all three dimension scores. Max 100"
    )
    pass_status: PassStatus = Field(
        description="pass / fail / near_pass / human_review"
    )
    regeneration_instructions: Optional[str] = Field(
        default=None,
        description="Targeted fix instructions if failed. Null if passed"
    )
    attempt_number: int = Field(
        default=1,
        description="Which attempt this score is for"
    )

    @validator("composite_score", always=True)
    def validate_composite(cls, v, values):
        if v >= 85:
            return v
        if v >= 80:
            values["pass_status"] = PassStatus.NEAR_PASS
        return v


class BundleScoreReport(BaseModel):
    """Phase 3 complete output — scores for all four assets"""
    video_script_score: AssetScore
    image_prompt_score: AssetScore
    google_ads_score: AssetScore
    blog_post_score: AssetScore
    all_passed: bool = Field(
        description="True only if all four assets passed"
    )
    assets_to_regenerate: list[AssetType] = Field(
        default=[],
        description="Asset types that need regeneration"
    )
    cycle_complete: bool = Field(
        description="True if all passed or max attempts reached"
    )



class CampaignBundle(BaseModel):
    """Phase 4 final packaged deliverable"""
    campaign_id: str = Field(
        description="Unique ID for this campaign bundle"
    )
    anchor_product: str = Field(
        default="Cicapair Soothing Color Correcting Treatment SPF 30"
    )
    trend_context: str = Field(
        description="The trend narrative this campaign was built around"
    )
    campaign_angle: str = Field(
        description="The unifying creative angle"
    )
    video_script: VideoScript = Field(
        description="Final passing video generation script"
    )
    image_prompt: ImagePrompt = Field(
        description="Final passing image generation prompt"
    )
    google_ads: GoogleAdsSet = Field(
        description="Final passing Google Ads set"
    )
    blog_post: BlogPost = Field(
        description="Final passing blog post"
    )
    score_report: BundleScoreReport = Field(
        description="Final scores for all four assets"
    )
    total_generation_attempts: int = Field(
        description="Total regeneration cycles used across all assets"
    )
    synthetic_content_used: bool = Field(
        default=False,
        description="Whether synthetic content was used in sourcing"
    )
    generated_at: str = Field(
        description="ISO timestamp of bundle generation"
    )