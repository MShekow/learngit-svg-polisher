# LearnGit SVG exporter

This simple Python script fixes some issues of SVGs exported by the Firefox
add-on [svg-screenshots](https://github.com/felixfbecker/svg-screenshots) that you make on Git trees generated
on https://learngitbranching.js.org/

The problem is that the SVG produced by the add-on has some errors.

The concrete fixes are:

- Remove surrounding clutter (including the blue background) -> the final SVG has a transparent background
- Change color from white to black for the edge-borders and node-text-labels

## Examples

| Input   |      Cleaned output      |
|----------|:-------------:|
|![](bad_input.svg) |  ![](processed_output.svg) |

## Usage

Run `pip3 install beautifulsoup4 lxml` (preferrably in a virtual-env!) before running the `main.py` script.
