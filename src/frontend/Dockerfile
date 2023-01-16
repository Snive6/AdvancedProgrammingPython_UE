FROM node as build
WORKDIR /app
COPY package*.json ./
RUN rm -rf node_modules
RUN yarn cache clean --force
RUN yarn install
COPY . .
RUN yarn run build

FROM nginx:alpine
EXPOSE 80
RUN rm -rf /etc/nginx/conf.d
COPY --from=build /app/nginxConf /etc/nginx
WORKDIR /usr/share/nginx/html
# COPY --from=build /app/build /app/env.sh /app/.env ./
# RUN apk add --no-cache bash && \
#     chmod +x env.sh
# ENTRYPOINT ["/bin/bash", "-c", "/usr/share/nginx/html/env.sh /usr/share/nginx/html/.env && nginx -g \"daemon off;\""]
ENTRYPOINT ["nginx -g"]
