# GetNReorgQT

Приложение позволяет автоматизировать и увеличить скорость обработки обращений для сотрудников технической поддержки, взаимодействующих с API Эвотор.

Как выглядит процесс анализа электронных чеков "вручную": 
1. Зайти в Админ панель или в БД, чтобы получить уникальный токен приложения (+ выполнить поиск по БД или Админке)
2. Выполнить запрос на получение торговых точек, чтобы также получить их UUID
3. Преобразовать время из "человеческого" в UNIX
4. Заполнить токен, тип документа, диапазон времени, UUID торговой точки
5. Сделать запрос к облаку Эвотор с этими данными и сохранить результат

Как выглядит процесс анализа с приложением:
1. Зайти в админ панель для получения ключа, указать его в приложении и выполнить запрос
2. Автоматичеки будет получена информация о торговых точках, на следующем шаге уточнения запроса их только нужно будет выбрать из списка вариантов
3. Дату также можно указать через удобный календарь, заполнить часы\минуты\секунды. Преобразование в UNIX произойдет внутри автоматически
4. Тип документа также выбирается из списка вариантов
5. Выполнить запрос, можно обработать результат как в итоговом поле, так и сохранить, для дальнейшего анализа

Итого: вместо 4 запросов, получаем, фактически, один - на получение токена из админки, а остальные параметры уточняем в интерфейсе

Запуск (GNULinux): 
- распаковать [архив](https://codeberg.org/First_Encounter2/GetNReorgQT/releases "Релизы")
- в рабочей директории запустить терминал
- выполнить "make"

Запуск (Windows):
- Скачать [установщик](https://codeberg.org/First_Encounter2/GetNReorgQT/releases "Релизы")
- выполнить "grqt_2_setup_windows_64.exe", следуя подсказкам установщика
- запустить "GRQT.exe" с правами Администратора
