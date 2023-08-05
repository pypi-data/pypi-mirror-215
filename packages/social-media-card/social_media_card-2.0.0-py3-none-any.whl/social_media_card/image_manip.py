"""Alter the image for LinkedIn, Facebook, and Twitter.

:author: Shay Hill
:created: 2022-11-10
"""

from pathlib import Path

from PIL import Image

from social_media_card.paths import FilePaths


def pad_image(
    image: Image.Image, left: int, top: int, right: int = 0, bottom: int = 0
) -> Image.Image:
    """Pad the image with the given values.

    :param image: the image to pad
    :param left: the number of pixels to add to the left
    :param top: the number of pixels to add to the top
    :param right: the number of pixels to add to the right, default 0
    :param bottom: the number of pixels to add to the bottom, default 0
    :return: the input image padded with transparency (if the input image has an
        alpha channel), else padded with white.
    """
    padded = Image.new(
        image.mode,
        (image.width + left + right, image.height + top + bottom),
        (255, 255, 255, 0),
    )
    padded.paste(image, (left, top))
    return padded


def _pad_to_landscape_aspect(image: Image.Image) -> Image.Image:
    """Pad a portrait image to a square. Do not alter landscape images.

    :param image: the image to pad
    :return: the input image padded to a square or horizontal rectangle

    LinkedIn will crop any image that is taller than it is wide. Pad images to they
    are at least square.
    """
    missing_width = round(image.height - image.width)
    if missing_width > 0:
        left = missing_width // 2
        right = missing_width - left
        return pad_image(image, left, 0, right, 0)
    return image


def _pad_to_twitter_aspect(image: Image.Image) -> Image.Image:
    """Pad the image to the Twitter aspect ratio. This is 2:1.

    :param image: the image to pad
    :return: the input image padded to the Twitter aspect ratio

    I don't have a Twitter account, so
    """
    missing_width = -round(image.width - image.height * 2)
    if missing_width > 0:
        left = missing_width // 2
        right = missing_width - left
        return pad_image(image, left, 0, right, 0)
    missing_height = round(image.height - image.width / 2)
    if missing_height > 0:
        top = missing_height // 2
        bottom = missing_height - top
        return pad_image(image, 0, top, 0, bottom)
    return image


def _add_banner_layer(image: Image.Image, banner: Image.Image) -> Image.Image:
    """Add the banner to the image.

    :param image: bottom layer
    :param banner: top layer with the same width as the image
    :return: the image with the banner pasted on top (mode = input image mode)

    The banner is added to the top of the image. Banner transparency is recognized
    even if the image argument does not have an alpha channel, but the output image
    will not have an alpha channel unless the input image has one. E.g., this will
    layer a transparent png over a jpg, and the output will be a jpg.
    """
    banner_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    banner_layer.paste(banner.convert("RGBA"))
    with_banner = Image.alpha_composite(image.convert("RGBA"), banner_layer)
    with_banner = with_banner.convert(image.mode)
    return with_banner


def get_image_with_banner(
    image_path: str | Path,
    banner_path: str | Path | None = None,
    banner_padding: int | None = None,
) -> Image.Image:
    """Return the image with the banner pasted on top.

    :param image_path: the path to the image
    :param banner_path: the path to the banner
    :param banner_padding: the number of pixels to pad the top of the image to make
        room for the banner
    :return: the image with the banner pasted on top

    If banner_path is None, return the image unmodified. If banner_padding is None,
    use the banner's height as the padding.
    """
    image = Image.open(image_path)
    if banner_path is None:
        return image

    banner = Image.open(banner_path)
    banner_scalar = image.width / banner.width
    banner_height = round(banner.height * banner_scalar)
    banner = banner.resize((image.width, banner_height))

    if banner_padding is None:
        image = pad_image(image, 0, banner_height)
    elif banner_padding:
        image = pad_image(image, 0, round(banner_padding * banner_scalar))

    return _add_banner_layer(image, banner)


def write_image_variants(image: Image.Image, paths: FilePaths) -> None:
    """Edit the base image for LinkedIn, Facebook, and Twitter. Write these to disk.

    :param image: the base image
    :param paths: the paths to the output files
    """
    linkedin_facebook_image = _pad_to_landscape_aspect(image)
    twitter_image = _pad_to_twitter_aspect(image)
    linkedin_facebook_image.save(paths.output_image_path)
    twitter_image.save(paths.output_image_path_twitter)
