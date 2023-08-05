"""Write clickable images adn HTML for social media cards.

See example usage in example_create_card.py.

:author: Shay Hill
:created: 2022-11-09
"""

from pathlib import Path

from social_media_card.html_template import write_social_media_card_html
from social_media_card.image_manip import (
    get_image_with_banner,
    pad_image,
    write_image_variants,
)
from social_media_card.paths import FilePaths


def write_social_media_card(
    author: str,
    title: str,
    description: str,
    url: str,
    remote_image_dir: str,
    local_image_path: str | Path,
    output_image_dir: str | Path,
    output_html_dir: str | Path,
    banner_path: str | Path | None = None,
    banner_padding: int | None = None,
    padding: int = 0,
) -> None:
    """Write the social media card to the output directories.

    :param author: The author of the page.
    :param title: The title of the page.
    :param description: The description of the page. Try to make this around 200
        characters to avoid warnings.
    :param url: The url to which the card will link.
    :param remote_image_dir: The directory on the remote server where the images will
        be hosted online. E.g. `https://example.com/images/`.
    :param local_image_path: The path to the image on the local machine.
    :param output_image_dir: output images will be written here
    :param output_html_dir: (optional) output html will be written here. If not
        given, output_image_dir will be used. The flexibility is here for those who
        like to keep binaries (output images) and text files (output html) separate.

    :param banner_path: The path to an optional banner image. This will be added on
        top of the input image.
    :param banner_padding: The padding to apply to the banner image. This is the
        number of pixels to add to the top of the image before pasting the banner. If
        not provided, the banner height will be used. Use something other that the
        banner height if you have transparency in your banner and would like to see
        some of the image through it.
    :param padding: Optional minimum padding around the image. This padding is added
        *after* any banner is applied. I often use screenshots of my website. In
        order to crop exactly around the images (this looks best with the banner), I
        have to crop exactly at the text margin, which can look a bit crowded.

    :effects:
        - writes two images to OUTPUT_IMAGES: one for LinkedIn and one for Twitter
        - writes a file to OUTPUT_HTML: the HTML file for the card
    """
    image_name = Path(local_image_path).name
    paths = FilePaths(image_name, remote_image_dir, output_image_dir, output_html_dir)
    image = get_image_with_banner(local_image_path, banner_path, banner_padding)
    if padding:
        image = pad_image(image, padding, padding, padding, padding)
    write_image_variants(image, paths)
    write_social_media_card_html(author, title, description, url, paths)
