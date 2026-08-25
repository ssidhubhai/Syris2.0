import json
import re
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = BACKEND_DIR.parent
SOURCE_DIR = BACKEND_DIR / "evals" / "results" / "phase4c_live"
FRONTEND_REGRESSION_DIR = WORKSPACE_DIR / "frontend" / "src" / "fixtures" / "regression"
FRONTEND_REGRESSION_DIR.mkdir(parents=True, exist_ok=True)
SOURCE_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_ts_key(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)


def clean_document_for_ts(doc: dict) -> dict:
    if not isinstance(doc, dict):
        return doc
    cleaned = {}
    for k, v in doc.items():
        if v is None:
            continue
        if isinstance(v, dict):
            cleaned[k] = clean_document_for_ts(v)
        elif isinstance(v, list):
            cleaned[k] = [clean_document_for_ts(elem) if isinstance(elem, dict) else elem for elem in v]
        else:
            cleaned[k] = v
    return cleaned


def export_fixtures():
    # If source dir has json files, convert them to typescript fixtures
    summary_path = SOURCE_DIR / "phase4c_summary.json"
    if not summary_path.exists():
        print(f"Summary file not found at {summary_path}")
        return

    data = json.loads(summary_path.read_text(encoding="utf-8"))
    index_exports = []

    for item in data:
        case_id = item["case_id"]
        ts_filename = f"{case_id.replace('-', '_')}_fixture.ts"
        ts_var_name = f"{sanitize_ts_key(case_id)}_fixture"
        doc = clean_document_for_ts(item["document"])

        ts_content = (
            f"import {{ ExplanationDocument }} from '@/types/explanation';\n\n"
            f"/**\n"
            f" * Frozen Real-AI Regression Fixture for Phase 4C\n"
            f" * Case: {item['title']} ({item['category']})\n"
            f" * Query: \"{item['query']}\"\n"
            f" * Model: {item['model_id']} | Prompt: {item['prompt_version']}\n"
            f" */\n"
            f"export const {ts_var_name}: ExplanationDocument = "
            f"{json.dumps(doc, indent=2)};\n"
        )

        target_file = FRONTEND_REGRESSION_DIR / ts_filename
        target_file.write_text(ts_content, encoding="utf-8")
        print(f"Exported fixture: {target_file.name}")
        index_exports.append((ts_var_name, ts_filename[:-3], case_id, item['title'], item['category']))

    # Write regression index.ts
    index_lines = ["// Auto-generated Phase 4C regression fixtures index\n"]
    for var_name, mod_name, case_id, title, cat in index_exports:
        index_lines.append(f"import {{ {var_name} }} from './{mod_name}';")

    index_lines.append("\nexport const REGRESSION_FIXTURES: Record<string, any> = {")
    for var_name, mod_name, case_id, title, cat in index_exports:
        index_lines.append(f"  '{case_id}': {var_name},")
    index_lines.append("};\n")

    index_lines.append("export const REGRESSION_METADATA = [")
    for var_name, mod_name, case_id, title, cat in index_exports:
        index_lines.append(f"  {{ id: '{case_id}', title: '{title}', category: '{cat}', fixture: '{var_name}' }},")
    index_lines.append("];\n")

    (FRONTEND_REGRESSION_DIR / "index.ts").write_text("\n".join(index_lines), encoding="utf-8")
    print(f"Generated index.ts in {FRONTEND_REGRESSION_DIR}")


if __name__ == "__main__":
    export_fixtures()
