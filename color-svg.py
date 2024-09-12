import json
import svgwrite

# Load the hex codes from the JSON file
with open('hexes.json', 'r') as file:
    data = json.load(file)

# Filter out entries without hex codes
filtered_data = {version: (name, hex_code) for version, (name, hex_code) in data.items() if hex_code}

# Define square size and image parameters
square_size = 200
spacing = 0
font_size = 20

# Calculate image dimensions
image_width = square_size * len(filtered_data) + spacing * (len(filtered_data) - 1)
image_height = square_size + 70

# Create an SVG drawing
dwg = svgwrite.Drawing('paccolors.svg', profile='tiny', size=(image_width, image_height))

# Draw each color square with text
for i, (version, (name, hex_code)) in enumerate(filtered_data.items()):
    x0 = i * (square_size + spacing)
    y0 = 0

    # Draw the color square
    dwg.add(dwg.rect(insert=(x0, y0), size=(square_size, square_size), fill=hex_code))

    # Add the version number
    version_position = (x0 + 5, y0 + square_size + 30)
    dwg.add(dwg.text(version, insert=version_position, fill="black", font_size=font_size, font_family="MesloLGS-NF-Regular"))

    # Add the name (below the version number)
    name_position = (x0 + 5, y0 + square_size + 30 + font_size + 5)  # Adjust position for the next line
    dwg.add(dwg.text(name, insert=name_position, fill="black", font_size=font_size, font_family="MesloLGS-NF-Regular"))

    # Add the hex code text
    hex_text_position = (x0 + 59, y0 + 108)
    dwg.add(dwg.text(hex_code, insert=hex_text_position, fill="black", font_size=font_size, font_family="MesloLGS-NF-Regular"))

# Save the SVG file
dwg.save()
