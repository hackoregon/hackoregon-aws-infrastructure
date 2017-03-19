FROM nginx

VOLUME /usr/share/nginx/html/housing

VOLUME /etc/nginx

COPY index.html /usr/share/nginx/html/housing/index.html

COPY /config/default.conf /etc/nginx/conf.d
EXPOSE 8000
