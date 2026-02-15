import json
from wx.core import EVT_MENU, EVT_BUTTON
import wx
from wx.lib.agw.buttonpanel import BoxSizer


DEL_TASK = 58

class Data:
    def __init__(self):

        self.kanban_cols = []  # [(name, address)()()()()()()]
        self.kanban_cols_seps = {}  # [(name, address)()()()()()()]
        self.kanban_cols_tasks = {}  # {coll_name:[task_text,...]}  
        #self.to_do_tasks = set()
        self.to_do_tasks = {}  #name:address

    def add_col(self,name, address):
        self.kanban_cols.append((name,address))

    def del_col(self, name):
        self.kanban_cols = [t for t in data.kanban_cols if t[0] != name]
        if name in self.kanban_cols_tasks.keys():
            self.kanban_cols_tasks.pop(name)



    def get_col_address(self, col_name):
        for c_n, p in self.kanban_cols:
            if c_n == col_name:
                panel = p
                return panel
        return None
    #def get_task_address(self, task_text):
    def get_col_index(self, col_name):
        i = 0
        for c_n, p in self.kanban_cols:
            if c_n == col_name:
                return i
            i += 1
        return None

    def del_task(self, task_txet):
        pass

    #def get_col_address()   #get col address buy givven name
        #pass
data = Data()


class MyMenuBar(wx.MenuBar):
    def __init__(self):
        super().__init__()
        self.col_menu_items = {}

        fileMenu = wx.Menu()
        self.delMenu = wx.Menu()
        statisticsMenu = wx.Menu()


        fileMenu.Append(wx.ID_NEW, "&New column\tCtrl+N")

        # fileMenu.Append(wx.ID_OPEN, "&Открить\tCtrl+O")
        # fileMenu.AppendSeparator()

        self.Append(fileMenu, "&File")
        self.Append(self.delMenu, "Delete")
        self.Append(statisticsMenu, "Statistics")

    def add_to_del_menu(self, col_name):
        item = self.delMenu.Append(wx.ID_ANY, col_name)
        self.col_menu_items[col_name] = item
        frame = self.GetTopLevelParent()

        if isinstance(frame, MyFrame):
            frame.Bind(wx.EVT_MENU, lambda event, name=col_name:
            frame.panel_kanban.remove_col_from_kanban(name), item)

    def remove_from_del_menu(self, col_name):
        item = self.col_menu_items.pop(col_name, None)
        if item:
            self.delMenu.Remove(item.GetId())

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, pos=(0,0), size=(1000, 600))

        tabs = wx.Notebook(self, id=wx.ID_ANY)

        panel_day = wx.Panel(tabs, name="Day panel")
        panel_week = wx.Panel(tabs)

        panel_chekbox = ToDoList(tabs)
        self.panel_kanban = KanBanPanel(tabs)


        self.menubar = MyMenuBar()
        self.SetMenuBar(self.menubar)

        self.Bind(wx.EVT_MENU, self.panel_kanban.add_col_to_kanban_user, id=wx.ID_NEW)


        tabs.InsertPage(0, panel_day, "Day")
        tabs.InsertPage(1, panel_week, "Week")
        tabs.InsertPage(2, panel_chekbox, "Checkbox")
        tabs.InsertPage(3, self.panel_kanban, "Kanban", select=True)

        self.Bind(wx.EVT_CLOSE, on_close)

class KanBanPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.hbox_kanban = wx.BoxSizer(wx.HORIZONTAL)

        self.SetSizer(self.hbox_kanban)



    def add_col_to_kanban(self, col_name):  #self, e
        if not data.get_col_address(col_name) and len(data.kanban_cols) < 10:

            panel = KanbanColumn(self,col_name)

            if len(data.kanban_cols) != 0:
                line = wx.StaticLine(self, style=wx.LI_VERTICAL)
                self.hbox_kanban.Add(line, 0, wx.EXPAND | wx.ALL, 3) #5
                data.kanban_cols_seps[col_name] = line
            self.hbox_kanban.Add(panel, 1, wx.EXPAND | wx.ALL, 2) #5
            data.add_col(col_name, panel)
            data.kanban_cols_tasks[col_name] = []
            self.GetTopLevelParent().menubar.add_to_del_menu(col_name)
            self.GetTopLevelParent().panel_kanban.Layout()
            return panel

    def add_col_to_kanban_user(self, e):
        dlg = wx.TextEntryDialog(self, "Type the name of column", "Add new column to kanban", "New")
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            col_name = dlg.GetValue()
            self.add_col_to_kanban(col_name)
        dlg.Destroy()


    def remove_col_from_kanban(self, col_name):
        panel = data.get_col_address(col_name)
        print(data.get_col_address)
        print(data.kanban_cols_seps)
        print(data.get_col_index(col_name))
        if data.get_col_index(col_name) == 0 and len(data.kanban_cols) > 1:
            next_col = next(iter(data.kanban_cols_seps.keys()))
            line = data.kanban_cols_seps[next_col]
            print(next_col, "next col")
            self.hbox_kanban.Detach(line)
            line.Destroy()
            del data.kanban_cols_seps[next_col]
        if panel:
            self.GetTopLevelParent().menubar.remove_from_del_menu(col_name)
            self.hbox_kanban.Detach(panel)
            panel.Destroy()
            data.del_col(col_name)
        line = data.kanban_cols_seps.get(col_name)
        if line:
            self.hbox_kanban.Detach(line)
            line.Destroy()
            del data.kanban_cols_seps[col_name]


        self.GetTopLevelParent().panel_kanban.Layout()

class KanbanColumn(wx.ScrolledWindow):
    def __init__(self, parent, col_name):
        super().__init__(parent,style=wx.VSCROLL | wx.HSCROLL)
        self.SetScrollRate(20, 20)
        self.col_name = col_name
        self.parent = parent

        text = wx.Button(self, label=col_name)

        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.ctx = wx.Menu()
        cl = self.ctx.Append(wx.ID_ANY, "Clear")
        dl = self.ctx.Append(wx.ID_ANY, "Delete")
        ad = self.ctx.Append(wx.ID_ANY, "Add")
        self.Bind(wx.EVT_MENU, self.clear_tasks, cl)
        self.Bind(wx.EVT_MENU, lambda event, name=col_name:parent.remove_col_from_kanban(name), dl)
        self.Bind(wx.EVT_MENU, self.on_add_task_user, ad)



        self.vbox_main = wx.BoxSizer(wx.VERTICAL)

        self.hbox = wx.BoxSizer(wx.HORIZONTAL)


        line = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
        self.hbox.AddStretchSpacer()
        self.hbox.Add(text, 0, wx.ALL, 2)
        self.hbox.AddStretchSpacer()
        self.vbox_main.Add(self.hbox, 0, wx.EXPAND | wx.ALL, 2)

        self.vbox_main.Add(line, 0, wx.EXPAND | wx.ALL, 0)

        self.add_button = wx.Button(self, wx.ID_ANY, "Add ✚", wx.DefaultPosition, size=(60, 25))
        self.vbox_main.Add(self.add_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Bind(wx.EVT_BUTTON, self.on_add_task_user, self.add_button)


        self.vbox_tasks = BoxSizer(wx.VERTICAL)
        self.vbox_main.Add(self.vbox_tasks, 0, wx.ALL | wx.EXPAND, 3) 

        self.SetSizer(self.vbox_main)
        self.vbox_main.Fit(self)
 

    def OnRightDown(self, e):
        self.PopupMenu(self.ctx, e.GetPosition())

    def add_task(self, task_text="123"):
        task = KanBanTask(self, task_text)
        if task:
            self.vbox_tasks.Add(task, 0, wx.ALL |wx.EXPAND, 0)
            text = task.text
            if text:
                col_name = task.column.col_name
                if col_name not in data.kanban_cols_tasks.keys():
                    data.kanban_cols_tasks[col_name] = [text]
                else:
                    data.kanban_cols_tasks[col_name].append(text)

                task.column.vbox_main.Detach(task.column.add_button)
                task.column.vbox_main.Add(task.column.add_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)




                task.column.Layout()
                self.parent.Layout()


    def on_add_task_user(self, event):
        task = KanBanTask(self)
        if task:
            self.vbox_tasks.Add(task, 0, wx.ALL |wx.EXPAND, 0)
            text = task.text
            if text:
                col_name = task.column.col_name
                if col_name not in data.kanban_cols_tasks.keys():
                    data.kanban_cols_tasks[col_name] = [text]
                else:
                    data.kanban_cols_tasks[col_name].append(text)

                task.column.vbox_main.Detach(task.column.add_button)

                self.vbox_main.Add(self.add_button, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

                task.column.Layout()
                self.parent.Layout()

    def update_tasks(self, tasks):
        self.Freeze()
        self.clear_tasks()

        for task in tasks:
            self.add_task(task)
        self.Thaw()

    def clear_tasks(self, e=None):

        for child in list(self.vbox_tasks.GetChildren()):
            wnd = child.GetWindow()
            if wnd:
                self.vbox_tasks.Detach(wnd)
                wnd.Destroy()

        data.kanban_cols_tasks[self.col_name] = []

        self.Layout()

class KanBanTask(wx.Panel):
    def __init__(self,parent, task_text=None):
        super().__init__(parent)

        self.column = parent

        if task_text:
            self.text = task_text
        else:
            dlg = MultiLineTextDialog(self, "Enter Task Description")
            if dlg.ShowModal() == wx.ID_OK:
                self.text = dlg.GetValue()
                if self.text == "":
                    self.text = None
                    dlg.Destroy()
                    self.Destroy()
            else:
                self.text = None
                dlg.Destroy()
                self.Destroy()
        if self.text:


            vbox = wx.BoxSizer(wx.VERTICAL)
            task_text = wx.StaticText(self, label=self.text)
            font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Times New Roman")
            task_text.SetFont(font)

            vbox.Add(task_text, 0, wx.EXPAND | wx.ALL, 5)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            del_button = wx.Button(self, label="✘", id=DEL_TASK, size=(30, 24))
            left_button = wx.Button(self, label="🡸", size=(24, 24))
            right_button = wx.Button(self, label="🡺", size=(24, 24))
            up_button = wx.Button(self, label="🡹", size=(24, 24))
            down_button = wx.Button(self, label="🡻", size=(24, 24))
            hbox.AddMany([
                (del_button, 0, wx.ALL, 2),
                (left_button, 0, wx.ALL, 2),
                (right_button, 0, wx.ALL, 2),
                (up_button, 0, wx.ALL, 2),
                (down_button, 0, wx.ALL, 2)
            ])
            vbox.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL, 1)
            line = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
            vbox.Add(line, 0, wx.EXPAND | wx.ALL, 0)
            self.SetSizer(vbox)
            col = self.GetTopLevelParent()
            self.Bind(wx.EVT_BUTTON, self.on_del_task, del_button)
            left_button.Bind(EVT_BUTTON, self.on_left_taks)
            right_button.Bind(EVT_BUTTON, self.on_right_task)
            down_button.Bind(EVT_BUTTON, self.on_down_task)
            up_button.Bind(EVT_BUTTON, self.on_up_task)

    def on_del_task(self, e):
        # Remove from layout
        self.column.vbox_tasks.Detach(self)
        self.Destroy()

        # Remove from data dict
        data.kanban_cols_tasks[self.column.col_name].remove(self.text)
        self.column.Layout()



    def on_left_taks(self, e):
        col_name = self.column.col_name
        ind = data.get_col_index(col_name)
        if ind > 0:
            left_col_id = data.kanban_cols[ind-1][1]
            text = self.text
            left_col_id.add_task(text)

            self.on_del_task(e)

    def on_right_task(self, e):
        col_name = self.column.col_name
        ind = data.get_col_index(col_name)
        if ind < len(data.kanban_cols)-1:
            right_col_id = data.kanban_cols[ind+1][1]
            text = self.text
            right_col_id.add_task(text)

            self.on_del_task(e)
    def on_up_task(self, e):
         col_name = self.column.col_name
         data.get_col_address(col_name)
         ind = data.kanban_cols_tasks[col_name].index(self.text)
         if ind - 1 >= 0:
             data.kanban_cols_tasks[col_name][ind], data.kanban_cols_tasks[col_name][ind - 1] = data.kanban_cols_tasks[col_name][ind - 1], data.kanban_cols_tasks[col_name][ind]
             self.column.update_tasks(data.kanban_cols_tasks[col_name])

    def on_down_task(self, e):
        col_name = self.column.col_name
        data.get_col_address(col_name)
        ind = data.kanban_cols_tasks[col_name].index(self.text)
        if ind + 1 <= len(data.kanban_cols_tasks[col_name])-1:
            data.kanban_cols_tasks[col_name][ind], data.kanban_cols_tasks[col_name][ind + 1] = data.kanban_cols_tasks[col_name][ind + 1], data.kanban_cols_tasks[col_name][ind]
            self.column.update_tasks(data.kanban_cols_tasks[col_name])

class MultiLineTextDialog(wx.Dialog):
    def __init__(self, parent, title="Enter text", default_text=""):
        super().__init__(parent, title=title, size=(250, 150))

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = wx.TextCtrl(self, value=default_text, style=wx.TE_MULTILINE)
        vbox.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        ok_btn = wx.Button(self, wx.ID_OK, "OK")
        cancel_btn = wx.Button(self, wx.ID_CANCEL, "Cancel")
        hbox.AddStretchSpacer()
        hbox.Add(ok_btn, 0, wx.RIGHT, 20)
        hbox.Add(cancel_btn, 0)
        hbox.AddStretchSpacer()

        vbox.Add(hbox, 0, wx.ALIGN_CENTER | wx.BOTTOM, 5)
        self.SetSizer(vbox)

    def GetValue(self):
        return self.text_ctrl.GetValue()

class ToDoList(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.i = 0

        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.vbox)
        self.add_button = wx.Button(self, wx.ID_ANY, "add task", wx.DefaultPosition, size=(60, 25))

        self.clear_button = wx.Button(self, wx.ID_ANY, "clear", wx.DefaultPosition, size=(60, 25))
        self.clear_button.Bind(wx.EVT_BUTTON, self.clear_tasks)


        self.vbox.Add(self.clear_button, 0, wx.ALL, 5)
        line = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
        self.vbox.Add(line, flag=wx.EXPAND, border=2)
        self.vbox.Add(self.add_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.add_button.Bind(wx.EVT_BUTTON, self.on_add_task)



    def on_add_task(self, e):
        self.i += 1
        task = ToDo(self)
        self.vbox.Detach(self.add_button)
        self.vbox.Add(task, 0, wx.ALL | wx.EXPAND, 2)
        self.vbox.Add(self.add_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        data.to_do_tasks[task.text] = task
        self.Layout()
    def upbade_old_task(self, old_task):
        self.i += 1
        task = old_task[3:]
        task = ToDo(self, task)

        self.vbox.Detach(self.add_button)
        self.vbox.Add(task, 0, wx.ALL | wx.EXPAND, 2)
        self.vbox.Add(self.add_button, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        data.to_do_tasks[task.text] = task
        self.Layout()




    def clear_tasks(self, e):
        self.Freeze()
        for task_text in data.to_do_tasks.keys():
            task = data.to_do_tasks[task_text]
            self.vbox.Detach(task)
            task.Destroy()
        self.Thaw()
        self.Layout()
        data.to_do_tasks = {}
        self.i = 0


    def update_tasks(self, new_tasks):
        self.Freeze()
        self.clear_tasks(None)
        for task in new_tasks:
            self.upbade_old_task(task)
        self.Thaw()










class ToDo(wx.Panel):
    def __init__(self, parent, task=None):
        super().__init__(parent)
        self.parent = parent



        if task:
            self.text = task
        else:
            dlg = MultiLineTextDialog(self, "Enter Task Description")
            if dlg.ShowModal() == wx.ID_OK:
                self.text = dlg.GetValue()
                if self.text == "":
                    self.text = None
                    dlg.Destroy()
                    self.Destroy()
            else:
                self.text = None
                dlg.Destroy()
                self.Destroy()

        if self.text:
            self.text = f"{parent.i}. " + self.text
            self.vbox = wx.BoxSizer(wx.VERTICAL)
            self.hbox = wx.BoxSizer(wx.HORIZONTAL)


            self.todo_text = wx.StaticText(self, label=self.text)
            self.todo_text.SetMaxSize((374,48))


            checkbox = wx.CheckBox(self)
            checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox)

            del_button = wx.Button(self, label="✘", size=(24, 24))
            up_button = wx.Button(self, label="🡹", size=(24, 24))
            down_button = wx.Button(self, label="🡻", size=(24, 24))

            del_button.Bind(wx.EVT_BUTTON, self.on_del_button)
            up_button.Bind(wx.EVT_BUTTON, self.on_up_button)
            down_button.Bind(wx.EVT_BUTTON, self.on_down_button)

            self.hbox.Add(checkbox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
            self.hbox.Add(self.todo_text, 1, wx.ALL | wx.EXPAND, 3)

            self.hbox.AddStretchSpacer(1)

            self.hbox.Add(del_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
            self.hbox.Add(up_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
            self.hbox.Add(down_button, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)


            line2 = wx.StaticLine(self, style=wx.LI_HORIZONTAL)
            self.vbox.Add(self.hbox, 0, wx.EXPAND)
            self.vbox.Add(line2,flag=wx.EXPAND, border=2)
            self.SetSizer(self.vbox)

    def on_checkbox(self, e):
        box = e.GetEventObject()
        #parent = box.GetTopLevelParent()
        value = box.GetValue()
        if value:
            font = self.todo_text.GetFont()
            font.SetStrikethrough(True)
            self.todo_text.SetFont(font)
        else:
            font = self.todo_text.GetFont()
            font.SetStrikethrough(False)
            self.todo_text.SetFont(font)

    def on_del_button(self, e):
        lst = list(data.to_do_tasks.keys())
        lst.remove(self.text)
        self.parent.update_tasks(lst)
        print(self.text)
    def on_up_button(self, e):
        lst = list(data.to_do_tasks.keys())
        ind = lst.index(self.text)
        if ind >= 1:
            lst[ind], lst[ind-1] = lst[ind-1], lst[ind]
            self.parent.update_tasks(lst)
    def on_down_button(self, e):
        lst = list(data.to_do_tasks.keys())
        ind = lst.index(self.text)
        if ind < len(lst) - 1:
            lst[ind], lst[ind + 1] = lst[ind + 1], lst[ind]
            self.parent.update_tasks(lst)






















def on_close(e):
    with open("kanban.json", "w") as f:
        json.dump(data.kanban_cols_tasks, f, indent=3)
    e.Skip()

with open("kanban.json", "r") as f:
    d = json.load(f)



app = wx.App()
frame = MyFrame(None, 'wxPython')



for i in d.keys():
    x = frame.panel_kanban.add_col_to_kanban(i)
    for j in d[i]:
        x.add_task(j)


frame.Show()
app.MainLoop()