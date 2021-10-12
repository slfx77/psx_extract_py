import traceback
import os
import struct
import sys
import png

from os import SEEK_SET
from bmp import write_bmp_file
from moser import bruijn


class Mem:
    unk = [0]
    add1 = [0] * 3  # v19
    buffer = 0
    add2 = [0] * 2


class PSXPVR:
    unk = [0] * 2
    width = 0
    height = 0
    palette = 0
    size = 0


class Color:
    r = 0
    g = 0
    b = 0
    a = 0


def get_add1(reader):
    # loc_4C9BAF
    reader.seek(4)

    add1 = struct.unpack("<I", reader.read(4))[0]

    if(add1 == 0xFFFFFFFF):
        return True

    # loc_4C9BBF
    new_add = add1
    while new_add != 0xFFFFFFFF:
        reader.seek(add1 + 4, SEEK_SET)
        new_add = struct.unpack("<I", reader.read(4))[0]

        add1 += new_add + 8

        reader.seek(add1, SEEK_SET)
        new_add = struct.unpack("<I", reader.read(4))[0]

    add1 += 4
    return add1


def get_v13(reader):
    reader.seek(8, SEEK_SET)
    v13 = struct.unpack("<I", reader.read(4))[0]
    reader.seek((9 * v13 + 3) * 4, SEEK_SET)
    return v13


def get_v101(reader, mem, v13):
    reader.seek((v13 * 4) + mem.add1[0], SEEK_SET)
    return struct.unpack("<I", reader.read(4))[0]


def get_v35(v13, v101, v34):
    return v34 + ((v13 + v101) * 4 + 8)


def get_num_textures(reader, v41):
    reader.seek(v41, SEEK_SET)
    return struct.unpack("<I", reader.read(4))[0]


def get_textures_add(reader, num_textures):
    tmp = 0
    for i in range(num_textures):
        tmp = struct.unpack("<I", reader.read(4))[0]
        print("{}: {}\n", i + 1, hex(tmp))


def get_v31(reader, cur_texture, v30):
    color_offset = 0
    reader.seek(((cur_texture + 0x800) + v30), SEEK_SET)
    color_offset = struct.unpack("<B", reader.read(1))[0]

    read = Color()
    reader.seek(cur_texture + 8 * color_offset, SEEK_SET)
    read.r = struct.unpack("<H", reader.read(2))[0]
    read.g = struct.unpack("<H", reader.read(2))[0]
    read.b = struct.unpack("<H", reader.read(2))[0]
    read.a = struct.unpack("<H", reader.read(2))[0]

    return read


def decompress_texture(reader, pvr):
    print("decompress_texture: Not yet implemented!")


def extract_texture(reader, cur_texture):
    texture_off = struct.unpack("<I", reader.read(4))[0]

    # save current offset
    current_off = reader.tell()

    pvr = PSXPVR()
    reader.seek(texture_off, SEEK_SET)
    pvr.unk[0] = struct.unpack("<B", reader.read(1))[0]
    pvr.unk[1] = struct.unpack("<B", reader.read(1))[0]
    pvr.width = struct.unpack("<H", reader.read(2))[0]
    pvr.height = struct.unpack("<H", reader.read(2))[0]
    pvr.palette = struct.unpack("<I", reader.read(4))[0]
    pvr.size = struct.unpack("<I", reader.read(4))[0]

    # skip unsupported textures
    # if((pvr.palette & 0xFF00) != 0x300):
    #     print("Not implement yet{}.\n".format(hex(pvr.palette)))
    #     return False

    decompressed = decompress_texture(reader, pvr)
    write_bmp_file(decompressed, pvr.width, pvr.height, texture_off + 0x1C, pvr.palette)
    reader.seek(current_off, SEEK_SET)


def main(directory, filename):
    input_file = os.path.join(directory, filename)
    mem = Mem()
    v13 = 0
    v35 = 0
    v37 = 0
    v41 = 0
    v101 = 0
    pad_hex = 8
    num_textures = 0

    with open(input_file, "rb") as input:
        mem.add1[0] = get_add1(input)
        v13 = get_v13(input)
        v101 = get_v101(input, mem, v13)
        v35 = get_v35(v13, v101, mem.add1[0] - 4)

        v37 = v35 + 4
        v41 = v37 + 4

        num_textures = get_num_textures(input, v41)

        print(f"ADD1: {mem.add1[0]:0{pad_hex}X} {mem.add1[1]:0{pad_hex}X} {mem.add1[2]:0{pad_hex}X}")
        print(f"v13:  {v13:0{pad_hex}X} v101: {v101:0{pad_hex}X} v35: {v35:0{pad_hex}X}\nv41:  {v41:0{pad_hex}X}")
        print("There are {} textures.\n".format(num_textures))

        for i in range(num_textures):
            extract_texture(input, i)
