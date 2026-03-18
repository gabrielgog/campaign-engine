"""Minimal test suite - focused on critical logic only."""

import pytest
from unittest.mock import MagicMock, patch


class TestImports:
    """Verify all modules can be imported."""

    def test_imports_phase_modules(self):
        """Test all phase modules import successfully."""
        import phase1_sourcing
        import phase2_processing
        import phase3_scoring
        import phase4_packaging
        import graph
        assert all([
            phase1_sourcing,
            phase2_processing,
            phase3_scoring,
            phase4_packaging,
            graph
        ])

    def test_imports_models(self):
        """Test models import successfully."""
        from models.schemas import (
            TrendSource,
            AssetBundle,
            VideoScript,
            ImagePrompt,
            GoogleAdsSet,
            BlogPost,
        )
        assert all([
            TrendSource,
            AssetBundle,
            VideoScript,
            ImagePrompt,
            GoogleAdsSet,
            BlogPost,
        ])


class TestChainBuilders:
    """Test that chain builders work."""

    def test_build_video_script_chain(self):
        """Video script chain builds successfully."""
        from phase2_processing import build_video_script_chain
        chain = build_video_script_chain()
        assert chain is not None

    def test_build_image_prompt_chain(self):
        """Image prompt chain builds successfully."""
        from phase2_processing import build_image_prompt_chain
        chain = build_image_prompt_chain()
        assert chain is not None

    def test_build_google_ads_chain(self):
        """Google ads chain builds successfully."""
        from phase2_processing import build_google_ads_chain
        chain = build_google_ads_chain()
        assert chain is not None

    def test_build_blog_post_chain(self):
        """Blog post chain builds successfully."""
        from phase2_processing import build_blog_post_chain
        chain = build_blog_post_chain()
        assert chain is not None


class TestGraphBuilders:
    """Test graph construction."""

    def test_build_graph(self):
        """Graph builds successfully."""
        from graph import build_graph
        graph = build_graph()
        assert graph is not None
        assert hasattr(graph, 'invoke')

    def test_build_scoring_graph(self):
        """Scoring graph builds successfully."""
        from phase3_scoring import build_scoring_graph
        graph = build_scoring_graph()
        assert graph is not None
        assert hasattr(graph, 'invoke')


class TestShouldRegenerate:
    """Test regeneration decision logic."""

    def test_should_regenerate_no_score_report(self):
        """Should return False when no score report."""
        from phase3_scoring import should_regenerate
        state = {
            "score_report": None,
            "attempt_number": 1
        }
        result = should_regenerate(state)
        assert result is False

    def test_should_regenerate_all_passed(self):
        """Should return False when all passed."""
        from phase3_scoring import should_regenerate

        mock_report = MagicMock()
        mock_report.all_passed = True

        state = {
            "score_report": mock_report,
            "attempt_number": 1,
            "assets_to_regenerate": []
        }
        result = should_regenerate(state)
        assert result is False

    def test_should_regenerate_max_attempts(self):
        """Should return False at max attempts."""
        from phase3_scoring import should_regenerate

        mock_report = MagicMock()
        mock_report.all_passed = False

        state = {
            "score_report": mock_report,
            "attempt_number": 3,
            "assets_to_regenerate": ["video_script"]
        }
        result = should_regenerate(state)
        assert result is False


class TestModelCreation:
    """Test that models can be created."""

    def test_trend_source_creation(self):
        """TrendSource can be created with valid data."""
        from models.schemas import TrendSource

        source = TrendSource(
            source_url="https://example.com",
            publish_date="2026-03-10",
            headline="Test",
            summary="Test",
            relevance_score=0.85,
            trend_signal="Test",
            product_connection="Test",
            sentiment="positive"
        )
        assert source.relevance_score == 0.85

    def test_video_script_creation(self):
        """VideoScript can be created."""
        from models.schemas import VideoScript

        script = VideoScript(
            hook="Hook",
            body="Body",
            cta="CTA",
            full_script="Full",
            estimated_duration_seconds=45,
            trend_reference="Trend"
        )
        assert script.estimated_duration_seconds == 45

    def test_asset_bundle_creation(self, mock_asset_bundle):
        """AssetBundle fixture works."""
        assert mock_asset_bundle is not None
        assert mock_asset_bundle.video_script is not None
        assert mock_asset_bundle.image_prompt is not None
        assert mock_asset_bundle.google_ads is not None
        assert mock_asset_bundle.blog_post is not None


class TestFixtures:
    """Verify all test fixtures work."""

    def test_sourcing_output_fixture(self, mock_sourcing_output):
        """Sourcing output fixture is valid."""
        assert mock_sourcing_output is not None
        assert mock_sourcing_output.primary_trend is not None
        assert mock_sourcing_output.trend_summary is not None

    def test_bundle_score_report_fixture(self, mock_bundle_score_report):
        """Bundle score report fixture is valid."""
        assert mock_bundle_score_report is not None
        assert hasattr(mock_bundle_score_report, 'all_passed')

    def test_asset_bundle_fixture(self, mock_asset_bundle):
        """Asset bundle fixture is valid."""
        assert mock_asset_bundle is not None
        assert mock_asset_bundle.video_script is not None
