"""AST Code Symbol Dependency Graph & Blast Radius Analyzer.
100% Python Standard Library.
"""

from typing import List, Dict, Any, Set
import ast


class ASTDependencyAnalyzer:
    """Parses Python source code AST to extract symbols (functions, classes),
    constructs local call graphs, and computes modification blast radius."""

    @classmethod
    def extract_symbols(cls, source_code: str) -> Dict[str, Any]:
        """Extracts declared functions, classes, and their parameters/docstrings."""
        try:
            tree = ast.parse(source_code)
        except SyntaxError as exc:
            return {"success": False, "error": f"Syntax error parsing code: {exc}"}

        functions = []
        classes = []
        imports = []

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = [arg.arg for arg in node.args.args]
                functions.append({
                    "name": node.name,
                    "type": "async_function" if isinstance(node, ast.AsyncFunctionDef) else "function",
                    "line": node.lineno,
                    "args": args,
                    "docstring": ast.get_docstring(node) or "",
                })
            elif isinstance(node, ast.ClassDef):
                methods = [
                    m.name for m in node.body
                    if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
                ]
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "methods": methods,
                    "docstring": ast.get_docstring(node) or "",
                })
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}" if module else alias.name)

        return {
            "success": True,
            "functions": functions,
            "classes": classes,
            "imports": imports,
        }

    @classmethod
    def build_call_graph(cls, source_code: str) -> Dict[str, Any]:
        """Maps caller functions to all callee functions invoked inside their bodies."""
        try:
            tree = ast.parse(source_code)
        except SyntaxError as exc:
            return {"success": False, "error": str(exc)}

        caller_to_callees: Dict[str, Set[str]] = {}
        all_funcs: Set[str] = set()

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_name = node.name
                all_funcs.add(func_name)
                callees: Set[str] = set()

                for subnode in ast.walk(node):
                    if isinstance(subnode, ast.Call):
                        if isinstance(subnode.func, ast.Name):
                            callees.add(subnode.func.id)
                        elif isinstance(subnode.func, ast.Attribute):
                            callees.add(subnode.func.attr)

                caller_to_callees[func_name] = callees

        # Build reverse index (callee -> who calls it)
        callee_to_callers: Dict[str, List[str]] = {f: [] for f in all_funcs}
        for caller, callees in caller_to_callees.items():
            for c in callees:
                if c in callee_to_callers:
                    callee_to_callers[c].append(caller)

        return {
            "success": True,
            "call_graph": {k: list(v) for k, v in caller_to_callees.items()},
            "reverse_call_graph": callee_to_callers,
        }

    @classmethod
    def calculate_blast_radius(cls, source_code: str, target_symbol: str) -> Dict[str, Any]:
        """Calculates all upstream dependent functions that directly or indirectly
        rely on the target symbol (transitive blast radius)."""
        cg_res = cls.build_call_graph(source_code)
        if not cg_res.get("success"):
            return cg_res

        reverse_graph = cg_res["reverse_call_graph"]
        if target_symbol not in reverse_graph:
            return {
                "target_symbol": target_symbol,
                "blast_radius_score": 0,
                "affected_symbols": [],
                "impact_level": "LOW",
                "notice": f"Symbol '{target_symbol}' has no internal upstream callers in this scope.",
            }

        # BFS for transitive upstream callers
        visited: Set[str] = set()
        queue = [target_symbol]

        while queue:
            curr = queue.pop(0)
            callers = reverse_graph.get(curr, [])
            for c in callers:
                if c not in visited and c != target_symbol:
                    visited.add(c)
                    queue.append(c)

        affected = sorted(list(visited))
        count = len(affected)

        if count >= 5:
            impact = "CRITICAL"
        elif count >= 2:
            impact = "MEDIUM"
        elif count == 1:
            impact = "LOW"
        else:
            impact = "ISOLATED"

        return {
            "target_symbol": target_symbol,
            "blast_radius_score": count,
            "impact_level": impact,
            "affected_symbols": affected,
            "recommendation": (
                f"Modifying '{target_symbol}' will impact {count} upstream dependent(s): {', '.join(affected)}."
                if count > 0 else f"Modifying '{target_symbol}' is low risk; no internal callers detected."
            ),
        }
