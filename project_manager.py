import asyncio
from playwright.async_api import async_playwright
from config import CONFIG

async def list_projects(page):
    """Lists all available projects in NotebookLM."""
    print(CONFIG["messages"]["info"]["listing_projects"])
    await page.wait_for_selector(CONFIG["selectors"]["project_button"])
    
    projects = await page.evaluate(f"""
        Array.from(document.querySelectorAll('{CONFIG["selectors"]["project_button"]}')).map(button => {{
            const titleElement = button.querySelector('span.project-button-title');
            return titleElement ? titleElement.innerText.trim() : null;
        }}).filter(title => title)
    """)

    if projects:
        print(CONFIG["messages"]["info"]["available_projects"])
        for p in projects:
            print(f"- {p}")
        print("\n--- 次のステップ ---") # 新しい見出しを追加
        print(CONFIG["messages"]["info"]["re_run_hint"])
    else:
        print(CONFIG["messages"]["info"]["no_projects_found"])
