# genpark-ast-code-symbol-dependency-graph-and-blast-radius-analyzer-skill

Parses source code abstract syntax trees to extract symbol definitions, call graphs, and calculate modification blast radius.

100% Python Standard Library implementation with zero external dependencies.

## Key Capabilities
- **AST Symbol Extraction**: Traverses Python abstract syntax trees to index functions, methods, classes, signatures, and imports.
- **Directional Call Graphs**: Analyzes internal call hierarchies and reverse dependencies (`callee -> callers`).
- **Transitive Blast Radius Calculation**: Uses BFS to discover all direct and indirect upstream dependents affected by altering or refactoring a symbol.
- **Zero Dependencies**: Pure Python standard library with microsecond parsing performance.

## Architecture

```
[Target Source Code File]
           │
           ▼
┌──────────────────────────────────────────────┐
│  ASTDependencyAnalyzer                       │
│  ├─ AST Syntax Tree Parser (ast)             │
│  ├─ Symbol Definition Indexer                │
│  ├─ Bi-Directional Call Graph Builder        │
│  └─ Transitive Blast Radius BFS Engine       │
└──────────────────────────────────────────────┘
           │
           ▼
[Affected Upstream Callers & Risk Level]
```

## MCP Server Integration

Run standard MCP stdio server:
```bash
python mcp_server.py
```

Exposed Tools:
- `extract_symbols`: Extracts declared functions, classes, and imports.
- `calculate_blast_radius`: Computes all upstream dependent functions that directly or transitively rely on a target symbol.

## Quickstart

```python
from client import ASTDependencyAnalyzer

code = """
def db_query(): pass
def get_user(): return db_query()
def render_profile(): return get_user()
"""

# Calculate impact of refactoring db_query
res = ASTDependencyAnalyzer.calculate_blast_radius(code, "db_query")
print("Blast Radius:", res["blast_radius_score"])  # 2
print("Affected Symbols:", res["affected_symbols"])  # ['get_user', 'render_profile']
```

---

## GenPark Ecosystem

- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)
