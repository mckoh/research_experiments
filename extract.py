# %%
from requests import post, get
from datetime import datetime
from os import getenv
from os.path import basename
from json import load


NOTION_TOKEN = getenv("NOTION_TOKEN")
DATABASE_ID = getenv("DATABASE_ID")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_notion_entry(filename, description, url, date=datetime.now().isoformat()):
    create_url = "https://api.notion.com/v1/pages"

    data = {
        "Filename": {"title": [{"text": {"content": filename}}]},
        "Description": {"rich_text": [{"text": {"content": description}}]},
        "Github URL": {"url": url},
        "Last modified": {"date": {"start": date}}
    }

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": data
    }

    response = post(create_url, headers=headers, json=payload)
    return response.status_code, response.text


def get_first_markdown_content(file_path):
    """Liest die erste Markdown-Zelle aus einem Jupyter Notebook."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            nb_data = load(f)

        for cell in nb_data.get("cells", []):
            if cell.get("cell_type") == "markdown":
                content = "".join(cell.get("source", []))
                return content[:1000] if content else "Keine Beschreibung gefunden."
    except Exception as e:
        print(f"Fehler beim Parsen von {file_path}: {e}")

    return "Notebook ohne Markdown-Beschreibung."


if __name__ == "__main__":

    new_files = getenv("NEW_FILES", "").split()

    print(new_files)

    for file_path in new_files:
        if file_path.startswith("notebooks/") and file_path.endswith(".ipynb"):
            filename = basename(file_path)
            description = get_first_markdown_content(file_path)
            url = f"https://github.com/mckoh/research_experiments/blob/main/{file_path}"
            status, text = create_notion_entry(
                filename=filename,
                description=description,
                url=url
            )
            print(f"Datei {filename} verarbeitet. Status: {status}")
            print(f"Response: {text}")
# %%
