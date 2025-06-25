# Reels Automation Api Gateway

## Insalación

Iniciar un virtual environment con:

virtualenv env

Ejecutar make install para instalar los modulos de requirements.txt

## Ejecución

Ejecutar make python-run

## Docker
```yaml
networks:
  default:
    driver: bridge
services:
  api_gateway:
    image: ghcr.io/reels-automation/reels-automation-api-gateway-new:main
    environment:
      DATABASE_URL: ${DATABASE_URL}
      ENVIRONMENT: ${ENVIRONMENT}
      JWT_KEY: ${JWT_KEY}
      MINIO_URL: ${MINIO_URL}
      MONGO_URL: ${MONGO_URL}
      KAFKA_URL: ${KAFKA_URL}
      MERCADO_PAGO_ACCESS_TOKEN: ${MERCADO_PAGO_ACCESS_TOKEN}
      MINIO_ACCESS_KEY: ${MINIO_ACCESS_KEY}
      MINIO_SECRET_KEY: ${MINIO_SECRET_KEY}
    container_name: api_gateway
    restart: unless-stopped
    networks:
      - default
    user: $UID:$GID
    ports:
      - "7080:7080"
```
Importante: Configurar las variables de entorno apropiadas en un .env
