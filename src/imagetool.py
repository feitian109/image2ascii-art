from PIL import Image


class ImageTool:
    """A collection of image tool. Including image preprocess."""

    @staticmethod
    def preprocess(
        image: Image.Image,
        max_length: int | None = 128,
        resample: int = Image.Resampling.NEAREST,
    ) -> Image.Image:
        """
        Image will be converted into `grayscale` mode. Then its size will be limit to `max_length`.

        :param image: Image needed to preprocess.
        :param max_length: Output image's max length will be resized to this number.
                           `None` means output image's size will not be limited.
        :param resample: Resize resample method (Default is `NEAREST`):

                         * `Image.Resampling.NEAREST`
                         * `Image.Resampling.LANCZOS`
                         * `Image.Resampling.BILINEAR`
                         * `Image.Resampling.BICUBIC`
                         * `Image.Resampling.BOX`
                         * `Image.Resampling.HAMMING`
        """

        # convert color mode to gray-scale
        if image.mode != "L":
            image = image.convert("L")
            print("Convert to grayscale mode")

        # resize image
        print(f"Original size: {image.width}x{image.height}")

        if max_length is not None:
            if max_length <= 0:
                msg = "`max_length` must bigger than 0"
                raise ValueError(msg)

            if max(image.width, image.height) > max_length:
                # W / w = H / h
                if image.width >= image.height:
                    target_width = max_length
                    target_height = int(image.height / image.width * max_length)
                else:
                    target_height = max_length
                    target_width = int(image.width / image.height * max_length)

                image = image.resize((target_width, target_height), resample=resample)
                print(f"Resized size: {image.width}x{image.height}")
        return image
