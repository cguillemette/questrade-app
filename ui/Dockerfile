FROM node:18-alpine

WORKDIR /workspace/ui

COPY . .

RUN corepack enable
RUN corepack prepare pnpm@latest --activate
CMD pnpm install && pnpm run dev
