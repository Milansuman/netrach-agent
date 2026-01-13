"""
Convenience module for local git operations.
"""
import subprocess

def get_author_info():
    """Get the author's name and email from git config."""
    try:
        name = subprocess.check_output(
            ["git", "config", "user.name"], universal_newlines=True
        ).strip()
        email = subprocess.check_output(
            ["git", "config", "user.email"], universal_newlines=True
        ).strip()
        return {
            "name": name,
            "email": email
        }
    except subprocess.CalledProcessError:
        return None, None
    
def get_current_repo():
    """Get the current git repository URL."""
    try:
        url = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"], universal_newlines=True
        ).strip()
        return url
    except subprocess.CalledProcessError:
        return None