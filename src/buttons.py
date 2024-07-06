'''
BUTTON FUNCTIONS DECLARED BELOW:
--------------------------------
- Add track
- Add directory
- Remove all tracks (Clear playlist) - *more added/compiled in MAIN

- Set button style/stylesheet functions

- Play/pause
- Play/pause via list
- Previous track
- Next track
- Toggle repeat
- Toggle shuffle



BUTTON FUNCTIONS DECLARED IN MAIN:
----------------------------------
- Remove track
- Settings
- Stop
- Toggle playlist
- Toogle video
- Duration info (text)
- Speaker / mute (picture)
'''


from PyQt6.QtWidgets import QFileDialog, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont


from .logger import logger_runtime
from .class_bridge import br
from .class_data import save_json, cv, settings, PATH_JSON_SETTINGS
from .func_coll import (
    add_record_grouped_actions,
    generate_duration_to_display,
    walk_and_add_dir,
    remove_track_from_playlist,
    remove_queued_tracks_after_playlist_clear,
    save_db,
    cur, # db
    connection, # db
    settings,   # json dic
    PATH_JSON_SETTINGS,
    )
from .message_box import MyMessageBoxWarning


ICON_SIZE = 20  # ICON/PICTURE IN THE BUTTONS


class MyButtons(QPushButton):
    def __init__(
            self,
            title,
            tooltip,
            icon = None):
        super().__init__()

        self.setText(title)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(tooltip)
        self.setToolTipDuration(2000)
        self.setFont(QFont('Times', 9, 600))
        if icon:
            self.setIcon(icon)
            self.setText(None)
            self.setIconSize(QSize(cv.icon_size, cv.icon_size))



    '''
    ########################
        PLAYLIST SECTION
    ########################
    '''
    ''' BUTTON PLAYLIST - ADD TRACK '''
    def button_add_track_clicked(self):
        ''' BUTTON - MUSIC '''
        dialog_add_track = QFileDialog()
        dialog_add_track.setWindowTitle("Select a media file")
        dialog_add_track.setNameFilters(cv.FILE_TYPES_LIST)
        dialog_add_track.exec()
        if dialog_add_track.result():
            add_record_grouped_actions(dialog_add_track.selectedFiles()[0])
            save_db()
            cv.active_pl_tracks_count = cv.active_pl_name.count()
        br.duration_sum_widg.setText(generate_duration_to_display(cv.active_pl_sum_duration))


    ''' BUTTON PLAYLIST - ADD DIRECTORY '''
    @logger_runtime
    def button_add_dir_clicked(self):
        dialog_add_dir = QFileDialog()
        dialog_add_dir.setWindowTitle("Select a directory")
        dialog_add_dir.setFileMode(QFileDialog.FileMode.Directory)
        dialog_add_dir.exec()
        if dialog_add_dir.result():
            walk_and_add_dir(dialog_add_dir.selectedFiles()[0])
        br.duration_sum_widg.setText(generate_duration_to_display(cv.active_pl_sum_duration))   


    ''' BUTTON PLAYLIST - REMOVE SINGLE TRACK '''
    def button_remove_single_track(self):
        if cv.active_pl_name.currentRow() > -1:
            remove_track_from_playlist()
            br.duration_sum_widg.setText(generate_duration_to_display(cv.active_pl_sum_duration))


    ''' BUTTON PLAYLIST - CLEAR PLAYLIST '''
    def button_remove_all_track(self):
        
        def clear_playlist():
            # QUEUE
            remove_queued_tracks_after_playlist_clear()
            # DB
            cur.execute("DELETE FROM {0}".format(cv.active_db_table))
            connection.commit()
            # PLAYLIST
            cv.active_pl_name.clear()
            cv.active_pl_queue.clear()
            cv.active_pl_duration.clear()
            # FOR SEARCH WINDOW
            cv.track_change_on_main_playlist_new_search_needed = True

        ''' Queued track in the playlist '''
        if cv.active_db_table in cv.queue_playlists_list:
            if MyMessageBoxWarning().clicked_continue():
                clear_playlist()
        else:
            clear_playlist()
        
        cv.playlist_widget_dic[cv.active_db_table]['active_pl_sum_duration'] = 0
        cv.active_pl_sum_duration = 0
        br.duration_sum_widg.setText(generate_duration_to_display(cv.active_pl_sum_duration))
        



    ''' BUTTON PLAYLIST - SET STYLE '''
    def set_style_playlist_buttons(self):
        self.setStyleSheet(
                        "QPushButton"
                            "{"
                            "background-color : QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 0.2 #F0F0F0, stop: 0.8 #F0F0F0, stop: 1 #C2C2C2);"
                            "color: grey;"   # font
                            "border: 1px solid grey;"
                            "border-radius: 4px;"
                            "margin: 3 px;" # 3 px != 3px
                            "}"
                        "QPushButton::pressed"
                            "{"
                            "background-color : #C2C2C2;"
                            "}"
                        )
    

    ''' BUTTON PLAYLIST - SETTINGS - SET STYLE '''
    def set_style_settings_button(self):
        self.setStyleSheet(
                        "QPushButton"
                            "{"
                            "background-color : QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 0.2 #F0F0F0, stop: 0.8 #F0F0F0, stop: 1 #C2C2C2);"
                            "color: grey;"   
                            "border: 1px solid grey;"
                            "border-radius: 4px;"
                            "margin: 3px;" # 3 px != 3px, diff. pre. style sheet
                            "}"
                        "QPushButton::pressed"
                            "{"
                            "background-color : #C2C2C2;"
                            "}"
                        )
    

    ''' BUTTON PLAYLIST - DURATION INFO - SET STYLE '''
    def set_style_duration_info_button(self):
        self.setFont(QFont('Times', 14, 600))
        self.setFlat(1)
        self.setStyleSheet(
                        "QPushButton"
                            "{"
                            "color: grey;"   
                            "}"
                        )


    ''' 
    #####################
        PLAY SECTION    
    #####################
    '''
    ''' BUTTON PLAY SECTION - PLAY / PAUSE '''
    def button_play_pause_clicked(self):
        if br.av_player.player.isPlaying():
            br.av_player.player.pause()
            br.av_player.paused = True
            self.setIcon(br.icon.start)
            br.av_player.screen_saver_on()
        elif br.av_player.paused:
            br.av_player.player.play()
            br.av_player.paused = False
            self.setIcon(br.icon.pause)
            br.av_player.screen_saver_on_off()
        elif not br.av_player.player.isPlaying() and not br.av_player.paused:
            br.play_funcs.play_track()
            if br.av_player.player.isPlaying(): # ignoring empty playlist
                self.setIcon(br.icon.pause)
        
    
    # TRIGGERED BY THE DOUBLE-CLICK IN THE PLAYLIST
    def button_play_pause_via_list(self):
        self.setIcon(br.icon.pause)
        br.play_funcs.play_track()
    

    ''' BUTTON PLAY SECTION - PREVIOUS TRACK '''
    def button_prev_track_clicked(self):
        if cv.playing_track_index == None:
            cv.playing_track_index = cv.playing_pl_name.currentRow() 
        if cv.playing_pl_name.count() > 0:
            if cv.playing_track_index != 0:
                cv.playing_track_index -= 1
                br.play_funcs.play_track(cv.playing_track_index)
            else:
                cv.playing_track_index = cv.playing_pl_name.count() - 1
                br.play_funcs.play_track(cv.playing_track_index)
    

    ''' BUTTON PLAY SECTION - NEXT TRACK '''
    def button_next_track_clicked(self):
        br.play_funcs.play_next_track()
    

    ''' BUTTON PLAY SECTION - TOGGLE REPEAT PLAYLIST '''
    def button_toggle_repeat_pl_clicked(self):
        cv.repeat_playlist =  (cv.repeat_playlist + 1) % 3
        
        # NO REPEAT
        if cv.repeat_playlist == 1:
            self.setFlat(0)
            self.setIcon(br.icon.repeat)
            br.av_player.text_display_on_video(1500, 'Repeat: OFF') 
        # REPEAT PLAYLIST
        elif cv.repeat_playlist == 2:
            self.setFlat(1)
            br.av_player.text_display_on_video(1500, 'Repeat: Playlist') 
        # REPEAT SINGLE TRACK
        else:
            self.setIcon(br.icon.repeat_single)
            br.av_player.text_display_on_video(1500, 'Repeat: Single track') 
        
        settings['repeat_playlist'] = cv.repeat_playlist
        save_json(settings, PATH_JSON_SETTINGS)
    

    ''' BUTTON PLAY SECTION - TOGGLE SHUFFLE PLAYLIST '''
    def button_toggle_shuffle_pl_clicked(self):
        if cv.shuffle_playlist_on:
            cv.shuffle_playlist_on = False
            self.setFlat(0)
            br.av_player.text_display_on_video(1500, 'Shuffle: OFF')            
        else:
            cv.shuffle_playlist_on = True
            self.setFlat(1)
            br.av_player.text_display_on_video(1500, 'Shuffle: ON') 
        
        settings['shuffle_playlist_on'] = cv.shuffle_playlist_on
        save_json(settings, PATH_JSON_SETTINGS)
    