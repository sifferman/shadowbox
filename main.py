import xml.etree.ElementTree as ET


def cm2pt(pt):
    if isinstance(pt, str) and pt.endswith("cm"):
        pt = float(pt[:-2])
    return pt / 0.0352777778
def pt2cm(pt):
    if isinstance(pt, str) and pt.endswith("pt"):
        pt = float(pt[:-2])
    return pt * 0.0352777778

def get_svg_dimensions(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    if root.tag == '{http://www.w3.org/2000/svg}svg':
        # Extract width and height attributes
        width_str = root.get('width', '')
        height_str = root.get('height', '')

        width_pt = None
        height_pt = None

        if width_str.endswith("pt"):
            width_pt = float(width_str[:-2])
        elif width_str.endswith("cm"):
            width_pt = cm2pt(width_str)
        if height_str.endswith("pt"):
            height_pt = float(height_str[:-2])
        elif height_str.endswith("cm"):
            height_pt = cm2pt(height_str)

        return width_pt, height_pt
    else:
        return None, None

CANVAS_WIDTH = cm2pt(33)
CANVAS_HEIGHT = cm2pt(38.862)

WIDTH_BETWEEN = {}
HEIGHT_BETWEEN = {}


# def create_image(x, y, svg_path):
#     width, height = get_svg_dimensions(svg_path)
#     return f''' <image x="{x}" y="{y}" width="{width}" height="{height}" href="{svg_path}"/>'''

def create_image(x, y, svg_path):
    width, height = get_svg_dimensions(svg_path)
    svg_contents = ""

    with open(svg_path, "r") as f:
        embedded_content = f.read()
        tree = ET.ElementTree(ET.fromstring(embedded_content))
        root = tree.getroot()

        # Extract only <g> elements from the SVG file
        for child in root:
            if child.tag.endswith("g"):
                svg_contents += ET.tostring(child).decode()

    return f'''<svg x="{x}" y="{y}" width="{width}" height="{height}">
{svg_contents}
</svg>
'''


def set_constraints():
    width_gb, height_gb = get_svg_dimensions("cut-templates/gb-cartridge.svg")
    width_gba, height_gba = get_svg_dimensions("cut-templates/gba-cartridge.svg")
    width_ngbc, height_ngbc = get_svg_dimensions("cut-templates/gbc-console.svg")
    width_ngba, height_ngba = get_svg_dimensions("cut-templates/gba-console.svg")

    WIDTH_BETWEEN["wall-gen1"] = 65
    WIDTH_BETWEEN["gen1-gen1"] = (CANVAS_WIDTH - 2*WIDTH_BETWEEN["wall-gen1"] - 4*width_gb) / 3
    WIDTH_BETWEEN["gen2-ngbc"] = (CANVAS_WIDTH - WIDTH_BETWEEN["wall-gen1"] - 3*width_gb - 2*WIDTH_BETWEEN["gen1-gen1"] - width_ngbc) / 2
    WIDTH_BETWEEN["gen3-gen3"] = 0.65*width_gba
    WIDTH_BETWEEN["wall-gen3"] = WIDTH_BETWEEN["wall-gen1"] + width_gb + WIDTH_BETWEEN["gen1-gen1"] + width_gb/2 - WIDTH_BETWEEN["gen3-gen3"] / 2 - width_gba
    WIDTH_BETWEEN["gen3-ngba"] = (CANVAS_WIDTH - WIDTH_BETWEEN["wall-gen3"] - 2*width_gb - WIDTH_BETWEEN["gen3-gen3"] - width_ngba) / 2
    WIDTH_BETWEEN["wall-emrd"] = WIDTH_BETWEEN["wall-gen3"] + (width_gba+WIDTH_BETWEEN["gen3-gen3"]) / 2
    HEIGHT_BETWEEN["ctop-gen1"] = 80
    HEIGHT_BETWEEN["gen1-ngbc"] = (CANVAS_HEIGHT - HEIGHT_BETWEEN["ctop-gen1"] - height_gb - height_ngbc - height_ngba) / 3
    HEIGHT_BETWEEN["gen1-gen2"] = 1.2*HEIGHT_BETWEEN["gen1-ngbc"]
    HEIGHT_BETWEEN["ngbc-ngba"] = HEIGHT_BETWEEN["gen1-ngbc"]
    HEIGHT_BETWEEN["gen2-gen3"] = HEIGHT_BETWEEN["gen1-gen2"]
    HEIGHT_BETWEEN["gen3-gen3"] = (CANVAS_HEIGHT - 2*HEIGHT_BETWEEN["ctop-gen1"] - 2*height_gb - 2*HEIGHT_BETWEEN["gen1-gen2"] - 3*height_gba) / 2

def generate_svg_from_constraints():
    # Initialize SVG XML content
    svg_xml = f'''<?xml version="1.0" encoding="utf-8" ?>
<svg baseProfile="full" height="{CANVAS_HEIGHT}" version="1.1" width="{CANVAS_WIDTH}" xmlns="http://www.w3.org/2000/svg" xmlns:ev="http://www.w3.org/2001/xml-events" xmlns:xlink="http://www.w3.org/1999/xlink">
<defs />
<rect width="100%" height="100%" fill="black"/>
'''

    width_gb, height_gb = get_svg_dimensions("cut-templates/gb-cartridge.svg")
    width_gba, height_gba = get_svg_dimensions("cut-templates/gba-cartridge.svg")
    width_ngbc, height_ngbc = get_svg_dimensions("cut-templates/gbc-console.svg")

    # green
    svg_xml += create_image(
        WIDTH_BETWEEN["wall-gen1"],
        HEIGHT_BETWEEN["ctop-gen1"],
        "cut-templates/gb-cartridge.svg"
    )
    # blue
    svg_xml += create_image(
        WIDTH_BETWEEN["wall-gen1"] + 1*(width_gb+WIDTH_BETWEEN["gen1-gen1"]),
        HEIGHT_BETWEEN["ctop-gen1"],
        "cut-templates/gb-cartridge.svg"
    )
    # red
    svg_xml += create_image(
        WIDTH_BETWEEN["wall-gen1"] + 2*(width_gb+WIDTH_BETWEEN["gen1-gen1"]),
        HEIGHT_BETWEEN["ctop-gen1"],
        "cut-templates/gb-cartridge.svg"
    )
    # yellow
    svg_xml += create_image(
        WIDTH_BETWEEN["wall-gen1"] + 3*(width_gb+WIDTH_BETWEEN["gen1-gen1"]),
        HEIGHT_BETWEEN["ctop-gen1"],
        "cut-templates/gb-cartridge.svg"
    )

    # gold
    svg_xml += create_image(
        WIDTH_BETWEEN["wall-gen1"],
        HEIGHT_BETWEEN["ctop-gen1"] + height_gb+HEIGHT_BETWEEN["gen1-gen2"],
        "cut-templates/gb-cartridge.svg"
    )
    # silver
    svg_xml += create_image(
        WIDTH_BETWEEN["wall-gen1"] + 1*(width_gb+WIDTH_BETWEEN["gen1-gen1"]),
        HEIGHT_BETWEEN["ctop-gen1"] + height_gb+HEIGHT_BETWEEN["gen1-gen2"],
        "cut-templates/gb-cartridge.svg"
    )
    # crystal
    svg_xml += create_image(
        WIDTH_BETWEEN["wall-gen1"] + 2*(width_gb+WIDTH_BETWEEN["gen1-gen1"]),
        HEIGHT_BETWEEN["ctop-gen1"] + height_gb+HEIGHT_BETWEEN["gen1-gen2"],
        "cut-templates/gb-cartridge.svg"
    )

    # ruby
    svg_xml += create_image(
        WIDTH_BETWEEN["wall-gen3"],
        HEIGHT_BETWEEN["ctop-gen1"]+height_gb + HEIGHT_BETWEEN["gen1-gen2"]+height_gb + HEIGHT_BETWEEN["gen2-gen3"],
        "cut-templates/gba-cartridge.svg"
    )
    # sapphire
    svg_xml += create_image(
        WIDTH_BETWEEN["wall-gen3"] + 1*(width_gba+WIDTH_BETWEEN["gen3-gen3"]),
        HEIGHT_BETWEEN["ctop-gen1"]+height_gb + HEIGHT_BETWEEN["gen1-gen2"]+height_gb + HEIGHT_BETWEEN["gen2-gen3"],
        "cut-templates/gba-cartridge.svg"
    )
    # emerald
    svg_xml += create_image(
        WIDTH_BETWEEN["wall-emrd"],
        HEIGHT_BETWEEN["ctop-gen1"]+height_gb + HEIGHT_BETWEEN["gen1-gen2"]+height_gb + HEIGHT_BETWEEN["gen2-gen3"] + 1*(HEIGHT_BETWEEN["gen3-gen3"]+height_gba),
        "cut-templates/gba-cartridge.svg"
    )
    # firered
    svg_xml += create_image(
        WIDTH_BETWEEN["wall-gen3"],
        HEIGHT_BETWEEN["ctop-gen1"]+height_gb + HEIGHT_BETWEEN["gen1-gen2"]+height_gb + HEIGHT_BETWEEN["gen2-gen3"] + 2*(HEIGHT_BETWEEN["gen3-gen3"]+height_gba),
        "cut-templates/gba-cartridge.svg"
    )
    # leafgreen
    svg_xml += create_image(
        WIDTH_BETWEEN["wall-gen3"] + 1*(width_gba+WIDTH_BETWEEN["gen3-gen3"]),
        HEIGHT_BETWEEN["ctop-gen1"]+height_gb + HEIGHT_BETWEEN["gen1-gen2"]+height_gb + HEIGHT_BETWEEN["gen2-gen3"] + 2*(HEIGHT_BETWEEN["gen3-gen3"]+height_gba),
        "cut-templates/gba-cartridge.svg"
    )

    # gbc
    svg_xml += create_image(
        WIDTH_BETWEEN["wall-gen1"] + 2*(width_gb+WIDTH_BETWEEN["gen1-gen1"]) + width_gb + WIDTH_BETWEEN["gen2-ngbc"],
        HEIGHT_BETWEEN["ctop-gen1"] + height_gb + HEIGHT_BETWEEN["gen1-ngbc"],
        "cut-templates/gbc-console.svg"
    )
    # gba
    svg_xml += create_image(
        WIDTH_BETWEEN["wall-gen3"] + width_gba+WIDTH_BETWEEN["gen3-gen3"] + width_gba + WIDTH_BETWEEN["gen3-ngba"],
        HEIGHT_BETWEEN["ctop-gen1"]+height_gb + HEIGHT_BETWEEN["gen1-ngbc"] + height_ngbc + HEIGHT_BETWEEN["ngbc-ngba"],
        "cut-templates/gba-console.svg"
    )

    # Close SVG tag
    svg_xml += '''</svg>'''

    return svg_xml

if __name__=='__main__':
    set_constraints()
    print(generate_svg_from_constraints())
    with open("output.svg", "w") as f:
        f.write(generate_svg_from_constraints())
