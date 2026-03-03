"""
Script to update the Commit Hall of Fame with latest commits from 1TSnakers repos.
Run this weekly to keep the hall of fame fresh!
"""
import os
from ghapi.all import GhApi

# Initialize GitHub API
api = GhApi()

# Repos to check - only the fun ones!
REPOS = [
    "1TSnakers/1TSnakers.github.io",
    "1TSnakers/OllamaSearchAPI",
    "1TSnakers/ProgressiveImageLoader",
]

# Generic commits to skip (too boring for the hall of fame)
GENERIC_COMMITS = {
    "Update README.md",
    "Update index.html",
    "Add files via upload",
    "Create README.md",
    "Update .gitattributes",
    "Create .gitattributes",
    "Update LICENSE with name",
    "Update requirements.txt",
    "Update package.json",
    "Update package-lock.json",
    "Update pyproject.toml",
    "Update setup.py",
    "Update .gitignore",
    "Delete README.md",
    "Create LICENSE",
    "Update LICENSE",
    "Update .env.example",
    "Create .env.example",
    "Update requirements.txt",
    "Remove package-lock.json",
    "Delete package-lock.json",
    # These are too generic/specific to skip
    "Add misc apps",
    "add version label",
    "bump to latest",
    "Update pyodide",
    "Update image_ruiner.py",
    "make language proficiency better",
}

# Curses to mask (replace with asterisks for the hall of fame)
CURSE_WORDS = ["fuck", "shit", "ass", "damn", "crap", "hell"]

def clean_commit(msg: str) -> str:
    """Replace curse words with asterisks."""
    words = msg.split()
    cleaned = []
    for word in words:
        lower = word.lower()
        if any(curse in lower for curse in CURSE_WORDS):
            if len(word) > 1:
                cleaned.append(word[0] + "*" * (len(word) - 1))
            else:
                cleaned.append("*")
        else:
            cleaned.append(word)
    return " ".join(cleaned)

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "pages", "commit_hall_of_fame.py")

def get_user_commits(repo: str, max_commits: int = 30) -> list:
    """Get commits authored by 1TSnakers for a given repo."""
    owner, name = repo.split("/")
    try:
        all_commits = api.repos.list_commits(owner=owner, repo=name, per_page=100)
        commits = []
        for c in all_commits:
            if c.author and c.author.login == "1TSnakers":
                msg = c.commit.message.split('\n')[0]  # First line only
                # Skip merge commits and generic ones
                if msg and not msg.startswith("Merge") and msg not in GENERIC_COMMITS:
                    # Skip very short or very generic messages
                    if len(msg) < 5:
                        continue
                    if msg.startswith("Update ") and len(msg) < 20:
                        continue
                    commits.append(msg)
            if len(commits) >= max_commits:
                break
        return commits
    except Exception as e:
        print(f"Error fetching {repo}: {e}")
        return []

def generate_page(commits_by_repo: dict) -> str:
    """Generate the Streamlit page content."""
    lines = [
        "import streamlit as st",
        "",
        "st.set_page_config(page_title=\"Commit Hall of Fame\", layout=\"wide\")",
        "",
        "st.markdown(\"\"\"",
        "<style>",
        ".block-container { max-width: 1600px; padding-left: 2rem; padding-right: 2rem; margin: auto; }",
        ".stContainer { background-color: rgba(13,17,23,0.85); border-radius: 12px; padding: 1.5rem; }",
        "</style>",
        "\"\"\", unsafe_allow_html=True)",
        "",
        "st.title(\"🏆 Commit Message Hall of Fame\")",
        "",
        "st.markdown(\"*The best commit messages from 1TSnakers (Thomas McNamee)*\")",
        "",
        "st.markdown(\"---\")",
        "",
        "col1, col2 = st.columns(2)",
        "",
        "with col1:",
    ]
    
    for repo, commits in commits_by_repo.items():
        if commits:
            lines.append(f'    st.header("{repo}")')
            # Clean curse words from commits
            cleaned_commits = [clean_commit(c) for c in commits]
            commit_text = "\\n".join(cleaned_commits)
            lines.append(f'    st.code("""{commit_text}""", language=None)')
            lines.append("")
    
    lines.append("with col2:")
    
    # Fill column 2 with extra content or leave space for Best in Show
    # Add repos that didn't fit in col1 if needed, or just show empty space
    
    lines.extend([
        "st.markdown(\"---\")",
        "",
        "st.header(\"🏅 Best in Show\")",
        "st.info(\"**\\\"i have no idea what i am doing\\\"** — 1TSnakers/OllamaSearchAPI\\n\\n*Timeless. Relatable. Pure catharsis.*\")",
    ])
    
    return "\n".join(lines)

def main():
    print("Fetching latest commits...")
    
    commits_by_repo = {}
    for repo in REPOS:
        print(f"  Checking {repo}...")
        commits = get_user_commits(repo)
        commits_by_repo[repo] = commits
        if commits:
            print(f"    Found {len(commits)} commits")
            for c in commits[:5]:
                print(f"      - {clean_commit(c)}")
    
    # Generate and write the page
    content = generate_page(commits_by_repo)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Updated {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
