FROM node:lts-alpine

WORKDIR /workspace/ui

COPY . .

RUN yarn
RUN npm rebuild

CMD npm run dev  