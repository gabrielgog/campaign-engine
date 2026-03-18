from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableParallel
from config import (
    GENERATION_MODEL,
    GENERATION_TEMPERATURE,
)
from models.schemas import (
    SourcingOutput,
    AssetBundle,
    VideoScript,
    ImagePrompt,
    GoogleAdsSet,
    GoogleAdsHeadline,
    GoogleAdsDescription,
    BlogPost,
)
from prompts.system_prompt import DR_JART_SYSTEM_PROMPT
from prompts.few_shots import FEW_SHOT_EXAMPLES
from prompts.video_script_prompt import VIDEO_SCRIPT_PROMPT
from prompts.image_prompt import IMAGE_PROMPT_TEMPLATE
from prompts.google_ads_prompt import GOOGLE_ADS_PROMPT
from prompts.blog_post_prompt import BLOG_POST_PROMPT


llm = ChatAnthropic(
    model=GENERATION_MODEL,
    temperature=GENERATION_TEMPERATURE
)



def build_video_script_chain():
    """Generate video script asset"""
    prompt_template = ChatPromptTemplate.from_template(VIDEO_SCRIPT_PROMPT)
    parser = JsonOutputParser()
    chain = prompt_template | llm | parser
    return chain


def build_image_prompt_chain():
    """Generate image generation prompt asset"""
    prompt_template = ChatPromptTemplate.from_template(IMAGE_PROMPT_TEMPLATE)
    parser = JsonOutputParser()
    chain = prompt_template | llm | parser
    return chain


def build_google_ads_chain():
    """Generate Google Ads set asset"""
    prompt_template = ChatPromptTemplate.from_template(GOOGLE_ADS_PROMPT)
    parser = JsonOutputParser()
    chain = prompt_template | llm | parser
    return chain


def build_blog_post_chain():
    """Generate blog post asset"""
    prompt_template = ChatPromptTemplate.from_template(BLOG_POST_PROMPT)
    parser = JsonOutputParser()
    chain = prompt_template | llm | parser
    return chain


def run_phase2(sourcing_output: SourcingOutput) -> AssetBundle:
    """
    Orchestrates Phase 2 asset generation using RunnableParallel.

    Generates all four assets simultaneously:
    - video_script
    - image_prompt
    - google_ads
    - blog_post

    Returns structured AssetBundle with all four assets.
    """
    print("\n" + "="*50)
    print("PHASE 2: PROCESSING")
    print("="*50)

    video_chain = build_video_script_chain()
    image_chain = build_image_prompt_chain()
    ads_chain = build_google_ads_chain()
    blog_chain = build_blog_post_chain()

    parallel_runner = RunnableParallel(
        video_script=video_chain,
        image_prompt=image_chain,
        google_ads=ads_chain,
        blog_post=blog_chain,
    )

    trend_context = sourcing_output.trend_summary
    campaign_brief = sourcing_output.campaign_angle

    inputs = {
        "system_prompt": DR_JART_SYSTEM_PROMPT.format(
            trend_context=trend_context,
            campaign_brief=campaign_brief
        ),
        "few_shots": FEW_SHOT_EXAMPLES,
        "trend_context": trend_context,
        "campaign_brief": campaign_brief,
    }

    print("[PHASE 2] Generating all four assets in parallel...")
    results = parallel_runner.invoke(inputs)
    video_script = VideoScript(**results["video_script"])
    image_prompt = ImagePrompt(**results["image_prompt"])
    ads_data = results["google_ads"]
    for i in [1, 2, 3]:
        headline_key = f"headline_{i}"
        text = ads_data[headline_key]["text"]
        if len(text) > 30:
            ads_data[headline_key]["text"] = text[:30].rstrip()

    for i in [1, 2, 3]:
        desc_key = f"description_{i}"
        text = ads_data[desc_key]["text"]
        if len(text) > 90:
            ads_data[desc_key]["text"] = text[:90].rstrip()

    ads_data["headline_1"] = GoogleAdsHeadline(**ads_data["headline_1"])
    ads_data["headline_2"] = GoogleAdsHeadline(**ads_data["headline_2"])
    ads_data["headline_3"] = GoogleAdsHeadline(**ads_data["headline_3"])
    ads_data["description_1"] = GoogleAdsDescription(**ads_data["description_1"])
    ads_data["description_2"] = GoogleAdsDescription(**ads_data["description_2"])
    ads_data["description_3"] = GoogleAdsDescription(**ads_data["description_3"])
    google_ads = GoogleAdsSet(**ads_data)
    blog_data = results["blog_post"]
    if "word_count" not in blog_data or not blog_data["word_count"]:
        blog_data["word_count"] = len(blog_data.get("body", "").split())

    if "cta" not in blog_data or not blog_data["cta"]:
        blog_data["cta"] = "Ready to experience the Cicapair difference? Shop now at drjart.com/cicapair and join thousands discovering the power of Centella Asiatica for barrier repair and redness correction."

    try:
        blog_post = BlogPost(**blog_data)
    except Exception as e:
        print(f"[PHASE 2] Error parsing blog post: {e}")
        print(f"[PHASE 2] Received fields: {list(blog_data.keys())}")
        raise

    asset_bundle = AssetBundle(
        trend_context=trend_context,
        campaign_angle=campaign_brief,
        video_script=video_script,
        image_prompt=image_prompt,
        google_ads=google_ads,
        blog_post=blog_post,
        generation_attempt=1,
    )

    print("[PHASE 2] All four assets generated ✓")
    print(f"[PHASE 2] Video: {video_script.estimated_duration_seconds}s")
    print(f"[PHASE 2] Blog: {blog_post.word_count} words")
    print("[PHASE 2] Complete ✓\n")
    return asset_bundle
