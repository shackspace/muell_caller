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
Don't forget to autostart

	etc/init.d/muellshack

will work on ubuntu
