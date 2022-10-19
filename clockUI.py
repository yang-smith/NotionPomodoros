from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import notionAPI
from PIL import Image
import asyncio


async def update(baseDict, name):
    print(baseDict[name])
    notionAPI.updateTomato(baseDict[name])

class App:
    def __init__(self, root):
        self.root = root
        w = 300 #窗口宽
        h = 200 #窗口高
        x = 0 #窗口右下角x轴位置
        y = 40 #窗口右下角y轴位置
        self.root.geometry("%dx%d-%d-%d" % (w, h, x, y))
        self.root.attributes('-topmost',True)
        self.root.title("test")
        self.root.attributes("-alpha", 0.7)
        self.root.overrideredirect(True)
        self.frm = ttk.Frame(self.root, padding=10)
        self.frm.grid()
        self.varstring = StringVar()
        #self.varstring.set("test init")
        #self.label = ttk.Label(self.frm, textvariable=self.varstring).grid(column=1, row=0)
        self.button = ttk.Button(self.frm, text="Quit", command=self.root.destroy, width=4).grid(column=0, row=0)
        self.button = ttk.Button(self.frm, text="Init", command=self.init, width=4).grid(column=0, row=1)

        self.data = notionAPI.readDatabase()
        self.baseDict = notionAPI.cleanData(self.data)
        self.setButton()
        self.root.mainloop()

    def click(self, name):
        print("click"+name)
        self.baseDict[name]['done'] += '🍅'
        self.baseDict[name]['total'] += 1
        asyncio.run(update(self.baseDict, name))
        self.root.destroy()
        root = Tk()
        Tomato(root, color='red', time=25)
 

    def setButton(self):
        locate = 0
        self.buttons = []
        for i in self.baseDict:
            locate += 1
            settext = i + self.baseDict[i]['done']
            self.buttons.append(ttk.Button(self.frm, text=settext, command=lambda name=i: self.click(name))) 
            self.buttons[locate-1].grid(column=3, row=locate)

    def init(self):
        locate = 0
        for i in self.baseDict:
            if self.baseDict[i]['done'] != '':
                self.baseDict[i]['done'] = ''
                self.buttons[locate].config(text= i)
                asyncio.run(update(self.baseDict, i))
            locate += 1
            

class Tomato:
    
    def __init__(self, root, color, time):
        self.root = root

        if color == 'red':
            imgpath = "tomato.gif"
            self.color = 'red'
        elif color == 'green':
            imgpath = "tomato-green.gif"
            self.color = 'green'
        else:
            imgpath = "tomato.gif"
            print('color wrong!!!')
        imgsize=Image.open(imgpath,mode='r')
        w,h=imgsize.size
        self.root.geometry(str(w)+'x'+str(h)+'-0'+'-40')
        global tomatoImg
        tomatoImg = PhotoImage(file=imgpath)

        self.clock = time
        self.clockvar = StringVar()
        self.clockvar.set(str(self.clock))
        img_back = Label(self.root, image = tomatoImg, textvariable=self.clockvar, compound = CENTER, fg = "white")
        img_back.image=tomatoImg
        img_back.place(x=0,y=0,relwidth=1,relheight=1)

        img_back.bind('<Double-Button-1>',self.try_close)#设置矩形区域内点击关闭
        img_back['bg']='#f0f0f1'#一般窗口为'#f0f0f0'，为了方便使用，改为'#f0f0f1'
        self.root.attributes('-transparent','#f0f0f1')
        self.root.overrideredirect(True)
        self.img_back=img_back
        self.img_back.after(60000, self.updateTime)
        self.root.attributes('-topmost',True)
        self.root.mainloop()

    def try_close(self,event):
        self.root.destroy()

    def updateTime(self):
        self.root.attributes('-topmost',True)
        self.img_back.after(60000, self.updateTime)
        self.clock -= 1
        if self.clock <= 0:
            self.root.destroy()
            if self.color == 'red':
                root = Tk()
                Tomato(root, color='green', time=5)
                return
            else:
                root = Tk()
                App(root)
                return
            
        self.clockvar.set(str(self.clock))




    