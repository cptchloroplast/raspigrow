FROM node:16.14-alpine as build
WORKDIR /app
COPY . .
RUN npm ci
RUN npm run build

FROM nginx:1.20-alpine as release
COPY --from=build /app/dist /usr/share/nginx/html