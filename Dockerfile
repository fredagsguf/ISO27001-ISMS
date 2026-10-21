# syntax=docker/dockerfile:1

# ---- Build stage: validate the ISMS and render the static site ----
FROM python:3.12-slim AS build
WORKDIR /src
COPY site/requirements.txt site/requirements.txt
RUN pip install --no-cache-dir -r site/requirements.txt
COPY . .
ARG ISMS_SITE_NAME="ISMS Portal"
ARG STRICT=""
ENV ISMS_SITE_NAME=${ISMS_SITE_NAME}
# Errors in the registers or documents fail the image build.
# Pass --build-arg STRICT=--strict to also fail on warnings.
RUN python tools/validate_isms.py --quiet ${STRICT} \
 && python tools/build_site.py \
 && mkdocs build --strict -f build/mkdocs.yml -d /out

# ---- Runtime stage: unprivileged nginx serving static files ----
FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY site/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /out /usr/share/nginx/html
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -q --spider http://127.0.0.1:8080/healthz || exit 1
