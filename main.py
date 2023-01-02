"""
Fixes SVGs exported by the add-on https://github.com/felixfbecker/svg-screenshots
Specifically:
- Remove surrounding clutter (including the blue background) -> the final SVG has a transparent background
- Change color from white to black for the edge-borders and node-text-labels

Run "pip3 install beautifulsoup4 lxml" before running this script.
"""
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup, Tag, NavigableString


def is_graph(tag: Tag) -> bool:
    try:
        return tag.name == "g" and tag.attrs["class"][0] == "svg-content"
    except:
        return False


def has_non_graph_children(svg_root: Tag) -> bool:
    for child in svg_root.children:
        if not is_graph(child) and type(child) != NavigableString:
            return True
    return False


def extract_real_graph(svg_root: Tag, actual_graphs: List[Tag]):
    for g in actual_graphs:
        svg_root.insert(0, g)

    # Remove all other tags that we don't need, e.g. "style" tags
    while has_non_graph_children(svg_root):
        # For unknown reasons, BeautifulSoup4 sometimes does not properly extract (=remove) all objects on the
        # first try
        for child in svg_root.children:
            if not is_graph(child):
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

    actual_graphs = b.find_all("g", {"class": "svg-content"})

    svg_root = b.find("svg")

    extract_real_graph(svg_root, actual_graphs)

    fix_colors(svg_root)

    save_to_file(svg_root, "out.svg")
