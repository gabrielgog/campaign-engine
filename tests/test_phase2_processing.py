import pytest
from unittest.mock import patch, MagicMock
from phase2_processing import (
    build_video_script_chain,
    build_image_prompt_chain,
    build_google_ads_chain,
    build_blog_post_chain,
)


class TestChainBuilders:
    def test_build_video_script_chain(self):
        """Test video script chain construction."""
        chain = build_video_script_chain()
        assert chain is not None
        assert hasattr(chain, 'invoke')

    def test_build_image_prompt_chain(self):
        """Test image prompt chain construction."""
        chain = build_image_prompt_chain()
        assert chain is not None
        assert hasattr(chain, 'invoke')

    def test_build_google_ads_chain(self):
        """Test Google Ads chain construction."""
        chain = build_google_ads_chain()
        assert chain is not None
        assert hasattr(chain, 'invoke')

    def test_build_blog_post_chain(self):
        """Test blog post chain construction."""
        chain = build_blog_post_chain()
        assert chain is not None
        assert hasattr(chain, 'invoke')
