"""Fill HTML template for social media card.

:author: Shay Hill
:created: 2022-11-10
"""


from datetime import datetime
from string import Template

from PIL import Image

from social_media_card.paths import HTML_TEMPLATE, FilePaths


def write_social_media_card_html(
    author: str, title: str, description: str, url: str, paths: FilePaths
) -> None:
    """Write social media card HTML to file.

    :param author: author of the page
    :param title: title of the page
    :param description: description of the page
    :param url: URL to which the card will redirect
    :param paths: file paths to necessary local and remote files

    Mostly just fills in the html template in template.txt

    Does just a small bit of processing to measure the output_image dimensions.
    """
    image_width, image_height = Image.open(paths.output_image_path).size
    date = datetime.now().strftime("%Y-%m-%d")

    with HTML_TEMPLATE.open(encoding="utf-8") as f:
        template = Template("".join(f.readlines()))
    html = template.substitute(
        today=date,
        author=author,
        title=title,
        description=description,
        image_url=paths.image_url,
        image_url_twitter=paths.image_url_twitter,
        url=url,
        image_width=image_width,
        image_height=image_height,
    )
    with paths.output_html_path.open("w", encoding="utf-8") as file:
        _ = file.write(html)
