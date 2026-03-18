import pytest
from unittest.mock import patch, MagicMock
from phase4_packaging import run_phase4


class TestPhase4Packaging:
    def test_run_phase4_creates_bundle(self):
        """Test Phase 4 creates campaign bundle."""
        mock_asset_bundle = MagicMock()
        mock_score_report = MagicMock()
        mock_sourcing = MagicMock()

        with patch('phase4_packaging.os.makedirs'):
            with patch('builtins.open', create=True):
                result = run_phase4(
                    mock_asset_bundle,
                    mock_score_report,
                    mock_sourcing,
                    1
                )

                assert result is not None
                assert result.campaign_id is not None
                assert "cicapair-" in result.campaign_id
                assert result.total_generation_attempts == 1

    def test_run_phase4_saves_file(self):
        """Test Phase 4 saves to file."""
        mock_asset_bundle = MagicMock()
        mock_score_report = MagicMock()
        mock_sourcing = MagicMock()
        mock_file = MagicMock()

        with patch('phase4_packaging.os.makedirs'):
            with patch('builtins.open', create=True) as mock_open:
                mock_open.return_value.__enter__.return_value = mock_file

                run_phase4(
                    mock_asset_bundle,
                    mock_score_report,
                    mock_sourcing,
                    1
                )

                # Verify file was written
                mock_file.write.assert_called()

    def test_run_phase4_includes_metadata(self):
        """Test Phase 4 includes required metadata."""
        mock_asset_bundle = MagicMock()
        mock_score_report = MagicMock()
        mock_sourcing = MagicMock()

        with patch('phase4_packaging.os.makedirs'):
            with patch('builtins.open', create=True):
                result = run_phase4(
                    mock_asset_bundle,
                    mock_score_report,
                    mock_sourcing,
                    2
                )

                assert result.anchor_product is not None
                assert result.trend_context is not None
                assert result.campaign_angle is not None
                assert result.video_script is not None
                assert result.image_prompt is not None
                assert result.google_ads is not None
                assert result.blog_post is not None
