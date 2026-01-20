# AutoChangeLog

AI-powered tool that automatically generates and adds comprehensive changelogs to your GitHub releases. Analyzes commits and pull requests between releases to create well-structured, human-readable changelog content that gets added directly to your release notes.

## Quick Start with GitHub Actions

Automatically generate and add changelog content to your GitHub releases. When you publish a new release, this workflow will analyze the changes and update the release notes with a detailed changelog.

Add this workflow to your repository at `.github/workflows/changelog.yml`:

```yaml
name: Add Changelog to Release

on:
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      version:
        description: 'Release version (e.g., v1.2.3)'
        required: true

jobs:
  add-changelog:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Fetch all history for changelog generation

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install AutoChangeLog
        run: pip install git+https://github.com/Milansuman/autochangelog.git

      - name: Generate Changelog
        env:
          GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Determine release version
          if [ -n "${{ github.event.inputs.version }}" ]; then
            VERSION="${{ github.event.inputs.version }}"
          else
            VERSION="${{ github.event.release.tag_name }}"
          fi
          
          # Generate changelog to file
          autochangelog --auto -r "$VERSION" --repo ${{ github.repository }} -f CHANGELOG.md

      - name: Add Changelog to Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Determine release version
          if [ -n "${{ github.event.inputs.version }}" ]; then
            VERSION="${{ github.event.inputs.version }}"
          else
            VERSION="${{ github.event.release.tag_name }}"
          fi
          
          # Read the generated changelog
          CHANGELOG_CONTENT=$(cat CHANGELOG.md)
          
          # Get the current release body
          RELEASE_ID=$(gh api repos/${{ github.repository }}/releases/tags/"$VERSION" --jq '.id')
          CURRENT_BODY=$(gh api repos/${{ github.repository }}/releases/"$RELEASE_ID" --jq '.body')
          
          # Append changelog to release notes
          NEW_BODY="${CURRENT_BODY}

## Changelog

${CHANGELOG_CONTENT}"
          
          # Update the release
          gh api repos/${{ github.repository }}/releases/"$RELEASE_ID" \
            -X PATCH \
            -f body="$NEW_BODY"
```

### Required Secrets

Configure these secrets in your repository settings (Settings → Secrets and variables → Actions):

- `GROQ_API_KEY`: Your Groq API key for AI-powered changelog generation
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions with write permissions to releases

### How It Works

1. When you publish a new release on GitHub, the workflow is triggered automatically
2. AutoChangeLog analyzes all commits and PRs since the previous release
3. An AI-generated changelog is created with categorized changes
4. The changelog is appended to your GitHub release notes
5. Your release page now contains a comprehensive, readable changelog

## Local Installation and Usage

### Install with pip

```bash
pip install git+https://github.com/Milansuman/autochangelog.git
```

### Environment Variables

Create a `.env` file with the following variables:

```env
GROQ_API_KEY=your_groq_api_key
GITHUB_TOKEN=your_github_token
```

### CLI Commands

```bash
# Add changelog to the latest GitHub release
$ autochangelog --auto --repo owner/repo

# Add changelog to a specific release version
$ autochangelog --auto -r v1.2.3 --repo owner/repo

# Generate changelog and save to file (optional)
$ autochangelog --auto -r v1.2.3 --repo owner/repo -f CHANGELOG.md

# Interactive mode - chat with the agent about your releases
$ autochangelog
```

### Examples

**Generate changelog for your latest release:**
```bash
export GROQ_API_KEY="your-api-key"
export GITHUB_TOKEN="your-github-token"
autochangelog --auto --repo username/my-project
```

**Generate changelog for a specific release:**
```bash
autochangelog --auto -r v2.0.0 --repo username/my-project
```

## Development Setup

Clone the repository and create a Python virtual environment:

```bash
git clone https://github.com/Milansuman/autochangelog.git
cd autochangelog
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run in development mode:

```bash
python3 -m autochangelog.agent
```