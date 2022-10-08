# ------------------------- [ Main Project File | Coding: utf-8 ] ------------------------- #
# Project: AsciCam                                                                          #
# File: main.py                                                                             #
# Python Version: 3.10.2 - Tested: 3.10.2 - All others are untested.                        #
# The libraries should get installed among the integrated libraries: cv2, pillow            #
# ----------------------------------------- [ ! ] ----------------------------------------- #
# This code doesn't have any errors. if you got an error, check syntax and python version.  #
# ----------------------------------------- [ ! ] ----------------------------------------- #
# Author: nihadenes - <nihadenesvideo@gmail.com>                                            #
# Links: <https://github.com/nihadenes>                                                     #
# Date: 3/28/2022                                                                           #
# License: MIT License                                                                      #
# --------------------------------------- [ Enjoy ] --------------------------------------- #

import cv2, os
from PIL import Image


def setscreen(col, line):
    try:
        os.system(f'mode con: cols={col} lines={line}')
    except:
        print("Failed to set screen.")


def changeFontSize(size=2):  # Changes the font size to *size* pixels (Kind of, but not really.)
    from ctypes import POINTER, WinDLL, Structure, sizeof, byref
    from ctypes.wintypes import BOOL, SHORT, WCHAR, UINT, ULONG, DWORD, HANDLE

    LF_FACESIZE, STD_OUTPUT_HANDLE = 32, -11

    class COORD(Structure):
        _fields_ = [
            ("X", SHORT),
            ("Y", SHORT),
        ]

    class CONSOLE_FONT_INFOEX(Structure):
        _fields_ = [
            ("cbSize", ULONG),
            ("nFont", DWORD),
            ("dwFontSize", COORD),
            ("FontFamily", UINT),
            ("FontWeight", UINT),
            ("FaceName", WCHAR * LF_FACESIZE)
        ]

    kernel32_dll = WinDLL("kernel32.dll")

    get_last_error_func = kernel32_dll.GetLastError
    get_last_error_func.argtypes = []
    get_last_error_func.restype = DWORD

    get_std_handle_func = kernel32_dll.GetStdHandle
    get_std_handle_func.argtypes = [DWORD]
    get_std_handle_func.restype = HANDLE

    get_current_console_font_ex_func = kernel32_dll.GetCurrentConsoleFontEx
    get_current_console_font_ex_func.argtypes = [HANDLE, BOOL, POINTER(CONSOLE_FONT_INFOEX)]
    get_current_console_font_ex_func.restype = BOOL

    set_current_console_font_ex_func = kernel32_dll.SetCurrentConsoleFontEx
    set_current_console_font_ex_func.argtypes = [HANDLE, BOOL, POINTER(CONSOLE_FONT_INFOEX)]
    set_current_console_font_ex_func.restype = BOOL

    stdout = get_std_handle_func(STD_OUTPUT_HANDLE)
    font = CONSOLE_FONT_INFOEX()
    font.cbSize = sizeof(CONSOLE_FONT_INFOEX)

    font.dwFontSize.X = size
    font.dwFontSize.Y = size

    set_current_console_font_ex_func(stdout, False, byref(font))


def print_large_block(text):
    print("", end="\r")
    print(text, end="\r")


def get_ascii_from_image(im):
    global char_list, mirrored
    lines = []
    x_range = range(im.size[0])[::-1] if mirrored else range(im.size[0])
    for y in range(im.size[1]):
        line = []
        for x in x_range:
            pix = sum(im.getpixel((x, y))) / 3
            char_list_pos = int((len(char_list) - 1) * pix / 255)
            line.append(char_list[char_list_pos])
        lines.append(''.join(line))
    return ('\n' + ("\n" if fontsize != 1 else "")).join(lines)


def get_video_frms(path, format="cv2"):
    cap = cv2.VideoCapture(path, cv2.CAP_DSHOW)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == True:
            if format == 'PIL':
                yield cv2_to_PIL(frame)
            else:
                yield frame
        else:
            cap.release()
            cv2.destroyAllWindows()
            break


def cv2_to_PIL(frame):
    return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


def print_ascii_from_im(im):
    global horizontal, vertical, set_screen
    horizontal = int(vertical * 2 * im.size[0] / im.size[1])
    if set_screen == 0:
        set_screen = 1
        setscreen(horizontal, vertical * (2 if fontsize != 1 else 1))
    im = im.resize((horizontal, vertical))
    print_large_block(get_ascii_from_image(im) + '\n')


def main():
    [print_ascii_from_im(im) for im in get_video_frms(camera, 'PIL')]


if __name__ == '__main__':
    camera = 0
    mirrored = 1
    vertical = 100
    fontsize = 1  # 3 is buggy, so don't use 3.

    set_screen = 0     
    char_list = "".join([' ', '.', "'", ',', ':', ';', 'c', 'l', 'x', 'o', 'k', 'X', 'd', 'O', '0', 'K', 'N'])

    try:
        changeFontSize(size=fontsize)
    except:
        print("Failed to set font size.")

    main()
