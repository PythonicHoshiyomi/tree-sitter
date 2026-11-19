import os
import sys
import ctypes
from tree_sitter import Language, Parser

dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "filter.dll"))
lib = ctypes.CDLL(dll_path)
fn = lib.tree_sitter_filter
fn.restype = ctypes.c_void_p
FILTER_LANG = Language(fn())
parser = Parser(FILTER_LANG)

def parse_val(node):
    raw = node.text.decode()
    if node.type == "string":
        return raw.strip('"')
    elif node.type == "number":
        return float(raw) if "." in raw else int(raw)
    elif node.type == "boolean":
        return raw.lower() == "true"
    return raw

def compile_node(node, params):
    if node.type == "query":
        return compile_node(node.named_children[0], params)

    elif node.type == "comparison":
        fld = node.child_by_field_name("field").text.decode()
        op = node.child_by_field_name("operator").text.decode()
        val = parse_val(node.child_by_field_name("value"))
        params.append(val)
        return f"{fld} {op} ?"

    elif node.type == "in_expression":
        fld = node.child_by_field_name("field").text.decode()
        vals_nodes = node.children_by_field_name("values")
        placeholders = []
        for vn in vals_nodes:
            params.append(parse_val(vn))
            placeholders.append("?")
        return f"{fld} IN ({', '.join(placeholders)})"

    elif node.type == "contains_expression":
        fld = node.child_by_field_name("field").text.decode()
        val = parse_val(node.child_by_field_name("value"))
        params.append(f"%{val}%")
        return f"{fld} LIKE ?"

    elif node.type == "and_expression":
        left = compile_node(node.child_by_field_name("left"), params)
        right = compile_node(node.child_by_field_name("right"), params)
        return f"({left} AND {right})"

    elif node.type == "or_expression":
        left = compile_node(node.child_by_field_name("left"), params)
        right = compile_node(node.child_by_field_name("right"), params)
        return f"({left} OR {right})"

    elif node.type == "not_expression":
        opnd = compile_node(node.child_by_field_name("operand"), params)
        return f"(NOT {opnd})"

    elif node.type == "parenthesized":
        return compile_node(node.named_children[0], params)

    raise ValueError(f"Unknown node type: {node.type}")

def filter_to_sql(dsl_text):
    tree = parser.parse(dsl_text.encode())
    if tree.root_node.has_error:
        raise ValueError("Sintaks DSL filter tidak valid.")
    params = []
    where_clause = compile_node(tree.root_node, params)
    return where_clause, params

if __name__ == "__main__":
    contoh_input = 'status in ("open", "pending") and (priority > 2 or owner = "budi")'
    where, params = filter_to_sql(contoh_input)
    print("DSL Filter :", contoh_input)
    print("SQL WHERE  :", where)
    print("Parameters :", params)
