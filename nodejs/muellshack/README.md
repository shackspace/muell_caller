Muellshack
==========

# Install

## nodejs

	npm install


## nginx
Maybe you have to add this to your config:
/etc/nginx/sites-available/default

	location /muellshack/ {
		proxy_pass http://localhost:8081/muellshack/;
	}

## startup
Don't forget to autostart with pm2

	sudo su -c "env PATH=$PATH:/usr/bin pm2 startup linux -u shack --hp /home/shack"
	pm2 start process.json
	pm2 save

will work on ubuntu

## check the process

	sudo su -c "pm2 status" shack

