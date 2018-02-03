# -*- coding: utf-8 -*-
import time, sys

# 判断python的版本然后import对应的模块
if sys.version < '3':
    from Tkinter import *
else:
    from tkinter import *

mydelaymin = 30  # 窗口提示的延迟时间，以分钟计


# ------------------def-------------------
def showMessage(msg):
    # show reminder message window
    root = Tk()  # 建立根窗口
    root.minsize(500, 200)   #定义窗口的大小
    root.maxsize(1000, 400)  #不过定义窗口这个功能我没有使用
    #root.withdraw()  # hide window
    # 获取屏幕的宽度和高度，并且在高度上考虑到底部的任务栏，为了是弹出的窗口在屏幕中间
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight() - 100
    root.resizable(False, False)
    # 添加组件
    root.title("Lucky!!")
    frame = Frame(root, relief=RIDGE, borderwidth=3)
    frame.pack(fill=BOTH, expand=1)  # pack() 放置组件若没有则组件不会显示
    # 窗口显示的文字、并设置字体、字号
    label = Label(frame, text=msg, font="Monotype\ Corsiva -20 bold")
    label.pack(fill=BOTH, expand=1)
    # 按钮的设置
    button = Button(frame, text="OK", font="Cooper -15 bold", fg="red", command=root.destroy)
    button.pack(side=BOTTOM)

    #root.update_idletasks()
    #root.deiconify()  # now the window size was calculated
    #root.withdraw()  # hide the window again 防止窗口出现被拖动的感觉 具体原理未知？
    #root.geometry('%sx%s+%s+%s' % (root.winfo_width() + 10, root.winfo_height() + 10,
    #                               (screenwidth - root.winfo_width()) / 2, (screenheight - root.winfo_height()) / 2))
    #root.deiconify()
    root.mainloop()

def main(argv):
    showMessage(argv[1])

if __name__ == '__main__':
    main(sys.argv)
'''
while True:
    #time.sleep(mydelaymin * 60)  # 参数为秒
    #time.sleep(mydelaymin * 60)  # 参数为秒
    showMessage()
    exit(0)
'''