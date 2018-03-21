import wx
import os
import datetime
import shutil
import importlib
from data.tools import *
from data.data_cache import *
import traceback

class MainFrame:
    select_file = False
    aim_path = "C:\\Users\\StarveZhou\\Desktop\\GitHub\\StockTrain\\usr\\"


    def __init__(self):
        self.app = wx.App()
        self.frame = wx.Frame(None, title = 'stock train', size=(1000, 400),style=wx.DEFAULT_FRAME_STYLE)
        self.frame.Maximize(True)
        (self.w, self.h) = self.frame.GetSize()
        print(self.w, self.h)
        self.panel = wx.Panel(self.frame)
        self.panel.SetBackgroundColour("#242424")
        self.get_default_image()

        self.main_panel()

        self.set_menu()
        self.frame.Centre()

        self.frame.Show(True)
        self.app.MainLoop()

    def set_icon(self):
        self.icon = wx.Icon("C:\\Users\\StarveZhou\\Desktop\\GitHub\\StockTrain\\gui\\exit.ico", wx.BITMAP_TYPE_ICO)
        self.frame.SetIcon(self.icon)


    def set_menu(self):
        self.menu_bar = wx.MenuBar()
        self.menu_bar.SetForegroundColour("#242424")
        self.file_menu = wx.Menu()
        filem = self.file_menu.Append(wx.ID_EXIT, "退出", "退出仿真程序")
        
        self.menu_bar.Append(self.file_menu, "&系统")
        self.frame.SetMenuBar(self.menu_bar)

        self.frame.Bind(wx.EVT_MENU, self.on_quit, filem)

    def main_panel(self):
        self.v_box_main = wx.BoxSizer(wx.VERTICAL)
        self.h_box_title = wx.BoxSizer(wx.HORIZONTAL)
        self.h_box_content = wx.BoxSizer(wx.HORIZONTAL)
        self.v_box_left = wx.BoxSizer(wx.VERTICAL)
        self.v_box_right = wx.BoxSizer(wx.VERTICAL)

        self.set_title_box()
        self.set_left_box()
        self.set_right_box()

        self.h_box_content.Add(self.v_box_left, flag=wx.EXPAND | wx.LEFT | wx.TOP | wx.BOTTOM, border=5, proportion=1)
        self.h_box_content.Add(self.v_box_right, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5, proportion=2)
        
        self.v_box_main.Add(self.h_box_title, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=5, proportion=1)
        self.v_box_main.Add(self.h_box_content, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=5, proportion=7)
        
        self.panel.SetSizer(self.v_box_main)

        

    def set_title_box(self):
        self.file_path_text = wx.StaticText(self.panel, label='Nothing', size=(100, 30), style=wx.ALIGN_CENTER)
        self.file_path_text.SetBackgroundColour("#242424")
        self.file_path_text.SetForegroundColour("White")
        font = wx.Font(13, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Consolas")
        self.file_path_text.SetFont(font)
        self.h_box_title.Add(self.file_path_text, flag=wx.RIGHT, border=10, proportion=7)
        
        self.h_box_title.Add((10, -1))

        select_file_button = wx.Button(self.panel, label='选择文件', size=(30, 30))
        select_file_button.SetBackgroundColour("#242424")
        select_file_button.SetForegroundColour("White")
        self.frame.Bind(wx.EVT_BUTTON, self.select_file_button_on_button, select_file_button)
        self.h_box_title.Add(select_file_button, flag=wx.LEFT, border=10, proportion=1)
        
        self.h_box_title.Add((10, -1))

        run_button = wx.Button(self.panel, label='运行策略', size=(30, 30))
        run_button.SetBackgroundColour("#242424")
        run_button.SetForegroundColour("White")
        self.frame.Bind(wx.EVT_BUTTON, self.run_button_on_button, run_button)
        self.h_box_title.Add(run_button, flag=wx.LEFT, border=10, proportion=1)
    
    def set_left_box(self):
        code_label = wx.StaticText(self.panel, label="策略代码", size=(400, 20), style=wx.ALIGN_CENTER)
        code_label.SetForegroundColour("White")
        code_label.SetBackgroundColour("#242424")
        label_font = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Roman")
        code_label.SetFont(label_font)
        self.v_box_left.Add(code_label, flag=wx.ALL, border=0)

        self.code_box = wx.TextCtrl(self.panel, -1, value="请先选择策略文件\n", size=(400, 440), style=wx.TE_READONLY | wx.TE_LEFT | wx.TE_MULTILINE)
        self.code_box.SetForegroundColour("White")
        self.code_box.SetBackgroundColour("#232323")
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Consolas")
        self.code_box.SetFont(font)
        self.v_box_left.Add(self.code_box, flag=wx.ALL, border=5)

        log_label = wx.StaticText(self.panel, label="日志", size=(400, 20), style=wx.ALIGN_CENTER)
        log_label.SetForegroundColour("White")
        log_label.SetBackgroundColour("#242424")
        log_label.SetFont(label_font)
        self.v_box_left.Add(log_label, flag=wx.ALL, border=0)

        self.log_box = wx.TextCtrl(self.panel, -1, value="请先选择策略文件\n", size=(400, 180), style=wx.TE_READONLY | wx.TE_LEFT | wx.TE_MULTILINE)
        self.log_box.SetForegroundColour("White")
        self.log_box.SetBackgroundColour("#232323")
        self.log_box.SetFont(font)
        self.v_box_left.Add(self.log_box, flag=wx.ALL, border=5)

    def set_right_box(self):
        main_label = wx.StaticText(self.panel, label="主回测曲线", size=(self.right_box_width, 20), style=wx.ALIGN_CENTER)
        main_label.SetForegroundColour("White")
        main_label.SetBackgroundColour("#242424")
        label_font = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Roman")
        main_label.SetFont(label_font)
        self.v_box_right.Add(main_label, flag=wx.ALL, border=2)

        self.main_panel = wx.Panel(self.panel)

        main_image = wx.StaticBitmap(self.main_panel, bitmap=self.default_image)
        self.v_box_right.Add(self.main_panel, border=5, flag=wx.ALIGN_CENTER)

        self.v_box_right.Add((20, 1))
        
        record_label = wx.StaticText(self.panel, label="记录曲线", size=(self.right_box_width, 20), style=wx.ALIGN_CENTER)
        record_label.SetForegroundColour("White")
        record_label.SetBackgroundColour("#242424")
        record_label.SetFont(label_font)
        self.v_box_right.Add(record_label, flag=wx.ALL, border=2)

        self.record_panel = wx.Panel(self.panel)

        record_image = wx.StaticBitmap(self.record_panel, bitmap=self.default_image)
        self.v_box_right.Add(self.record_panel,border=5, flag=wx.ALIGN_CENTER)
        
        self.v_box_right.Add((20, 1))

        result_label = wx.StaticText(self.panel, label="回测结果", size=(self.right_box_width, 20), style=wx.ALIGN_CENTER)
        result_label.SetForegroundColour("White")
        result_label.SetBackgroundColour("#242424")
        result_label.SetFont(label_font)
        self.v_box_right.Add(result_label, flag=wx.ALL, border=2)
        
        
        self.result_box = wx.TextCtrl(self.panel, -1, value="请先执行策略\n", size=(self.right_box_width, 180), style=wx.TE_READONLY | wx.TE_LEFT | wx.TE_MULTILINE)
        self.result_box.SetForegroundColour("White")
        self.result_box.SetBackgroundColour("#232323")
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Consolas")
        self.result_box.SetFont(font)
        self.v_box_right.Add(self.result_box, flag=wx.ALL, border=2)
        

    def on_quit(self, e):
        self.frame.Close()

    def select_file_button_on_button(self, e):
        dlg = wx.FileDialog(self.frame, u"选择文件", style=wx.DEFAULT_DIALOG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.file_path = dlg.GetPath()
            self.file_path_text.SetLabel(self.file_path)
            self.refresh_code_box(self.file_path)
            # print("File : " + dlg.GetPath())
            self.log_box.Clear()
            self.append_log("read file from " + self.file_path)
            self.select_file = True
        dlg.Destroy()

    def refresh_code_box(self, file_path):
        file_path = file_path.replace('\\', '\\\\')
        # print(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            code_text = f.read()
            # print(code_text)
            self.code_box.SetValue(code_text)
            f.close()

    def get_default_image(self):
        file_path = "C:\\Users\\StarveZhou\\Desktop\\GitHub\\StockTrain\\log\\default.png"
        image = wx.Bitmap(self.read_image(file_path))
        w = image.GetWidth(); h = image.GetHeight()
        image = image.ConvertToImage().Scale(w/4.7, h/4.7)
        self.right_box_width = image.GetWidth()+40
        self.default_image = image.ConvertToBitmap()
        
    def show_image(self):
        file_path = "C:\\Users\\StarveZhou\\Desktop\\GitHub\\StockTrain\\log\\main.png"
        image = wx.Bitmap(self.read_image(file_path))
        w = image.GetWidth(); h = image.GetHeight()
        image = image.ConvertToImage().Scale(w/2, h/2)
        image = image.ConvertToBitmap()
        self.main_panel.DestroyChildren()
        main_image = wx.StaticBitmap(self.main_panel, bitmap=image)
        
        file_path = "C:\\Users\\StarveZhou\\Desktop\\GitHub\\StockTrain\\log\\record.png"
        image = wx.Bitmap(self.read_image(file_path))
        w = image.GetWidth(); h = image.GetHeight()
        image = image.ConvertToImage().Scale(w/2, h/2)
        image = image.ConvertToBitmap()
        self.record_panel.DestroyChildren()
        record_image = wx.StaticBitmap(self.record_panel, bitmap=image)


    def read_image(self, file_path):
        image = wx.Image(file_path, wx.BITMAP_TYPE_PNG)
        return image

    def set_result_box(self, text):
        self.result_box.SetLabel(text)

    def run_button_on_button(self, e):
        if self.select_file == False:
            self.append_log(self.get_time() + "请先选择回测文件")
            return
        
        self.usr_file_name = "aim-" + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        shutil.copyfile(self.file_path, self.aim_path + self.usr_file_name + ".py")
        self.append_log(self.get_time() + "文件拷贝至目标文件夹")
        self.append_log(self.get_time() + "filename:" + self.usr_file_name + ".py")

        
        
        try:
            import st
            from inspect import isfunction
            import draw
            import StockTrain

            st.log_aim = self
            self.append_log(self.get_time() + "import 相关文件成功")

            aim = importlib.import_module('usr.' + self.usr_file_name)

            self.append_log(self.get_time() + "import 策略文件成功")

            check_cache_in_memory()
            info = st.get_info()

            st.set_date()

            meet_end = False

            aim.initialize(st.context)
            # info.today = info.start_date
            

            info.earning = {}
            info.benchmark_earning = {}
            benchmark_data = get_data(code=info.benchmark, start_date=info.start_date, end_date=info.end_date)
            benchmark_cost = -1
            benchmark_cost_last = -1

            self.append_log(self.get_time() + "回测环境初始化成功")
            self.append_log(self.get_time() + "开始回测")

            while True:
                if meet_end == True:
                    self.append_log(self.get_time() + "回测结束")
                    break         
                st.context.update_info()
                self.append_log(self.get_time() + "开始回测 DAY : " + info.today)
                aim.trade(st.context)
                self.append_log(self.get_time() + "回测完成 DAY : " + info.today)

                info.earning[info.today] = st.context.calculate()
                if info.today == info.start_date:
                    info.benchmark_earning[info.today] = info.original_cash
                    benchmark_cost_last = info.original_cash
                elif benchmark_data[benchmark_data.date == info.today].empty is False:
                    if benchmark_cost is -1:
                        benchmark_cost = float(benchmark_data[benchmark_data.date == info.today]['open'])
                    info.benchmark_earning[info.today] = info.original_cash * float(benchmark_data[benchmark_data.date == info.today]['open']) / benchmark_cost
                    benchmark_cost_last = info.benchmark_earning[info.today]
                else:
                    info.benchmark_earning[info.today] = benchmark_cost_last

                
                if info.today == info.end_date:
                    meet_end = True
                info.today = date_tool(info.today, 1)
            # print(info.str())
            self.set_result_box(info.get_result_box())
            #st.log_aim = None
            StockTrain.generate_file(info)
            #StockTrain.run()
            self.append_log(self.get_time() + "曲线图生成完成")
            self.show_image()
            self.append_log(self.get_time() + "图片加载完成")

        except Exception:
            self.append_log(self.get_time() + "回测失败")
            self.append_log(self.get_time() + "%s" % traceback.print_exc())
            
            

    def get_time(self):
        return "[" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "]"

    def append_log(self, text):
        self.log_box.AppendText(text + "\n")
        self.log_box.ShowPosition(self.log_box.GetLastPosition())