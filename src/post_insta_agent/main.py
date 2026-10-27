
from PIL import Image, ImageDraw, ImageFont

# Load image
image = Image.open("./input_image/input_img.png").convert("RGB")
draw = ImageDraw.Draw(image)

# Input: 10-30 words
while True:
    text = input("Enter text (10-30 words): ").strip()
    word_count = len(text.split())

    if 10 <= word_count <= 30:
        break

    print(f"Enter 10-30 words. Current count: {word_count}")

# Font
font_path = "Mukta-ExtraBold.ttf"
font_size = 55
font = ImageFont.truetype(font_path, font_size)

# Text area for 1248x1248 sunset image
left, top = 100, 180
right, bottom = 1150, 800

max_width = right - left
line_spacing = 75

# Text wrapping
lines = []
current_line = ""

for word in text.split():
    test_line = f"{current_line} {word}".strip()

    if draw.textbbox((0, 0), test_line, font=font)[2] <= max_width:
        current_line = test_line
    else:
        if current_line:
            lines.append(current_line)
        current_line = word

if current_line:
    lines.append(current_line)

# Check whether all text fits
if len(lines) * line_spacing > bottom - top:
    print("Text is too large. Reduce font_size or line_spacing.")
else:
    # Draw text
    y = top

    for line in lines:
        draw.text(
            (left, y),
            line,
            font=font,
            fill=(255, 255, 255),
            stroke_width=2,
            stroke_fill=(40, 30, 20)
        )
        y += line_spacing

    image.save("./output_image/written_page.jpg")
    print("Image saved as written_page.jpg")
