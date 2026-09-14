# -*- coding: utf-8 -*-
"""Metadata, Manifest, and Documentation Parity Tests for COMA."""
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_version_parity():
    """Verify that all version strings across package definitions match exactly."""
    pyproject_path = REPO_ROOT / "pyproject.toml"
    assert pyproject_path.exists(), "pyproject.toml missing"
    pyproject_content = pyproject_path.read_text(encoding="utf-8")
    pyproject_ver_match = re.search(r'version\s*=\s*"([^"]+)"', pyproject_content)
    assert pyproject_ver_match, "version not found in pyproject.toml"
    version = pyproject_ver_match.group(1)

    # Check ellmos-module.v2.json
    manifest_path = REPO_ROOT / "ellmos-module.v2.json"
    assert manifest_path.exists(), "ellmos-module.v2.json missing"
    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest_data.get("version") == version, (
        f"Manifest version {manifest_data.get('version')} does not match pyproject.toml {version}"
    )

    # Check coma/__init__.py
    coma_init = REPO_ROOT / "coma" / "__init__.py"
    assert coma_init.exists(), "coma/__init__.py missing"
    coma_init_content = coma_init.read_text(encoding="utf-8")
    coma_ver_match = re.search(r'__version__\s*=\s*"([^"]+)"', coma_init_content)
    assert coma_ver_match, "__version__ missing in coma/__init__.py"
    assert coma_ver_match.group(1) == version, (
        f"coma.__version__ {coma_ver_match.group(1)} does not match {version}"
    )

    # Check comas/__init__.py
    comas_init = REPO_ROOT / "comas" / "__init__.py"
    assert comas_init.exists(), "comas/__init__.py missing"
    comas_init_content = comas_init.read_text(encoding="utf-8")
    assert "__version__" in comas_init_content, "__version__ missing in comas/__init__.py"

    # Check CHANGELOG.md
    changelog_path = REPO_ROOT / "CHANGELOG.md"
    assert changelog_path.exists(), "CHANGELOG.md missing"
    changelog_content = changelog_path.read_text(encoding="utf-8")
    assert f"[{version}]" in changelog_content, (
        f"Release [{version}] header missing from CHANGELOG.md"
    )


def test_core_documentation_files():
    """Verify presence and non-emptiness of core documentation and policy files."""
    required_files = [
        "README.md",
        "README_de.md",
        "llms.txt",
        "SECURITY.md",
        "LICENSE",
        "KONZEPT.md",
        "BEFUNDE.md",
        "CHANGELOG.md",
        "MARKETING-LOG.txt",
        "THIRD_PARTY_LICENSES.md",
        "TODO.md",
        "pyproject.toml",
        "ellmos-module.v2.json",
    ]
    for rel_path in required_files:
        file_path = REPO_ROOT / rel_path
        assert file_path.exists(), f"Required file {rel_path} does not exist"
        assert file_path.stat().st_size > 0, f"Required file {rel_path} is empty"


def test_manifest_schema_and_boundaries():
    """Verify ellmos-module.v2.json metadata structure and integrity."""
    manifest_path = REPO_ROOT / "ellmos-module.v2.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest.get("schema") == "ellmos.module.v2"
    assert manifest.get("id") == "coma"
    assert manifest.get("category") == "orchestration"
    assert manifest.get("kind") == "runtime"
    assert manifest.get("status") in ("development", "stable", "production")
    assert manifest.get("visibility") == "public"

    boundaries = manifest.get("boundaries", {})
    assert boundaries.get("network") == "none", "COMA must declare network: none boundary"
    assert boundaries.get("data") == "user-local", "COMA data must be user-local"

    source_of_truth = manifest.get("source_of_truth", {})
    assert source_of_truth.get("repository") == "https://github.com/ellmos-ai/coma"


def test_llms_txt_structure():
    """Verify that llms.txt provides complete RAG context and valid metadata."""
    llms_path = REPO_ROOT / "llms.txt"
    content = llms_path.read_text(encoding="utf-8")

    assert "# COMA" in content
    assert "Last-checked:" in content
    assert "Verification:" in content
    assert "ClaudeAdapter" in content
    assert "CodexAdapter" in content
    assert "AntigravityAdapter" in content
    assert "KimiAdapter" in content
    assert "JobBoard" in content
    assert "JobRunner" in content
    assert "INV-COMA-01" in content
    assert "MARKETING-LOG.txt" in content


def test_readme_badge_and_ecosystem_parity():
    """Verify that README.md and README_de.md include valid badges and ecosystem links."""
    readme_en = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (REPO_ROOT / "README_de.md").read_text(encoding="utf-8")

    for readme, lang in [(readme_en, "EN"), (readme_de, "DE")]:
        assert "ellmos-ai" in readme, f"Ecosystem badge/link missing in {lang} README"
        assert "open-bricks" in readme, f"Umbrella badge/link missing in {lang} README"
        assert "llms.txt" in readme, f"llms.txt reference missing in {lang} README"
        assert "pytest" in readme, f"Pytest badge missing in {lang} README"
        assert "MIT" in readme, f"License badge missing in {lang} README"
        assert "docs/assets/banner.svg" in readme, f"Banner reference missing in {lang} README"
        assert "sequenceDiagram" in readme, f"Sequence diagram missing in {lang} README"
        assert "flowchart TD" in readme, f"Flowchart diagram missing in {lang} README"
        for inv_num in range(1, 9):
            assert f"INV-COMA-0{inv_num}" in readme, f"INV-COMA-0{inv_num} missing in {lang} README"


def test_pyproject_pep621_urls():
    """Verify that pyproject.toml defines complete PEP 621 project URLs."""
    pyproject_content = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "[project.urls]" in pyproject_content
    assert "Homepage" in pyproject_content
    assert "Repository" in pyproject_content
    assert "Documentation" in pyproject_content
    assert "Issues" in pyproject_content
    assert "Changelog" in pyproject_content
    assert "Security" in pyproject_content
    assert "LLM Ready" in pyproject_content
    assert "Marketing Log" in pyproject_content
    assert "Parent Organization" in pyproject_content
    assert "Umbrella Ecosystem" in pyproject_content


def test_marketing_log_structure():
    """Verify that MARKETING-LOG.txt exists and contains required strategic sections."""
    marketing_log_path = REPO_ROOT / "MARKETING-LOG.txt"
    assert marketing_log_path.exists()
    content = marketing_log_path.read_text(encoding="utf-8")
    assert "Ziel-Personas" in content or "Target" in content
    assert "Discoverability" in content or "SEO" in content
    assert "Awesome-" in content
    assert "Roadmap" in content or "Empfehlungen" in content


def test_license_and_third_party_inventory():
    """Verify THIRD_PARTY_LICENSES.md invariant and PEP 639 license-files."""
    licenses_path = REPO_ROOT / "THIRD_PARTY_LICENSES.md"
    assert licenses_path.exists()
    content = licenses_path.read_text(encoding="utf-8")
    assert "Zero External Runtime Dependencies" in content
    assert "INV-COMA-02" in content
    assert "MIT License" in content

    pyproject_content = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'license-files = ["LICENSE", "THIRD_PARTY_LICENSES.md"]' in pyproject_content


def test_todo_status_table():
    """Verify TODO.md existence and STATUS table format."""
    todo_path = REPO_ROOT / "TODO.md"
    assert todo_path.exists()
    content = todo_path.read_text(encoding="utf-8")
    assert "## STATUS" in content
    assert "| Category" in content or "|Category" in content
    assert "TASK-COMA-" in content


def test_ci_workflow_timeouts_concurrency_and_runner():
    """Verify .github/workflows/tests.yml CI workflow timeouts and concurrency."""
    ci_path = REPO_ROOT / ".github" / "workflows" / "tests.yml"
    assert ci_path.exists(), ".github/workflows/tests.yml missing"
    content = ci_path.read_text(encoding="utf-8")
    assert "timeout-minutes: 15" in content
    assert "cancel-in-progress: true" in content
    assert "pytest -ra -v" in content


def test_stale_workflow_present_and_safe():
    """Verify .github/workflows/stale.yml stale lifecycle automation."""
    stale_path = REPO_ROOT / ".github" / "workflows" / "stale.yml"
    assert stale_path.exists(), ".github/workflows/stale.yml missing"
    content = stale_path.read_text(encoding="utf-8")
    assert "actions/stale@v9" in content
    assert "timeout-minutes: 10" in content
    assert "cancel-in-progress: true" in content
    assert "issues: write" in content
    assert "pull-requests: write" in content


def test_welcome_workflow_present_and_safe():
    """Verify .github/workflows/welcome.yml contributor greeting workflow."""
    welcome_path = REPO_ROOT / ".github" / "workflows" / "welcome.yml"
    assert welcome_path.exists(), ".github/workflows/welcome.yml missing"
    content = welcome_path.read_text(encoding="utf-8")
    assert "actions/first-interaction@v3" in content
    assert "timeout-minutes: 5" in content
    assert "cancel-in-progress: true" in content


def test_gitignore_canonical_locks_and_multihost_defense():
    """Verify .gitignore hardening for canonical locks, host sync artifacts, and caches."""
    gi_path = REPO_ROOT / ".gitignore"
    assert gi_path.exists(), ".gitignore missing"
    content = gi_path.read_text(encoding="utf-8")
    required_patterns = [
        "LOCK",
        "LOCK.*",
        "uv.lock",
        "*-WORKSTATION*",
        "*-ASUS*",
        "*-LAPTOP*",
        "* (kopie)*",
        "* (copy)*",
        "*conflicted copy*",
        ".coverage.*",
        "htmlcov/",
        ".mypy_cache/",
        ".hypothesis/",
        ".turbo/",
    ]
    for pattern in required_patterns:
        assert pattern in content, f"Missing required .gitignore pattern: {pattern}"


def test_pyproject_pytest_addopts():
    """Verify pyproject.toml configures standard pytest runner options."""
    content = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'addopts = "-ra -v"' in content


def test_marketing_log_recent_hygiene_entry():
    """Verify MARKETING-LOG.txt includes recent Pfad A hygiene audit entry."""
    content = (REPO_ROOT / "MARKETING-LOG.txt").read_text(encoding="utf-8")
    assert "Stand: 2026-09-14" in content
    assert "Pfad A" in content
    assert "Release 0.3.1 Highlights" in content


def test_changelog_recent_pfad_a_entry():
    """Verify CHANGELOG.md documents Release 0.3.1 on 2026-09-14."""
    content = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "[0.3.1] — 2026-09-14" in content
    assert ".github/workflows/tests.yml" in content

