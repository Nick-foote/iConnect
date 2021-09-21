FROM nginx:1.19.0-alpine

# removing default setup
RUN rm /etc/nginx/conf.d/default.conf

# adding our setup 
COPY ./config/nginx/default.conf /etc/nginx/conf.d/default.conf