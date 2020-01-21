# use the lasted nginx image
FROM nginx:1.17-alpine

# remove the default conf file
RUN rm /etc/nginx/conf.d/default.conf

#copy our config file as the new config
COPY nginx.conf /etc/nginx/conf.d