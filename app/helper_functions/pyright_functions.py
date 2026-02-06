def extract_pyright_errors(pyright_json: dict) -> list[dict]:
    diagnostics = pyright_json.get("generalDiagnostics", [])

    errors = []

    for diag in diagnostics:
        errors.append({
            "file": diag.get("file"),
            "line": diag.get("range", {}).get("start", {}).get("line", 0) + 1,
            "character": diag.get("range", {}).get("start", {}).get("character", 0),
            "message": diag.get("message"),
            "severity": diag.get("severity"),
            "rule": diag.get("rule", None)
        })

    return errors