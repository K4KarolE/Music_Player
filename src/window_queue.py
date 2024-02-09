''' 
WINDOW QUEUE & SEARCH

Window title update to display the current track details
is declared in main / update_title_window_queue()
'''


from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QFrame,
    QTabWidget,
    QVBoxLayout,
    QScrollBar,
    QLineEdit,
    QListWidget
    )

from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from .list_widget_queue_window import MyQueueListWidget
from .cons_and_vars import cv
from .func_coll import (
 
    update_playing_playlist_vars_and_widgets,
 
    add_queue_window_list_widgets_header,
    get_playlist_details_from_queue_window_list,

    )
from .icons import MyIcon


class MyQueueWindow(QWidget):
    
    def __init__(self, play_track, playlists_all):
        super().__init__()
        self.play_track = play_track
        self.playlists_all = playlists_all
       
        WINDOW_WIDTH, WINDOW_HEIGHT = 700, 400
        WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT = 400, 200
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Sheet)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.setWindowIcon(MyIcon().queue_blue)
        self.setWindowTitle("Queue")
        
        

        TABS_POS_X, TABS_POS_Y  = 12, 12
        TABS_WIDTH = int(WINDOW_WIDTH - TABS_POS_X *2)
        TABS_HEIGHT = int(WINDOW_HEIGHT - TABS_POS_Y *2)
        tabs = QTabWidget()
        tabs.setFont(QFont('Verdana', 10, 500))
        tabs.resize(TABS_WIDTH, TABS_HEIGHT) 
        tabs.move(TABS_POS_X, TABS_POS_Y)
        tabs.setStyleSheet(
                        "QTabBar::tab:selected"
                            "{"
                            "background-color: #287DCC;" 
                            "color: white;"   # font
                            "border: 2px solid #F0F0F0;"
                            "border-radius: 4px;"
                            "padding: 6px"
                            "}"
                        "QTabBar::tab:!selected"
                            "{"
                            "background-color : QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 0.3 white, stop: 0.8 #C9C9C9, stop: 1 #C2C2C2);"
                            "color: black;"   # font
                            "border: 2px solid #F0F0F0;"
                            "border-radius: 4px;"
                            "padding: 6px"
                            "}"
                        "QTabWidget::pane"
                            "{" 
                            "position: absolute;"
                            "top: 0.3em;"
                            "border: 1px solid #C2C2C2;"
                            "border-radius: 2px;"
                            "}"
                        )
        
    
        
        ''' QUEUE TAB '''
        ''' 
        Lists -> QHBoxLayout -> QFrame -> 
        Add as a Tab --> Layout --> Window
        '''
        scroll_bar_else_ver = QScrollBar()
        scroll_bar_else_hor = QScrollBar()
        scroll_bar_duration_ver = QScrollBar()
        scroll_bar_duration_hor = QScrollBar()

        scroll_bar_else_ver.valueChanged.connect(scroll_bar_duration_ver.setValue)
        scroll_bar_duration_ver.valueChanged.connect(scroll_bar_else_ver.setValue)

        scroll_bar_else_ver.setStyleSheet(
                        "QScrollBar::vertical"
                            "{"
                            "width: 0px;"
                            "}"
                        )
        
        scroll_bar_else_hor.setStyleSheet(
                        "QScrollBar::horizontal"
                            "{"
                            "width: 0px;"
                            "}"
                        )
        
        scroll_bar_duration_ver.setStyleSheet(
                        "QScrollBar::vertical"
                            "{"
                            "width: 10px;"
                            "}"
                        )               
        
        scroll_bar_duration_hor.setStyleSheet(
                        "QScrollBar::horizontal"
                            "{"
                            "height: 0px;"
                            "}"
                        )
        
        
        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        for item in cv.queue_widget_dic:
            title = cv.queue_widget_dic[item]['list_widget_title']
            ratio = cv.queue_widget_dic[item]['list_widget_window_ratio']
            fixed_width = cv.queue_widget_dic[item]['fixed_width']
            
            cv.queue_widget_dic[item]['list_widget'] = MyQueueListWidget(self.play_list_item, self.playlists_all)
            list_widget = cv.queue_widget_dic[item]['list_widget']
            list_widget.itemDoubleClicked.connect(self.play_list_item)
            
            if fixed_width:
                list_widget.setFixedWidth(fixed_width)
            
            if item == 'duration_list_widget':
                list_widget.setVerticalScrollBar(scroll_bar_duration_ver)
                list_widget.setHorizontalScrollBar(scroll_bar_duration_hor)
            else:
                list_widget.setVerticalScrollBar(scroll_bar_else_ver)
                list_widget.setHorizontalScrollBar(scroll_bar_else_hor)
            

            add_queue_window_list_widgets_header(title, list_widget)
            layout.addWidget(list_widget, ratio)
        
        cv.queue_widget_dic['queue_list_widget']['list_widget'].currentRowChanged.connect(lambda: self.row_changed_sync('queue_list_widget'))
        cv.queue_widget_dic['name_list_widget']['list_widget'].currentRowChanged.connect(lambda: self.row_changed_sync('name_list_widget'))
        cv.queue_widget_dic['playlist_list_widget']['list_widget'].currentRowChanged.connect(lambda: self.row_changed_sync('playlist_list_widget'))
        cv.queue_widget_dic['duration_list_widget']['list_widget'].currentRowChanged.connect(lambda: self.row_changed_sync('duration_list_widget'))

        frame = QFrame()
        frame.setStyleSheet(
                        "QFrame"
                            "{"
                            "border: 0px;"
                            "}"
                        )
        frame.setLayout(layout)

        tabs.addTab(frame, 'Queue')



        
        

        
        '''
        ###################
            SEARCH TAB     
        ###################
        '''
        layout_search_base = QVBoxLayout()
        layout_search_base.setSpacing(0)
        layout_search_base.setContentsMargins(0, 0, 0, 0)

        layout_search_top = QHBoxLayout()
        layout_search_bottom = QHBoxLayout()

        layout_search_base.addLayout(layout_search_top, 10)
        layout_search_base.addLayout(layout_search_bottom, 90)


        ''' TOP WIDGETS '''
        search_line_edit = QLineEdit()



        ''' BOTTOM WIDGETS '''
        search_list_widget = QListWidget() #MyQueueListWidget(self.play_list_item, self.playlists_all)


        layout_search_top.addWidget(search_line_edit)
        layout_search_bottom.addWidget(search_list_widget)

        frame_search = QFrame()
        frame_search.setStyleSheet(
                        "QFrame"
                            "{"
                            "border: 0px;"
                            "}"
                        )
        frame_search.setLayout(layout_search_base)

        tabs.addTab(frame_search, 'Search')


        '''
        #################################
            TABS -> Layout -> Window
        #################################
        '''
        layout_window = QVBoxLayout(self)
        layout_window.addWidget(tabs)



    def play_list_item(self):
        current_row_index = cv.queue_widget_dic['name_list_widget']['list_widget'].currentRow() - 1
        playlist, playlist_index, track_index, queue_tracking_title = get_playlist_details_from_queue_window_list(current_row_index)
        cv.playing_playlist_index = playlist_index
        update_playing_playlist_vars_and_widgets()
        self.play_track(track_index)
    

    def row_changed_sync(self, list_widget_row_changed):
        current_row = cv.queue_widget_dic[list_widget_row_changed]['list_widget'].currentRow()
        for item in cv.queue_widget_dic:
            if item != list_widget_row_changed:
                if current_row == 0:    # first row: Order number, Title, Queue, Duration
                    color = '#D5DFE2'
                else:
                    color = '#CCE8FF'
                cv.queue_widget_dic[item]['list_widget'].setCurrentRow(current_row)
                cv.queue_widget_dic[item]['list_widget'].setStyleSheet(
                                                            "QListWidget::item:selected"
                                                                "{"
                                                                f"background: {color};" 
                                                                "color: black;"   
                                                                "}"
                                                            )


