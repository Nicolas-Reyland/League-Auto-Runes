# Runes setting automation with python
import win32api, win32con, win32gui
import tkinter as tk
from tkinter import messagebox
from numpy import load
from time import sleep
from selenium import webdriver, common
from datetime import datetime
import autoit
import os, json
import pyperclip

# consts & lambdas
chromedriver_path = '../web/chromedriver_win32/chromedriver.exe'
d = json.load(open('data/rune_sets.json', 'r'))
champ_rune_url = 'https://euw.op.gg/champion/{}/statistics/{}/rune'

opgg_to_rune_set = lambda champion, lane: indexs_to_rune_set(get_opgg_rune_indexs(champion, lane))
add_opgg_to_db = lambda champion, lane: _add_to_json('{} {}'.format(champion, lane if lane != 'bottom' else 'adc'), opgg_to_rune_set(champion, lane if lane != 'adc' else 'bottom'))

read_db = lambda : json.load(open(os.path.join(os.getcwd(), 'data', 'rune_sets.json'), 'r'))

# functions
def rune_set_to_img(rune_set):
    opgg_indexs = _exploit_opgg_indexs()
    indexs = []
    for i in range(len(rune_set)):
        if i == 1: # delete i == 0 branch for index-matching
            del opgg_indexs[1][rune_set[0][0]]
        for j in range(len(rune_set[i])):
            # j == 0
            if j == 0 and i < 2: # primary & secondary runes
                indexs.append([ opgg_indexs[i][rune_set[i][j]][0] ])
                continue
            if j == 0 and i == 2:
                indexs.append([ opgg_indexs[i][j][rune_set[i][j]] ])
                continue

            # j > 0
            if i == 0:
                indexs[i].append(opgg_indexs[i] [rune_set[i][0]] [1] [rune_set[i][j]] )
                continue
            if i == 1:
                indexs[i].append(opgg_indexs[i] [rune_set[i][0]] [1] [rune_set[i][j][0]] [rune_set[i][j][1]] )
                continue
            if i == 2:
                indexs[i].append(opgg_indexs[i] [j] [rune_set[i][j]] )
                continue
    return indexs

def dl_images():
    import requests, io
    from PIL import Image
    url = 'https://opgg-static.akamaized.net/images/lol/perk{}/{}.png?image=q_auto&amp;v=1583298869'
    indexs = [8000, 8005, 8008, 8021, 8010, 9101, 9111, 8009, 9104, 9105, 9103, 8014, 8017, 8299, 8100, 8112, 8124, 8128, 9923, 8126, 8139, 8143, 8136, 8120, 8138, 8135, 8134, 8105, 8106, 8200, 8214, 8229, 8230, 8224, 8226, 8275, 8210, 8234, 8233, 8237, 8232, 8236, 8400, 8437, 8439, 8465, 8446, 8463, 8401, 8429, 8444, 8473, 8451, 8453, 8242, 8300, 8351, 8360, 8358, 8306, 8304, 8313, 8321, 8316, 8345, 8347, 8410, 8352, 8000, 9101, 9111, 8009, 9104, 9105, 9103, 8014, 8017, 8299, 8100, 8126, 8139, 8143, 8136, 8120, 8138, 8135, 8134, 8105, 8106, 8200, 8224, 8226, 8275, 8210, 8234, 8233, 8237, 8232, 8236, 8400, 8446, 8463, 8401, 8429, 8444, 8473, 8451, 8453, 8242, 8300, 8306, 8304, 8313, 8321, 8316, 8345, 8347, 8410, 8352, 5008, 5002, 5003, 5001, 5002, 5003]
    get_add = lambda n: ('Style' if n in range(8000,8401,100) else 'Shard') if n <= 5010 or n in range(8000,8401,100) else ''
    total = len(indexs)
    for i,n in enumerate(indexs):
        add = get_add(n)
        print('doing {}/{} : {} with add {}'.format(i, total, n, add))
        sleep(.5)
        rep = requests.get(url.format(add, n), stream=True)
        image = Image.open(io.BytesIO(rep.content))
        image.save('./data/rune_icons/{}.png'.format(n))

def get_opgg_rune_indexs(champion, lane):
    global driver # only for debugging, etc.
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # was chrome_options=options before
    driver = webdriver.Chrome(options=options, executable_path=chromedriver_path)
    driver.get(champ_rune_url.format(champion, lane))
    rune = _try_find(driver, lambda : driver.find_element_by_xpath("//div[@class='perk-page-wrap']"))
    elems = driver.find_elements_by_xpath("//img[contains(@src, 'opgg-static.akamaized.net/images/lol/perk') and not(contains(@src, 'grayscale'))and not(contains(@src, 'image=q_auto,w_'))]")
    srcs = [elem.get_attribute('src') for elem in elems]
    # extract the index in the src
    indexs = []
    for src in srcs[:11]:
        if 'perkStyle' in src or 'perkShard' in src:
            i = 10
        else:
            i = 5
        index = int(src[src.index('perk') + i : src.index('.png')])
        indexs.append(index)

    driver.quit()
    return indexs

def update_json(new_db):
    date = datetime.now().strftime('%d %m %Y - %H %M %S')
    old_db = read_db()
    json.dump(old_db, open('data/rune_sets {}.json'.format(date), 'w'))
    json.dump(new_db, open('data/rune_sets.json', 'w'))

def _add_to_json(name, rune_set):
    assert len(rune_set) == 3
    assert len(rune_set[0]) == 5
    assert len(rune_set[1]) == 3
    assert len(rune_set[2]) == 3
    d = json.loads(open('data/rune_sets.json', 'r').read())
    # assert name not in d.keys() # might use as update
    d[name] = rune_set
    json.dump(d, open('data/rune_sets.json', 'w'))

def _exploit_opgg_indexs():
    # format string (see text file for more...)
    opgg = open('data/op.gg rune index exploitable.txt', 'r').read()
    opgg = opgg.split('\nSEPARATOR\n')
    opgg = [categ.split('\n\n') for categ in opgg]

    # primary & secondary runes
    final_opgg = [[], [], []]
    for i,categ in enumerate(opgg[:2]):
        for book in categ:
            book = list(filter(None, book.split('\n')))
            rune_head = int(book[0])
            rune_tail = [list(map(int, line.split(', '))) for line in book[1:]]
            final_opgg[i].append([rune_head] + [rune_tail])

    # perk shard (bonus)
    opgg[2] = list(filter(None, list(filter(None, opgg[2]))[0].split('\n')))
    opgg[2] = list(map(lambda line: [int(elem) for elem in line.split(', ')], opgg[2]))
    final_opgg[2] = opgg[2]

    return final_opgg


def indexs_to_rune_set(indexs):
    global opgg, rune_set#for debugging
    opgg = load('data/opgg_indexs.npy', allow_pickle=True).tolist()
    rune_set = [[], [], []]

    # primary
    primary_rune_index = [x for x,y in opgg[0]].index(indexs[0])
    rune_set[0].append(primary_rune_index)
    rune_set[0].append(opgg[0][primary_rune_index][1][0].index(indexs[1]))
    rune_set[0].append(opgg[0][primary_rune_index][1][1].index(indexs[2]))
    rune_set[0].append(opgg[0][primary_rune_index][1][2].index(indexs[3]))
    rune_set[0].append(opgg[0][primary_rune_index][1][3].index(indexs[4]))

    # secondary
    secondary_rune_index = [x for x,y in opgg[0]].index(indexs[5])
    secondary_1 = [(i,line.index(indexs[6])) for i,line in enumerate(opgg[1][secondary_rune_index][1]) if indexs[6] in line][0]
    secondary_2 = [(i+secondary_1[0]+1,line.index(indexs[7])) for i,line in enumerate(opgg[1][secondary_rune_index][1][secondary_1[0]+1:]) if indexs[7] in line][0]

    if primary_rune_index <= secondary_rune_index:
        secondary_rune_index -= 1
    rune_set[1].append(secondary_rune_index)
    rune_set[1].append(secondary_1)
    rune_set[1].append(secondary_2)

    # bonus
    rune_set[2] = [line.index(indexs[8+i]) for i,line in enumerate(opgg[2])]

    return rune_set


def _try_find(driver, f, maxtries=10, sleeptime=1, stdout=True, onbreak_do_raise=True, wait_for_content=False):
	found, count, elem = False, 0, None
	while not found:
		try:
			elem = f()
			if wait_for_content:
				if elem:
					found = True
				else:
					raise common.exceptions.NoSuchElementException('custom exception')
			else:
				found = True
		except common.exceptions.NoSuchElementException:
			count += 1
			if stdout: print(f'tried {count} times')
			sleep(1)
			if count == maxtries:
				if stdout: print('tried too many times')
				if onbreak_do_raise: raise RuntimeError('Ran out of tries')
	return elem

def set_rune_page(name, offset=(0,0)):
    rune_set = d[name]
    apply_rune_set(name, rune_set, offset=offset)

def isRealWindow(hWnd):
    '''Return True if given window is a real Windows application window.'''
    if not win32gui.IsWindowVisible(hWnd):
        return False
    if win32gui.GetParent(hWnd) != 0:
        return False
    hasNoOwner = win32gui.GetWindow(hWnd, win32con.GW_OWNER) == 0
    lExStyle = win32gui.GetWindowLong(hWnd, win32con.GWL_EXSTYLE)
    if (((lExStyle & win32con.WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
      or ((lExStyle & win32con.WS_EX_APPWINDOW != 0) and not hasNoOwner)):
        if win32gui.GetWindowText(hWnd):
            return True
    return False

def getWindowGeometry():
    '''
    Return a list of tuples (handler, rect) for each real window.
    '''
    def callback(hWnd, windows):
        if not isRealWindow(hWnd):
            return
        rect = win32gui.GetWindowRect(hWnd)
        windows.append((hWnd, rect)) # (rect[2] - rect[0], rect[3] - rect[1])))
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

def get_league_pos():
    try:
        return autoit.win_get_pos('League of Legends')
    except Exception as e:
        messagebox.showerror('Error', str(e))
        return None

def mouse_click(pos):
    x, y = pos
    win32api.SetCursorPos((x,y)) # win32api.SetCursorPos((x,y)) is better to be replaced by win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(x/SCREEN_WIDTH*65535.0), int(y/SCREEN_HEIGHT*65535.0))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def keyboard_type(s):
    autoit.send(s)

def show_rune_set(img_set):
    # [[l0, l1, l1bis, l2, l3, l4, l4bis], [sl0, sl1, sl2, sl3], [bl0, bl1, bl2]]
    coords = load('data/coords.npy', allow_pickle=True)
    width, height = 1280, 720
    tk_width, tk_height = 300, 150
    width_ratio, height_ratio = tk_width/width, tk_height/height

    # add game position coords
    for i in range(len(coords)):
        for j in range(len(coords[i])):
            for k in range(len(coords[i][j])):
                coords[i][j][k][0] *= width_ratio
                coords[i][j][k][1] *= height_ratio
                coords[i][j][k][0] += 5
                coords[i][j][k][1] += 5

    # tkinter
    toplevel = tk.Toplevel()
    toplevel.overridedirect(True)
    toplevel.wm_attributes('-transparentcolor', 'white')






def apply_rune_set(name, rune_set, offset=(0, 0)):
    global coords
    initial_mouse_position = win32api.GetCursorPos()
    current_game_window_position = get_league_pos()
    if current_game_window_position is None:
        return
    game_x, game_y = current_game_window_position[:2]
    name_button_pos = [155,122]
    name_entry_pos = [170, 122]
    save_button_pos = [500,122]
    '''
    rune_set is a list that comes like that:
    [
        [
        0-4 -> index of primary rune ,
        0-2/4 -> index of primary keystone ,
        0-2 -> index of 1/3 secondary keystone ,
        0-2 -> index of 2/3 secondary keystone ,
        0-2/3 -> index of 3/3 secondary keystone
        ] ,

        [
        0-4 -> index of secondary rune ,
        (0-2, 0-2) -> index of 1/2 secondary , (row-index, column-index)
        (0-2, 0-2) -> index of 2/2 secondary (row-index, column-index)
        ] ,

        [
        0-2 -> index of 1/3 bonuses ,
        0-2 -> index of 2/3 bonuses ,
        0-2 -> index of 3/3 bonuses
        ]
    ]
    '''

    # [[l0, l1, l1bis, l2, l3, l4, l4bis], [sl0, sl1, sl2, sl3], [bl0, bl1, bl2]]
    coords = load('data/coords.npy', allow_pickle=True)

    # add game position coords
    for i in range(len(coords)):
        for j in range(len(coords[i])):
            for k in range(len(coords[i][j])):
                coords[i][j][k][0] += game_x + offset[0]
                coords[i][j][k][1] += game_y + offset[1]

    # choose right positions
    primary_rune_1 = coords[0][0][rune_set[0][0]]

    if rune_set[0][0] == 0 or rune_set[0][0] == 1:
        primary_rune_2 = coords[0][2][rune_set[0][1]]
    else:
        primary_rune_2 = coords[0][1][rune_set[0][1]]

    primary_rune_3_1 = coords[0][3][rune_set[0][2]]
    primary_rune_3_2 = coords[0][4][rune_set[0][3]]
    if rune_set[0][0] == 1:
        primary_rune_3_3 = coords[0][6][rune_set[0][4]]
    else:
        primary_rune_3_3 = coords[0][5][rune_set[0][4]]

    secondary_rune_1 = coords[1][0][rune_set[1][0]]
    secondary_rune_2 = coords[1][rune_set[1][1][0]+1][rune_set[1][1][1]]
    secondary_rune_3 = coords[1][rune_set[1][2][0]+1][rune_set[1][2][1]]

    bonus_1 = coords[2][0][rune_set[2][0]]
    bonus_2 = coords[2][1][rune_set[2][1]]
    bonus_3 = coords[2][2][rune_set[2][2]]

    # clicking
    mouse_click(primary_rune_1)
    mouse_click(secondary_rune_1)

    def do_sub_runes():

        mouse_click(bonus_1)
        mouse_click(bonus_2)
        mouse_click(bonus_3)

        sleep(.5)
        mouse_click(primary_rune_2)
        mouse_click(primary_rune_3_1)
        mouse_click(primary_rune_3_2)
        mouse_click(primary_rune_3_3)

        sleep(.5)
        mouse_click(secondary_rune_2)
        mouse_click(secondary_rune_3)

    do_sub_runes()

    save_button_pos = [save_button_pos[0] + game_x + offset[0], save_button_pos[1] + game_y + offset[1]]


    # rename rune page
    mouse_click(save_button_pos) # first save
    name_button_pos = [name_button_pos[0] + game_x + offset[0], name_button_pos[1] + game_y + offset[1]]
    name_entry_pos = [name_entry_pos[0] + game_x + offset[0], name_entry_pos[1] + game_y + offset[1]]
    mouse_click(name_button_pos)
    sleep(3)
    mouse_click(name_entry_pos)
    sleep(1)
    keyboard_type('{CTRLDOWN}')
    keyboard_type('a')
    keyboard_type('{CTRLUP}')
    pyperclip.copy(name)
    keyboard_type('{CTRLDOWN}') # faire avec control+v (copy-paste) pour la rapidité
    keyboard_type('v')
    keyboard_type('{CTRLUP}')
    sleep(.5)
    keyboard_type('{ENTER}')
    sleep(2) # sleep bc else the name won't be edited every where

    # save rune page
    mouse_click(save_button_pos)

    # redo sub-runes to be sure
    #do_sub_runes()
    #mouse_click(save_button_pos)

    # relocate mous position to initial posititon
    win32api.SetCursorPos(initial_mouse_position)









#
