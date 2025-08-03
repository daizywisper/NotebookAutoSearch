import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from config import CONFIG

async def setup_auth():
    """Handles the initial browser login to create a user profile."""
    print(CONFIG["messages"]["info"]["profile_creation"].format(CONFIG["paths"]["user_data_dir"]))
    print(CONFIG["messages"]["info"]["separator"])
    print(CONFIG["messages"]["info"]["launching_browser"])
    print(CONFIG["messages"]["info"]["manual_login_prompt"])
    print(CONFIG["messages"]["info"]["script_auto_termination"])
    print(CONFIG["messages"]["info"]["separator"])

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            CONFIG["paths"]["user_data_dir"],
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = await context.new_page()
        try:
            await page.goto(CONFIG["urls"]["notebooklm"])
            print(CONFIG["messages"]["info"]["waiting_for_login"])
            await page.wait_for_selector(
                CONFIG["selectors"]["project_button"], timeout=CONFIG["timeouts"]["login"]
            )
            print(CONFIG["messages"]["info"]["login_detected"])
        except PlaywrightTimeoutError:
            print(CONFIG["messages"]["error"]["generic_error"].format("Login timed out."))
            print(CONFIG["messages"]["error"]["timeout_suggestion"])
        except Exception as e:
            print(CONFIG["messages"]["error"]["generic_error"].format(e))
        finally:
            await context.close()
            print(CONFIG["messages"]["info"]["browser_closed"])
