import re
import tomllib


def ler_requirements(caminho):
    deps = []
    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha or linha.startswith("#") or linha.startswith("-"):
                continue
            match = re.match(r"^([A-Za-z0-9_.\-]+)(?:\[.*\])?\s*(==|>=|<=|~=)?\s*([A-Za-z0-9_.\-]*)", linha)
            if match:
                nome, _op, versao = match.groups()
                deps.append({"nome": nome, "versao": versao or None})
    return deps


def ler_pyproject(caminho):
    with open(caminho, "rb") as f:
        data = tomllib.load(f)

    deps = []

    for item in data.get("project", {}).get("dependencies", []):
        match = re.match(r"^([A-Za-z0-9_.\-]+)\s*(==|>=|<=|~=)?\s*([A-Za-z0-9_.\-]*)", item)
        if match:
            nome, _op, versao = match.groups()
            deps.append({"nome": nome, "versao": versao or None})

    poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    for nome, spec in poetry_deps.items():
        if nome.lower() == "python":
            continue
        if isinstance(spec, str):
            versao = spec.strip("^~>=<")
        else:
            versao = None
        deps.append({"nome": nome, "versao": versao})

    return deps


def ler_dependencias(caminho):
    if caminho.endswith("pyproject.toml"):
        return ler_pyproject(caminho)
    return ler_requirements(caminho)
