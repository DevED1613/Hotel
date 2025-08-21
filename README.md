# Hotels
docker network create MyNetwork

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=eugeny \
    -e POSTGRES_PASSWORD=1613 \
    -e POSTGRES_DB=booking \
    --network=MyNetwork \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:15

docker run --name booking_cache \
    -p 7379:6379 \
    --network=MyNetwork \
    -d redis:7 

docker run --name booking_back \
    -p 8888:8000 \
    --network=MyNetwork \
    booking_image


docker run --name booking_celery_worker \
    --network=MyNetwork \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_ngnix \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --network=MyNetwork \
    -d -p 80:80 nginx 

docker build -t booking_image .