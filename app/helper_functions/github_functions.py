
import httpx
from fastapi import HTTPException
from unidiff import PatchSet


async def fetch_github_diff(owner: str, repo: str, before_sha: str, after_sha: str, token: str='') -> str:
    '''This function fetches the git diff of the recent code changes from GitHub using the GitHub API.
    It takes the repository owner, repository name, before and after commit SHAs, and an optional GitHub token for authentication. It returns the raw diff text for the specified commits.'''
   
    diff_text = ""
    
    # Call the GitHub Compare API to get the diff
    compare_url = f"https://api.github.com/repos/{owner}/{repo}/compare/{before_sha}...{after_sha}"
    
    headers = {
        "Authorization":"",
        "Accept": "application/vnd.github.v3.diff"  # IMPORTANT: This returns the raw diff text
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(compare_url, headers=headers)
        
        if response.status_code == 200:
            diff_text = response.text  # This is your actual code diff
        else:
            raise HTTPException(status_code=500, detail="Failed to fetch diff from GitHub")
    
    return diff_text

def parse_diff(diff_text: str):
    
    '''This function parses the raw diff text using the unidiff library and extracts the relevant information about the changed files, including the file paths, change status (added, removed, modified), and the specific lines that were added or removed. The output is a structured list of dictionaries representing each changed file and its associated changes, which can be used for further processing by the diff checker reviewer agent.
    It takes the raw diff text as input and returns a list of dictionaries with "path", "status", "added", and "removed" keys.'''
    patch = PatchSet(diff_text)
    files = []

    for file in patch:
        if file.is_added_file:
            status = "added"
        elif file.is_removed_file:
            status = "removed"
        else:
            status = "modified"

        files.append({
            "path": file.path,
            "status": status,
            "added": [
                line.value
                for hunk in file
                for line in hunk
                if line.is_added
            ],
            "removed": [
                line.value
                for hunk in file
                for line in hunk
                if line.is_removed
            ],
        })

    return files


