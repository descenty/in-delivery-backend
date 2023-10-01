FROM quay.io/keycloak/keycloak:22.0.3
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true
COPY certs/fullchain.pem /opt/keycloak/conf/certs/tls.crt
COPY certs/privkey.pem /opt/keycloak/conf/certs/tls.key
COPY realm-export.json /opt/keycloak/data/import/realm-export.json