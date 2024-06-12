import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import SquareModuleDrawer, GappedSquareModuleDrawer, CircleModuleDrawer, RoundedModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
from PIL import Image, ImageDraw


def create_qr_code(data, module_drawer_index):
    # Get the right module_drawer the user asked for
    match module_drawer_index:
        case 1:
            module_drawer = SquareModuleDrawer()
        case 2:
            module_drawer = GappedSquareModuleDrawer()
        case 3:
            module_drawer = CircleModuleDrawer()
        case 4:
            module_drawer = RoundedModuleDrawer()
        case 5:
            module_drawer = VerticalBarsDrawer()
        case 6:
            module_drawer = HorizontalBarsDrawer()
        case _:
            module_drawer = SquareModuleDrawer()

    # Create the qr code
    qr = qrcode.QRCode(
        version=6,
        error_correction=qrcode.constants.ERROR_CORRECT_L)
    # Add the right data to qr
    qr.add_data(data)
    qr.make()
    # Create an image of the qr with rounded corners
    # We have to convert to RGB when embedding a color image in a black and white qr code
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=module_drawer).convert("RGB")
    return img


def create_embedded_image(image_path, qr):
    # Make the image so that it's the right size for the qr code
    size = 80
    image = Image.open(image_path)
    image_size = (size, size)
    image = image.resize(image_size, Image.Resampling.LANCZOS)
    # Get the right position for embedded image (middle of qr)
    pos = ((qr.size[0] - image.size[0]) // 2, (qr.size[1] - image.size[1]) // 2)
    qr.paste(image, pos)
    return qr


def create_square(qr):
    # Make the square just a little bigger then the image
    size = 90
    square_size = (size, size)
    # Get the right position for the square (middle of qr)
    pos = ((qr.size[0] - square_size[0]) // 2, (qr.size[1] - square_size[1]) // 2)
    draw = ImageDraw.Draw(qr)
    draw.rectangle(
        [pos, (pos[0] + square_size[0], pos[1] + square_size[1])],
        fill="white"
    )
    return qr


def generate_qr_code(data, image_path):
    module_drawer_index = 4
    qr = create_qr_code(data, module_drawer_index)
    if image_path:
        qr = create_square(qr)
        qr = create_embedded_image(image_path, qr)
    return qr
