local jwt = require "resty.jwt"
local validators = require "resty.jwt-validators"

if ngx.var.request_method ~= "OPTIONS" then
    local jwtToken = ngx.var.http_Authorization
    if jwtToken == nil then
        ngx.status = ngx.HTTP_UNAUTHORIZED
        ngx.header.content_type = "application/json; charset=utf-8"
        ngx.say('{"error": "Token not found"}')
        ngx.exit(ngx.HTTP_UNAUTHORIZED)
    end

    local claim_spec = {
        exp = validators.is_not_expired() -- To check expiry
    }

    local secret = os.getenv("JWT_SECRET")
    local jwt_obj = jwt:verify(secret, jwtToken, claim_spec)
    if not jwt_obj["verified"] then
        ngx.status = ngx.HTTP_UNAUTHORIZED
        ngx.header.content_type = "application/json; charset=utf-8"
        ngx.say(jwt_obj.reason)
        ngx.exit(ngx.HTTP_UNAUTHORIZED)
    end
end
