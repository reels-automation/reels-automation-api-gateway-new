# Reels Automation Api Gateway

## Entorno de desarrollo local 

### Clonar el repositorio 
```bash
git@github.com:reels-automation/reels-automation-api-gateway-new.git
```

### Iniciar un virtual environment
```bash
virtualenv env
```

### Instalar las dependencias

```bash
make install
```
### Configurar variables de entorno
```bash
cp .env.template .env

DATABASE_URL # Url a una base de datos SQL
MONGO_URL    # Url a una base de datos mongo
KAFKA_URL    # Url al broker de kafka
MINIO_URL    # Url del contenedor minio donde se obtienen los videos
MINIO_ACCESS_KEY #Clave de acceso para acceder al contendor de minio
MINIO_SECRET_KEY #Clave secreta para acceder al contenedor de minio
JWT_KEY      # La clave JWT para encriptar los tokens
MERCADO_PAGO_ACCESS_TOKEN #Token de acceso de mercado pago para recibir pagos
```

### Ejecutar
```bash
bash -c 'source env/bin/activate && fastapi dev main.py --port 7080' #Reemplazar por cualquier puerto
```

## Entorno de desarrollo de producción

### Docker
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

### Kuberentes

## Como contribuir

