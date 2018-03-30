import numpy as np

try:
    from PIL import Image as pil_image
except ImportError:
    pil_image = None


def preprocess_input(x):
    x /= 255.  # normalization
    return x


def custom_load_img_padding(path, grayscale=False, target_size=None):
    # print 'custom load img', path
    """Loads an image into PIL format.

        # Arguments
            path: Path to image file
            grayscale: Boolean, whether to load the image as grayscale.
            target_size: Either `None` (default to original size)
                or tuple of ints `(img_height, img_width)`.

        # Returns
            A PIL Image instance.

        # Raises
            ImportError: if PIL is not available.
        """
    if pil_image is None:
        raise ImportError('Could not import PIL.Image. '
                          'The use of `array_to_img` requires PIL.')
    img = pil_image.open(path)
    if grayscale:
        if img.mode != 'L':
            img = img.convert('L')
    else:
        if img.mode != 'RGB':
            img = img.convert('RGB')
    if target_size:
        img = custom_padding(img, target_size)

    return img


def custom_padding(img, target_size):
    wh_tuple = (target_size[1], target_size[0])
    if img.size != wh_tuple:
        if target_size[1] == target_size[0]:
            # img = scale(img, target_size)
            max_size = 0
            if img.size[0] > img.size[1]:
                max_size = img.size[0]
            else:
                max_size = img.size[1]

            wh_tuple2 = [max_size, max_size]

            back = pil_image.new("RGB", wh_tuple2, (0, 0, 0))
            offset = (int((wh_tuple2[0] - img.size[0]) / 2), int((wh_tuple2[1] - img.size[1]) / 2))
            back.paste(img, offset)

            img = back.resize(wh_tuple)

        else:
            img = img.resize(wh_tuple)

    return img


def custom_load_img_random_crop(path, grayscale=False, target_size=None):
    # print 'custom load img', path
    """Loads an image into PIL format.

        # Arguments
            path: Path to image file
            grayscale: Boolean, whether to load the image as grayscale.
            target_size: Either `None` (default to original size)
                or tuple of ints `(img_height, img_width)`.

        # Returns
            A PIL Image instance.

        # Raises
            ImportError: if PIL is not available.
        """
    if pil_image is None:
        raise ImportError('Could not import PIL.Image. '
                          'The use of `array_to_img` requires PIL.')
    img = pil_image.open(path)
    if grayscale:
        if img.mode != 'L':
            img = img.convert('L')
    else:
        if img.mode != 'RGB':
            img = img.convert('RGB')
    if target_size:
        wh_tuple = (target_size[1], target_size[0])
        if img.size != wh_tuple:
            img = custom_radom_crop(img, target_size)
           

    return img


def custom_radom_crop(img, target_size):
    if target_size[1] == target_size[0]:
        # img = scale(img, target_size)
        # max_size = 0
        diff = abs(img.size[0] - img.size[1])
        random_shift = np.random.rand(1) * diff
        if img.size[0] > img.size[1]:
            crop_img = img.crop((random_shift, 0, (img.size[1] + random_shift), img.size[1]))
        else:
            crop_img = img.crop((0, random_shift, img.size[0], (img.size[0] + random_shift)))

        img = crop_img.resize(target_size)
    else:
        img = img.resize(target_size)
    return img