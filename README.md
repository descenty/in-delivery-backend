# in-delivery-backend
- Python
- FastAPI
- asyncpg

Для запуска на локальной машине выполните команду:
```bash
poe run
```
Обновление сертификатов для KeyCloak:
На сервере, где запущен KeyCloak выполните команду:
```bash
sudo certbot renew
```
Затем скопируйте обновленные сертификаты в проект через scp в папки certs и containers/keycloak/certs.