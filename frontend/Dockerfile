FROM nginx:alpine

COPY . /usr/share/nginx/html

RUN sed -i 's/listen       80;/listen       3000;/g' /etc/nginx/conf.d/default.conf

EXPOSE 3000
