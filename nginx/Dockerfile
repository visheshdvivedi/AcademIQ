# Use the official OpenResty image
FROM openresty/openresty:alpine-fat

# Install dependencies
RUN apk update && apk add --no-cache \
    luarocks \
    git \
    gcc \
    musl-dev \
    make \
    libressl-dev

# Install Lua modules using luarocks
RUN luarocks install lua-resty-jwt \
    && luarocks install lua-resty-http

# Copy NGINX configuration and Lua scripts
COPY nginx.conf /usr/local/openresty/nginx/conf/nginx.conf
COPY jwt.lua /usr/local/openresty/nginx/lua/jwt.lua

# Expose the port
EXPOSE 80

# Start OpenResty
CMD ["/usr/local/openresty/bin/openresty", "-g", "daemon off;"]
