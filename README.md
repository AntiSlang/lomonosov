установка:
pip install -r requirements.txt
.env файл вписываете токен, токен надо получить тут:
https://oauth.vk.com/authorize?client_id=6121396&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline,messages&response_type=token&v=5.21
вроде всё, питон у меня 3.12

бот работает так: добавляете каждую беседу, из неё подтягиваются все ученики (не админы то есть).
дальше можно писать:
в каждую беседу в конкретным тарифом
каждому ученику с конкретным тарифом
в специфическую беседу
каждому ученику в специфической беседе
