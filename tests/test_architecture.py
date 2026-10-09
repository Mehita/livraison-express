"""Tests d'architecture : la règle de dépendance est vérifiée, pas seulement écrite.

On lit les `import` de chaque module (analyse syntaxique, pas une recherche de texte : un
commentaire qui cite « infrastructure » n'est pas une dépendance).

- `domain`, `application`, `abstractions` et `api` n'importent jamais `infrastructure` :
  seuls `bootstrap.py` et les tests le font ;
- les routeurs n'importent pas `joblib` : charger un fichier est un détail d'infrastructure,
  il reste dans l'adaptateur (`FileModelRepository`), assemblé par `bootstrap.py`.
"""

from __future__ import annotations

import ast
from pathlib import Path

SOURCE = Path(__file__).resolve().parent.parent / "src" / "livraison_express"
INNER_LAYERS = ("domain", "application", "abstractions", "api")


def _imported_modules(path: Path) -> set[str]:
    modules: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add("." * node.level + (node.module or ""))
            modules.update(
                "." * node.level + (node.module or "") + "." + a.name for a in node.names
            )
    return modules


def _python_files(*layers: str) -> list[Path]:
    return [path for layer in layers for path in (SOURCE / layer).rglob("*.py")]


def test_inner_layers_never_import_infrastructure() -> None:
    violations = [
        f"{path.relative_to(SOURCE)} importe {module}"
        for path in _python_files(*INNER_LAYERS)
        for module in _imported_modules(path)
        if "infrastructure" in module.split(".")
    ]

    assert violations == []


def test_routers_do_not_import_joblib() -> None:
    violations = [
        f"{path.relative_to(SOURCE)} importe {module}"
        for path in _python_files("api")
        for module in _imported_modules(path)
        if module.split(".")[0] == "joblib"
    ]

    assert violations == []


def test_the_check_detects_a_violation(tmp_path: Path) -> None:
    """The guard itself works: a module importing infrastructure is reported."""
    bad = tmp_path / "bad.py"
    bad.write_text("from ..infrastructure.dev import x\n", encoding="utf-8")

    assert any("infrastructure" in module.split(".") for module in _imported_modules(bad))
