FROM nginx:1.11.3
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
COPY nginx.crt /etc/nginx/ssl/
COPY nginx.key /etc/nginx/ssl/
RUN rm /etc/nginx/conf.d/default.conf
COPY onesteward.conf /etc/nginx/conf.d/
