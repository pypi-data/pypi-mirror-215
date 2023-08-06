"""Functions for indexing Python code."""

import json
from pathlib import Path
from typing import List, Union

from llama_index import GPTVectorStoreIndex
from llama_index.data_structs.node_v2 import Node, DocumentRelationship

from automata.utilities.module_processing import (
    split_module_chunks,
    extract_function_name,
    construct_fn_id,
    construct_module_path,
)


def create_python_code_node(
    code_chunk: str,
    module_prefix: List[str],
    name_placeholder: str,
    package_dir: Path = Path(),
    class_name: Union[str, None] = None,
) -> Node:
    """Create a node for a Python function or method."""
    fn_name = extract_function_name(code_chunk) or name_placeholder
    fn_id = construct_fn_id(fn_name, package_dir, module_prefix, class_name)
    module_path = construct_module_path(module_prefix, package_dir)
    node = Node(text=code_chunk, doc_id=fn_id)
    node.relationships[DocumentRelationship.SOURCE] = str(module_path)
    return node


def create_py_module_index(
    package_dir: Path, module_prefix: List[str]
) -> GPTVectorStoreIndex:
    """Create an index for a Python module."""
    path = package_dir.joinpath(*module_prefix).with_suffix(".py")
    code = path.read_text(encoding="utf-8")
    chunks = split_module_chunks(code)
    nodes = [
        create_python_code_node(
            chunk,
            module_prefix,
            name_placeholder=f"chunk_{i + 1}",
            package_dir=package_dir,
        )
        for i, chunk in enumerate(chunks)
    ]
    for i, node in enumerate(nodes):
        if i > 0:
            node.relationships[DocumentRelationship.PREVIOUS] = nodes[
                i - 1
            ].get_doc_id()
        if i < len(nodes) - 1:
            node.relationships[DocumentRelationship.NEXT] = nodes[i + 1].get_doc_id()
    index = GPTVectorStoreIndex(nodes)
    return index


def create_notebook_module_index(notebook_path: Path) -> GPTVectorStoreIndex:
    """Create an index for an automaton notebook"""
    if not notebook_path.suffix == ".jsonl":
        raise ValueError("Automaton notebook must be a JSONL file.")
    with open(notebook_path, encoding="utf-8") as file:
        nodes = (Node(text=entry, doc_id=json.loads(entry)["timestamp"]) for entry in file)
        nodes = list(nodes)
        for node in nodes:
            node.relationships[DocumentRelationship.SOURCE] = str(notebook_path)
    return GPTVectorStoreIndex(nodes)


def demo() -> None:
    """Demo the indexing functionality."""
    index = create_py_module_index(Path("scripts"), ["run_automata"])
    print(index.query("tell me about this module"))
    print(index.query("tell me about the `load_automaton` function"))


if __name__ == "__main__":
    demo()
