# League Runes
import os, sys, tkinter as tk
from tkinter import messagebox

# set right path
os.chdir(os.path.dirname(os.path.join(os.getcwd(), __file__)))

# continue imports
from PIL import ImageTk, Image
from CustomTkWidget import CustomTkWidget
from automate import *
from string import ascii_lowercase
import webbrowser
import traceback

# constant
collection_offset = (-112, 5)
dir_path = r'C:\Users\Nicolas\Documents\League Runes'
command_list = ['exit', 'list', 'blitz', 'blitzo', 'op.gg', 'op.ggo', 'open', 'add', 'rename', 'remove', 'showblitz', 'lane', 'laneo', 'help', 'bo', 'b', 'sb', 'l', 'lo', 'e', 'h']

help_content = {
    'help': {'alias': ['h'], 'description': 'Show the help content'},
    'list': {'alias': [], 'description': 'List the image/champs, select one and get the image'},
    'blitz': {'alias': ['b'], 'description': 'List all the db/champs, select one and the runes get set'},
    'blitzo': {'alias': ['bo'], 'description': 'Same as "blitz", but with not-in-CS offset'},
    'op.gg': {'alias': [], 'description': '/op.gg [champ] [lane]/ fetch the runes on op.gg, then set them'},
    'op.ggo': {'alias': [], 'description': 'Same as "op.gg", but with not-in-CS offset'},
    'open': {'alias': [], 'description': '/open [champ] [lane]/ open the op.gg page of champion'},
    'add': {'alias': [], 'description': '/add [champ] [lane]/ add the champ runes to the db'},
    'rename': {'alias': [], 'description': '/rename "[db/champ name]" "[db/new champ name]"/ rename db entry with new name'},
    'remove': {'alias': [], 'description': '/remove "[db/champ name]"/ removes the db entry with champ name'},
    'showblitz': {'alias': ['sb'], 'description': '/showblitz [db/champ name]/ show the runes of the db entry'},
    'lane': {'alias': ['l'], 'description': 'lets you choose the lane, then the champ to set the runes'},
    'laneo': {'alias': ['lo'], 'description': 'Same as "lane", but with not-in-CS offset'},
    'exit': {'alias': ['e'], 'description': 'Exit the program'},
}

sort_key = ['top', 'jungle', 'mid', 'adc', 'support'] # keys = list(sorted(list(l.keys()), key=lambda key: ascii_lowercase.index(key.lower().split()[-1][0])))
lane_colors = ['#666699', # metallic gray
               '#009933', # jugle green
               '#33ccff', # light blue
               '#ff3300', # light-ferm red
               '#999966', # light brown
               '#ff66ff'  # light pink
               ] # GRAPHICS: add activebackground color
root, arg = None, None

# functions
def list_champs_from_lane(lane_index):
    lane_list = ['top', 'jungle', 'mid', 'adc', 'support', 'other']
    lane = lane_list[lane_index]

    l = read_db()
    keys = list(sorted(list(l.keys()), key=lambda key: sort_key.index(key.split()[-1]) * 100 + ascii_lowercase.index(key.lower().split()[-1][0]) if key.split()[-1] in sort_key else 500 + ascii_lowercase.index(key.lower().split()[-1][0])))
    if lane != 'other':
        keys = list(filter(lambda key : key.split()[-1] == lane, keys))
    else:
        keys = list(filter(lambda key : key.split()[-1] not in lane_list[:-1], keys))

    temp_l = {}
    for key in keys:
        temp_l[key] = l[key]
    l = temp_l
    del temp_l
    offset = 10
    width = 150
    height = 30 * len(l) + 40 # all runes + exit button
    buttons = []
    rune_index = tk.IntVar()
    rune_index.set(-1)
    toplevel = tk.Toplevel()
    toplevel.overrideredirect(True)
    toplevel.attributes('-topmost', 'true')
    toplevel.geometry('{0}x{1}+{2}+{3}'.format(100, height, 10, 10))
    #tk.Frame(toplevel, bg='#00ffff').place(x=0, y=0, width=width, height=height-40)

    for i in range(len(l)):
        key = list(l.keys())[i]

        widget = CustomTkWidget(toplevel, info=i, function=lambda info: rune_index.set(info), **{'text': key if lane_index == 5 else ' '.join(key.split()[:-1]), 'bg': lane_colors[lane_index]})
        widget.widget.place(x=0, y=i*30, relwidth=1, height=30)
        buttons.append(widget)

    tk.Button(toplevel, text='X', bg='#ff5050', activebackground='#ff5050', command=lambda : rune_index.set(-1)).place(x=0, y=len(l)*30 + 10, relwidth=1, height=30)
    toplevel.wait_variable(rune_index)
    if rune_index.get() == -1:
        toplevel.destroy()
        return False
    toplevel.destroy()
    arg = list(l.keys())[rune_index.get()]
    print(rune_index.get())
    return arg


def choose_lane():
    toplevel = tk.Toplevel()
    toplevel.overrideredirect(True)
    toplevel.attributes('-topmost', 'true')
    toplevel.geometry('{0}x{1}+{2}+{3}'.format(100, 320, 10, 10))

    y = 5

    tk.Label(toplevel, text='Choose Lane').place(x=5, y=y, width=90, height=30)

    lane_val = tk.IntVar()
    lane_val.set(0)

    #top_button =
    y += 40
    tk.Button(toplevel, text='top', bg=lane_colors[(y - 5) // 40 - 1], command=lambda : lane_val.set(1)).place(x=5, y=y, width=90, height=30)
    #jungle_button =
    y += 40
    tk.Button(toplevel, text='jungle', bg=lane_colors[(y - 5) // 40 - 1], command=lambda : lane_val.set(2)).place(x=5, y=y, width=90, height=30)
    #mid_button =
    y += 40
    tk.Button(toplevel, text='mid', bg=lane_colors[(y - 5) // 40 - 1], command=lambda : lane_val.set(3)).place(x=5, y=y, width=90, height=30)
    #adc_button =
    y += 40
    tk.Button(toplevel, text='adc', bg=lane_colors[(y - 5) // 40 - 1], command=lambda : lane_val.set(4)).place(x=5, y=y, width=90, height=30)
    #support_button =
    y += 40
    tk.Button(toplevel, text='support', bg=lane_colors[(y - 5) // 40 - 1], command=lambda : lane_val.set(5)).place(x=5, y=y, width=90, height=30)
    #other_button =
    y += 40
    tk.Button(toplevel, text='other', bg=lane_colors[(y - 5) // 40 - 1], command=lambda : lane_val.set(6)).place(x=5, y=y, width=90, height=30)
    #exit_button =
    y += 40
    tk.Button(toplevel, text='X', bg='#ff5050', command=lambda : lane_val.set(7)).place(x=5, y=y, width=90, height=30)

    toplevel.wait_variable(lane_val)
    lane_index = lane_val.get() - 1

    toplevel.destroy()

    if lane_index == 6:
        sys.exit('X pressed')
    else:
        return lane_index


def list_champs(src='dir'): # possible src: dir, db
    if src == 'dir':
        l = os.listdir(dir_path)
        l = list(sorted(l, key=lambda key: sort_key.index(key[:-4].split()[-1]) * 100 + ascii_lowercase.index(key[:-4].lower().split()[-1][0]) if key[:-4].split()[-1] in sort_key else 500 + ascii_lowercase.index(key[:-4].lower().split()[-1][0])))
    else: # src == 'db'
        l = read_db()
        keys = list(sorted(list(l.keys()), key=lambda key: sort_key.index(key.split()[-1]) * 100 + ascii_lowercase.index(key.lower().split()[-1][0]) if key.split()[-1] in sort_key else 500 + ascii_lowercase.index(key.lower().split()[-1][0])))
        temp_l = {}
        for key in keys:
            temp_l[key] = l[key]
        l = temp_l
        del temp_l
    offset = 10
    width = 150
    height = 30 * len(l) + 40 + offset * 5 # all runes + exit button + 5 lane separation (4 + customs)
    buttons = []
    rune_index = tk.IntVar()
    rune_index.set(-1)
    toplevel = tk.Toplevel()
    toplevel.overrideredirect(True)
    toplevel.attributes('-topmost', 'true')
    toplevel.geometry('{0}x{1}+{2}+{3}'.format(100, height, 10, 10))
    #tk.Frame(toplevel, bg='#00ffff').place(x=0, y=0, width=width, height=height-40)

    lane_list = ['top', 'jungle', 'mid', 'adc', 'support']
    current_lane_index = 0
    for i in range(len(l)):
        if src == 'dir':
            key = l[i][:-4]
        else:
            key = list(l.keys())[i]

        if current_lane_index != 5:
            if key.split()[-1] != lane_list[current_lane_index]:
                current_lane_index += 1
        if src == 'dir': widget = CustomTkWidget(toplevel, info=i, function=lambda info: rune_index.set(info), **{'text': l[i][:-4], 'bg': lane_colors[current_lane_index]})
        if src == 'db': widget = CustomTkWidget(toplevel, info=i, function=lambda info: rune_index.set(info), **{'text': key if current_lane_index == 5 else ' '.join(key.split()[:-1]), 'bg': lane_colors[current_lane_index]})
        widget.widget.place(x=0, y=i*30 + offset * current_lane_index, relwidth=1, height=30)
        buttons.append(widget)
    tk.Button(toplevel, text='X', bg='#ff5050', activebackground='#ff5050', command=lambda : rune_index.set(-1)).place(x=0, y=len(l)*30 + 10 + offset * current_lane_index, relwidth=1, height=30)
    toplevel.wait_variable(rune_index)
    if rune_index.get() == -1:
        toplevel.destroy()
        return False
    toplevel.destroy()
    if src == 'dir':
        arg = l[rune_index.get()][:-4]
    else:
        arg = list(l.keys())[rune_index.get()]
    return arg


def command_handler(command):
    global dir_path
    assert command.startswith('!')
    command = command[1:]
    command = list(filter(None, command.split()))
    if command[0] in ['exit', 'e']:
        return True
    elif command == ['list']:
        arg = list_champs()
        if arg == False:
            return
        file_path = os.path.join(dir_path, arg + '.png')
        show_runes(file_path, arg)
        return True
    elif command[0] in ['blitz', 'b']:
        arg = list_champs(src='db')
        if arg == False:
            return
        set_rune_page(arg)
        return True
    elif command[0] in ['blitzo', 'bo']:
        arg = list_champs(src='db')
        if arg == False:
            return
        set_rune_page(arg, offset=collection_offset)
        return True
    elif command[0] == 'op.gg':
        rune_set = opgg_to_rune_set(command[1:])
        name = 'op.gg {} {}'.format(command[1], command[2])
        apply_rune_set(name, rune_set)
        return True
    elif command[0] == 'op.ggo':
        rune_set = opgg_to_rune_set(command[1:])
        name = 'op.gg {} {}'.format(command[1], command[2])
        apply_rune_set(name, rune_set, offset=collection_offset)
        return True
    elif command[0] == 'open':
        url = 'http://euw.op.gg/champion/{}/statistics/{}'
        url = url.format(command[1], command[2])
        webbrowser.open(url)
    elif command[0] == 'add':
        add_opgg_to_db(command[1], command[2])
    elif command[0] == 'rename':
        s = ' '.join(command[1:])
        s = list(filter(lambda ss: ss not in ['', ' '], s.split('"')))
        old_key, new_key = s
        l = read_db()
        assert new_key not in list(l.keys())
        l[new_key] = l[old_key]
        del l[old_key]
        update_json(l)
    elif command[0] == 'remove':
        s = ' '.join(command[1:])
        l = read_db()
        assert s in list(l.keys())
        del l[s]
        update_json(l)
    elif command[0] in ['showblitz', 'sb']:
        arg = list_champs(src='db')
        rune_set = read_db()[arg]
        messagebox.showinfo('Rune Set', '{}Primary:\n{}Secondary:\n{}Bonus:\n{}'.format(arg + '\n' * 2,
                                                                                         ', '.join([str(i) for i in rune_set[0]]) + '\n' * 2,
                                                                                         ', '.join([str(i) for i in rune_set[1]]) + '\n' * 2,
                                                                                         ', '.join([str(i) for i in rune_set[2]])))
    elif command[0] in ['lane', 'l']:
        lane_index = choose_lane()
        arg = list_champs_from_lane(lane_index)
        if arg == False:
            return
        set_rune_page(arg)
    elif command[0] in ['laneo', 'lo']:
        lane_index = choose_lane()
        arg = list_champs_from_lane(lane_index)
        if arg == False:
            return
        set_rune_page(arg, offset=collection_offset)
    elif command[0] in ['help', 'h']:
        help_str = ''
        for key,value in help_content.items():
            help_str += f' * {key}: alias: {", ".join(value["alias"])} descr: {value["description"]}\n'
        messagebox.showinfo('Help - List of Commands', help_str)
        return

    else:
        # command not found
        return False

def ask_arg():
    toplevel = tk.Toplevel()
    toplevel.overrideredirect(True)
    toplevel.attributes('-topmost', 'true')
    toplevel_width = 100
    toplevel_height = 40
    toplevel.geometry('{0}x{1}+{2}+{3}'.format(toplevel_width, toplevel_height, 10, 10))
    toplevel.bind('<Return>', lambda *args: next_var.set(True))
    toplevel.bind('<Control-x>', lambda *args: quit())
    next_var = tk.BooleanVar()
    next_var.set(False)
    tk.Label(toplevel, text='Rune Set').pack(anchor='n')
    entry = tk.Entry(toplevel)
    entry.pack()
    entry.focus_set()
    toplevel.wait_variable(next_var)
    arg = entry.get()
    toplevel.destroy()
    return arg

def show_runes(file_path, arg):
    root.title(arg)
    root.deiconify()

    image = Image.open(file_path)
    tk_image = ImageTk.PhotoImage(image)

    cv = tk.Canvas()
    cv.pack(side='top', fill='both', expand='yes')
    cv.create_image(10, 10, image=tk_image, anchor='nw')

    width = image.width + 10 + 50
    height = image.height + 20

    root.geometry('{0}x{1}+{2}+{3}'.format(width, height, 10, 10))

    quit_button = tk.Button(root, text='X', bg='#ff5050', activebackground='#ff5050', command=quit_function) # ff5050, ef242e
    quit_button.place(x = width - 45, y = 5, width = 40, height = height - 10)

    label = tk.Label(cv, text=arg, font='Helvetica 20', bg='white')
    label.place(relx=.3,rely=0.05,relwidth=.4,relheight=.15)

    tk.mainloop()

def quit_function(*args):
    root.destroy()

# main
def main(sys_arg):
    global root, arg

    root = tk.Tk()
    root.overrideredirect(True) # attributes('-type', 'splash')
    root.attributes('-topmost', 'true')
    # root.wm_attributes("-transparentcolor", 'white') # <- SUPOER INTERESTING !!!
    root.withdraw()

    arg, file_path = sys_arg, ''

    while not os.path.isfile(file_path) and (not arg[1:].split()[0] in command_list if arg.startswith('!') else (arg not in command_list)):
        arg = ask_arg()
        file_path = os.path.join(dir_path, '{}.png'.format(arg))

    if arg in command_list: arg = '!' + arg

    if arg.startswith('!'):
        if command_handler(arg):
            exit()

    else:
        file_path = os.path.join(dir_path, '{}.png'.format(arg))
        show_runes(file_path, arg)

#
if __name__ == '__main__':
    global err

    if len(sys.argv) > 1:
        sys_arg = sys.argv[1]
    else:
        sys_arg = ''

    try:
        main(sys_arg=sys_arg)
    except Exception as e:
        messagebox.showerror('Error', 'An eror has occured:\n{}'.format(traceback.format_exc()))

#
