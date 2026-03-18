#!/usr/bin/env python3

"""
Dr.Jart+ Campaign Generation Pipeline
Trend-to-content in 4 phases using LangChain and LangGraph
"""

from dotenv import load_dotenv
load_dotenv()

from graph import build_graph


def main():
    """Run the full campaign generation pipeline."""
    # Build the LangGraph
    graph = build_graph()

    # Execute the pipeline
    result = graph.invoke({
        "sourcing_output": None,
        "asset_bundle": None,
        "score_report": None,
        "campaign_bundle": None,
        "attempt_number": 0,
        "cycle_complete": False,
        "assets_to_regenerate": [],
    })

    # Print summary
    print("\n" + "="*50)
    print("CAMPAIGN GENERATION COMPLETE")
    print("="*50)

    campaign_bundle = result["campaign_bundle"]
    print(f"\n✓ Campaign ID: {campaign_bundle.campaign_id}")
    print(f"✓ Saved to: output/campaign_bundle.json")
    print(f"✓ Total attempts: {campaign_bundle.total_generation_attempts}")
    print(f"✓ Synthetic content used: {campaign_bundle.synthetic_content_used}")

    print("\n📊 Final Scores:")
    score_report = campaign_bundle.score_report
    print(f"  • Video Script: {score_report.video_script_score.composite_score}/100")
    print(f"  • Image Prompt: {score_report.image_prompt_score.composite_score}/100")
    print(f"  • Google Ads: {score_report.google_ads_score.composite_score}/100")
    print(f"  • Blog Post: {score_report.blog_post_score.composite_score}/100")

    print("\n✨ Ready to deploy!\n")


if __name__ == "__main__":
    main()
