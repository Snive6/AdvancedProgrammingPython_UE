FROM node:17.3.0-alpine3.14 as build
WORKDIR /app
COPY package*.json ./
RUN rm -rf node_modules
RUN npm cache clean --force
RUN npm install --legacy-peer-deps
COPY . .
RUN npm run build

FROM nginx:alpine
EXPOSE 80
RUN rm -rf /etc/nginx/conf.d
COPY --from=build /app/nginxConf /etc/nginx
WORKDIR /usr/share/nginx/html
COPY --from=build /app/build /app/env.sh /app/.env ./
RUN apk add --no-cache bash && \
    chmod +x env.sh
ENTRYPOINT ["/bin/bash", "-c", "/usr/share/nginx/html/env.sh /usr/share/nginx/html/.env && nginx -g \"daemon off;\""]
