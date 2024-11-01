# Cloud Voyage
A web application for travelers that allows you to conveniently download the route and see the weather at each point of the route.

## How to run it
You can run it with docker-compose or localy. For localy running you can see doc for `backend` and `frontend` in their directories. For docker you need to do this steps:
### Docker
1. Create `.env` file and paste here this:
```sh
ACCU_WEATHER_API_KEY=<your-key>
```

2. Build the containers:
```sh
docker compose build
```

3. Up containers:
```sh
docker compose up
```

After this steps open your browser and go to `http://localsho:3000`. Success!


## Ответы на аналитические вопросы
> **1. Какие графики лучше всего подходят для визуализации погодных данных? Объяснии свой выбор.**
>
>Такие-то и такие-то

> **2. Как можно улучшить пользовательский опыт с помощью интерактивных графиков?**
>
> Такие-то и такие-то

