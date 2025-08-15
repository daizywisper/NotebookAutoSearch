import asyncio
import re
import os
from pathlib import Path
from datetime import datetime
from config import CONFIG

def sanitize_filename(name):
    """Sanitizes a string to be a valid filename."""
    # Remove invalid characters
    name = re.sub(r'[\\/:*?"<>|]', '_', name)
    # Replace whitespace with underscores
    name = re.sub(r'\s+', '_', name)
    # Truncate to a reasonable length
    return name[:100]

async def search_and_save(page, project_name, search_term):
    """Performs a search and saves the result."""
    print(CONFIG["messages"]["info"]["starting_search"].format(search_term))

    print(CONFIG["messages"]["info"]["wait_for_search_box"])
    await page.wait_for_selector(CONFIG["selectors"]["search_box"])

    print(CONFIG["messages"]["info"]["filling_search_box"].format(search_term))
    await page.fill(CONFIG["selectors"]["search_box"], "")
    await page.fill(CONFIG["selectors"]["search_box"], search_term)

    print(CONFIG["messages"]["info"]["clicking_send"])
    await page.wait_for_selector(CONFIG["selectors"]["send_button"])
    await page.click(CONFIG["selectors"]["send_button"])

    print(CONFIG["messages"]["info"]["wait_for_response"])
    last_message = page.locator(CONFIG["selectors"]["result_message_card"]).last
    text_container = last_message.locator(CONFIG["selectors"]["message_text_content"])

    await text_container.wait_for(state="visible", timeout=CONFIG["timeouts"]["wait_for_visible"])

    previous_text = ""
    stable_iterations = 0
    deadline = asyncio.get_event_loop().time() + CONFIG["timeouts"]["stabilization"] / 1000

    while asyncio.get_event_loop().time() < deadline:
        current_text = await text_container.inner_text()
        if current_text == previous_text and current_text.strip() != "":
            stable_iterations += 1
        else:
            stable_iterations = 0
        
        if stable_iterations >= CONFIG["stability"]["required_stable_iterations"]:
            print(CONFIG["messages"]["info"]["text_stabilized"])
            break
        
        previous_text = current_text
        await asyncio.sleep(CONFIG["timeouts"]["stabilization_interval"] / 1000)

    if stable_iterations < CONFIG["stability"]["required_stable_iterations"]:
        print(CONFIG["messages"]["warn"]["text_not_stable"])

    result_text = await text_container.inner_text()
    
    print(CONFIG["messages"]["info"]["search_result_header"])
    print(result_text.strip())
    print(CONFIG["messages"]["info"]["search_result_footer"])

    # Clean up the text by removing reference numbers and formatting
    cleaned_lines = []
    for line in result_text.split('\n'):
        # Remove trailing reference numbers (e.g., "1:", "1.", " [1]")
        line = re.sub(r'\s*\d+[:.]?$', '', line).strip()
        line = re.sub(r'\[\d+\]', '', line).strip()
        # Remove leading list numbers (e.g., "1. ")
        line = re.sub(r'^\s*\d+\.\s*', '', line).strip()
        if line: # Only add non-empty lines
            cleaned_lines.append(line)
    
    # Markdown形式で整形
    file_content = f"## {search_term}\n\n"
    
    if cleaned_lines:
        # 最初の行は要約としてそのまま残す
        file_content += f"{cleaned_lines[0]}\n\n"
        # 残りの行を箇条書きとして整形
        if len(cleaned_lines) > 1:
            for line in cleaned_lines[1:]:
                # 既存の箇条書き記号があれば削除
                if line.startswith(('•', '*', '-')):
                    line = line[1:].lstrip()
                file_content += f"* {line}\n"
    
    file_content += "\n---\n" # 区切り線を追加

    timestamp = datetime.now().strftime("%Y%m%d")
    safe_project_name = sanitize_filename(project_name)
    safe_search_term = sanitize_filename(search_term)
    file_path = CONFIG["paths"]["output_dir"] / f"{timestamp}_{safe_project_name}_{safe_search_term}.md"

    CONFIG["paths"]["output_dir"].mkdir(exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(file_content)
    
    relative_path = os.path.relpath(file_path, CONFIG["paths"]["project_root"])
    print(CONFIG["messages"]["info"]["file_saved"].format(f"/{relative_path}"))