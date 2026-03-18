import pytest
from unittest.mock import patch, MagicMock
from graph import (
    sourcing_node,
    processing_node,
    scoring_node,
    packaging_node,
    build_graph
)


class TestPipelineNodes:
    def test_sourcing_node_calls_phase1(self):
        """Test sourcing node calls run_phase1."""
        mock_output = MagicMock()

        with patch('graph.run_phase1') as mock_phase1:
            mock_phase1.return_value = mock_output

            state = {
                "sourcing_output": None,
                "asset_bundle": None,
                "score_report": None,
                "campaign_bundle": None,
                "attempt_number": 1,
                "cycle_complete": False,
                "assets_to_regenerate": []
            }

            result = sourcing_node(state)
            assert result["sourcing_output"] == mock_output
            mock_phase1.assert_called_once()

    def test_processing_node_calls_phase2(self):
        """Test processing node calls run_phase2."""
        mock_input = MagicMock()
        mock_output = MagicMock()

        with patch('graph.run_phase2') as mock_phase2:
            mock_phase2.return_value = mock_output

            state = {
                "sourcing_output": mock_input,
                "asset_bundle": None,
                "score_report": None,
                "campaign_bundle": None,
                "attempt_number": 1,
                "cycle_complete": False,
                "assets_to_regenerate": []
            }

            result = processing_node(state)
            assert result["asset_bundle"] == mock_output
            mock_phase2.assert_called_once_with(mock_input)

    def test_scoring_node_calls_phase3(self):
        """Test scoring node calls run_phase3."""
        mock_asset_bundle = MagicMock()
        mock_asset_bundle.generation_attempt = 2
        mock_score_report = MagicMock()
        mock_sourcing = MagicMock()

        with patch('graph.run_phase3') as mock_phase3:
            mock_phase3.return_value = (mock_score_report, mock_asset_bundle)

            state = {
                "sourcing_output": mock_sourcing,
                "asset_bundle": mock_asset_bundle,
                "score_report": None,
                "campaign_bundle": None,
                "attempt_number": 1,
                "cycle_complete": False,
                "assets_to_regenerate": []
            }

            result = scoring_node(state)
            assert result["score_report"] == mock_score_report
            assert result["asset_bundle"] == mock_asset_bundle
            assert result["attempt_number"] == 2

    def test_packaging_node_calls_phase4(self):
        """Test packaging node calls run_phase4."""
        mock_campaign_bundle = MagicMock()

        with patch('graph.run_phase4') as mock_phase4:
            mock_phase4.return_value = mock_campaign_bundle

            state = {
                "sourcing_output": MagicMock(),
                "asset_bundle": MagicMock(),
                "score_report": MagicMock(),
                "campaign_bundle": None,
                "attempt_number": 2,
                "cycle_complete": False,
                "assets_to_regenerate": []
            }

            result = packaging_node(state)
            assert result["campaign_bundle"] == mock_campaign_bundle


class TestGraphConstruction:
    def test_build_graph_returns_callable(self):
        """Test graph is properly constructed and callable."""
        graph = build_graph()
        assert graph is not None
        assert callable(graph.invoke)
