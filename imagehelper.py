from tkinter import *
from PIL import Image, ImageTk, ImageOps
import os


class ImageHelper:
    @classmethod
    def slice(cls, img_path: str, destination: str, columns: int, rows: int = 1,transpose:bool=False):
        filename, file_extension = os.path.splitext(img_path)
        if not os.path.isfile(destination):
            os.mkdir(destination)
        im = Image.open(img_path)
        if transpose:
            im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        imgwidth, imgheight = im.size
        height = imgheight // rows
        width = imgwidth // columns

        if transpose:
            count = 0
            for row in range(rows -1,-1, -1):
                for col in range(columns-1,-1, -1):
                    box = (col * width, row * height, (col + 1) * width, (row + 1) * height)
                    a = im.crop(box)
                    a.save(destination + str(count) + file_extension)
                    count += 1
        else:
            count = 0
            for row in range(0, rows):
                for col in range(0, columns):
                    box = (col * width, row * height, (col + 1) * width, (row + 1) * height)
                    a = im.crop(box)
                    a.save(destination + str(count) + file_extension)
                    count += 1

    @classmethod
    def slice_to_list(cls, img_path: str, columns: int, rows: int = 1,
                      width:int=32,height:int=32,transpose: bool = False):
        images = []
        im = Image.open(img_path)
        if transpose:
            im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        imgwidth, imgheight = im.size
        frame_height = imgheight // rows
        frame_width = imgwidth // columns
        for row in range(0, rows):
            for col in range(0, columns):
                box = (col * frame_width, row * frame_height, (col + 1) * frame_width, (row + 1) * frame_height)
                a = im.crop(box)
                a = a.resize((width,height),Image.Resampling.LANCZOS)
                image = ImageTk.PhotoImage(a)
                if transpose:
                    images.insert(0, image)
                else:
                    images.append(image)
        return images

    @staticmethod
    def get_sized_image(image_file: str, width: int, height: int):
        img = Image.open(image_file)
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        return img

    @classmethod
    def get_sized_images(cls, image_files: list, width: int, height: int):
        images = []
        for image_name in image_files:
            image = cls.get_sized_image(image_name, width, height)
            images.append(image)
        return images

    @classmethod
    def get_sized_images_in_range(cls, file_path: str, start_number: int,
                                  end_number: int,
                                  extension: str,width: int, height: int):
        images = []
        for i in range(start_number, end_number + 1):
            image = cls.get_sized_image('{}/{}.{}'.format(file_path, i, extension), width, height)
            images.append(image)
        return images