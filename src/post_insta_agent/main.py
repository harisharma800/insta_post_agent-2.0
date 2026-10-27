from .model import get_google_output
from .text_to_image import text_to_image
from .instagram_connection import publish_image
from .cloudinary_upload import upload_image


def main():
    # Step 1: Generate quote
    quote = get_google_output("Motivation for UPSC aspirants")
    print("Generated quote:", quote)

    # Step 2: Create image with quote
    image_path = text_to_image(quote)
    print("Image saved:", image_path)

    # Step 3: Upload image to Cloudinary
    image_url = upload_image(str(image_path))
    print("Uploaded image URL:", image_url)

    # Step 4: Publish on Instagram
    result = publish_image(
        image_url=image_url,
        caption=f"{quote}\n\n#Motivation #UPSC #Success"
    )

    print("Instagram publishing result:", result)


if __name__ == "__main__":
    main()