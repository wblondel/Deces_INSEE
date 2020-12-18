1. Create TLS certificates for encrypted communications between nodes
`docker-compose -f create-certs.yml run --rm create_certs`

2. Copy .env.example to .env

3. Edit conf/nginx/sites-enabled/ conf files (don't modify example files)

4. Create self-signed certificate for Nginx default HTTPS server
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./conf/nginx/ssl/nginx.key -out ./conf/nginx/ssl/nginx.crt
```

5. 
```
chmod +x init-letencrypt
./init-letsencrypt.sh
```
(must be root)

6. Start the stack
```
docker-compose up -d
```

7. Generate passwords
```
docker exec es01 /bin/bash -c "bin/elasticsearch-setup-passwords auto --batch --url https://es01:9200"
```

8. Fill in .env, except LOGSTASH_USER and LOGSTASH_PASSWORD
LOGSTASH_USER and LOGSTASH_PASSWORD are credentials for the user you will use in your logstash pipeline (aka NOT logstash_system)

9. Create your LOGSTASH_USER in Kibana and assign the correct roles (see ELK doc)

10. Stop the stack
```
docker-compose stop
```

11. Fill in .env

12. Start the stack
```
docker-compose up -d
```
