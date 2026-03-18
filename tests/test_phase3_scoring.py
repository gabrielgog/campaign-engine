import pytest
from unittest.mock import patch, MagicMock
from phase3_scoring import (
    should_regenerate,
    build_scoring_graph,
)


class TestShouldRegenerate:
    def test_should_regenerate_false_no_score_report(self):
        """Test should_regenerate returns False with no score report."""
        state = {
            "score_report": None,
            "attempt_number": 1
        }
        result = should_regenerate(state)
        assert result is False

    def test_should_regenerate_false_all_passed(self):
        """Test should_regenerate returns False when all passed."""
        mock_report = MagicMock()
        mock_report.all_passed = True

        state = {
            "score_report": mock_report,
            "attempt_number": 1,
            "assets_to_regenerate": []
        }
        result = should_regenerate(state)
        assert result is False

    def test_should_regenerate_false_max_attempts(self):
        """Test should_regenerate returns False at max attempts."""
        mock_report = MagicMock()
        mock_report.all_passed = False

        state = {
            "score_report": mock_report,
            "attempt_number": 3,
            "assets_to_regenerate": ["video_script"]
        }
        result = should_regenerate(state)
        assert result is False


class TestBuildScoringGraph:
    def test_build_scoring_graph_structure(self):
        """Test scoring graph is properly constructed."""
        graph = build_scoring_graph()
        assert graph is not None
        assert callable(graph.invoke)

    def test_build_scoring_graph_has_invoke(self):
        """Test scoring graph can be invoked."""
        graph = build_scoring_graph()
        assert hasattr(graph, 'invoke')
