# YPTeam_samolet
Team repository for [Urbancode Hakatone](https://changellenge.com/championships/urbancode/)

Структура репозитория:
- /app - инференс модели (в рамках хакатона был стандартизован)
- /coco_scrypts - скрипты и функции для работы с разметкой CoCo
- /notebooks - ноутбуки с экспериментами
- /pictures - рисунки для readme
____________
## Постановка задачи

Анализ готовности многоквартирных домов по изображениям с камер наблюдения. Есть датасет из 252 изображений с Сoco- разметкой по ячейкам 3 типов готовности (epmty, window, filled) и около 200 изображений без разметки. Нужно научиться на аналогичных фотографиях находить ячейки и определять их тип. Целевая метрика mAP50. [Подробности](https://jonathan-hui.medium.com/map-mean-average-precision-for-object-detection-45c121a31173)

<img src="https://github.com/fedor-konovalenko/YPTeam_samolet/blob/main/pictures/0000007202building.jpg" width="750" height="500">

*Пример изображения*

## Дополнительные данные

Поскольку фотографий в исходном датасете мало, и могие фотографии в нем повторяются, были вручную размечены фотографии из неразмеченного датасета, а также сгенерированы изображения строящихся зданий, например, с помощьью [kandinsky.ai](https://fusionbrain.ai/en/editor/). 

<img src="https://github.com/fedor-konovalenko/YPTeam_samolet/blob/main/pictures/00012-3676209845.png" width="750" height="500">

<img src="https://github.com/fedor-konovalenko/YPTeam_samolet/blob/main/pictures/Untitled.jpeg" width="750" height="500">

*Сгенерированные изображения*

## Предобработка данных

При предобработке изображений изображения нормализовывались, корректировалась констрастность, выполнялся поворот на угол до 15 градусов (отклонение от горизонта, характерное для камер наблюдения). Попытки коррекции искажения типа "эффект рыбьего глаза" успеха не имели: [средствами opencv решить проблему не удалось. сетка, по которой производится undistortion хорошо строится на шахматной доске, но не строится на доме](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html).

## Рассмотренные модели

- Использование предобученных детекторов, тюнинг и дообучение их на имеющихся данных
- Использование OpenCV и классификатора

## Результаты

### Предобученные детекторы

|Модель|mAP@50|
|-----|----|
|SSD300-VGG16|0,15|
|Faster-RCNN|0,20|
|SSD300-Mobilenet|0,05|

<img src="https://github.com/fedor-konovalenko/YPTeam_samolet/blob/main/pictures/ssd300.jpg" width="750" height="500">

*Пример работы SSD300-VGG16*

### OpenCV + ResNet18

Обучение
- Обрезка изображения по контурам из имеющейся разметки до отдельных ячеек
- Дообучение ResNet18 для классификации ячеек (из данных получено 40000 ячеек)

Инференс
- Предобработка изображения OpenCV для поиска контуров
- Обрезка по ячейкам
- Классификация ячейки

<img src="https://github.com/fedor-konovalenko/YPTeam_samolet/blob/main/pictures/Untitl1ed.png" width="750" height="500">

<img src="https://github.com/fedor-konovalenko/YPTeam_samolet/blob/main/pictures/33.jpeg" width="750" height="500">

*Результат поиска контуров ячеек*

<img src="https://github.com/fedor-konovalenko/YPTeam_samolet/blob/main/pictures/Screenshot_2023-09-23_23-38-55.png" width="250" height="500">

*Предобработка обрезанных ячеек*

<img src="https://github.com/fedor-konovalenko/YPTeam_samolet/blob/main/pictures/Screenshot_2023-09-23_23-39-19.png" width="250" height="500">

*Результат классификации*

При детектировании ячеек таким способом метрика mAP не измерялась, однако, точность классификации составила 98% на валидационной выборке.

## Выводы

ПОлученные в заданные сроки результаты оставляют желать лучшего, однако могут быть намечены следующие пути совершенствования:
- сбор или генерация и разметка дополнительных данных
- отказ от open cv в версии с двумя моделями в пользу более точного способа поиска контуров не проемов, а именно ячеек
- использование моделей детекции, требующих больше вычислительных ресурсов, чем расссмотренные.

## Список источников

Примеры использования моделей- детекторов:
- [раз](https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html)
- [два](https://habr.com/en/articles/691464/)
- [три](https://towardsdatascience.com/how-to-work-with-object-detection-datasets-in-coco-format-9bf4fb5848a4)
- [три с половиной](https://habr.com/en/companies/itmai/articles/541858/)



