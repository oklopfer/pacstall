import json
from PIL import Image, ImageDraw, ImageFont

# Load the hex codes from the JSON file
with open('hexes.json', 'r') as file:
    data = json.load(file)

# Filter out entries without hex codes
filtered_data = {version: (name, hex_code) for version, (name, hex_code) in data.items() if hex_code}

# Define square size and image parameters
square_size = 200
spacing = 0
font_size = 20
font = ImageFont.truetype("MesloLGS-NF-Regular.ttf", 20)

# Calculate image dimensions
image_width = square_size * len(filtered_data) + spacing * (len(filtered_data) - 1)
image_height = square_size + 70

# Create the image
image = Image.new('RGB', (image_width, image_height), 'white')
draw = ImageDraw.Draw(image)

# Draw each color square with text
for i, (version, (name, hex_code)) in enumerate(filtered_data.items()):
    x0 = i * (square_size + spacing)
    y0 = 0
    x1 = x0 + square_size
    y1 = y0 + square_size

    # Draw the color square
    draw.rectangle([x0, y0, x1, y1], fill=hex_code)

    # Add the version number and name text
    text_position = (x0 + 5, y1 + 10)
    draw.text(text_position, f"{version}\n{name}", fill="black", font=font)

    text_position = (x0 + 59, y0 + 88)
    draw.text(text_position, f"{hex_code}", fill="black", font=font)

# Show or save the image
image.show()  # To display the image
image.save('paccolors.png')  # To save the image
