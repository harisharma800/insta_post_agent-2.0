import text_to_image
from model import get_google_output
quote_text=get_google_output("quote of upse")
text_to_image.text_to_image(quote_text)