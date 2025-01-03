# Cloud Voyage
A web application for travelers that allows you to conveniently download the route and see the weather at each point of the route.

## How to run it
You can run it with docker-compose or localy. For docker you need to do this steps:
### Docker
1. Create `.env` by `.env.example` and fill:
```sh
cp .env.example .env
```

2. Build the containers:
```sh
docker compose build
```

3. Up containers:
```sh
docker compose up
```

After this steps open your browser and go to `http://localsho:3000` for using web app. Or go to your telegram bot and test it! If you yousin my bot token, you can test in `@central_weather_bot`


## Ответы на аналитические вопросы
> **1. Какие графики лучше всего подходят для визуализации погодных данных? Объяснии свой выбор.**
>1. **Линейные графики** для отображения изменений температуры, влажности, и скорости ветра.
>*Почему линейные графики?* Линейные графики идеально подходят для представления временных рядов, таких как температура или ветер в зависимости от времени. Они легко передают изменения параметров во времени.
>2. **Гистограммы или столбчатые графики** для показателей, которые не меняются плавно, как, например, осадки или индекс качества воздуха:
>*Почему гистограммы?* Осадки часто измеряются в определенные моменты, а не непрерывно, поэтому столбчатые графики помогут отобразить их объем по дням или часам.
>3. **Круговые диаграммы** для представления категорий данных, таких как вероятность осадков по типам (дождь, снег и т.д.) или процент облачности:
>*Почему круговые диаграммы?* Они хорошо показывают процентное соотношение и позволяют легко оценить вероятность разных видов осадков или распределение показателей в общем виде.
>4. **Тепловые карты** для географических данных, показывающие температуру или осадки по регионам:
>*Почему тепловые карты?* Они полезны для наглядного отображения данных по географическому положению. Цветовая шкала позволяет интуитивно понять, в каких регионах погода лучше или хуже.

> **2. Как можно улучшить пользовательский опыт с помощью интерактивных графиков?**
>1. **Фильтры и диапазоны:** позволить пользователю выбрать, какие параметры отобразить (температура, осадки, влажность) и задать временной интервал для анализа, например, день, неделя или месяц.
>2. **Интерактивные всплывающие подсказки:** дать возможность пользователю видеть точные данные, наводя курсор на точку графика (например, температура и дата).
>3. **Обновляемые данные:** позволить обновлять данные в реальном времени или вручную, чтобы информация всегда оставалась актуальной.
>4. **Анимации:** визуально отображать изменения в погодных данных, например, через проигрывание изменений по дням или часам.

