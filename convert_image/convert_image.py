""""
Author：         xiejingjing
Date：           2021-7-13
Description：    converter image
Version：        1.0
公众号：          Python小作坊
个人博客：        isxjj.xyz
"""

import os
import glob

import tkinter
import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog

from PIL import Image, ImageDraw, ImageFont, ImageTk

pwd = os.getcwd()


class ImageConverter:
    def __init__(self, image, text, save_path, font_path, font_size=7):
        self.image = image
        self.font_size = font_size
        self.text = text
        self.save_path = save_path
        self.font_path = font_path

    def character_generator(self):
        while True:
            for i in range(len(self.text)):
                yield self.text[i]

    def run(self):
        global font
        img_array = self.image.load()

        img_new = Image.new("RGB", self.image.size, (0, 0, 0))
        draw = ImageDraw.Draw(img_new)

        try:
            font = ImageFont.truetype(self.font_path, self.font_size)
        except OSError:
            self.show_waring("无法转换该字体，目前我也不知道是什么原因QAQ")

        ch_factory = self.character_generator()

        for y in range(0, self.image.size[1], self.font_size):
            for x in range(0, self.image.size[0], self.font_size):
                draw.text((x, y), next(ch_factory), font=font, fill=img_array[x, y], direction=None)

        self.save_full_path = os.path.join(self.save_path, "result.jpeg")
        img_new.convert('RGB').save(self.save_full_path)

    def show_waring(self, message):
        tkinter.messagebox.showinfo(title='友情提示', message=message)

    def show_image(self):
        self.done_img = Image.open(self.save_full_path)
        self.done_img.show()


class Windows:
    def __init__(self, title, size):
        self.init_window(title, size)
        self.init_window_var()
        self.init_label()
        self.init_button()
        self.init_combox()
        self.init_canvas()

    def init_window(self, title, size):
        self.win = tkinter.Tk()
        self.win.title(title)
        self.win.geometry(size)
        self.win.iconbitmap(os.path.join(pwd, 'Python小作坊.ico'))

    def init_window_var(self):
        self.image_path_var = tkinter.StringVar()
        self.save_path_var = tkinter.StringVar(value=pwd)
        self.combox_var = tkinter.StringVar()

        self.image_path = ""
        self.font_path = "C:/Windows/fonts/Dengl.ttf"
        self.save_path = ""

    def init_button(self):
        button_pic = tkinter.Button(self.win, text="选择图片", command=self.chose_image)
        button_pic.place(x=20, y=70)

        button_save_path = tkinter.Button(self.win, text="保存路径", command=self.chose_save_path)
        button_save_path.place(x=20, y=120)

        button_font = tkinter.Button(self.win, text="选择字体")
        button_font.place(x=20, y=170)

        button_reset = tkinter.Button(self.win, text="开始制作", command=self.convert_pic)
        button_reset.place(x=50, y=240)
        button_reset = tkinter.Button(self.win, text="重新制作", command=self.reset_all_variable)
        button_reset.place(x=150, y=240)
        button_reset = tkinter.Button(self.win, text="放大预览", command=self.show_image)
        button_reset.place(x=250, y=240)
        button_reset = tkinter.Button(self.win, text="下载源码", command=self.download_source_code)
        button_reset.place(x=350, y=240)

    def init_label(self):
        file_path_label = tkinter.Label(self.win, textvariable=self.image_path_var, bg='white', font=('Arial', 8),
                                        width=50, height=1,
                                        anchor="w")
        font_path_label = tkinter.Label(self.win, textvariable=self.save_path_var, bg='white', font=('Arial', 8),
                                        width=50, height=1,
                                        anchor="w")

        weixin_label = tkinter.Label(self.win, text="作者：只会写BUG的老晶 \n微信公众号：Python小作坊", bg='gray', font=('Arial', 8),
                                     width=25, height=2, anchor="w")
        file_path_label.place(x=100, y=70)
        font_path_label.place(x=100, y=120)
        weixin_label.place(x=150, y=20)

    def init_combox(self):
        self.comboxlist = ttk.Combobox(self.win, textvariable=self.combox_var, state='readonly', width=40)
        self.comboxlist["values"] = glob.glob(r"C:\Windows\Fonts\*.*")
        self.comboxlist.set(r"C:\Windows\Fonts\Dengl.ttf")
        self.comboxlist.place(x=100, y=170)

    def init_canvas(self):
        # 预览图
        self.default_before_image_path = os.path.join(pwd, "before_bg.png")
        self.default_after_image_path = os.path.join(pwd, "after_bg.png")
        self.default_before_image = self.create_image_obj(self.default_before_image_path)
        self.default_after_image = self.create_image_obj(self.default_after_image_path)

        self.before_canvas = tkinter.Canvas(self.win, height=200, width=200)
        self.after_canvas = tkinter.Canvas(self.win, height=200, width=200)

        self.load_image(self.before_canvas, self.default_before_image)
        self.load_image(self.after_canvas, self.default_after_image)

        self.before_canvas.place(x=30, y=300)
        self.after_canvas.place(x=270, y=300)

    def load_image(self, canvas, image_obj):
        canvas.create_image(0, 0, image=image_obj, anchor="nw")

    def create_image_obj(self, image_path):
        image = Image.open(image_path)
        resized_image = image.resize((200, 200), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized_image)

    def chose_image(self):
        self.image_path = filedialog.askopenfilename(title='请选择你的图片', initialdir=pwd, filetypes=[(
            "jpg图片", ".jpg"), ("jpeg图片", ".jpeg")], defaultextension='.jpg', multiple=False)
        if not self.image_path:
            # 取消选择
            return

        self.image_path_var.set(self.image_path)

        default_save_path = os.path.split(self.image_path)[0]
        self.save_path_var.set(default_save_path)
        self.save_path = default_save_path

        self.before_image_obj = self.create_image_obj(self.image_path)
        self.load_image(self.before_canvas, self.before_image_obj)

    def chose_save_path(self):
        self.save_path = filedialog.askdirectory(title='请选择保存路径', initialdir=pwd)
        if not self.save_path:
            # 取消选择
            return

        self.save_path_var.set(self.save_path)

    def reset_all_variable(self):
        self.image_path_var.set("")
        self.save_path_var.set(pwd)

        self.image_path = ""
        self.save_path = ""

        self.load_image(self.before_canvas, self.default_before_image)
        self.load_image(self.after_canvas, self.default_after_image)

        self.comboxlist.set(r"C:\Windows\Fonts\Dengl.ttf")

        try:
            del self.ic
        except AttributeError:
            pass

    def show_warning(self, message):
        tkinter.messagebox.showwarning(title="FBI WARNING", message=message)

    def show_message(self, message):
        tkinter.messagebox.showinfo(title="友情提示", message=message)

    def convert_pic(self):
        if not self.image_path:
            self.show_warning("你个笨蛋，你还没选择原图片路径呢~")
            return

        image = Image.open(self.image_path)
        self.font_path = self.comboxlist.get()
        self.ic = ImageConverter(image=image, text="我喜欢你！", save_path=self.save_path, font_path=self.font_path)
        self.ic.run()

        self.after_image_obj = self.create_image_obj(self.ic.save_full_path)
        self.load_image(self.after_canvas, self.after_image_obj)

    def show_image(self):
        if not hasattr(self, "ic") or not os.path.exists(self.ic.save_full_path):
            self.show_warning("你个笨蛋，要先生成目标图片啊~")
            return

        self.ic.show_image()

    def download_source_code(self):
        self.show_message("微信搜索、关注公众号【Python小作坊】，回复 '源码' 即可下载。")

    def start(self):
        self.win.mainloop()


def main():
    window = Windows(title='图片转换器', size='500x550')
    window.start()


if __name__ == '__main__':
    main()
