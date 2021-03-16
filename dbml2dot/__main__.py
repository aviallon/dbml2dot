import pydbml.classes
import pathlib
import argparse

from dbml2dot.generators import generate_graph_from_dbml
from dbml2dot.utils import debug, set_debug

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

    set_debug(args.debug)

    if args.output is None:
        output_path = input_path.with_suffix('.dot')
    else:
        output_path = pathlib.Path(args.output)

    with open(input_path, 'r') as f:
        input_data = f.read()

    dbml = pydbml.PyDBML(input_data)
    graph = generate_graph_from_dbml(dbml)

    with open(output_path, "w") as f:
        f.write(graph.to_string())

    if args.type != "none":
        from subprocess import check_call

        check_call(['dot', f'-T{args.type}', output_path.absolute(), '-o', output_path.with_suffix('.svg').absolute()])

    debug(f"Input: {input_path}, Output: {output_path}")
