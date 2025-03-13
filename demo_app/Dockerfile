FROM nginx:alpine
COPY index.html /tmp/index.html
CMD ["/bin/sh", "-c", "envsubst '$$APP_NAME' < /tmp/index.html > /usr/share/nginx/html/index.html && exec nginx -g 'daemon off;'"]