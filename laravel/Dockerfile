FROM composer:2.8.10 AS composer-bin

FROM php:8.3.24-cli-bookworm

ARG LARAVEL_SKELETON_URL="https://github.com/laravel/laravel/archive/refs/tags/v13.8.0.tar.gz"
ARG LARAVEL_SKELETON_SHA256="d32991650cb93458a935aa309ecd7258f237a5f21519225efd367125af2b14c7"
ARG LARAVEL_FRAMEWORK_VERSION="13.23.0"

ENV APP_ENV=production \
    APP_DEBUG=false \
    LOG_CHANNEL=stderr \
    PORT=8080 \
    COMPOSER_ALLOW_SUPERUSER=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl libicu-dev libonig-dev libzip-dev unzip \
    && docker-php-ext-install -j"$(nproc)" bcmath intl mbstring pcntl pdo_mysql zip \
    && pecl install redis-6.2.0 \
    && docker-php-ext-enable redis \
    && rm -rf /var/lib/apt/lists/* /tmp/pear

COPY --from=composer-bin /usr/bin/composer /usr/local/bin/composer

WORKDIR /app
RUN curl -fsSL "${LARAVEL_SKELETON_URL}" -o /tmp/laravel.tar.gz \
    && echo "${LARAVEL_SKELETON_SHA256}  /tmp/laravel.tar.gz" | sha256sum -c - \
    && tar -xzf /tmp/laravel.tar.gz --strip-components=1 -C /app \
    && rm /tmp/laravel.tar.gz \
    && composer require "laravel/framework:${LARAVEL_FRAMEWORK_VERSION}" --no-update --no-interaction \
    && composer update --no-dev --prefer-dist --no-interaction --no-progress --optimize-autoloader \
    && mkdir -p storage/framework/cache storage/framework/sessions storage/framework/views storage/logs \
    && chmod -R 0775 storage bootstrap/cache

COPY entrypoint.sh /usr/local/bin/railway-laravel
RUN chmod 0755 /usr/local/bin/railway-laravel

EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/railway-laravel"]

