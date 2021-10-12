class BmpFileHeader:
    type = 0
    size = 0
    reserved1 = 0
    reserved2 = 0
    off_bits = 0


class BmpImageHeader:
    header_size = 0
    width = 0
    height = 0
    planes = 0
    bit_count = 0
    compression = 0
    size_of_image = 0
    xpm = 0
    ypm = 0
    clr_used = 0
    clr_imp = 0
    red_mask = 0
    green_mask = 0
    blue_mask = 0
    alpha_mask = 0
    cs_type = 0
    cie = [0] * 9
    gamma = [0] * 3


class Bmp:
    file = BmpFileHeader()
    image = BmpImageHeader()


def write_bmp_file(buffer, width, height, file_name, palette):
    print("write_bmp_file: Not yet implemented!")
