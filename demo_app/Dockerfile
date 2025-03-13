FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
RUN envsubst '${APP_NAME}' < /usr/share/nginx/html/index.html > /usr/share/nginx/html/index.html