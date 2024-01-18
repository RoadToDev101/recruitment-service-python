# MySQL Docker

## Start database

```bash
docker compose up -d
```

## Import database

```bash
docker exec -i mysql mysql -uroot -p{root_user_password} < db-dumps/job_db.sql
```

> **Note:** The default root user password is `Admin@123`. Find it in the `docker-compose.yml` file.
