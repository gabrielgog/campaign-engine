# Campaign Automation Engine

An end-to-end campaign generation pipeline that uses LLMs and LangGraph to automatically create marketing assets from trend research. The system validates each asset through multi-criteria scoring and regenerates content that doesn't meet quality thresholds.

## Features

- Phase 1: Trend research and source validation
- Phase 2: Automated asset generation (video scripts, image prompts, Google Ads, blog posts)
- Phase 3: Quality scoring with multi-attempt regeneration
- Phase 4: Output bundling and reporting
- LangSmith integration for observability
- Full test coverage with pytest

## Requirements

- Python 3.9 or higher
- API keys for Anthropic and Serper

## Setup

### 1. Clone and Install

```bash
git clone <repository>
cd campaign-automation
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root with the following:

```
ANTHROPIC_API_KEY=*******
SERPER_API_KEY=****
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=******
LANGCHAIN_PROJECT=campaign-automation
```

Required keys:
- ANTHROPIC_API_KEY: Get from https://console.anthropic.com
- SERPER_API_KEY: Get from https://serper.dev

Optional keys:
- LANGCHAIN_TRACING_V2: Set to "true" to enable LangSmith tracing
- LANGCHAIN_API_KEY: Required if LANGCHAIN_TRACING_V2 is enabled

## Running the Project

### Generate Campaign

Run the full pipeline:

```bash
python main.py
```

This will:
1. Research trends using Serper API
2. Generate marketing assets using Claude
3. Score each asset and regenerate if needed (up to 3 attempts)
4. Output a complete campaign bundle to output/campaign_bundle.json

### Run Tests

```bash
pytest
```

Run tests with coverage report:

```bash
pytest --cov=.
```

## Output

Upon completion, the pipeline generates:

- Campaign bundle JSON file at `output/campaign_bundle.json`
- Campaign ID for tracking
- Final scores for each asset (0-100)
- Total generation attempts
- Synthesis report indicating which content is synthetic vs. real

Example output structure:
```
campaign_id: unique identifier
all_passed: boolean indicating if all assets passed threshold
total_generation_attempts: number of regeneration attempts
score_report:
  video_script_score: composite score and detailed breakdown
  image_prompt_score: composite score and detailed breakdown
  google_ads_score: composite score and detailed breakdown
  blog_post_score: composite score and detailed breakdown
```

## Configuration

Key settings in config.py:

- GENERATION_TEMPERATURE: 0.7 (controls creativity)
- SCORING_TEMPERATURE: 0.1 (controls scoring consistency)
- PASS_THRESHOLD: 85 (score to pass without regeneration)
- NEAR_PASS_THRESHOLD: 80 (score requiring review)
- MAX_REGENERATION_ATTEMPTS: 3 (max retries per asset)

Asset constraints (character limits, word counts, durations) can be modified in ASSET_CONSTRAINTS.

## Project Structure

```
.
├── main.py                    Main entry point
├── config.py                  Configuration and constants
├── graph.py                   LangGraph pipeline definition
├── phase1_sourcing.py        Trend research and source validation
├── phase2_processing.py      Asset generation
├── phase3_scoring.py         Quality scoring and regeneration
├── phase4_packaging.py       Output formatting
├── models/                   Data models and schemas
├── prompts/                  LLM prompt templates
├── tests/                    Test suite
└── output/                   Generated campaign bundles
```

## Troubleshooting

API Key Issues:
- Verify ANTHROPIC_API_KEY is correct and has available credits
- Verify SERPER_API_KEY is valid (test at serper.dev)

Memory Issues:
- Reduce MAX_RAW_SOURCES in config.py if experiencing memory pressure

Scoring Issues:
- Adjust PASS_THRESHOLD and NEAR_PASS_THRESHOLD in config.py
- Review score_report output for detailed feedback on what failed

## Development

To run LangSmith tracing for debugging:

1. Set LANGCHAIN_TRACING_V2=true in .env
2. Add LANGCHAIN_API_KEY from https://smith.langchain.com
3. Run the pipeline - traces will appear in LangSmith dashboard

## License

See LICENSE file for details.