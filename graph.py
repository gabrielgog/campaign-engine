from typing import Optional, TypedDict
from langgraph.graph import StateGraph, END
from phase1_sourcing import run_phase1
from phase2_processing import run_phase2
from phase3_scoring import run_phase3
from phase4_packaging import run_phase4
from models.schemas import (
    SourcingOutput,
    AssetBundle,
    BundleScoreReport,
    CampaignBundle,
)


class PipelineState(TypedDict):
    """State for the full campaign generation pipeline"""
    sourcing_output: Optional[SourcingOutput]
    asset_bundle: Optional[AssetBundle]
    score_report: Optional[BundleScoreReport]
    campaign_bundle: Optional[CampaignBundle]
    attempt_number: int
    cycle_complete: bool
    assets_to_regenerate: list


def sourcing_node(state: PipelineState) -> dict:
    """Phase 1: Trend sourcing"""
    print("\n" + "▶" * 25)
    print("STARTING CAMPAIGN GENERATION PIPELINE")
    print("▶" * 25)

    sourcing_output = run_phase1()
    return {"sourcing_output": sourcing_output}


def processing_node(state: PipelineState) -> dict:
    """Phase 2: Asset generation"""
    asset_bundle = run_phase2(state["sourcing_output"])
    return {"asset_bundle": asset_bundle}


def scoring_node(state: PipelineState) -> dict:
    """Phase 3: Scoring loop (subgraph)"""
    score_report, final_asset_bundle = run_phase3(
        state["asset_bundle"],
        state["sourcing_output"]
    )
    return {
        "score_report": score_report,
        "asset_bundle": final_asset_bundle,
        "attempt_number": final_asset_bundle.generation_attempt,
    }


def packaging_node(state: PipelineState) -> dict:
    """Phase 4: Final packaging"""
    campaign_bundle = run_phase4(
        state["asset_bundle"],
        state["score_report"],
        state["sourcing_output"],
        state["attempt_number"],
    )
    return {"campaign_bundle": campaign_bundle}


def build_graph():
    """
    Build the main campaign generation pipeline.

    Sequential flow:
    sourcing_node → processing_node → scoring_node → packaging_node → END
    """
    graph = StateGraph(PipelineState)
    graph.add_node("sourcing", sourcing_node)
    graph.add_node("processing", processing_node)
    graph.add_node("scoring", scoring_node)
    graph.add_node("packaging", packaging_node)

    graph.add_edge("sourcing", "processing")
    graph.add_edge("processing", "scoring")
    graph.add_edge("scoring", "packaging")
    graph.add_edge("packaging", END)

    graph.set_entry_point("sourcing")
    return graph.compile()