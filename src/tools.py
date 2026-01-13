import requests
import os
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

@tool
def get_releases(owner: str, repo: str) -> str:
    """Get releases for a GitHub repository. Returns formatted list of recent releases with name, tag, and publish date."""
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        releases = response.json()
        
        if not releases:
            return "No releases found."
        
        result = []
        for release in releases[:10]:
            result.append(f"- {release['name']} ({release['tag_name']}) - {release['published_at']}")
        return "\n".join(result)
    except Exception as e:
        return f"Error fetching releases: {str(e)}"

@tool
def get_commits(owner: str, repo: str, per_page: int = 30) -> str:
    """Get recent commits for a GitHub repository. Returns formatted list of commits with SHA, message, and author."""
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"

    params = {
        "per_page": min(per_page, 100),
        "page": 1
    }
    
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        commits = response.json()
        
        if not commits:
            return "No commits found."
        
        result = []
        for commit in commits:
            sha = commit['sha']
            message = commit['commit']['message'].split('\n')[0]
            author = commit['commit']['author']['name']
            result.append(f"- {sha}: {message} (by {author})")
        return "\n".join(result)
    except Exception as e:
        return f"Error fetching commits: {str(e)}"
    
@tool
def get_user_repos(username: str) -> str:
    """Get public repositories for a GitHub user. Returns formatted list of repository names and descriptions."""
    url = f"https://api.github.com/users/{username}/repos"
    
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        repos = response.json()
        
        if not repos:
            return "No repositories found."
        
        result = []
        for repo in repos:
            description = repo['description'] if repo['description'] else "No description"
            result.append(f"- {repo['name']}: {description}")
        return "\n".join(result)
    except Exception as e:
        return f"Error fetching user repositories: {str(e)}"

