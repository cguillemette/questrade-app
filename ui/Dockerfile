FROM node:18-alpine

WORKDIR /workspace/ui

COPY . .

RUN corepack enable
RUN corepack prepare yarn@3.2.3+sha224.953c8233f7a92884eee2de69a1b92d1f2ec1655e66d08071ba9a02fa --activate
CMD yarn install && yarn run dev
