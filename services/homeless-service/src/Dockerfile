FROM nginx

VOLUME /usr/share/nginx/html/homeless

VOLUME /etc/nginx

COPY index.html /usr/share/nginx/html/homeless/index.html

COPY /config/default.conf /etc/nginx/conf.d

EXPOSE 8000
