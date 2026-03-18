import pytest
from unittest.mock import patch, MagicMock, Mock
from phase1_sourcing import (
    search_serper,
    collect_raw_sources,
)
from models.schemas import TrendSource


class TestSearchSerper:
    def test_search_serper_success(self):
        """Test successful Serper search."""
        mock_serper_api = {
            "organic": [
                {
                    "position": 1,
                    "title": "Article Title",
                    "link": "https://example.com/article",
                    "snippet": "Article snippet...",
                    "date": "2026-03-10"
                }
            ]
        }

        with patch('phase1_sourcing.serper') as mock_serper:
            mock_serper.results.return_value = mock_serper_api
            results = search_serper("test query")

            assert len(results) == 1
            assert results[0]['title'] == "Article Title"
            assert results[0]['link'] == "https://example.com/article"

    def test_search_serper_failure(self):
        """Test Serper search failure handling."""
        with patch('phase1_sourcing.serper') as mock_serper:
            mock_serper.results.side_effect = Exception("API error")
            results = search_serper("test query")
            assert results == []

    def test_search_serper_no_results(self):
        """Test Serper returning no results."""
        with patch('phase1_sourcing.serper') as mock_serper:
            mock_serper.results.return_value = {}
            results = search_serper("test query")
            assert results == []


class TestCollectRawSources:
    def test_collect_raw_sources_deduplication(self):
        """Test deduplication by URL."""
        mock_organic = [
            {
                "title": "Article Title",
                "link": "https://example.com/article",
                "snippet": "Snippet",
                "date": "2026-03-10"
            }
        ]

        with patch('phase1_sourcing.search_serper') as mock_search:
            mock_search.return_value = mock_organic
            with patch('phase1_sourcing.SEARCH_QUERIES', ['query1', 'query2']):
                results = collect_raw_sources()

                # Should have exactly 1 result even though called twice
                assert len(results) == 1
                assert results[0]['url'] == "https://example.com/article"

    def test_collect_raw_sources_respects_limit(self):
        """Test respects MAX_RAW_SOURCES limit."""
        mock_organic = [
            {
                "title": f"Article {i}",
                "link": f"https://example.com/article{i}",
                "snippet": "Snippet",
                "date": "2026-03-10"
            }
            for i in range(10)
        ]

        with patch('phase1_sourcing.search_serper') as mock_search:
            mock_search.return_value = mock_organic
            with patch('phase1_sourcing.MAX_RAW_SOURCES', 3):
                with patch('phase1_sourcing.SEARCH_QUERIES', ['q1', 'q2']):
                    results = collect_raw_sources()
                    assert len(results) <= 3
