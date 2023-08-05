"""Paths to local files and directories and remote file urls.

:author: Shay Hill
:created: 2022-11-10
"""

import dataclasses
from pathlib import Path
from urllib.parse import urljoin

PROJECT = Path(__file__, "..", "..").resolve()
HTML_TEMPLATE = PROJECT / "social_media_card" / "resources" / "template.html"


def _twitterize_filename(filename: str | Path) -> str:
    """Return an image filename for Twitter."""
    stem = Path(filename).stem
    suffix = Path(filename).suffix
    return f"{stem}_twitter{suffix}"


@dataclasses.dataclass
class FilePaths:
    """Paths to output files and image host urls.

    :param filename: The name of the input image file. The card itself and all images
        will be variations of this name.
    :param remote_image_url: The directory where the output images will be hosted.
    """

    image_filename: str
    remote_image_dir: str
    _output_image_dir: str | Path
    _output_html_dir: str | Path | None = None
    output_image_dir: Path = dataclasses.field(init=False)
    output_html_dir: Path = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        """Create output directories."""
        self.output_image_dir = Path(self._output_image_dir)
        self.output_image_dir.mkdir(parents=True, exist_ok=True)
        if self._output_html_dir is None:
            self.output_html_dir = self.output_image_dir
        else:
            self.output_html_dir = Path(self._output_html_dir)
            self.output_html_dir.mkdir(parents=True, exist_ok=True)

    @property
    def _stem(self) -> str:
        """Return the stem of the image filename."""
        return Path(self.image_filename).stem

    @property
    def _twitter_image_filename(self) -> str:
        """Return the filename for Twitter images."""
        return _twitterize_filename(self.image_filename)

    @property
    def output_image_path(self) -> Path:
        """Return the path to the output image for LinkedIn / Facebook cards."""
        return self.output_image_dir / self.image_filename

    @property
    def output_image_path_twitter(self) -> Path:
        """Return the path to the output image for Twitter cards."""
        return self.output_image_dir / self._twitter_image_filename

    @property
    def output_html_path(self) -> Path:
        """Return the path to the output HTML file."""
        return self.output_html_dir / f"{self._stem}.html"

    @property
    def image_url(self) -> str:
        """Return the image url for LinkedIn / Facebook cards."""
        return urljoin(self.remote_image_dir, self.image_filename)

    @property
    def image_url_twitter(self) -> str:
        """Return the image url for Twitter cards."""
        return urljoin(self.remote_image_dir, self._twitter_image_filename)
