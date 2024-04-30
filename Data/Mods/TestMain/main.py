#ВСЕ ФАЙЛЫ В ВАШЕЙ ПАПКЕ МОДА С НАЗВАНИЕМ main.py, load.py БУДУТ ЗАГРУЖАТЬСЯ НЕЗАВИСЕМО ОТ КОДА (ЕСЛИ НЕ НАЙДУТ СТРОКИ КОТОРЫЕ НЕДОПУСТИМЫ)
#ТО ЕСТЬ ЖЕЛАТЕЛЬНО НАДО ЧТОБЫ В ВАШЕЙ ПАПКЕ МОДА БЫЛ ТОЛЬКО 1 ФАЙЛ С НАЗВАНИЕМ main.py И load.py

#self — кот

#Создание новых собак
#Пояснение:
#CreateDog(Сколько дадут денег за убиство собаки, вес собаки (сложность), '(название собаки, должно быть уникальным иначе будут конфликты)', картинка собаки, жизни собаки, скорость, урон собаки, уникал собаки, перезарядка собаки такая же как у котов, тип собаки (0: по умолчанию если это обычная собака, 1: собака взрывается)) 
new_dog = CreateDog(3, 1, 'Dog', dog_image, 2, 2, 1, 1, 1, 0, 'Data/Img/Dog1.png', 60, 60)
new_dog = CreateDog(7, 5, 'FastDog', dog_image, 1, 4, 1, 1, 1, 0, 'Data/Img/Dog1.png', 60, 60)
new_dog = CreateDog(7, 5, 'BigDog', dog_image, 6, 1, 1, 1, 1, 0, 'Data/Img/Dog1.png', 60, 60)
new_dog = CreateDog(20, 10, 'KillerDog', dog_image, 4, 3, 4, 1, 1, 0, 'Data/Img/Dog1.png', 60, 60)
new_dog = CreateDog(100, 65, 'KiberDog', dog2_image, 40, 1, 6, 1, 1, 0, 'Data/Img/Dog2.png', 60, 60)
new_dog = CreateDog(300, 220, 'BoomDog', dog3_image, 7, 5, 20, 2, 1, 1, 'Data/Img/Dog3.png', 60, 60)
new_dog = CreateDog(100, 40, 'NecDog', dog_image, 15, 1, 2, 3, 2, 0, 'Data/Img/Dog1.png', 60, 60)
new_dog = CreateDog(5000, 1500, 'MehoDog', dog4_image, 320, 1, 30, 6, 1, 0, 'Data/Img/Dog4.png', 60, 60)
new_dog = CreateDog(1000, 1500, 'BomberDog', dog5_image, 400, 2, 100, 9, 1, 2, 'Data/Img/Dog5.png', 60, 60)
new_dog.damagecats.append(1)
new_dog.damagecats.append(2)
new_dog = CreateDog(10000, 8400, 'TrojanDog', dog6_image, 1000, 1, 0, 10, 1, 0, 'Data/Img/Dog6.png', 60, 60)
#Создание новых котов
#Пояснение:
#BuyCat('Название переменной с иконкой покупки кота, Стоимость кота, f"Описание кота (когда пишите про урон пишите так {1+cats_boost} урон)", Картинка самого кота на поле боя, Радиус поражения собак, Жизни кота, Максимальное количество собак которым можно нанести урон за удар, Тип перезарядки (1:удар каждую секунду, 2:удар каждые 3 секунды, 3:удар каждые пол секунды, 4:каждую волну, 5:каждую мега волну), урон, супер кота (1:Обычный кот,2:Приносит {self.damage+cat_works_boost}$ за волну место удара),3: Усиливает удар курсором на self.damage,4: Востанавливает всем котам в его радиусе востанавливает он self.damage', на какой волне появится кот, на какой волне пропадает (-1: он не пропадёт не когда))
new_buy_cat = BuyCat(cat_image, 10, f'4 жизни, атакует 2 собаки за раз, средняя перезарядка, {1+cats_boost} урон', cat_image, 130, 4, 3, 1, 1, 1, 0, 10, 'Data/Img/Cat1.png', 60, 60)
new_buy_cat = BuyCat(cat2_image, 20, "40 жизни, не атакует собак", cat2_image, 0, 40, 0, 1, 0, 1, 0, 45, 'Data/Img/Cat2.png', 60, 60)
new_buy_cat = BuyCat(cat3_image, 200, f'6 жизней, атакует 3 собаки за раз, долгая перезарядка, {10+cats_boost} урон', cat3_image, 400, 6, 3, 2, 10, 1, 20, -1, 'Data/Img/Cat3.png', 60, 60)
new_buy_cat = BuyCat(cat4_image, 80, f'20 жизнь, атакует 3 собаки за раз, быстрая перезарядка, {1.5+cats_boost} урон', cat4_image, 150, 20, 3, 3, 1.5, 1, 10, -1, 'Data/Img/Cat4.png', 60, 60)
new_buy_cat = BuyCat(cat5_image, 70, f'15 жизней, не атакует собак, но зар  абатывает {10+cat_works_boost}$ каждую волну', cat5_image, 0, 15, 0, 4, 10, 2, 5, -1, 'Data/Img/Cat5.png', 60, 60)
new_buy_cat = BuyCat(cat6_image, 10000, f'80 жизней, не атакует собак, усиливает атаку курсором игрока', cat6_image, 0, 80, 0, 1, 0.1, 3, 30, -1, 'Data/Img/Cat6.png', 60, 60)
new_buy_cat = BuyCat(cat7_image, 300, f'60 жизней, не атакует собак, лечит котов в его радиусе', cat7_image, 160, 60, 9999, 2, 0.3, 4, 25, -1, 'Data/Img/Cat7.png', 60, 60)
new_buy_cat = BuyCat(cat8_image, 600, f'60 жизней, атакует 1 собаки за раз, быстрая перезарядка, \nбьёт только взрывучих или в полёте собак, {150+cats_boost} урон', cat8_image, 300, 60, 1, 3, 150, 1, 15, -1, 'Data/Img/Cat8.png', 120, 60)
new_buy_cat.blacklist.append(1)
new_buy_cat.blacklist.append(2)
new_buy_cat = BuyCat(cat9_ico_image, 500, f'30 жизней, атакует 1 собаки за раз, долгая перезарядка, {100+cats_boost} урон', cat9_image, 500, 30, 1, 2, 100, 1, 40, -1, 'Data/Img/Cat9.png', 60, 60)
new_buy_cat = BuyCat(cat10_image, 99999, "1000 жизней, собака получает 5% урона при нападение на кота", cat10_image, 0, 1000, 0, 1, 5, 5, 45, -1, 'Data/Img/Cat10.png', 60, 60)
new_buy_cat = BuyCat(cat11_image, 300, f'80 жизней, не атакует собак, лечит котов в его радиусе', cat11_image, 200, 80, 9999, 1, 0.3, 4, 35, -1, 'Data/Img/Cat11.png', 60, 60)
new_buy_cat = BuyCat(cat12_image, 50, f'1 жизнь, атакует 1 собаки за раз, быстрая перезарядка,\nпри получения урона собака получается урон 50% от своего хп', cat12_image, 0, 1, 1, 3, 98, 5, 5, -1, 'Data/Img/Cat12.png', 60, 60)

#Загрузка бонусов
bad_list.extend(['собаки наносят больше урона', 'игра станет сложнее', 'всем котам на поле боя нанесут 10 урона', '-1000$'])
good_list.extend(['+1000$', '+1 главных сердец', '+30 жизней каждому коту на поле боя', 'Игра станет легче', 'Коты работники дают на 5$ больше', 'Коты наносят больше урона'])

#ПРИ СОЗДАНИЕ МОДОВ УДАЛЯЙТЕ ВСЁ ЛИШНЕЕ ТАК КАК ВАШ МОД МОЖЕТ НЕ ЗАПУСТИТСЯ ИЛИ КОНФЛИКТОВАТЬ С ДРУГИМИ

#Загрузка скриптов, в папке scirpts есть api по этому
Script('Data\\Mods\\Main\\Scripts\\cat_supers.py', 'remove_dogs_periodically')
Script('Data\\Mods\\Main\\Scripts\\dog_supers_attack.py', 'attack_dog')
Script('Data\\Mods\\Main\\Scripts\\dog_supers_bump.py', 'bump_dog')
Script('Data\Mods\\Main\\Scripts\\dog_supers_info.py', 'info_dog')
Script('Data\\Mods\\Main\\Scripts\\dog_supers_move.py', 'move_dog')