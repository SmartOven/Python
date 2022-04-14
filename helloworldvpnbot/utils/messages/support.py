no_access_message = """
Для доступа к данной функции оформите подписку на сервис (/subscribe) или обновите уже существующую (/renew) ☺
"""

guide_not_ready_message = """
Гайд по настройке устройства с данной ОС еще в разработке :(
"""

ask_guide_message = """
Выберите для какой операционной системы вам нужен гайд
"""

windows_guide_message = """
*Windows*

Вначале необходимо импортировать сертификат root, выполнив следующие шаги:

1. Введите /certificate и скачайте файл "certificate.pem", затем нажмите `WIN + R` на клавиатуре, чтобы открыть диалоговое окно `Выполнить` и введите `mmc.exe`, чтобы открыть `Консоль управления Windows`.

2. Из меню `Файл` перейдите в раздел `Добавить или удалить оснастку`, выберите `Сертификаты` из списка доступных оснасток и нажмите `Добавить`.

3. Чтобы разрешить VPN работать для любых пользователей, выберите `Учетная запись компьютера` и нажмите Далее.

4. Поскольку мы выполняем настройку на локальном компьютере, выберите пункт `Локальный компьютер` и нажмите `Готово`.

5. Под узлом `Корень консоли` откройте запись `Сертификаты (локальный компьютер)`, раскройте `Доверенные корневые центры сертификации` и выберите запись `Сертификаты`

6. В меню `Действие` выберите пункт `Все задачи` и нажмите `Импорт`, чтобы открыть мастер импорта сертификатов. Нажмите `Далее`, чтобы пролистать вводное окно.

7. На экране `Импортируемый файл` нажмите кнопку `Обзор`, убедитесь, что вы изменили тип файла с `X.509 Certificate (.cer;.crt)` на `All Files (.)` и выберите сохраненный ранее файл `certificate.pem`. Затем нажмите `Далее`.

8. Убедитесь, что `Хранилище сертификатов` имеет значение `Доверенные корневые центры сертификации` и нажмите `Далее`.

9. Нажмите `Готово`, чтобы импортировать сертификат

10. Закройте `Консоль управления Windows`, в диалоговом окне выберите `Не сохранять`

11. Откройте `Панель управления` и перейдите в `Центр управления сетями и общим доступом`.

12. Нажмите `Создание и настройка нового подключения или сети` и выберите пункт `Подключение к рабочем месту`.

13. Выберите пункт `Использовать мое подключение к Интернету (VPN)`.

14. Введите данные сервера VPN. Введите IP-адрес сервера из /home в поле `Адрес в Интернете`, затем введите в поле `Имя пункта назначения` описание (короткое название) своего соединения VPN. Затем нажмите `Готово`

15. Нажмите на иконку `Сеть` на панели задач - сверху над доступными Wi-Fi сетями появится настроенное нами VPN-соединение. Жмем `Подключиться`, в появившемся диалоговом окне вводим логин и пароль из /home.
"""

android_guide_message = """
*Android*

1. Введите /certificate и сохраните полученный файл в папку `Загрузки`.

2. Загрузите клиент `StrongSwan VPN` из магазина `Play Store` - [ссылка](https://play.google.com/store/apps/details?id=org.strongswan.android).

3. Откройте приложение. Нажмите на значок «подробнее» (...) в правом верхнем углу и выберите `Сертификаты СА`.

4. Снова нажмите на значок `подробнее` (...) в правом верхнем углу. Выберите пункт `Импорт сертификата`.

5. Найдите файл сертификата `certificate.pem` в папке `Загрузки` и выберите его для импорта в приложение

6. В приложении нажмите `Добавить VPN профиль` сверху.

7. Введите в поле `Сервер` IP-адрес вашего сервера VPN из /home.

8. Обязательно выберите тип VPN: `IKEv2 EAP (Username/Password)`.

9. Введите в поля `Логин` и `Пароль` введите логин и пароль из /home.

10. Уберите флажок `Выбирать автоматически` в разделе `Сертификат СА` и нажмите `Выбрать сертификат СА`.

11. Откройте вкладку `IMPORTED` вверху экрана и выберите импортированный CA (возможно, список будет пуст, тогда нажмите на значок «подробнее» (...) в правом верхнем углу и импортируйте тот же сертификат еще раз, тогда он появится в списке - выбираем его)

12. В `Название профиля` введите любое желаемое название VPN-соединения.

13. Профиль для подключения к VPN-серверу создан. Для подключения просто нажмите на сам профиль

14. Для отключения от VPN-сервера, нажмите на `Отключить` вверху приложения
"""

ios_guide_message = """
*iOS*

1. Введите /certificate и сохраните полученный файл в папку Загрузки в `iCloud Drive`.

2. Откройте `Файлы`, найдите скачанный сертификат и нажмите на него один (или несколько) раз. Должна появиться надпись "Профиль загружен".

3. Откройте `Настройки` -> `Основные` -> `VPN и управление устройством`

4. В списке загруженных профилей нажмите на появившийся сертификат и установите (будет запрошен пароль для входа - вводим его и со всем соглашаемся), жмем `Готово`

5. Нажимаем на `VPN > Не подключено` -> `Добавить конфигурацию VPN`. После этого откроется экран конфигурации подключения VPN.

6. Нажмите `Тип` и выберите `IKEv2` (если он еще не выбран).

7. В поле `Описание` введите короткое имя для подключения VPN (можно написать что угодно)

8. В поле `Сервер` и `Удаленный ID` введите IP-адрес сервера из /home. В поле `Локальный ID` введите цифру 1.

9. Введите имя пользователя и пароль из /home в разделе `Аутентификация`, а затем нажмите `Готово`.

10. Выберите соединение VPN, которое вы только что создали, нажмите переключатель вверху страницы, и подключение будет установлено.
"""