from textwrap import dedent

import pydbml
import pydbml.classes
import pathlib
import pydot
import argparse

DEBUG = False


def generate_table_label(name: str, attribute_list: list[str]):
    attribute_list_str: str = ""
    for attr in attribute_list:
        attribute_list_str += f""""<TR><TD align="left">{attr}</TD></TR>\n"""
    return dedent(
        f'''<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="1">
            <TR><TD><B>{name}</B></TD></TR><HR />
            {attribute_list_str}
        </TABLE>>
        '''
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="dbml2dot")
    parser.add_argument("-i", "--input", dest="input", help="Input file (.dbml)", type=str, required=True)
    parser.add_argument("-o", "--output", dest="output",
                        help="Output file (.dot), by default the input filename with .dot prefix",
                        default=None, required=False)
    parser.add_argument("-d", "--debug", dest="debug", help="Enable debug output", default=False, action="store_true")
    parser.add_argument("-T", "--type", dest="type",
                        help="Output file type for graphviz. If not specified, don't output anything",
                        default="none",
                        choices='bmp canon cmap cmapx cmapx_np dot dot_json eps fig gd gd2 gif gtk gv ico imap imap_np ismap jpe jpeg jpg json json0 mp pdf pic plain plain-ext png pov ps ps2 svg svgz tif tiff tk vdx vml vmlz vrml wbmp webp x11 xdot xdot1.2 xdot1.4 xdot_json xlib'.split(
                            ' '), action="store")

    args = parser.parse_args()

    input_path = pathlib.Path(args.input)

    output_path = None

    DEBUG = args.debug

    if args.output is None:
        output_path = input_path.with_suffix('.dot')
    else:
        output_path = pathlib.Path(args.output)

    with open(input_path, 'r') as f:
        input_data = f.read()

    dbml = pydbml.PyDBML(input_data)
    graph = pydot.Graph()
    graph.set_node_defaults(fontname="Bitstream Vera Sans", fontsize=8, shape="none")
    graph.set_edge_defaults(fontname="Bitstream Vera Sans", fontsize=8)

    enums = []
    for enum in dbml.enums:
        enum: pydbml.classes.Enum = enum

        graph.add_node(pydot.Node(
            enum.name,
            label=generate_table_label(enum.name, enum.items)
        ))

        enums.append(enum.name.strip())

    if DEBUG:
        print(f"{enums=}")

    if DEBUG:
        print("Tables:")
    for table_name, table_contents in dbml.table_dict.items():
        table_contents: pydbml.classes.Table
        if DEBUG:
            print(f"{table_name}: {table_contents}")

        attributes = []
        for column_name, column_attributes in table_contents.column_dict.items():
            column_attributes: pydbml.classes.Column = column_attributes
            not_null_string = "" if column_attributes.not_null or column_attributes.pk else "?"
            col_string = f"{column_name}{not_null_string}"
            if column_attributes.pk:
                col_string = f"<B>{col_string}</B>"
            if column_attributes.unique:
                col_string = f"<I>{col_string}</I>"

            attribute_str = f"{col_string} : {column_attributes.type}"
            attributes += [attribute_str]

            if str(column_attributes.type).strip() in enums:
                if DEBUG:
                    print(f"{column_attributes.type} is in enums")
                graph.add_edge(pydot.Edge(
                    str(column_attributes.type), table_name,
                    style="invis"
                ))

        label = generate_table_label(table_name, attributes)
        graph.add_node(pydot.Node(
            table_name,
            label=label
        ))

    for reference in dbml.refs:
        reference: pydbml.classes.Reference = reference

        graph.add_edge(pydot.Edge(
            reference.table1.name, reference.table2.name,
            label=f"{reference.col1.name} {reference.type} {reference.col2.name}"
        ))

    with open(output_path, "w") as f:
        f.write(graph.to_string())

    graph.set_simplify(True)
    graph.set_type("digraph")

    if args.type != "none":
        from subprocess import check_call

        check_call(['dot', f'-T{args.type}', output_path.absolute(), '-o', output_path.with_suffix('.svg').absolute()])

    if DEBUG:
        print(f"Input: {input_path}, Output: {output_path}")
