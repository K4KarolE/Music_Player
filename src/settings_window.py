from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLineEdit,
    QLabel,
    QTabWidget
    )

from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt

from pathlib import Path

from .cons_and_vars import cv, settings, PATH_JSON_SETTINGS
from .cons_and_vars import save_json
from .func_coll import inactive_track_font_style
from .message_box import MyMessageBoxError



class MySettingsWindow(QWidget):
    
    
    def __init__(self):
        super().__init__()

        ''' WINDOW '''
        WINDOW_WIDTH, WINDOW_HEIGHT = 250, 530
        
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Sheet)
        self.setFixedWidth(WINDOW_WIDTH)
        self.setFixedHeight(WINDOW_HEIGHT)
        self.setWindowIcon(QIcon(str(Path(Path().resolve(), 'skins', cv.skin_selected, 'settings.png'))))
        self.setWindowTitle("Settings")


        ''' TABS '''
               
        TABS_POS_X = 10
        TABS_POS_Y = 10

        tabs = QTabWidget(self)
        tabs.setFont(QFont('Times', 10, 500))
        tabs.resize(WINDOW_WIDTH-TABS_POS_X*2, WINDOW_HEIGHT-TABS_POS_Y*6) 
        tabs.move(TABS_POS_X+2, TABS_POS_Y+2)
        tabs.setStyleSheet(
                        "QTabBar::tab:selected"
                            "{"
                            "background: #287DCC;" 
                            "color: white;"   # font
                            "}"
                        )

        tab_playlist = QWidget() 
        tab_general = QWidget()
        tab_hotkey = QWidget()

        tabs.addTab(tab_playlist, 'Playlists')
        tabs.addTab(tab_general, 'General')
        tabs.addTab(tab_hotkey, 'Hotkeys')


        ''' TAB - GENEREAL '''
        WIDGET_GENERAL_POS_X=45
        widget_general_pos_y=30
        WIDGET_GENERAL_POS_Y_DIFF = 60
        LABEL_LINE_EDIT_POS_Y_DIFF = 25

        for item in cv.general_settings_dic:
            item_text = cv.general_settings_dic[item]['text']
            item_value = cv.general_settings_dic[item]['value']
            # item_line_edit_widget = cv.general_settings_dic[item]['line_edit_widget']

            item_label = QLabel(tab_general, text=item_text)
            item_label.setFont(inactive_track_font_style)
            item_label.move(WIDGET_GENERAL_POS_X, widget_general_pos_y)

            cv.general_settings_dic[item]['line_edit_widget'] = QLineEdit(tab_general)
            cv.general_settings_dic[item]['line_edit_widget'].setText(str(int(item_value/1000)))
            cv.general_settings_dic[item]['line_edit_widget'].setFont(inactive_track_font_style)
            cv.general_settings_dic[item]['line_edit_widget'].setAlignment(Qt.AlignmentFlag.AlignCenter)
            cv.general_settings_dic[item]['line_edit_widget'].setGeometry(
                WIDGET_GENERAL_POS_X + 10,
                widget_general_pos_y + LABEL_LINE_EDIT_POS_Y_DIFF,
                120,
                20
                )

            widget_general_pos_y += WIDGET_GENERAL_POS_Y_DIFF
        
        def general_fields_validation(pass_validation = True):
            for item in cv.general_settings_dic:
                line_edit_text = cv.general_settings_dic[item]['line_edit_widget'].text()
                if not line_edit_text.isdecimal():
                    pass_validation = False
            if not pass_validation:
                MyMessageBoxError('GENERAL TAB', 'The jump values need to be integers!')
                return False
            else:
                return True
        
        def general_fields_to_save(to_save = False):
            for item in cv.general_settings_dic:
                if settings['general_settings'][item] != int(cv.general_settings_dic[item]['line_edit_widget'].text())*1000:
                    settings['general_settings'][item] = int(cv.general_settings_dic[item]['line_edit_widget'].text())*1000
                    to_save = True
            return to_save
            


        ''' TAB - PLAYLISTS '''
        WIDGET_PL_POS_X=25
        widget_pl_pos_y=25
        number_counter = 1

        for pl in cv.paylist_widget_dic:
            number = QLabel(tab_playlist, text=f'{number_counter}.')
            number.setFont(inactive_track_font_style)
            
            if number_counter >= 10:
                number.move(WIDGET_PL_POS_X - 7, widget_pl_pos_y)
            else:
                number.move(WIDGET_PL_POS_X, widget_pl_pos_y)

            cv.paylist_widget_dic[pl]['line_edit'] = QLineEdit(tab_playlist)
            cv.paylist_widget_dic[pl]['line_edit'].setText(settings[pl]['tab_title'])
            cv.paylist_widget_dic[pl]['line_edit'].setGeometry(WIDGET_PL_POS_X + 20, widget_pl_pos_y, 150, 20)
            cv.paylist_widget_dic[pl]['line_edit'].setFont(inactive_track_font_style)
            cv.paylist_widget_dic[pl]['line_edit'].setAlignment(Qt.AlignmentFlag.AlignCenter)

            number_counter += 1
            widget_pl_pos_y += 40
        
        

        ''' BUTTON - SAVE'''
        BUTTON_SAVE_WIDTH = 50
        BUTTON_SAVE_HIGHT = 25
        BUTTON_SAVE_POS_X = WINDOW_WIDTH - TABS_POS_X - BUTTON_SAVE_WIDTH
        BUTTON_SAVE_POS_Y = WINDOW_HEIGHT - TABS_POS_Y - BUTTON_SAVE_HIGHT

        def is_at_least_one_playlist_title_kept():
            pl_list_with_title = []
            for pl in cv.paylist_widget_dic:
                playlist_title = cv.paylist_widget_dic[pl]['line_edit'].text().strip()
                if len(playlist_title) != 0:
                    pl_list_with_title.append(pl)
            if len(pl_list_with_title) == 0:
                MyMessageBoxError('PAYLISTS TAB', 'At least one playlist title needed!')
                return pl_list_with_title
            else:
                return pl_list_with_title

    
        def button_save_clicked(to_save = False):
                
            pl_list_with_title = is_at_least_one_playlist_title_kept()
            
            if pl_list_with_title and general_fields_validation():

                ''' GENERAL TAB FIELDS '''
                to_save = general_fields_to_save()

                ''' PAYLISTS TAB FIELDS '''
                for pl in cv.paylist_widget_dic:
                    playlist_title = cv.paylist_widget_dic[pl]['line_edit'].text().strip()
                    
                    if playlist_title != settings[pl]['tab_title']:
                        settings[pl]['tab_title'] = playlist_title
                        to_save = True

                ''' IF THE LAST USED TAB/PLAYLIST REMOVED '''
                if  len(settings[cv.paylist_list[cv.active_tab]]['tab_title']) == 0:
                    cv.active_tab = settings[pl_list_with_title[-1]]['tab_index']
                    settings['last_used_tab'] = cv.active_tab
                    to_save = True

                if to_save:
                    save_json(settings, PATH_JSON_SETTINGS)
            
                self.hide()


        button_save = QPushButton(self, text='SAVE')
        button_save.setGeometry(BUTTON_SAVE_POS_X, BUTTON_SAVE_POS_Y, BUTTON_SAVE_WIDTH, BUTTON_SAVE_HIGHT)    
        button_save.clicked.connect(button_save_clicked)
