import tkinter as tk
from tkinter import ttk
import json

current_lang = "en"

help_window = None
setting_window_lang = None  # Додай цей рядок обов'язково


current_theme = 'dark'
def_font = 'Arial'        # Стандартний шрифт
def_font_size = 10        # Стандартний розмір


with open('system_resources.json', 'r', encoding='utf-8') as f:
    res = json.load(f)

color_bg = {name: d["bg"] for name, d in res["palette"].items()}
color_fg = {name: d["fg"] for name, d in res["palette"].items()}


fonts_use = res["fonts"]["list"]
fonts_size = res["fonts"]["sizes"]

obj_them = []
entry_them = []
chang_shrifts = []
chang_texts = []



setting_window = None  
setting_window_theme = None
setting_window_font = None 
def update_ui_localization():
    global current_lang
    
    files = {
        "start": "con_start.json",
        "settings": "con_settings.json",
        "lang": "con_lang.json",
        "help": "con_help.json",
        "font": "con_font.json",
        "resources": "system_resources.json"
    }
    
    cached_data = {}
    for key, path in files.items():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                # Беремо блок мови (uk або en)
                cached_data[key] = json.load(f)[current_lang]
        except: continue

    # Оновлюємо всі зареєстровані віджети
    for obj, file_key, path in chang_texts:
        try:
            if obj.winfo_exists():
                new_text = cached_data[file_key]
                for key in path:
                    new_text = new_text[key]
                obj.config(text=new_text)
        except: continue
            
    # Оновлюємо заголовки вікон
    try:
        if start_win.winfo_exists(): 
            start_win.title(cached_data["start"]["text"]["Window"][0])

        if setting_window and setting_window.winfo_exists(): 
            setting_window.title(cached_data["settings"]["text"]["Window"][0])

        if setting_window_lang and setting_window_lang.winfo_exists():
            setting_window_lang.title(cached_data["lang"]["Window"][0])

        if help_window and help_window.winfo_exists():
            help_window.title(cached_data["help"]["text"]["Window"][0])

        if setting_window_font and setting_window_font.winfo_exists():
            setting_window_font.title(cached_data["font"]["text"]["Window"][0])

        if setting_window_theme and setting_window_theme.winfo_exists():
            setting_window_theme.title(cached_data["resources"]["theme_win"]["title"])

    except:
        pass

def save_system_config():
    """Зберігає поточну мову та тему в окремий файл налаштувань"""
    config_to_save = {
        "theme": current_theme,
        "lang": current_lang,
        "font_family": def_font,
        "font_size": def_font_size
    }
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config_to_save, f, indent=4)
#--------window menu------------
def menu_win():

    global menu_window
    menu_window = tk.Toplevel()

    apply_current_theme()
    change_font_os()
#--------changer font os------
def change_font_os():
    # Проходимо по всіх віджетах, які ти зареєстрував у список для шрифтів
    for shr in chang_shrifts:
        try:
            # Використовуємо .config — це надійніший спосіб для Tkinter
            shr.config(font=(def_font, def_font_size))
        except:
            # Якщо об'єкт не підтримує шрифт, просто пропускаємо
            pass
#--------changer theme os------
def apply_current_theme():
    set_os_theme(current_theme)#--------theme os color-------------
#--------window for change theme----------
def set_os_theme(color_name):
    """Універсальна зміна теми для всієї PyOS"""
    global current_theme
    current_theme = color_name
    
    # 1. Дістаємо кольори безпосередньо з нашого великого JSON-словника
    # Припускаємо, що ти вже завантажив файл у змінну 'res'
    try:
        bg = res["palette"][color_name]["bg"]
        fg = res["palette"][color_name]["fg"]
    except KeyError:
        # Запасний варіант, якщо кольору немає в JSON
        bg, fg = "#101010", "#E0E0E0"

    # 2. Оновлюємо всі зареєстровані об'єкти
    for obj in obj_them:
        try:
            # Спробуємо змінити і фон, і текст (для Label, Button)
            obj.config(bg=bg, fg=fg)
        except:
            try:
                # Якщо у об'єкта немає параметра 'fg' (наприклад, Frame)
                obj.config(bg=bg)
            except:
                pass
    
    # 3. Зберігаємо вибір у конфіг (щоб PyOS пам'ятала тему)
    save_system_config()

def set_system_language(lang_code):
    global current_lang
    current_lang = lang_code
    
    # 1. Сохраняем в конфиг (память)
    save_system_config()

    # 2. ОБНОВЛЯЕМ ТЕКСТЫ ОНЛАЙН ЧЕРЕЗ ЦИКЛ
    # Эта функция теперь сделает всю работу за тебя
    update_ui_localization() 
    
    print(f"System language changed to: {lang_code}")
# --- Окно выбора языка ---
def setting_win_lang():
    global setting_window_lang, current_lang, lbl_lang_info, btn_ua, btn_en
    
    # Проверка на существование окна
    if setting_window_lang is not None and setting_window_lang.winfo_exists():
        setting_window_lang.lift()
        return

    # --- ЗАГРУЗКА ИЗ JSON (с учетом ключа) ---
    try:
        with open('con_lang.json', 'r', encoding='utf-8') as f:
            # ДОБАВЛЯЕМ В КОНЦЕ ПУТИ
            l_data = json.load(f)[current_lang]
    except Exception as e:
        print(f"Ошибка JSON: {e}")
        l_data = {"Window": ["Lang"], "Label": ["Choose:"], "Button": ["UA", "EN"]}

    setting_window_lang = tk.Toplevel(setting_window)
    setting_window_lang.geometry('350x250')
    setting_window_lang.title(l_data["Window"][0])
    setting_window_lang.config(bg='black')

    top_bar_l = tk.Frame(setting_window_lang, bg='black')
    top_bar_l.pack(side='top', fill='x', padx=10, pady=5)

    tk.Button(top_bar_l, text='[ X ]', fg='red', bg='black', bd=0, 
              command=setting_window_lang.destroy).pack(side='right')

    # Лейбл информации
    lbl_lang_info = tk.Label(setting_window_lang, text=l_data["Label"][0], 
                             fg='white', bg='black', font=('Arial', 10))
    lbl_lang_info.pack(pady=20)
    # Регистрируем для онлайн перевода: (объект, файл, список, индекс)
    chang_texts.append((lbl_lang_info, "lang", ["Label", 0]))

    # Кнопка UA
    btn_ua = tk.Button(setting_window_lang, text=l_data["Button"][0], width=15,
                       command=lambda: set_system_language("uk"))
    btn_ua.pack(pady=5)
    chang_texts.append((btn_ua, "lang", ["Button", 0]))

    # Кнопка EN
    btn_en = tk.Button(setting_window_lang, text=l_data["Button"][1], width=15,
                       command=lambda: set_system_language("en"))
    btn_en.pack(pady=5)
    chang_texts.append((btn_en, "lang", ["Button", 1]))

    # Регистрация темы
    obj_them.extend([setting_window_lang, top_bar_l, btn_ua, btn_en, lbl_lang_info])
    apply_current_theme()
    change_font_os()
#--------window for change font----------
def setting_win_font():
    global setting_window_font, def_font, def_font_size
    
    if setting_window_font is not None and setting_window_font.winfo_exists():
        setting_window_font.lift()
        return
    
    # --- 1. ЗАВАНТАЖЕННЯ JSON ---
    try:
        with open('con_font.json', 'r', encoding='utf-8') as f:
            f_data = json.load(f)
        f_txt = f_data[current_lang]["text"]
    except:
        f_txt = {"Window": ["Fonts"], "Button": ["Apply"]}

    # --- 2. ЛОГІКА ЗМІНИ ТА ЗБЕРЕЖЕННЯ ---
    def change_font():
        global def_font, def_font_size
        def_font = fonts_use_setting.get()
        def_font_size = int(fonts_size_setting.get())
        
        # Викликаємо твій глобальний оновлювач
        change_font_os()
        
        # ЗБЕРІГАЄМО В КОНФІГ (щоб PyOS пам'ятала шрифт після перезапуску)
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                cfg = json.load(f)
            cfg["font_family"] = def_font
            cfg["font_size"] = def_font_size
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(cfg, f, indent=4)
        except:
            pass

    # --- 3. СТВОРЕННЯ ВІКНА ---
    setting_window_font = tk.Toplevel(setting_window)
    setting_window_font.geometry('400x400')
    setting_window_font.title(f_txt["Window"][0])
    setting_window_font.config(bg='black')

    top_bar_f = tk.Frame(setting_window_font, bg='black')
    top_bar_f.pack(side='top', fill='x', padx=10, pady=5)
    
    btn_close = tk.Button(top_bar_f, text='[ X ]', fg='red', bg='black', 
                          font=('Consolas', 8), bd=0, command=setting_window_font.destroy)
    btn_close.pack(side='right')

    # Списки шрифтів (беремо зі статики, яку ми обговорювали)
    # fonts_use та fonts_size мають бути завантажені на старті
    fonts_use_setting = ttk.Combobox(setting_window_font, values=fonts_use)
    fonts_use_setting.pack(pady=10)
    fonts_use_setting.set(def_font) # Встановлюємо той, що зараз працює

    fonts_size_setting = ttk.Combobox(setting_window_font, values=fonts_size)
    fonts_size_setting.pack(pady=10)
    fonts_size_setting.set(str(def_font_size))

    # Кнопка з текстом із JSON
    btn_apply = tk.Button(setting_window_font, text=f_txt["Button"][0], 
                          width=15, command=change_font)
    btn_apply.pack(pady=20)
    chang_texts.append((btn_apply, "font", ["text", "Button", 0]))

    # Реєстрація для тем
    obj_them.extend([setting_window_font, top_bar_f, btn_apply])
    
    apply_current_theme()
    change_font_os()
#--------window help -----------
def help_win():
    global help_window, lbl_help, top_bar_help, btn_close_help

    if help_window is not None and help_window.winfo_exists():
        help_window.lift()
        return
    
    # --- ЗАВАНТАЖЕННЯ JSON ---
    try:
        with open('con_help.json', 'r', encoding='utf-8') as f:
            help_data = json.load(f)
        h_txt = help_data[current_lang]["text"]
    except Exception as e:
        print(f"Помилка довідки: {e}")
        h_txt = {"Window": ["Help"], "Label": ["Help text error", "File not found"]}

    help_window = tk.Toplevel(start_win)
    help_window.geometry('500x500')
    help_window.title(h_txt["Window"][0]) # Заголовок вікна
    help_window.config(bg='black')
    help_window.resizable(True, True)
    
    top_bar_help = tk.Frame(help_window, bg='black')
    top_bar_help.pack(side='top', fill='x', padx=10, pady=5)

    btn_close_help = tk.Button(top_bar_help, text='[ X ]', fg='red', bg='black', 
                               font=('Consolas', 8), bd=0, cursor='hand2', 
                               command=help_window.destroy)
    btn_close_help.pack(side='right')

    # Заголовок довідки
    lbl_title_help = tk.Label(help_window, text=h_txt["Label"][0], 
                              fg='white', bg='black', font=('Arial', 12, 'bold'))
    lbl_title_help.pack(pady=(20, 5))
    chang_texts.append((lbl_title_help, "help", ["text", "Label", 0]))

    # Основний текст довідки (з переносом рядків)
    lbl_help = tk.Label(help_window, text=h_txt["Label"][1], 
                        fg='white', bg='black', font=('Arial', 10),
                        wraplength=450, justify="center") # wraplength щоб текст не вилізав
    lbl_help.pack(pady=10, padx=20)
    chang_texts.append((lbl_help, "help", ["text", "Label", 1]))

    # Реєстрація об'єктів
    obj_them.extend([help_window, top_bar_help, lbl_title_help, lbl_help])
    chang_shrifts.extend([lbl_title_help, lbl_help])

    apply_current_theme()
    change_font_os()

def setting_win_theme():
    # Додаємо всі необхідні глобальні змінні
    global setting_window_theme, color_bg, obj_them, current_lang, res

    # Перевірка, чи вікно вже відкрите
    if setting_window_theme is not None and setting_window_theme.winfo_exists():
        setting_window_theme.lift()
        return

    # --- 1. ЗАВАНТАЖЕННЯ ТЕКСТІВ З JSON ---
    try:
        # res — це твій завантажений system_resources.json
        t_txt = res[current_lang]["theme_win"]
    except:
        t_txt = {"title": "Theme PyOs", "frame": "Colors"}

    # --- 2. СТВОРЕННЯ ВІКНА ---
    setting_window_theme = tk.Toplevel(start_win) # Використовуємо start_win як батька
    setting_window_theme.title(t_txt["title"])
    setting_window_theme.geometry('500x200') # Трохи зменшив висоту для компактності
    setting_window_theme.config(bg='black')

    # Верхня панель
    top_bar_window_theme = tk.Frame(setting_window_theme, bg='black')
    top_bar_window_theme.pack(side='top', fill='x', padx=10, pady=5)

    btn_close_window_theme = tk.Button(top_bar_window_theme, text='[ X ]', fg='red', bg='black',
                                        font=('Consolas', 8), bd=0, cursor='hand2', 
                                        command=setting_window_theme.destroy)
    btn_close_window_theme.pack(side='right')

    # Рамка для кнопок
    frame_btn_color_theme = tk.LabelFrame(setting_window_theme, text=t_txt["frame"], bg='black', fg='white')
    frame_btn_color_theme.pack(pady=20, padx=10)
    chang_texts.append((frame_btn_color_theme, "resources", ["theme_win", "frame"]))

    # --- 3. ЦИКЛ СТВОРЕННЯ КНОПОК ---
    for color_name in color_bg.keys():
        # Отримуємо HEX-код кольору
        this_btn_color = color_bg[color_name]
    
        btn = tk.Button(
            frame_btn_color_theme, 
            bg=this_btn_color,        
            activebackground=this_btn_color, 
            width=5, 
            height=2,
            cursor='hand2',
            # lambda з аргументом c=color_name, щоб кожна кнопка мала свій колір
            command=lambda c=color_name: set_os_theme(c)
        )
        # ТЕПЕР ПРАВИЛЬНО: pack всередині циклу!
        btn.pack(side='left', padx=5, pady=10)
        
        # Ми НЕ додаємо кнопки в obj_them, щоб вони лишалися кольоровими
        # Але додаємо в список шрифтів, щоб вони теж оновлювались
        chang_shrifts.append(btn)

    # Додаємо вікно та рамку в список тем
    obj_them.extend([setting_window_theme, top_bar_window_theme, frame_btn_color_theme])

    # Застосовуємо стилі
    apply_current_theme()
    change_font_os()
#--------window setting -----------
def setting_win():
    global setting_window, top_bar_setting, btn_close_setting, lbl_setting, frame_setting_1, btn_setting_theme, btn_setting_lang, frame_setting_2, btn_setting_font

    # Перевірка, чи вікно вже відкрите
    if setting_window is not None and setting_window.winfo_exists():
        setting_window.lift()
        return
    
    # --- ЗАВАНТАЖЕННЯ ТЕКСТІВ ---
    try:
        with open('con_settings.json', 'r', encoding='utf-8') as f:
            set_data = json.load(f)
        s_txt = set_data[current_lang]["text"]
    except:
        s_txt = {"Window": ["Settings"], "Label": ["Settings"], "Button": ["Theme", "Lang", "Font"]}

    setting_window = tk.Toplevel(start_win)
    setting_window.geometry('500x500')
    setting_window.title(s_txt["Window"][0])
    setting_window.config(bg='black')
    setting_window.resizable(True, True)

    top_bar_setting = tk.Frame(setting_window, bg='black')
    top_bar_setting.pack(side='top', fill='x', padx=10, pady=5)

    btn_close_setting = tk.Button(top_bar_setting, text='[ X ]', fg='red', bg='black', font=('Consolas', 8), bd=0, cursor='hand2', command=setting_window.destroy)
    btn_close_setting.pack(side='right')

    # Заголовок "testing" замінюємо на текст із JSON
    lbl_setting = tk.Label(setting_window, text=s_txt["Label"][0], bg='black', fg='white')
    lbl_setting.pack(pady=(20, 10))
    chang_texts.append((lbl_setting, "settings", ["text", "Label", 0]))

    # --- ПЕРШИЙ РЯД КНОПОК ---
    frame_setting_1 = tk.Frame(setting_window, bg='black')
    frame_setting_1.pack()
    
    btn_setting_theme = tk.Button(frame_setting_1, text=s_txt["Button"][0], command=setting_win_theme) # Має відкривати вікно тем

    btn_setting_theme.pack(side='left', padx=10, pady=5)
    chang_texts.append((btn_setting_theme, "settings", ["text", "Button", 0]))

    btn_setting_lang = tk.Button(frame_setting_1, text=s_txt["Button"][1], fg='white', bg='black',
                                  font=('Consolas', 8), cursor='hand2', width=15, command=setting_win_lang)
    btn_setting_lang.pack(side='left', padx=10, pady=5)
    chang_texts.append((btn_setting_lang, "settings", ["text", "Button", 1]))

    # --- ДРУГИЙ РЯД КНОПОК ---
    frame_setting_2 = tk.Frame(setting_window, bg='black')
    frame_setting_2.pack()
    
    btn_setting_font = tk.Button(frame_setting_2, text=s_txt["Button"][2], fg='white', bg='black',
                                  font=('Consolas', 8), cursor='hand2', width=15, command=setting_win_font)
    btn_setting_font.pack(side='left', padx=10, pady=5)
    chang_texts.append((btn_setting_font, "settings", ["text", "Button", 2]))

    # РЕЄСТРАЦІЯ ОБ'ЄКТІВ
    obj_them.extend([setting_window, top_bar_setting, lbl_setting, frame_setting_1, 
                     btn_setting_theme, btn_setting_lang, frame_setting_2, btn_setting_font])
    
    chang_shrifts.extend([lbl_setting, btn_setting_theme, btn_setting_lang, btn_setting_font])

    apply_current_theme()
    change_font_os()
#--------window welcome------------
def start_window():
    global start_win, top_bar, btn_top_l2, btn_top_l3, btn_close, lbl_start_win, frame_center, btn_regist, btn_guest, lbl_end_win
    
    # --- ЗАВАНТАЖЕННЯ ДАНИХ З JSON ---
    try:
        # Відкриваємо твій файл (назви його con_start.json або як тобі зручно)
        with open('con_start.json', 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
        # Витягуємо тексти для поточної мови (uk або en)
        txt = lang_data[current_lang]["text"]
    except Exception as e:
        print(f"Помилка завантаження JSON: {e}")
        return

    # Створення головного вікна
    start_win = tk.Tk()
    start_win.geometry('500x350')
    start_win.title(txt["Window"][0])  # "Вітаємо у PyOs" / "Welcome to PyOs"
    start_win.config(bg='black')
    start_win.resizable(False, False)

    # --- 1. ВЕРХНЯ ПАНЕЛЬ (Top Bar) ---
    top_bar = tk.Frame(start_win, bg='black')
    top_bar.pack(side='top', fill='x', padx=10, pady=5)

    # Кнопка Settings: Button[0]
    btn_top_l2 = tk.Button(top_bar, text=txt["Button"][0], fg='white', bg='black', 
                           font=('Consolas', 8), cursor='hand2', command=setting_win)
    btn_top_l2.pack(side='left', padx=2)
    chang_texts.append((btn_top_l2, "start", ["text", "Button", 0]))

    # Кнопка Help: Button[1]
    btn_top_l3 = tk.Button(top_bar, text=txt["Button"][1], fg='white', bg='black', 
                           font=('Consolas', 8), cursor='hand2', command=help_win)
    btn_top_l3.pack(side='left', padx=2)
    chang_texts.append((btn_top_l3, "start", ["text", "Button", 1]))

    # Кнопка закрити
    btn_close = tk.Button(top_bar, text='[ X ]', fg='red', bg='black', 
                          font=('Consolas', 8), bd=0, cursor='hand2', command=start_win.destroy)
    btn_close.pack(side='right')

    # --- 2. ЦЕНТРАЛЬНИЙ КОНТЕНТ ---
    # Напис WELCOME: Label[0]
    lbl_start_win = tk.Label(start_win, fg='white', bg='black', 
                             text=txt["Label"][0], font=('Arial', 10))
    lbl_start_win.pack(expand=True, pady=(20, 0))
    chang_texts.append((lbl_start_win, "start", ["text", "Label", 0]))

    frame_center = tk.Frame(start_win, bg='black')
    frame_center.pack(expand=True)

    # Кнопка Log in (Увійти): Button[2]
    btn_regist = tk.Button(frame_center, text=txt["Button"][2], fg='white', bg='black', 
                           font=('Arial', 10), activebackground='white', activeforeground='black', 
                           cursor='hand2', width=10)
    btn_regist.pack(side='left', padx=10)
    chang_texts.append((btn_regist, "start", ["text", "Button", 2]))

    # Кнопка Guest (Гість): Button[3]
    btn_guest = tk.Button(frame_center, text=txt["Button"][3], fg='white', bg='black', 
                          font=('Arial', 8), activebackground='white', activeforeground='black', 
                          cursor='hand2', width=10)
    btn_guest.pack(side='left', padx=10)
    chang_texts.append((btn_guest, "start", ["text", "Button", 3]))

    # --- 3. НИЖНІЙ НАПИС (Copyright): Label[1] ---
    lbl_end_win = tk.Label(start_win, fg='gray', bg='black', 
                           text=txt["Label"][1], font=('Consolas', 8))
    lbl_end_win.pack(side='bottom', fill='x', pady=10)
    chang_texts.append((lbl_end_win, "start", ["text", "Label", 1]))

    # --- РЕЄСТРАЦІЯ ОБ'ЄКТІВ У ТВОЇ СПИСКИ ---
    # Додаємо все в obj_them (для тем)
    obj_them.extend([start_win, top_bar, btn_top_l2, btn_top_l3, lbl_start_win, 
                     frame_center, btn_regist, btn_guest, lbl_end_win])
    
    # Додаємо текстові об'єкти в chang_shrifts (для шрифтів)
    chang_shrifts.extend([btn_top_l2, btn_top_l3, lbl_start_win, btn_regist, btn_guest])

    # Застосовуємо твої системні налаштування
    apply_current_theme()
    change_font_os()

    start_win.mainloop()

start_window()