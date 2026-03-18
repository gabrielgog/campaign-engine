from typing import Optional, TypedDict
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import StateGraph, END
from config import (
    SCORING_MODEL,
    SCORING_TEMPERATURE,
    PASS_THRESHOLD,
    MAX_REGENERATION_ATTEMPTS,
)
from models.schemas import (
    SourcingOutput,
    AssetBundle,
    AssetType,
    PassStatus,
    DimensionScore,
    AssetScore,
    BundleScoreReport,
)
from prompts.scoring_prompt import SCORING_PROMPT
from phase2_processing import run_phase2


scoring_llm = ChatAnthropic(
    model=SCORING_MODEL,
    temperature=SCORING_TEMPERATURE
)


class ScoringState(TypedDict):
    """State for the Phase 3 scoring graph"""
    asset_bundle: AssetBundle
    score_report: Optional[BundleScoreReport]
    attempt_number: int
    assets_to_regenerate: list[AssetType]
    cycle_complete: bool
    sourcing_output: SourcingOutput


def score_node(state: ScoringState) -> dict:
    """
    Score all four assets using Claude as judge.
    Returns DimensionScore objects for each asset type.
    """
    print(f"\n[PHASE 3] Scoring attempt {state['attempt_number']} of 3...")

    asset_bundle = state["asset_bundle"]
    sourcing_output = state["sourcing_output"]
    trend_context = sourcing_output.trend_summary
    scores = {}

    scores["video_script"] = score_asset(
        asset_type="video_script",
        asset=asset_bundle.video_script.model_dump_json(),
        trend_context=trend_context,
        attempt_number=state["attempt_number"]
    )

    scores["image_prompt"] = score_asset(
        asset_type="image_prompt",
        asset=asset_bundle.image_prompt.model_dump_json(),
        trend_context=trend_context,
        attempt_number=state["attempt_number"]
    )

    scores["google_ads"] = score_asset(
        asset_type="google_ads",
        asset=asset_bundle.google_ads.model_dump_json(),
        trend_context=trend_context,
        attempt_number=state["attempt_number"]
    )

    scores["blog_post"] = score_asset(
        asset_type="blog_post",
        asset=asset_bundle.blog_post.model_dump_json(),
        trend_context=trend_context,
        attempt_number=state["attempt_number"]
    )

    score_report = BundleScoreReport(
        video_script_score=scores["video_script"],
        image_prompt_score=scores["image_prompt"],
        google_ads_score=scores["google_ads"],
        blog_post_score=scores["blog_post"],
        all_passed=all(s.pass_status == PassStatus.PASS for s in scores.values()),
        cycle_complete=False
    )

    assets_to_regenerate = [
        s.asset_type for s in scores.values()
        if s.pass_status in [PassStatus.FAIL, PassStatus.NEAR_PASS]
    ]

    return {
        "score_report": score_report,
        "assets_to_regenerate": assets_to_regenerate,
    }


def score_asset(
    asset_type: str,
    asset: str,
    trend_context: str,
    attempt_number: int
) -> AssetScore:
    """
    Score a single asset using Claude as creative director.
    Returns AssetScore with dimensions and composite.
    """
    prompt_template = ChatPromptTemplate.from_template(SCORING_PROMPT)
    parser = JsonOutputParser()
    chain = prompt_template | scoring_llm | parser

    result = chain.invoke({
        "asset_type": asset_type,
        "asset_content": asset,
        "trend_context": trend_context,
        "attempt_number": attempt_number,
    })

    # Convert to AssetScore
    return AssetScore(
        asset_type=AssetType(asset_type),
        brand_alignment=DimensionScore(
            score=result["scores"]["brand_alignment"]["score"],
            reasoning=result["scores"]["brand_alignment"]["reasoning"],
            issues=result["scores"]["brand_alignment"]["issues"],
        ),
        format_compliance=DimensionScore(
            score=result["scores"]["format_compliance"]["score"],
            reasoning=result["scores"]["format_compliance"]["reasoning"],
            issues=result["scores"]["format_compliance"]["issues"],
        ),
        trend_alignment=DimensionScore(
            score=result["scores"]["trend_alignment"]["score"],
            reasoning=result["scores"]["trend_alignment"]["reasoning"],
            issues=result["scores"]["trend_alignment"]["issues"],
        ),
        composite_score=result["composite_score"],
        pass_status=PassStatus.PASS if result["pass"] else PassStatus.FAIL,
        regeneration_instructions=result.get("regeneration_instructions"),
        attempt_number=attempt_number,
    )



def evaluate_node(state: ScoringState) -> dict:
    """
    Evaluate composite scores and determine next action.

    Logic:
    - Pass >= 85 → all_passed, cycle_complete
    - Near pass 80-84 → targeted regeneration
    - Fail < 80 → full asset regeneration
    - attempt_number >= 3 → force complete, flag human_review
    """
    score_report = state["score_report"]
    attempt_number = state["attempt_number"]

    print(f"\n[PHASE 3] Evaluating scores...")
    print(f"[PHASE 3] Video: {score_report.video_script_score.composite_score}")
    print(f"[PHASE 3] Image: {score_report.image_prompt_score.composite_score}")
    print(f"[PHASE 3] Ads: {score_report.google_ads_score.composite_score}")
    print(f"[PHASE 3] Blog: {score_report.blog_post_score.composite_score}")

    if score_report.all_passed:
        print("[PHASE 3] ✓ All assets passed!")
        return {
            "cycle_complete": True,
            "assets_to_regenerate": [],
        }

    if attempt_number >= MAX_REGENERATION_ATTEMPTS:
        print(f"[PHASE 3] Max attempts ({MAX_REGENERATION_ATTEMPTS}) reached.")
        print("[PHASE 3] Flagging remaining assets for human review...")

        # Mark failed assets for human review
        for score in [
            score_report.video_script_score,
            score_report.image_prompt_score,
            score_report.google_ads_score,
            score_report.blog_post_score,
        ]:
            if score.pass_status != PassStatus.PASS:
                score.pass_status = PassStatus.HUMAN_REVIEW

        return {
            "cycle_complete": True,
            "score_report": score_report,
        }

    assets_to_regenerate = []
    for score in [
        score_report.video_script_score,
        score_report.image_prompt_score,
        score_report.google_ads_score,
        score_report.blog_post_score,
    ]:
        if score.composite_score < PASS_THRESHOLD:
            assets_to_regenerate.append(score.asset_type)

    return {
        "assets_to_regenerate": assets_to_regenerate,
        "score_report": score_report,
    }


def regenerate_node(state: ScoringState) -> dict:
    """
    Regenerate the entire asset bundle and increment attempt counter.
    """
    print(f"\n[PHASE 3] Regenerating failed assets...")

    attempt_number = state["attempt_number"] + 1
    new_bundle = run_phase2(state["sourcing_output"])
    new_bundle.generation_attempt = attempt_number

    return {
        "asset_bundle": new_bundle,
        "attempt_number": attempt_number,
        "score_report": None,
        "assets_to_regenerate": [],
    }



def complete_node(state: ScoringState) -> dict:
    """
    Mark scoring cycle as complete.
    """
    print("[PHASE 3] Scoring cycle complete ✓\n")
    return {"cycle_complete": True}


def should_regenerate(state: ScoringState) -> bool:
    """
    Return True if not all passed AND attempt < max.
    """
    if not state.get("score_report"):
        return False

    score_report = state["score_report"]
    attempt_number = state["attempt_number"]

    if score_report.all_passed or attempt_number >= MAX_REGENERATION_ATTEMPTS:
        return False

    return len(state.get("assets_to_regenerate", [])) > 0


def build_scoring_graph():
    """
    Build the Phase 3 LangGraph StateGraph.

    Nodes:
    - score_node: Score all four assets
    - evaluate_node: Decide on next action
    - regenerate_node: Regenerate failed assets
    - complete_node: Mark cycle as complete

    Edges:
    score_node → evaluate_node
    evaluate_node → complete_node (if all_passed OR attempt >= 3)
    evaluate_node → regenerate_node (if failed AND attempt < 3)
    regenerate_node → score_node
    complete_node → END
    """
    graph = StateGraph(ScoringState)
    graph.add_node("score", score_node)
    graph.add_node("evaluate", evaluate_node)
    graph.add_node("regenerate", regenerate_node)
    graph.add_node("complete", complete_node)

    graph.add_edge("score", "evaluate")
    graph.add_conditional_edges(
        "evaluate",
        should_regenerate,
        {
            True: "regenerate",
            False: "complete",
        }
    )

    graph.add_edge("regenerate", "score")
    graph.add_edge("complete", END)
    graph.set_entry_point("score")

    return graph.compile()


def run_phase3(
    asset_bundle: AssetBundle,
    sourcing_output: SourcingOutput
) -> tuple[BundleScoreReport, AssetBundle]:
    """
    Orchestrates the full Phase 3 scoring loop using LangGraph.

    Returns:
    - Final BundleScoreReport
    - Final (possibly regenerated) AssetBundle
    """
    print("\n" + "="*50)
    print("PHASE 3: SCORING")
    print("="*50)

    graph = build_scoring_graph()
    initial_state: ScoringState = {
        "asset_bundle": asset_bundle,
        "score_report": None,
        "attempt_number": 1,
        "assets_to_regenerate": [],
        "cycle_complete": False,
        "sourcing_output": sourcing_output,
    }

    final_state = graph.invoke(initial_state)

    print(f"[PHASE 3] Total attempts: {final_state['attempt_number']}")
    print("[PHASE 3] Complete ✓\n")

    return final_state["score_report"], final_state["asset_bundle"]