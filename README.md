[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ESWFX1kF)
[![Tests](https://github.com/Unti1/LelaTestCases/actions/workflows/tests.yml/badge.svg)](https://github.com/your-username/LelaTestCases/actions/workflows/tests.yml)

## Описание задачи

В данном репозитории содержится код, решающий следующую задачу: сгруппировать файлы по исполнителям, исполнитель находится в названии файла в квадратных скобках. Для файлов без исполнителя, поместить их в папку с названием VA. При этом в названии папки должно быть кол-во треков.

Пример входных данных:

```
- Chill Vibes
  - song2 [Artist B].mp3
  - track1 [Artist A].mp3
  - track3.mp3

- Classic Hits
  - song1 [Artist B].mp3
  - song3.mp3
  - track2 [Artist A].mp3

- Jazz Essentials
  - jazz_track1.flac
  - jazz_track2 [Artist C].mp3

- Rock Anthems
  - rock_song1.mp3
  - rock_song2 [Artist D].flac
```

Пример результата:

```
- Artist A (2)
  - track1 [Artist A].mp3
  - track2 [Artist A].mp3

- Artist B (2)
  - song1 [Artist B].mp3
  - song2 [Artist B].mp3

- Artist C (1)
  - jazz_track2 [Artist C].mp3

- Artist D (1)
  - rock_song2 [Artist D].flac

- VA (4)
  - jazz_track1.flac
  - rock_song1.mp3
  - track3.mp3
  - song3.mp3
```

The structure of the files is always the same, that is, the files cannot be in the root folder, but there are no subacages inside the folders. The names of the performers have the upper register at the beginning of each word (for example, 'Linkin Park' will be 'Linkin Park')

## Баллы

- `1 балл` Сделать тесты, покрывающие 90% строк кода. Не нужно тестить тривиальные вещи, тесты должны быть осмысленные. **ВАЖНО: Тесты должны запускаться при запуске команды `uv run pytest`** (uv - программа, создающая виртуальные окружения в питоне, [ссылка](https://github.com/astral-sh/uv)). Если тесты не проходят проверку из-за проблемы в изначальном коде, то нужно создать в репозитории файл failed_tests.md, где будет объяснено, почему. Если причина провала теста на вашей стороне, то баллы за тесты не начисляются.
- `1 балл` Тесты проверяют множество разных кейсов
- `1 балл` Имеются креативные тесты (проверка неочевидных edge-кейсов, особенностей задачи)
- `1 балл` Реализовать CI, который будет запускать тесты при каждом пуше
- `0.5 балла` Cделать интеграцию CI-системы и вашего репозитория на GitHub: сделайте бэйдж в *README.md*, который будет показывать текущий статус тестов. Для информации смотрите [тут](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge), [тут](https://www.codeblocq.com/2016/04/Add-a-build-passing-badge-to-your-github-repository/). Как выглядят бэйджи в целом, можно посмотреть в любом проекте на GitHub, где они сделаны, например, в [репозитории Telegram](https://github.com/telegramdesktop/tdesktop)
- `0.5 балла` Сделайте любую интеграцию CI-системы и какого-либо мессенджера (например, `telegram`, `slack`, `msteams` и т.п.). Настройте систему так, чтобы при успешном прохождении теста посылалось сообщение "все ок", при неуспешном - посылалась информация, какие именно тесты не пройдены. Обратите внимание, тут не нужно писать код, нужно взять готовые аддоны / расширения и просто настроить. **Для подтверждения работы этого пункта укажите в файле ci_messages.md ссылку на видео**, где вы делаете пуш, и получаете уведомление

Решением будет считаться последний коммит в ветке main, отправленный до дедлайна. Тесты должны находиться в папке tests

При обнаружении плагиата баллы за обе работы будут обнулены (в прошлом ТЗ решение было более однообразным, так что мы не штрафовали подозрительные работы. В этот раз так не будет)
