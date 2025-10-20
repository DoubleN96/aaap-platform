# Multi-stage build for Next.js

FROM node:20-alpine AS base
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Builder
FROM base AS builder
COPY package.json ./
COPY . .
RUN npm install
RUN npm run build

# Runner
FROM base AS runner
ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
