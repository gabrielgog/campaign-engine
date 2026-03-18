"""Sanity tests to verify basic test functionality."""

import pytest


def test_imports():
    """Verify all test modules can be imported."""
    try:
        from models.schemas import (
            TrendSource,
            VideoScript,
            ImagePrompt,
            GoogleAdsSet,
            GoogleAdsHeadline,
            GoogleAdsDescription,
            BlogPost,
            AssetBundle,
            PassStatus,
            AssetType,
            BundleScoreReport,
            AssetScore,
            DimensionScore,
        )
        assert TrendSource is not None
        assert VideoScript is not None
        assert AssetBundle is not None
    except ImportError as e:
        pytest.fail(f"Failed to import models: {e}")


def test_phase_imports():
    """Verify all phase modules can be imported."""
    try:
        import phase1_sourcing
        import phase2_processing
        import phase3_scoring
        import phase4_packaging
        import graph
        assert phase1_sourcing is not None
        assert phase2_processing is not None
        assert phase3_scoring is not None
        assert phase4_packaging is not None
        assert graph is not None
    except ImportError as e:
        pytest.fail(f"Failed to import phases: {e}")


def test_fixtures_available(mock_trend_source, mock_sourcing_output, mock_asset_bundle):
    """Verify test fixtures are available."""
    assert mock_trend_source is not None
    assert mock_sourcing_output is not None
    assert mock_asset_bundle is not None


def test_mock_data_valid(mock_google_ads, mock_blog_post):
    """Verify mock data is properly structured."""
    assert mock_google_ads.headline_1.text is not None
    assert len(mock_google_ads.headline_1.text) <= 30
    assert mock_blog_post.word_count >= 800
