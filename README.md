

## Prepare Dev Environment

1. Pull PostgreSQL:
    ```shell
    docker pull postgres:latest
    ```
2. Run PostgreSQL container:
    ```shell
    docker run --name postgresql-rashodomer -p 5432:5432 -e POSTGRES_USER=rashodomer -e POSTGRES_PASSWORD=123456 -e POSTGRES_DB=rashodomer-db -d {{IMAGE_ID}}
    ```