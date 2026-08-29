import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mcp_config_exists_and_valid():
    mcp_file = ROOT / ".mcp.json"
    assert mcp_file.is_file(), ".mcp.json must exist in root"
    data = json.loads(mcp_file.read_text(encoding="utf-8"))
    assert "graphify" in data.get("mcpServers", {}), "graphify server must be declared in .mcp.json"
    args = data["mcpServers"]["graphify"]["args"]
    assert "graphify.serve" in args, "graphify server must use official python -m graphify.serve"


def test_graph_json_exists_and_tracked():
    graph_file = ROOT / "graphify-out" / "graph.json"
    assert graph_file.is_file(), "graphify-out/graph.json must exist"
    data = json.loads(graph_file.read_text(encoding="utf-8"))
    assert len(data.get("nodes", [])) > 0, "graph.json must contain nodes"


def test_mcp_serve_cli_runs():
    # Verify uvx can invoke graphify.serve correctly
    res = subprocess.run(
        ["uvx", "--from", "graphifyy[mcp]", "python3", "-m", "graphify.serve", "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "Serve a graphify knowledge graph over MCP" in res.stdout


def test_git_tracking_and_cache_ignored():
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "!graphify-out/graph.json" in gitignore, "graph.json must be un-ignored in .gitignore"


def main():
    test_mcp_config_exists_and_valid()
    print("ok  test_mcp_config_exists_and_valid")
    test_graph_json_exists_and_tracked()
    print("ok  test_graph_json_exists_and_tracked")
    test_mcp_serve_cli_runs()
    print("ok  test_mcp_serve_cli_runs")
    test_git_tracking_and_cache_ignored()
    print("ok  test_git_tracking_and_cache_ignored")
    print("\nall tests passed!")


if __name__ == "__main__":
    main()
