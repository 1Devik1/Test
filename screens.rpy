################################################################################
## Инициализация
################################################################################

## Приоритет
init offset = -1

## Переменные для сохранений
default current_slot = None
default save_enable = False
define param = {0: (355, 275), 1: (1033, 275), 2: (356, 573), 3: (1034, 573)}

################################################################################
## Начало игры
################################################################################

screen game_start():
    modal True 
    add "black" at game_start

    timer 1.0 action Start()

################################################################################
## Блокировка нажатия
################################################################################

screen block_screen():
    zorder 201
    imagebutton idle "empty_full" action NullAction()

################################################################################
## Пропуск видео
################################################################################

define is_selected = False

screen movie_skip(movie, movie_time):
    modal True style_prefix 'movie'

    add movie

    if persistent.start_movie_watch:
        frame align(1., 1.):
            button at mm_but:
                add Frame("bg_button") at but_bg
                text _("Пропустить")
                action [With(Dissolve(0.5)), SetVariable('is_selected', True), Return()]
    
    timer movie_time action With(Dissolve(0.5)), Return()
    on 'show' action SetVariable('is_selected', False)
    
################################################################################
## Главное меню
################################################################################

screen main_menu():
    style_prefix "main_menu" tag menu

    add gui.main_menu_background
    add "fog_002"
    add "paticle_2"
    add "fog_001"
    add "paticle_1_1"
    add "shadow"
    add "paticle_1_2"
    add "right_dark_frame"
    add "small_snow_frame"

    add "black" at mm_bg_diss
    add "logo" at mm_elements

    vbox style_prefix "url" at mm_elements:
        align(0.98, 0.9)
        spacing 10

        frame:
            xpos 25
            button at mm_but_url:
                background "interface/main_menu/tg_button.png"
                action OpenURL('https://t.me/TBSOD_TG')
        
        button at mm_but_url:
            background "interface/main_menu/vk_button.png"
            action OpenURL('https://vk.com/tbsod')
        
        frame:
            xpos -25
            button at mm_but_url:
                background "interface/main_menu/yt_button.png"
                action OpenURL('https://youtube.com/@_UltraSteel?si=-SW8IgOZw8pEPo_1')
    
    imagemap style_prefix "other_buttons" at mm_other_elements:
        ground Null(1920, 1080)
        idle "interface/main_menu/other_buttons.png"
        hover im.MatrixColor("interface/main_menu/other_buttons.png", im.matrix.contrast(0.75))

        hotspot (1203, 939, 87, 143) at hotspot_shaking_x(1203, 939) action NullAction()
        hotspot (1329, 940, 95, 146) at hotspot_shaking_x(1329, 940) action NullAction()
        hotspot (1457, 940, 87, 143) at hotspot_shaking_x(1457, 940) action NullAction()

    add "dark_top_bottom_frame"

    vbox align(0.756, 0.7) spacing 5 at mm_elements:
        button at mm_but:
            add Frame("bg_button") at but_bg
            text _("Новая игра")
            action Show("game_start")
        button at mm_but:
            add Frame("bg_button") at but_bg
            text _("Загрузить")
            action ShowMenu("file_slots", "Загрузить")
        button at mm_but:
            add Frame("bg_button") at but_bg
            text _("Настройки")
            action ShowMenu("preferences")
        button at mm_but:
            add Frame("bg_button") at but_bg
            text _("Об авторах")
            action ShowMenu("about")
        button at mm_but:
            add Frame("bg_button") at but_bg
            text _("Выход")
            action Quit(confirm=False)

    key "game_menu" action Quit(confirm=True)  
    
    on "show" action Show("block_screen")
    on "replaced" action SetVariable("save_enable", False)
    timer 3.2 action Hide("block_screen")

################################################################################
## Подтверждение действия
################################################################################

screen confirm(message, yes_action, no_action):
    style_prefix "confirm" modal True zorder 200

    add "bg_menu_anim" at conf_fon

    vbox align(0.5, 0.4) spacing 30:
        text message style "message_text" at other_elements
    
        hbox align(0.5, 0.5) spacing 80 at other_elements:
            button at mm_but:
                add Frame("bg_button") at but_bg
                text _("Да")
                action yes_action
            button at mm_but:
                add Frame("bg_button") at but_bg
                text _("Нет")
                action no_action
    
    key "game_menu" action no_action
    on "show" action [Play("sfx_five", "sounds/menu/menu_confirm.ogg"), Show("block_screen")]
    on "replace" action Play("sfx_five", "sounds/menu/menu_confirm.ogg")
    timer 1.0 action Hide("block_screen")

################################################################################
## Сохранения и загрузки
################################################################################

screen file_slots(title):
    style_prefix "save_load" tag menu

    add "bg_menu_save" at conf_fon
    add "line" at save_elements
    text _("СОХРАНЕНИЯ И ЗАГРУЗКИ") style "title" at save_elements

    frame pos(310, 126) at save_elements:
        button at mm_but:
            sensitive save_enable
            add Frame("bg_button") at but_bg
            text _("Сохранить")
            action [SetVariable("current_slot", "Сохранить"), With(Dissolve(0.2))]
    frame pos(965, 126) at save_elements:
        button at mm_but:
            add Frame("bg_button") at but_bg
            text _("Загрузить")
            action [SetVariable("current_slot", "Загрузить"), With(Dissolve(0.2))]
    
    imagemap at save_elements:
        ground "bg_save_load"
        insensitive "bg_save_load"
        idle "save_load"
        hover "save_load"
        alpha True
    
        for i in range(gui.file_slot_rows * gui.file_slot_cols):

            hotspot(*param[i], config.thumbnail_width+6, config.thumbnail_height+6):
                hover_sound None
                activate_sound None
                action If(current_slot == "Загрузить", FileLoad(i), FileSave(i))

                add FileScreenshot(i) pos(3, 3) at file_screen
                key "save_delete" action FileDelete(i)
            
            vbox xysize(140, 200):
                style_prefix "save_load_other"
                pos(param[i][0] + config.thumbnail_width + 15, param[i][1] + 10)

                $ file_time = FileTime(i, empty=_("Слот пуст"))
                $ save_name = FileSaveName(i)
                $ number_of_del = i

                text "[file_time!t]\n[save_name!t]"

                if file_time != _("Слот пуст"):
                    frame background Null() yalign 1.0 padding(12, 12, 12, 12):
                        textbutton _("УДАЛИТЬ") background Null() action FileDelete(number_of_del) at btn_shaking
    
        hotspot (724, 821, 188, 88) action FilePagePrevious(quick=False) at hotspot_shaking(724, 821)
        hotspot (986, 821, 188, 88) action FilePageNext(100) at hotspot_shaking(986, 821)
        hotspot (1673, 821, 108, 88) action Return() at hotspot_shaking(1673, 821)
    
    text FilePageName() color "#ffffff" min_width 100 align(0.495, 0.825) at save_elements

    key "game_menu" action Return()

    on "show" action Play("sfx_five", "sounds/menu/menu_save_load.ogg")
    on "replace" action [Play("sfx_five", "sounds/menu/menu_save_load.ogg"), Show("block_screen"), SetVariable("current_slot", title)]
    timer 1.0 action Hide("block_screen")

################################################################################
## Настройки
################################################################################

screen preferences():
    style_prefix "pref" tag menu

    add "bg_menu_preferences" at conf_fon
    
    add "line" at other_elements
    add "chains_frame" at other_elements
    add "snow_frame" at other_elements
    add "fog_frame" at other_elements

    text _("НАСТРОЙКИ") style "title" at other_elements

    if renpy.variant("touch"):
        use preferences_android
    else:
        use preferences_PC
    
    frame align(0.5, 0.9) at other_elements:
        imagebutton idle "button_back" action Return() at btn_shaking

    key "game_menu" action Return()

    on "show" action Play("sfx_five", "sounds/menu/menu_preferences.ogg")
    on "replace" action [Show("block_screen"), Play("sfx_five", "sounds/menu/menu_preferences.ogg")]
    timer 1.0 action Hide("block_screen")

## Для ПК
screen preferences_PC():

    vbox align (0.2, 0.4) first_spacing 50 spacing 20 at other_elements:

        text _("Громкость") size 55 xalign 0.5
        
        for k, v in {"main": "Общее", "music": "Музыка", "sfx": "Звук", "voice": "Голос"}.items():

            hbox:
                frame xysize(120, 100):
                    text _(v) yalign 0.5

                frame xysize(400, 90):
                    background Frame("pref_frame")
                    bar value Preference("%s volume" % k)
                
                frame xysize(50, 100):
                    text _("%.0f%%" % (preferences.get_mixer(k) * 100)) yalign 0.5
    
    vbox align (0.73, 0.65) first_spacing 50 spacing 20 at other_elements:

        text _("Скорость") size 55 xalign 0.5
        
        for k, v in {"text speed": "Текст", "auto-forward time": "Авточтение"}.items():
            hbox:
                frame xysize(180, 100):
                    text _(v) yalign 0.5

                frame xysize(400, 90):
                    background Frame("pref_frame")
                    bar value Preference(k)
                
                frame xysize(50, 100):
                    text _("%.0f" % (preferences.afm_time, preferences.text_cps)[v == "Текст"]) yalign 0.5
          
    vbox align(0.58, 0.2) first_spacing 50 at other_elements:
        style_prefix "pref_btn"

        text _("Режим") size 55 xalign 0.5 color "#ffffff"

        vbox:
            button at mm_but:
                add Frame("bg_button") at but_bg
                text _("Оконный")
                action Preference("display", "any window")
            button at mm_but:
                add Frame("bg_button") at but_bg
                text _("Полноэкранный")
                action Preference("display", "fullscreen")               
    
    vbox align(0.83, 0.2) first_spacing 50 at other_elements:
        style_prefix "pref_btn"

        text _("Пропуск") size 55 xalign 0.5 color "#ffffff"

        vbox:
            button at mm_but:
                add Frame("bg_button") at but_bg
                text _("Весь текст")
                action Preference("skip", "all")
            button at mm_but:
                add Frame("bg_button") at but_bg
                text _("Прочитанный")
                action Preference("skip", "seen")

## Для андроид
screen preferences_android():

    vbox align(0.2, 0.5) spacing 50 at other_elements:

        text _("Громкость") size 55 xalign 0.5 
    
        hbox spacing 20:

            for k, v in {"main": "Общее", "music": "Музыка", "sfx": "Звук", "voice": "Голос"}.items():
                vbox:

                    frame xysize(150, 50):
                        text _("%.0f%%" % (preferences.get_mixer(k) * 100)) xalign 0.5

                    frame xysize(130, 400):
                        background Frame("pref_frame_android")
                        vbar value Preference("%s volume" % k)
                    
                    frame xysize(150, 100):
                        text _(v) xalign 0.5

    vbox align(0.82, 0.5) spacing 50 at other_elements:

        text _("Скорость") size 55 xalign 0.5 
    
        hbox spacing 20:

            for k, v in {"text speed": "Текст", "auto-forward time": "Авточтение"}.items():
                vbox:

                    frame xysize(150, 50):
                        text _("%.0f" % (preferences.afm_time, preferences.text_cps)[v == "Текст"]) xalign 0.5

                    frame xysize(130, 400):
                        background Frame("pref_frame_android")
                        vbar value Preference(k)
                    
                    frame xysize(150, 100):
                        text _(v) xalign 0.5

    vbox align(0.6, 0.5) first_spacing 50 at other_elements:
        style_prefix "pref_btn"

        text _("Пропуск") size 55 xalign 0.5 color "#ffffff"

        vbox:
            button at mm_but:
                add Frame("bg_button") at but_bg
                text _("Весь текст")
                action Preference("skip", "all")
            button at mm_but:
                add Frame("bg_button") at but_bg
                text _("Прочитанный")
                action Preference("skip", "seen")

################################################################################
## Об авторах
################################################################################

screen about():
    style_prefix "about" tag menu

    add "bg_menu_about" at conf_fon
    add "line" at other_elements

    text _("ОБ АВТОРАХ") style "title" at other_elements
    
    vbox align(0.5, 0.6) spacing 5 first_spacing 50 at other_elements:
        text _("В разработка принимали участие:") xalign 0.5
        text _("Лидер:  Надежда Неустроева")
        text _("Сценаристы:  Влад Холодков, Николай Золичев, Никита Маршалл")
        text _("Писатели:  Евгений Сокарев, Максим Кабир")
        text _("Художники:  Надежда Неустроева, Айнур Мун, Лада Гончарова, Кирилл Филлипов, JUST HUMAN")
        text _("3D Модельер:  Сергей Яковцев")
        text _("Композиторы:  Глеб Аюпов, MIKINITZ, Даниил Турчик")
        text _("Программисты:  Анатолий Козлов, Даниил Горин")
        text _("Редакторы:  Надежда Неустроева, Никита Маршалл")
        text _("Корректор:  Надежда Неустроева\n\n")
        text _("Следите за обновлениями! :)\n") xalign 0.5

    frame align(0.9, 0.9) at other_elements:
        imagebutton idle "button_back" action Return() at btn_shaking

    key "game_menu" action Return()

    on "show" action Play("sfx_five", "sounds/menu/menu_other.ogg")
    on "replace" action [Show("block_screen"), Play("sfx_five", "sounds/menu/menu_other.ogg")]
    timer 1.0 action Hide("block_screen")

################################################################################
## Пауза
################################################################################

screen quick_menu():
    modal True tag menu style_prefix "quick" 
    
    add "bg_menu_quick"

    vbox align(0.475, 0.38) at qm_elements:
        button at mm_but:
            add Frame("bg_button") at but_bg
            text _("Продолжить")
            action [Return(), With(dissolve)]
        button at mm_but:
            add Frame("bg_button") at but_bg
            text _("Сохранить")
            action ShowMenu("file_slots", "Сохранить")
        button at mm_but:
            add Frame("bg_button") at but_bg
            text _("Загрузить")
            action ShowMenu("file_slots", "Загрузить")
        button at mm_but:
            add Frame("bg_button") at but_bg
            text _("Настройки")
            action ShowMenu("preferences")
        button at mm_but:
            add Frame("bg_button") at but_bg
            text _("В меню")
            action MainMenu(confirm=True)
        button at mm_but:
            add Frame("bg_button") at but_bg
            text _("Выход")
            action Quit(confirm=True)
    
    imagemap style_prefix "other_buttons":
        idle Null()
        hover im.MatrixColor("interface/quick_menu/other_buttons_black.png", im.matrix.contrast(0.75))

        hotspot (776, 714, 88, 140) action NullAction()
        hotspot (960, 712, 88, 142) action NullAction()
    
    on "show" action [Play("sfx_five", "sounds/menu/menu_pause.ogg"), Show("block_screen"), SetVariable("save_enable", True)]
    on "replace" action [Play("sfx_five", "sounds/menu/menu_pause.ogg")]
    timer 0.6 action Hide("block_screen")

################################################################################
## Диалоговое окно
################################################################################

screen say(who, what):
    style_prefix "say" zorder 3

    window:
        id "window"
        if who is not None:
            window style "namebox":
                id "namebox" 
                text who id "who" xpos 42
        text what id "what"
    
    use qq_menu

################################################################################
## Кнопки диалогового окна
################################################################################

screen qq_menu():
    style_prefix "qq" zorder 5

    hbox align(0.5, 0.99) spacing 190:

        button at qq_btn:
            background "q01"
            tooltip (570, __("ИСТОРИЯ"))
            action ShowMenu("history")
        
        button at qq_btn:
            background "q02"
            tooltip (800, __("АВТО"))
            action Preference("auto-forward", "toggle")

        button at qq_btn:
            background "q03"
            tooltip (1050, __("ПЕРЕМОТКА"))
            action Skip()

        button at qq_btn:
            background "q04"
            tooltip (1290, __("МЕНЮ"))
            action ShowMenu("quick_menu")
    
    button at qq_btn:
        background "q06"
        pos(1675, 850)
        tooltip ((1675, 870), __("СКРЫТЬ"))
        action [With(Dissolve(0.2)), HideInterface(), With(Dissolve(0.2))]
    
    $ tt = GetTooltip()
    if tt:
        if type(tt[0]) is tuple:
            text tt[1] pos(tt[0]) align(1.0, 0.5) size 38
        else:
            text tt[1] align(1.0, 0.99) yoffset 5 xpos tt[0] size 44

################################################################################
## История диалогов
################################################################################

screen history():
    style_prefix "history" tag menu
    modal True predict False

    add "bg_menu_anim" at conf_fon
    add "line" at other_elements
    
    text _("ИСТОРИЯ") style "title" at other_elements

    viewport xysize(1380, 850) align(0.5, 0.5) at other_elements:
        mousewheel True
        draggable True
        yinitial 1.0

        vbox spacing 60:
            for h in _history_list:

                hbox spacing 10:
                
                    if h.who:
                        label h.who:
                            text_color h.who_args.get("color")
                        vbox:
                            null height 70
                            text h.what
                    else:
                        text h.what
        
        if not _history_list:
            label _("История диалогов пуста.")
    
    frame align(0.95, 0.9) at other_elements:
        imagebutton idle "button_back" action Return() at btn_shaking
    
    on "show" action [Show("block_screen"), Play("sfx_five", "sounds/menu/menu_other.ogg")]
    timer 1.0 action Hide("block_screen")

################################################################################
## Индикатор пропуска
################################################################################

screen skip_indicator():
    zorder 100 style_prefix 'skip'

    frame at delayed_show:
        has hbox spacing 9

        text 'Пропускаю'
        text "▸" at delayed_blink(0.0, 1.0) font "DejaVuSans.ttf"
        text "▸" at delayed_blink(0.0, 1.0) font "DejaVuSans.ttf"
        text "▸" at delayed_blink(0.0, 1.0) font "DejaVuSans.ttf"
