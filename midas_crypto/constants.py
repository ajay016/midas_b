# Extracted from xmidas-sdk.js (injected into DOM as hidden <input id="xMidasToken">)
# 96 hex chars = 48 bytes:
#   bytes  0-31 → AES-256 key
#   bytes 32-47 → auxiliary material (not used directly in encryption)
XMIDAS_TOKEN = "3ba22cbf8bea411868a1ea9611979910684f8fc4f493a76eb5129303e93a941f197616e264eab6c363f09d9be3624bd2"

# Version string injected alongside the token (<input id="xMidasVersion">)
XMIDAS_VERSION = "1.0.1"

# Midasbuy base URL
MIDASBUY_BASE_URL = "https://www.midasbuy.com"

# Known API endpoints (from 46374.aa36b94c9a17d3c2.js)
ENDPOINT_QUERY_ROLE_DETAIL    = "/interface/queryRoleDetail"
ENDPOINT_QUERY_VIP            = "/interface/queryVip"
ENDPOINT_GET_CHARAC_BY_OPENID = "/interface/getCharacByOpenid"
ENDPOINT_SHELF_PROTO          = "/interface/shelfProto"
ENDPOINT_VERIFY_BALANCE       = "/interface/verifyBalance"

# PUBG Mobile appid used in requests (seen in 46374.js)
PUBGM_APPID = "1900000047"

# Default platform field
DEFAULT_PF = "mds_pc_browser-yy-android-midasweb-midasbuy-self.midasbuy_saas"
