printf "$USER:$(openssl passwd -crypt $PASSWORD)\n" >> /etc/nginx/.htpasswd