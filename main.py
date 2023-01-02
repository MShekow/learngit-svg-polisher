"""
Fixes SVGs exported by the add-on https://github.com/felixfbecker/svg-screenshots
Specifically:
- Remove surrounding clutter (including the blue background) -> the final SVG has a transparent background
- Change color from white to black for the edge-borders and node-text-labels

Run "pip3 install beautifulsoup4 lxml" before running this script.
"""

from pathlib import Path

from bs4 import BeautifulSoup, Tag


def extract_real_graph(svg_root: Tag, actual_graph: Tag):
    svg_root.insert(0, actual_graph)
    for child in svg_root.children:
        keep = False
        try:
            if child.name == "g" and child.attrs["class"][0] == "svg-content":
                keep = True
        except:
            pass

        if not keep:
            child.extract()


def fix_colors(svg_root: Tag):
    for tag_name in ["circle", "path", "rect"]:
        for node in svg_root.find_all(tag_name):
            node.attrs["stroke"] = "rgb(0, 0, 0)"

    for text in svg_root.find_all("tspan"):
        text.attrs["fill"] = "rgb(0, 0, 0)"

    # Fix arrow-tips
    for arrow in svg_root.find_all("path"):
        if arrow.attrs["fill"] == "rgb(51, 51, 51)":
            arrow.attrs["fill"] = "rgb(0, 0, 0)"


def save_to_file(svg_root: Tag, file_name: str) -> None:
    f = Path(".") / file_name
    f.write_text(str(svg_root).replace("viewbox", "viewBox"), encoding="utf-8")


if __name__ == '__main__':
    # tree = ET.parse('index.svg')
    # root = tree.getroot()
    f = Path(".") / "index.svg"
    with f.open() as fp:
        content = f.read_text(encoding="utf-8")
        b = BeautifulSoup(content, "lxml")

    actual_graph = b.find("g", {"class": "svg-content"})

    svg_root = b.find("svg")

    while len(svg_root.contents) > 1:
        extract_real_graph(svg_root, actual_graph)

    fix_colors(svg_root)

    save_to_file(svg_root, "out.svg")
