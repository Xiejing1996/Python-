""""
Author：         xiejingjing
Date：           2021-7-14
Description：    converter(PNG2ico)
Version：        1.0
"""

import os

import tkinter
import tkinter.messagebox
from tkinter import ttk
from tkinter import filedialog

import PythonMagick

pwd = os.getcwd()


class ImageConverter:
    def __init__(self, image_path, save_path, image_size, image_result_name):
        self.image_path = image_path
        self.image_size = image_size
        self.save_path = save_path
        self.image_result_name = image_result_name

    def run(self):
        self.image = PythonMagick.Image(self.image_path)
        self.image.sample(self.image_size)  # 重新设置尺寸
        try:
            self.image.write(os.path.join(self.save_path, self.image_result_name + '.ico'))
            self.show_result("转换成功！")
        except:
            self.show_result("转换失败！")

    def show_result(self, message):
        tkinter.messagebox.showinfo(title='转换结果', message=message)


class Windows:
    def __init__(self, title, size):
        self.init_window(title, size)
        self.init_window_var()
        self.init_label()
        self.init_button()
        self.init_combox()

    def init_window(self, title, size):
        self.win = tkinter.Tk()
        self.win.title(title)
        self.win.geometry(size)
        self.win.resizable(0, 0)
        self.win.iconbitmap(os.path.join(pwd, 'Python小作坊.ico'))

    def init_window_var(self):
        self.image_path_var = tkinter.StringVar()
        self.save_path_var = tkinter.StringVar(value=pwd)
        self.combox_var = tkinter.StringVar()

        self.image_path = ""
        # self.save_path = ""

    def init_button(self):
        button_pic = tkinter.Button(self.win, text="选择图片", command=self.chose_image)
        button_pic.place(x=20, y=80)

        button_save_path = tkinter.Button(self.win, text="保存路径", command=self.chose_save_path)
        button_save_path.place(x=20, y=130)

        button_font = tkinter.Button(self.win, text="选择尺寸")
        button_font.place(x=20, y=180)

        button_reset = tkinter.Button(self.win, text="开始转换", command=self.convert_pic)
        button_reset.place(x=150, y=250)

        button_reset = tkinter.Button(self.win, text="下载源码", command=self.download_source_code)
        button_reset.place(x=250, y=250)

    def init_label(self):
        file_path_label = tkinter.Label(self.win, textvariable=self.image_path_var, bg='white', font=('Arial', 8),
                                        width=50, height=1,
                                        anchor="w")
        font_path_label = tkinter.Label(self.win, textvariable=self.save_path_var, bg='white', font=('Arial', 8),
                                        width=50, height=1,
                                        anchor="w")

        weixin_label = tkinter.Label(self.win, text="作者：只会写BUG的老晶 \n微信公众号：Python小作坊", bg='gray', font=('Arial', 8),
                                     width=24, height=2, anchor="w")
        file_path_label.place(x=110, y=85)
        font_path_label.place(x=110, y=135)
        weixin_label.place(x=180, y=20)

    def init_combox(self):
        self.comboxlist = ttk.Combobox(self.win, textvariable=self.combox_var, state='readonly', width=40)
        self.comboxlist["values"] = ["16x16", "32x32", "48x48", "64x64", "128x128"]
        self.comboxlist.set("64x64")
        self.comboxlist.place(x=110, y=185)

    def chose_image(self):
        self.image_path = filedialog.askopenfilename(title='请选择你的图片', initialdir=pwd, filetypes=[("png图片", ".png"), ("jpeg图片", ".jpeg"), ("bmp图片", ".bmp")],
                                                     defaultextension='.png', multiple=False)
        if not self.image_path:
            # 取消选择
            return

        self.image_path_var.set(self.image_path)

        default_save_path = os.path.split(self.image_path)[0]
        self.save_path_var.set(default_save_path)
        self.save_path = default_save_path

    def get_image_name(self):
        self.image_full_name = os.path.split(self.image_path)[1]
        self.image_result_name = self.image_full_name.split('.')[0]
        return self.image_result_name

    def chose_save_path(self):
        self.save_path = filedialog.askdirectory(title='请选择保存路径', initialdir=pwd)
        if not self.save_path:
            # 取消选择
            return

        self.save_path_var.set(self.save_path)

    def show_warning(self, message):
        tkinter.messagebox.showwarning(title="FBI WARNING", message=message)

    def show_message(self, message):
        tkinter.messagebox.showinfo(title="友情提示", message=message)

    def convert_pic(self):
        if not self.image_path:
            self.show_warning("你个笨蛋，你还没选择原图片路径呢~")
            return

        self.image_size = self.comboxlist.get()
        self.image_name = self.get_image_name()
        self.ic = ImageConverter(image_path=self.image_path, save_path=self.save_path, image_size=self.image_size,
                                 image_result_name=self.image_name)
        self.ic.run()

    def download_source_code(self):
        self.show_message("微信搜索、关注公众号【Python小作坊】，回复 '源码' 即可下载。")

    def start(self):
        self.win.mainloop()


def main():
    window = Windows(title='图片转换器', size='500x350')
    window.start()


if __name__ == '__main__':
    main()
