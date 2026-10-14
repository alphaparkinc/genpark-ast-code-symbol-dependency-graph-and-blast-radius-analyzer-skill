"""MCP server for AST Code Symbol Dependency Graph & Blast Radius Analyzer."""
import sys
import json
from client import ASTDependencyAnalyzer


def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "extract_symbols",
                    "description": "Extracts declared functions, classes, and imports from Python source code using AST",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "source_code": {"type": "string", "description": "Python code string"}
                        },
                        "required": ["source_code"],
                    },
                },
                {
                    "name": "calculate_blast_radius",
                    "description": "Computes all upstream dependent functions that directly or transitively rely on a target symbol",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "source_code": {"type": "string", "description": "Python source code"},
                            "target_symbol": {"type": "string", "description": "Name of function or method about to be edited/removed"},
                        },
                        "required": ["source_code", "target_symbol"],
                    },
                },
            ]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "extract_symbols":
            res = ASTDependencyAnalyzer.extract_symbols(args.get("source_code", ""))
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
        elif tool_name == "calculate_blast_radius":
            res = ASTDependencyAnalyzer.calculate_blast_radius(
                args.get("source_code", ""),
                args.get("target_symbol", ""),
            )
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
