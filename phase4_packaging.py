import json
import os
from datetime import datetime
from uuid import uuid4
from models.schemas import (
    AssetBundle,
    BundleScoreReport,
    SourcingOutput,
    CampaignBundle,
)
from config import OUTPUT_DIR, BUNDLE_FILENAME


def run_phase4(
    asset_bundle: AssetBundle,
    score_report: BundleScoreReport,
    sourcing_output: SourcingOutput,
    total_attempts: int,
) -> CampaignBundle:
    """
    Phase 4: Package final assets into CampaignBundle.

    Takes the final passing (or max-attempt) assets
    and bundles them with metadata for delivery.

    Saves to output/campaign_bundle.json

    Returns CampaignBundle.
    """
    print("\n" + "="*50)
    print("PHASE 4: PACKAGING")
    print("="*50)

    # Create unique campaign ID
    campaign_id = f"cicapair-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid4().hex[:8]}"

    # Bundle all final assets
    campaign_bundle = CampaignBundle(
        campaign_id=campaign_id,
        anchor_product="Cicapair Soothing Color Correcting Treatment SPF 30",
        trend_context=asset_bundle.trend_context,
        campaign_angle=asset_bundle.campaign_angle,
        video_script=asset_bundle.video_script,
        image_prompt=asset_bundle.image_prompt,
        google_ads=asset_bundle.google_ads,
        blog_post=asset_bundle.blog_post,
        score_report=score_report,
        total_generation_attempts=total_attempts,
        synthetic_content_used=sourcing_output.synthetic_content_used,
        generated_at=datetime.now().isoformat(),
    )

    print(f"[PHASE 4] Campaign ID: {campaign_id}")
    print(f"[PHASE 4] Total attempts: {total_attempts}")
    print(f"[PHASE 4] Synthetic content used: {sourcing_output.synthetic_content_used}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, BUNDLE_FILENAME)
    with open(output_path, "w") as f:
        json.dump(campaign_bundle.model_dump(), f, indent=2)

    print(f"[PHASE 4] Saved to {output_path}")
    print("[PHASE 4] Complete ✓\n")

    return campaign_bundle