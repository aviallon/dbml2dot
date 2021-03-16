import math
from textwrap import dedent
import pydbml.classes
import pydot

from dbml2dot.utils import debug


def generate_table_label(name: str, attributes: list[str]):
    attribute_list: list[str] = []
    for attr in attributes:
        attribute_list += [f"""<TR><TD align="left">{attr}</TD></TR>"""]
    attribute_list_str = "\n".join(attribute_list)
    return dedent(f'''
        <<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="1">
        <TR><TD><B>{name}</B></TD></TR><HR></HR>
        {attribute_list_str}
        </TABLE>>''').strip().replace('\n', '\n\t')


def generate_column_node(name: str, column_attributes: pydbml.classes.Column, enums: list[str]):
    not_null_string = "" if column_attributes.not_null or column_attributes.pk else "?"
    col_string = f"{name}{not_null_string}"
    if column_attributes.pk:
        col_string = f"<B>{col_string}</B>"
    if column_attributes.unique:
        col_string = f"<I>{col_string}</I>"
    attribute_str = f"{col_string} : {column_attributes.type}"

    enums_used = []
    if str(column_attributes.type).strip() in enums:
        enums_used += [str(column_attributes.type)]

    return attribute_str, enums_used


def generate_table_nodes(name: str, contents: pydbml.classes.Table, enums: list[str]) -> tuple[
    pydot.Node, list[pydot.Edge]]:
    debug(f"{name}: {contents}")

    attributes = []
    enums_used = []
    for column_name, column_attributes in contents.column_dict.items():
        attribute_str, enums_used_by_column = generate_column_node(column_name, column_attributes, enums)
        attributes += [attribute_str]
        enums_used += enums_used_by_column

    node: pydot.Node = pydot.Node(
        name,
        label=generate_table_label(name, attributes)
    )

    edges: list[pydot.Edge] = []
    for enum_used in enums_used:
        debug(f"{enum_used} is in enums")
        edges += [
            pydot.Edge(
                enum_used, name,
                style="invis"
            )
        ]

    return node, edges


def generate_graph_from_dbml(dbml: pydbml.PyDBML) -> pydot.Graph:
    graph = pydot.Graph()
    graph.set_node_defaults(fontname="Bitstream Vera Sans", fontsize=8, shape="none")
    graph.set_edge_defaults(fontname="Bitstream Vera Sans", fontsize=8, labeldistance=2, color="grey")
    graph.set_graph_defaults(rankdir='LR')
    enums = []
    for enum in dbml.enums:
        enum: pydbml.classes.Enum = enum

        graph.add_node(pydot.Node(
            enum.name,
            label=generate_table_label(f"<I>Enum</I><BR></BR>{enum.name}", enum.items)
        ))

        enums.append(enum.name.strip())

    debug(f"{enums=}")
    debug("Tables:", list(dbml.table_dict.keys()))

    for table_name, table_contents in dbml.table_dict.items():
        node, edges = generate_table_nodes(table_name, table_contents, enums)

        graph.add_node(node)
        for edge in edges:
            graph.add_edge(edge)

    for reference in dbml.refs:
        reference: pydbml.classes.Reference = reference

        orig = reference.col1.name
        dest = reference.col2.name

        label_len = (len(dest) + len(orig))

        if reference.table1.name == reference.table2.name:
            debug("Origin and destination are identical", reference.table1.name)
            for i in range(label_len // 8):
                graph.add_edge(pydot.Edge(reference.table1.name, reference.table2.name, style="invis"))
                # graph.

        graph.add_edge(pydot.Edge(
            reference.table1.name, reference.table2.name,
            headlabel=dest,
            taillabel=orig,
            xlabel=" " * label_len*2,
            minlen=int(math.sqrt(1+label_len/2))
            # xlabel=f"{reference.col1.name} {reference.type} {reference.col2.name}"
        ))

    # graph.set_simplify(True)
    graph.set_type("digraph")

    return graph
