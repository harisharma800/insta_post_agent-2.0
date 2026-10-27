
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def text_to_image(input_text):
    # Validate input
    text = input_text.strip()
    word_count = len(text.split())

    if not 10 <= word_count <= 30:
        raise ValueError(
            f"Text must contain 10-30 words. Current: {word_count}"
        )

    # Project root
    project_root = Path(__file__).resolve().parents[2]

    # Image paths
    input_image_path = (
        project_root / "src" / "post_insta_agent"
        / "input_image" / "input_img.png"
    )

    output_image_path = (
        project_root / "src" / "post_insta_agent"
        / "output_image" / "written_page.jpg"
    )

    # Check image
    if not input_image_path.exists():
        raise FileNotFoundError(f"Image not found: {input_image_path}")

    # Find Mukta font automatically
    font_files = list(project_root.rglob("Mukta-ExtraBold.ttf"))

    if not font_files:
        raise FileNotFoundError(
            "Mukta-ExtraBold.ttf not found in project folder."
        )

    font_path = font_files[0]

    # Load image and font
    image = Image.open(input_image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    font_size = 55
    font = ImageFont.truetype(str(font_path), font_size)

    # Text area
    width, height = image.size
    left = int(width * 0.08)
    top = int(height * 0.15)
    right = int(width * 0.92)
    bottom = int(height * 0.70)

    max_width = right - left
    line_spacing = int(font_size * 1.35)

    # Wrap text
    lines = []
    current_line = ""

    for word in text.split():
        test_line = f"{current_line} {word}".strip()

        text_width = draw.textbbox(
            (0, 0), test_line, font=font
        )[2]

        if text_width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    # Check height
    if len(lines) * line_spacing > bottom - top:
        raise ValueError(
            "Text does not fit. Reduce font_size or line_spacing."
        )

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

    # Save image
    output_image_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_image_path)

    return output_image_path
