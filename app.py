import PySimpleGUI as sg
import os
import sys
from utils.music_utilities import get_files_inside_directory_not_recursive, play_sound, is_sound_playing, pause_sounds, stop_sounds, unpause

# ===== PASSO 2: FUNÇÃO RESOURCE_PATH (compatível com PyInstaller) =====
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

sg.theme('Reddit')

# ========== Imagens com path relativo corrigido ==========
GO_BACK_IMAGE_PATH = resource_path('Images/back.png')
GO_FORWARD_IMAGE_PATH = resource_path('Images/next.png')
PLAY_SONG_IMAGE_PATH = resource_path('Images/play_button.png')
PAUSE_SONG_IMAGE_PATH = resource_path('Images/pause.png')
ALBUM_COVER_IMAGE_PATH = resource_path('Images/pylot.png')

# ===== Layout da Interface =====
song_title_column = [
    [sg.Text(text='Press play..', justification='center', background_color='black',
             text_color='white', size=(200, 0), font='Tahoma', key='song_name')]
]

player_info = [
    [sg.Text('PySimpleGUI Player - By youtube.com/devaprender',
             background_color='black', text_color='white',  font=('Tahoma', 7))]
]

currently_playing = [
    [sg.Text(background_color='black', size=(200, 0), text_color='white',
             font=('Tahoma', 10), key='currently_playing')]
]

main = [
    [sg.Canvas(background_color='black', size=(480, 20), pad=None)],
    [sg.Column(layout=player_info, justification='c',
               element_justification='c', background_color='black')],
    [
        sg.Canvas(background_color='black', size=(40, 350), pad=None),
        sg.Image(filename=ALBUM_COVER_IMAGE_PATH,
                 size=(350, 350), pad=None),
        sg.Canvas(background_color='black', size=(40, 350), pad=None)
    ],
    [sg.Canvas(background_color='black', size=(480, 10), pad=None)],
    [sg.Column(song_title_column, background_color='black',
               justification='c', element_justification='c')],
    [sg.Text('_'*80, background_color='black', text_color='white')],
    [
        sg.Canvas(background_color='black', size=(99, 200), pad=(0, 0)),
        sg.Image(pad=(10, 0), filename=GO_BACK_IMAGE_PATH, enable_events=True,
                 size=(35, 44), key='previous', background_color='black'),
        sg.Image(filename=PLAY_SONG_IMAGE_PATH,
                 size=(64, 64), pad=(10, 0), enable_events=True, key='play', background_color='black'),
        sg.Image(filename=PAUSE_SONG_IMAGE_PATH,
                 size=(58, 58), pad=(10, 0), enable_events=True, key='pause', background_color='black'),
        sg.Image(filename=GO_FORWARD_IMAGE_PATH, enable_events=True,
                 size=(35, 44), pad=(10, 0), key='next', background_color='black'),
    ],
    [sg.Column(layout=currently_playing, justification='c',
               element_justification='c', background_color='black', pad=None)]
]

window = sg.Window('Spotify', layout=main, size=(480, 730),
                   background_color='black', finalize=True, grab_anywhere=True, resizable=False)

# === Seleção da pasta de músicas ===
# Define caminho automático para músicas dentro do executável ou pasta local
MUSIC_FOLDER = resource_path("Music")

# Verifica se o diretório existe
if not os.path.exists(MUSIC_FOLDER):
    sg.popup_error("A pasta de músicas não foi encontrada!")
    sys.exit(1)

songs_in_directory = get_files_inside_directory_not_recursive(MUSIC_FOLDER)

songs_in_directory = get_files_inside_directory_not_recursive(MUSIC_FOLDER)
song_count = len(songs_in_directory)
current_song_index = 0

def update_song_display():
    window['song_name'].update(os.path.basename(
        songs_in_directory[current_song_index]))
    window['currently_playing'].update(
        f'Playing: {os.path.basename(songs_in_directory[current_song_index])}')

# === Loop de eventos ===
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'play':
        if not is_sound_playing():
            play_sound(songs_in_directory[current_song_index])
            update_song_display()

    elif event == 'pause':
        if is_sound_playing():
            pause_sounds()
        else:
            unpause()

    elif event == 'next':
        if current_song_index + 1 < song_count:
            stop_sounds()
            current_song_index += 1
            play_sound(songs_in_directory[current_song_index])
            update_song_display()
        else:
            print('Reached last song')

    elif event == 'previous':
        if current_song_index > 0:
            stop_sounds()
            current_song_index -= 1
            play_sound(songs_in_directory[current_song_index])
            update_song_display()
        else:
            print('Reached first song')
