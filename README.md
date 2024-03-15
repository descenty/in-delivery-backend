in-delivery-backend

Для запуска на локальной машине выполните команду:
```bash
poe run
```

Обновление сертификатов для KeyCloak:
На сервере, где запущен KeyCloak выполните команду:
```bash
sudo certbot renew --dry-run
```
Затем скопируйте обновленные сертификаты в проект через scp в папки certs и containers/keycloak/certs.