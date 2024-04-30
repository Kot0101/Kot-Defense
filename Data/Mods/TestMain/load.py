#ВСЕ ФАЙЛЫ В ВАШЕЙ ПАПКЕ МОДА С НАЗВАНИЕМ main.py, load.py БУДУТ ЗАГРУЖАТЬСЯ НЕЗАВИСЕМО ОТ КОДА (ЕСЛИ НЕ НАЙДУТ СТРОКИ КОТОРЫЕ НЕДОПУСТИМЫ)
#ТО ЕСТЬ ЖЕЛАТЕЛЬНО НАДО ЧТОБЫ В ВАШЕЙ ПАПКЕ МОДА БЫЛ ТОЛЬКО 1 ФАЙЛ С НАЗВАНИЕМ main.py И load.py

#Этот файл нужен чтобы загрузить текстуры игры

#Установка картинок, в ващем случае надо писать Data/Mods/Название мода/Data/Название картинки.расширение
cat_image = pygame.image.load('Data/Img/Cat1.png')
cat2_image = pygame.image.load('Data/Img/Cat2.png')
cat3_image = pygame.image.load('Data/Img/Cat3.png')
cat4_image = pygame.image.load('Data/Img/Cat4.png')
cat5_image = pygame.image.load('Data/Img/Cat5.png')
cat6_image = pygame.image.load('Data/Img/Cat6.png')
cat7_image = pygame.image.load('Data/Img/Cat7.png')
cat8_image = pygame.image.load('Data/Img/Cat8.png')
cat9_image = pygame.image.load('Data/Img/Cat9.png')
cat9_ico_image = pygame.image.load('Data/Img/Cat9_ico.jpg')
cat10_image = pygame.image.load('Data/Img/Cat10.png')
cat11_image = pygame.image.load('Data/Img/Cat11.png')
cat12_image = pygame.image.load('Data/Img/Cat12.png')

dog_image = pygame.image.load('Data/Img/Dog1.png')
dog2_image = pygame.image.load('Data/Img/Dog2.jpg')
dog3_image = pygame.image.load('Data/Img/Dog3.png')
dog4_image = pygame.image.load('Data/Img/Dog4.png')
dog5_image = pygame.image.load('Data/Img/Dog5.png')
dog6_image = pygame.image.load('Data/Img/Dog6.png')

#Обработка картинок
cat_image = pygame.transform.scale(cat_image, (60, 60))
cat2_image = pygame.transform.scale(cat2_image, (60, 60))
cat3_image = pygame.transform.scale(cat3_image, (60, 60))
cat4_image = pygame.transform.scale(cat4_image, (60, 60))
cat5_image = pygame.transform.scale(cat5_image, (60, 60))
cat6_image = pygame.transform.scale(cat6_image, (60, 60))
cat7_image = pygame.transform.scale(cat7_image, (60, 60))
cat8_image = pygame.transform.scale(cat8_image, (60, 60))
cat9_image = pygame.transform.scale(cat9_image, (120, 60))
cat9_ico_image = pygame.transform.scale(cat9_ico_image, (60, 60))
cat10_image = pygame.transform.scale(cat10_image, (60, 60))
cat11_image = pygame.transform.scale(cat11_image, (60, 60))
cat12_image = pygame.transform.scale(cat12_image, (60, 60))

dog_image = pygame.transform.scale(dog_image, (60, 60))
dog2_image = pygame.transform.scale(dog2_image, (60, 60))
dog3_image = pygame.transform.scale(dog3_image, (60, 60))
dog4_image = pygame.transform.scale(dog4_image, (60, 60))
dog5_image = pygame.transform.scale(dog5_image, (60, 60))
dog6_image = pygame.transform.scale(dog6_image, (70, 70))

#загрузка звуков, музыки
# try:
#   "script sound"
# except:
#    pass
# try except обязательны при работе с звуками, иначе игра не будет работать если нет гарниторы для выдачи звуков
try:
    dog_bump = pygame.mixer.Sound('Data/Sounds/bump.mp3')
    boom = pygame.mixer.Sound('Data/Sounds/boom.mp3')
    click = pygame.mixer.Sound('Data/Sounds/click.mp3')
    sirena = pygame.mixer.Sound('Data/Sounds/sirena.mp3')
except:
    pass

#Обработка звуков и музыки
#Пояснение:
#global music_playing делает чтобы переменную music_playing могли использовать в любом месте кода (но надо в начале кода добавить music_playing)
#Для справки, все переменные сделаные здесь могут быть использованы в main.py без функции global
global music_playing
music_playing = True
try:
    dog_bump.set_volume(0.1)
    boom.set_volume(0.1)
except:
    pass