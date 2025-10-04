# PolzaAgencyTestBot

Тестовое задание.
Docker билд пока не готов, для запуска нужно распаковать директорию и запустить файл __main__.py


## API Reference

### Ping

```http
  POST /api/resume
```

#### Request body

`plain/text`
```
Текст резюме
```

#### Response on success

`application/json`
```json
{
  "skills": "Ключевые навыки из резюме"
}
```
