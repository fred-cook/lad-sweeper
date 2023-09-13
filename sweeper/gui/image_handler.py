from pathlib import Path

from PIL import Image, ImageTk

class ImageHandler:
    """
    Handles the opening and sizing of the images needed
    for lad-sweeper

    The class can be used like a dictionary where values
    can only be read, not set.

    Images
    ------
    lad
    flag
    dead_lad
    lad_rear
    winning_lad
    """
    def __init__(self, size: int, filepath: Path=Path("assets/images/")):
        """
        Parameters
        ----------
        size: int
            The size the images should be in pixels
        filepath: Path
            Path to lad images folder
        """
        self.image_root = filepath
        self.raw_images = dict((path.stem, Image.open(path))
                               for path in self.image_root.iterdir())
        
        self.size = size #  Image size in pixels
        self.images: dict[str, ImageTk.PhotoImage]
        
    def __getitem__(self, key: str):
        return self.images[key]
    
    @property
    def size(self) -> int:
        return self._size
    
    @size.setter
    def size(self, value: int) -> None:
        """
        Set the new size value, and make sure all of the
        images are resized
        """
        self._size = value
        self.images = {key: ImageTk.PhotoImage(img.resize((value, value)))
                        for key, img in self.raw_images.items()}