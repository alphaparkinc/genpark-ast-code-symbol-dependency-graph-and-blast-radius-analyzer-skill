"""Example usage for AST Code Symbol Dependency Graph & Blast Radius Analyzer."""
from client import ASTDependencyAnalyzer

SAMPLE_CODE = """
def fetch_raw_data(query):
    return {"data": query}

def validate_payload(payload):
    data = fetch_raw_data(payload)
    return data is not None

def process_pipeline(input_val):
    if validate_payload(input_val):
        return True
    return False

def standalone_helper():
    return 42
"""

if __name__ == "__main__":
    # 1. Extract symbols
    symbols = ASTDependencyAnalyzer.extract_symbols(SAMPLE_CODE)
    print("Discovered Functions:", [f["name"] for f in symbols["functions"]])

    # 2. Calculate blast radius of modifying low-level dependency
    radius = ASTDependencyAnalyzer.calculate_blast_radius(SAMPLE_CODE, "fetch_raw_data")
    print("\nTarget Symbol:", radius["target_symbol"])
    print("Blast Radius Score:", radius["blast_radius_score"])
    print("Impact Level:", radius["impact_level"])
    print("Affected Upstream Callers:", radius["affected_symbols"])
