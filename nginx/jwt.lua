ngx.log(ngx.ERR, "JWT Validation: Start")

local jwt = require "resty.jwt"
local validators = require "resty.jwt-validators"

local jwtToken = ngx.var.http_Authorization
if jwtToken == nil then
    ngx.status = ngx.HTTP_UNAUTHORIZED
    ngx.header.content_type = "application/json; charset=utf-8"
    ngx.say('{"error":"Unauthorized"}')
    ngx.exit(ngx.HTTP_UNAUTHORIZED)
end

local claim_spec = {
    exp = validators.is_not_expired()
}

if jwtToken:find("Bearer ") == 1 then
    jwtToken = jwtToken:sub(8)
end

local secret = os.getenv("SECRET_KEY")
local jwt_obj = jwt:verify(secret, jwtToken, claim_spec)
if not jwt_obj["verified"] then
    ngx.status = ngx.HTTP_UNAUTHORIZED
    ngx.header.content_type = "application/json; charset=utf-8"
    ngx.say(jwt_obj.reason)
    ngx.exit(ngx.HTTP_UNAUTHORIZED)
end
