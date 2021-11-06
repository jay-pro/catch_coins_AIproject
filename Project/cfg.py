import os

IMAGE_PATHS = {
    'gold': os.path.join(os.getcwd(), 'D:/18110168_GITHUBS/catch_coins_AIproject/Project/resources/images/gold.png'),
    'apple': os.path.join(os.getcwd(), 'D:/18110168_GITHUBS/catch_coins_AIproject/Project/resources/images/apple.png'),
    'background': os.path.join(os.getcwd(), 'D:/18110168_GITHUBS/catch_coins_AIproject/Project/resources/images/background.jpg'),
    'hero': [os.path.join(os.getcwd(), 'D:/18110168_GITHUBS/catch_coins_AIproject/Project/resources/images/%d.png' % i) for i in range(1, 11)]
}

AUDIO_PATHS = {
    'bgm': os.path.join(os.getcwd(), 'D:/18110168_GITHUBS/catch_coins_AIproject/Project/resources/audios/bgm.mp3'),
    'get': os.path.join(os.getcwd(), 'D:/18110168_GITHUBS/catch_coins_AIproject/Project/resources/audios/get.wav'),
}

FONT_PATH = os.path.join(os.getcwd(), 'D:/18110168_GITHUBS/catch_coins_AIproject/Project/resources/font/font.TTF')

HIGHEST_SCORE_RECORD_FILEPATH = 'D:/18110168_GITHUBS/catch_coins_AIproject/Project/highest.rec'

SCREENSIZE = (800, 600)

BACKGROUND_COLOR = (0, 160, 233)

FPS = 30
