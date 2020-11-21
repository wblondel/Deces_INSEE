1. Create TLS certificates for encrypted communications between nodes
`docker-compose -f create-certs.yml run --rm create_certs`

2. Copy .env.example to .env

3. Copy conf/nginx/vars.conf.example to conf/nginx/vars.conf and edit it
$cert_name is the first domain in the SSL cert you will generate

4. 
```
chmod +x init-letencrypt
./init-letsencrypt.sh
```
(must be root)

5. Start the stack

6. Generate passwords
```
docker exec es01 /bin/bash -c "bin/elasticsearch-setup-passwords auto --batch --url https://es01:9200"
```

7. Fill in .env

8. Restart the stack
```
docker-compose stop
docker-compose up -d
```