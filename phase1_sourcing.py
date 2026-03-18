import json
from datetime import datetime
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import (
    SERPER_API_KEY,
    GENERATION_MODEL,
    JSON_OUTPUT_TEMPERATURE,
    SEARCH_QUERIES,
    MAX_RAW_SOURCES,
    TOP_SOURCES_COUNT,
    MIN_RELEVANCE_SCORE,
    ANCHOR_PRODUCT,
)
from models.schemas import TrendSource, SourcingOutput
from prompts.score_sources_prompt import SCORE_SOURCES_PROMPT
from prompts.synthetic_sources_prompt import SYNTHETIC_SOURCES_PROMPT
from prompts.trend_narrative_prompt import TREND_NARRATIVE_PROMPT

# LangChain LLM
llm = ChatAnthropic(
    model=GENERATION_MODEL,
    temperature=JSON_OUTPUT_TEMPERATURE
)

serper = GoogleSerperAPIWrapper(serpapi_api_key=SERPER_API_KEY)


def detect_trigger() -> str:
    """
    Defines what starts a new content cycle.

    Trigger conditions:
    1. Scheduled - weekly cycle every Monday 8AM
    2. Trend spike - search volume spike detected
    3. Competitor activity - new competitor campaign found
    4. Seasonal - upcoming seasonal skincare moment
    5. Manual - human initiates a new cycle

    For this implementation we run on-demand
    which simulates a manual or scheduled trigger.
    In production this would be a cron job or
    webhook from a trend monitoring service.
    """
    trigger = {
        "type": "scheduled_weekly",
        "detected_at": datetime.now().isoformat(),
        "description": (
            "Weekly content cycle triggered. "
            "Sourcing current trends relevant to "
            "Cicapair and sensitive skin category."
        )
    }
    print(f"[PHASE 1] Trigger detected: {trigger['type']}")
    return trigger["description"]


def search_serper(query: str) -> list[dict]:
    """
    Search the web using Serper API via LangChain.
    Returns raw search results for a single query.
    """
    try:
        results = serper.results(query)
        return results.get("organic", [])
    except Exception as e:
        print(f"[PHASE 1] Serper search failed for '{query}': {e}")
        return []


def collect_raw_sources() -> list[dict]:
    """
    Run all search queries and collect raw results, deduplicated by URL.
    """
    print(f"[PHASE 1] Running {len(SEARCH_QUERIES)} search queries...")
    all_results = []
    seen_urls = set()

    for query in SEARCH_QUERIES:
        results = search_serper(query)
        for result in results:
            url = result.get("link", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_results.append({
                    "url": url,
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "date": result.get("date", ""),
                    "query": query
                })

        if len(all_results) >= MAX_RAW_SOURCES:
            break

    print(f"[PHASE 1] Collected {len(all_results)} raw sources")
    return all_results


def score_and_filter_sources(raw_sources: list[dict]) -> list[TrendSource]:
    """
    Score each source for relevance and extract trend signals.
    Returns sources above minimum relevance threshold.
    """
    print(f"[PHASE 1] Scoring {len(raw_sources)} sources with Claude...")

    sources_text = json.dumps(raw_sources, indent=2)
    product_context = json.dumps(ANCHOR_PRODUCT, indent=2)

    prompt_template = ChatPromptTemplate.from_template(SCORE_SOURCES_PROMPT)

    parser = JsonOutputParser()
    chain = prompt_template | llm | parser

    scored_sources = chain.invoke({
        "product_context": product_context,
        "sources_text": sources_text,
        "min_relevance": MIN_RELEVANCE_SCORE
    })

    validated_sources = []
    for source in scored_sources:
        try:
            validated_sources.append(TrendSource(**source))
        except Exception as e:
            print(f"[PHASE 1] Skipping invalid source: {e}")
            continue

    print(
        f"[PHASE 1] {len(validated_sources)} sources "
        f"passed relevance threshold"
    )
    return validated_sources


def generate_synthetic_sources() -> tuple[list[TrendSource], str]:
    """
    Generate synthetic but logically grounded trend data to fill gaps.
    """
    print("[PHASE 1] Generating synthetic trend data to fill gaps...")

    llm_synthetic = ChatAnthropic(
        model=GENERATION_MODEL,
        temperature=0.4
    )

    prompt_template = ChatPromptTemplate.from_template(SYNTHETIC_SOURCES_PROMPT)
    parser = JsonOutputParser()
    chain = prompt_template | llm_synthetic | parser

    synthetic_data = chain.invoke({
        "product_context": json.dumps(ANCHOR_PRODUCT, indent=2)
    })

    synthetic_sources = []
    for s in synthetic_data:
        try:
            synthetic_sources.append(TrendSource(**s))
        except Exception as e:
            print(f"[PHASE 1] Skipping invalid synthetic source: {e}")
            print(f"[PHASE 1] Fields received: {list(s.keys())}")
            continue

    note = (
        "Insufficient real-world sources found for some trend signals. "
        "Synthetic but logically grounded trend extrapolations were "
        "generated to ensure comprehensive campaign coverage. "
        "All synthetic data is clearly marked with synthetic:// URLs."
    )

    return synthetic_sources, note



def synthesise_trend_narrative(top_sources: list[TrendSource]) -> tuple[str, str, str]:
    """
    Synthesise sources into primary trend, summary, and campaign angle.
    """
    print("[PHASE 1] Synthesising trend narrative...")

    sources_summary = "\n".join([
        f"- {s.trend_signal}: {s.product_connection}"
        for s in top_sources
    ])

    prompt_template = ChatPromptTemplate.from_template(TREND_NARRATIVE_PROMPT)
    parser = JsonOutputParser()
    chain = prompt_template | llm | parser

    narrative = chain.invoke({
        "sources_summary": sources_summary,
        "product_context": json.dumps(ANCHOR_PRODUCT, indent=2)
    })

    return (
        narrative["primary_trend"],
        narrative["trend_summary"],
        narrative["campaign_angle"]
    )


def run_phase1() -> SourcingOutput:
    """
    Orchestrates the full Phase 1 sourcing pipeline.

    Steps:
    1. Detect trigger
    2. Collect raw sources via Serper
    3. Score and filter with Claude
    4. Fill gaps with synthetic content if needed
    5. Synthesise trend narrative
    6. Return structured SourcingOutput
    """
    print("\n" + "="*50)
    print("PHASE 1: SOURCING")
    print("="*50)

    trigger = detect_trigger()
    raw_sources = collect_raw_sources()
    validated_sources = score_and_filter_sources(raw_sources)

    synthetic_used = False
    synthetic_note = None

    if len(validated_sources) < TOP_SOURCES_COUNT:
        print(
            f"[PHASE 1] Only {len(validated_sources)} sources passed. "
            f"Minimum needed: {TOP_SOURCES_COUNT}. "
            f"Generating synthetic content..."
        )
        synthetic_sources, synthetic_note = generate_synthetic_sources()
        validated_sources.extend(synthetic_sources)
        synthetic_used = True

    validated_sources.sort(
        key=lambda x: x.relevance_score,
        reverse=True
    )

    top_sources = validated_sources[:TOP_SOURCES_COUNT]
    primary_trend, trend_summary, campaign_angle = \
        synthesise_trend_narrative(top_sources)

    output = SourcingOutput(
        cycle_trigger=trigger,
        primary_trend=primary_trend,
        trend_summary=trend_summary,
        campaign_angle=campaign_angle,
        sources=validated_sources,
        top_sources=top_sources,
        synthetic_content_used=synthetic_used,
        synthetic_content_note=synthetic_note
    )

    print(f"\n[PHASE 1] Primary trend: {primary_trend}")
    print(f"[PHASE 1] Campaign angle: {campaign_angle}")
    print(f"[PHASE 1] Sources used: {len(top_sources)}")
    print(f"[PHASE 1] Synthetic content: {synthetic_used}")
    print("[PHASE 1] Complete ✓\n")

    return output