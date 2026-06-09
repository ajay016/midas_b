"""
Makes Midasbuy API calls from inside a live browser session.

How encryption works (from 91.79b63beb.bundle.js + Chaos VM disassembly):
  ctoken      = <input id="xMidasToken">.value
  ctoken_ver  = <input id="xMidasVersion">.value
  encrypt_msg = Base64(hexToBytes(window.xMidas({d: JSON(fullPayload)})))

The Chaos VM is authoritative. A previous AES-only approximation can produce
bytes, but Midasbuy rejects them as an invalid encrypt_msg.

publicParams come from ei() in the bundle:
  appid, pf, zoneid, country, device_id (from __Report_INFO),
  muid (from __Report_INFO), tdrc_fp (= UUID cookie, NOT Forter),
  cgi_extend (base64 of device object), drm_info (base64 of empty obj),
  midasbuyArea, shopcode, buyType, midas_sdk, currency_type, _id (random).

The Chaos VM CDN script is intercepted via page.route and appended with a
configurable:false property lock so React SPA hydration cannot delete
window.xMidas.  The route must be registered BEFORE page.goto.

Note: forterToken / feh-- localStorage keys are NOT read by the Chaos VM
(confirmed by full disassembly — zero references).
"""
import json
import logging
import os
import time
from dataclasses import dataclass, field
from threading import Lock, get_ident
from typing import Dict, Optional, Tuple
from urllib.parse import parse_qs, urlparse

logger = logging.getLogger(__name__)


@dataclass
class _CachedBrowserSession:
    manager: object
    browser: object
    context: object
    page: object
    storage_state_path: str
    country_code: str
    storage_mtime: float
    created_at: float
    last_used: float
    lock: Lock = field(default_factory=Lock)


_SESSION_CACHE: Dict[Tuple[str, str, int], _CachedBrowserSession] = {}
_SESSION_CACHE_LOCK = Lock()
_CACHED_ENDPOINTS = {
    "/interface/getCharac",
    "/interface/shelfProto/shelves_svr/QueryRedeemCodeInfo",
}

# Local copy of the Chaos VM CDN script (served via page.route to avoid CDN latency)
_CHAOS_VM_LOCAL_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__), "..", "..", "..",
        "kEc9hjFh5DQJbz_iPEWrfFxadMVk4PbLDS-5P8jE73pfdUuDwNGKNVZjdEztcHdofAVaHXo6zRGXgLwuvsK_afAEj6w_mKyiUmq-7AesIRU~.js",
    )
)
_MIDAS_SDK_LOCAL_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__), "..", "..", "..",
        "midas-oversea-h5page.js",
    )
)

# Appended to the Chaos VM script (served via page.route).
# Tries to lock window.xMidas immediately; if the VM assigned it async,
# falls back to a 10ms poll so we catch it before SPA hydration deletes it.
_CHAOS_VM_PROTECTION = b"""
;(function(){
    function _lock(fn) {
        try {
            Object.defineProperty(window, 'xMidas', {
                get: function() { return fn; },
                set: function() {},
                configurable: false,
                enumerable: true,
            });
        } catch(e) {}
    }
    var _fn = window.xMidas;
    if (typeof _fn === 'function') { _lock(_fn); return; }
    var _t = setInterval(function() {
        var f = window.xMidas;
        if (typeof f === 'function') { clearInterval(_t); _lock(f); }
    }, 10);
    setTimeout(function() { clearInterval(_t); }, 30000);
})();
"""


def _get_playwright():
    """Prefer patchright (undetected); fall back to standard playwright."""
    try:
        from patchright.sync_api import sync_playwright, TimeoutError as PWTimeout
        logger.debug("[CRYPTO] using patchright")
        return sync_playwright, PWTimeout
    except ImportError:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
        logger.warning("[CRYPTO] patchright not installed — falling back to standard playwright")
        return sync_playwright, PWTimeout


# ── Stealth init script ────────────────────────────────────────────────────────
_STEALTH_JS = """
(() => {
    try { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); } catch(e) {}

    if (!window.chrome) {
        try {
            Object.defineProperty(window, 'chrome', {
                writable: true, enumerable: true, configurable: false,
                value: {
                    app: { isInstalled: false, getDetails(){}, getIsInstalled(){ return false; },
                           installState(){}, runningState(){ return 'cannot_run'; } },
                    csi(){}, loadTimes(){ return {}; }, runtime: {},
                },
            });
        } catch(e) {}
    }

    try {
        if (!navigator.plugins || navigator.plugins.length === 0) {
            const mk = (n, f) => ({ name: n, filename: f,
                description: 'Portable Document Format', length: 1,
                0: { type: 'application/pdf', suffixes: 'pdf', description: '' } });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [mk('PDF Viewer','internal-pdf-viewer'),
                            mk('Chrome PDF Viewer','internal-pdf-viewer'),
                            mk('Chromium PDF Viewer','internal-pdf-viewer')],
                enumerable: true,
            });
        }
    } catch(e) {}

    try { Object.defineProperty(navigator, 'languages', { get: () => ['en-US','en'] }); } catch(e) {}
    try { Object.defineProperty(navigator, 'platform',  { get: () => 'Win32' }); } catch(e) {}
    try {
        if (!navigator.hardwareConcurrency || navigator.hardwareConcurrency < 2)
            Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
    } catch(e) {}

    // Pre-intercept window.xMidas with a capturing setter so the Chaos VM's
    // synchronous assignment is caught before SPA hydration can delete it.
    // Works if this init script runs in the main JS world (standard Playwright
    // behaviour). The configurable:false lock prevents any subsequent deletion.
    try {
        var _xMidasFn = null;
        Object.defineProperty(window, 'xMidas', {
            get: function() { return _xMidasFn; },
            set: function(v) {
                if (typeof v === 'function' && _xMidasFn === null) {
                    _xMidasFn = v;
                    // Re-lock as non-configurable so the SPA cannot delete it
                    try {
                        Object.defineProperty(window, 'xMidas', {
                            get: function() { return _xMidasFn; },
                            set: function() {},
                            configurable: false,
                            enumerable: true,
                        });
                    } catch(e) {}
                }
            },
            configurable: true,
            enumerable: true,
        });
    } catch(e) {}
})();
"""

# ── JS evaluated inside the page ──────────────────────────────────────────────

_JS_CALL_API = """
async ({payloadJson, endpoint, method}) => {
    try {
        // Wait for xMidasToken (up to 15s)
        let tokenWait = 0;
        while ((!document.getElementById('xMidasToken')?.value) && tokenWait < 150) {
            await new Promise(r => setTimeout(r, 100));
            tokenWait++;
        }
        const tokenEl = document.getElementById('xMidasToken');
        if (!tokenEl || !tokenEl.value) return {error: 'no_xmidas_token'};

        const ctoken     = tokenEl.value;
        const versionEl  = document.getElementById('xMidasVersion');
        const ctoken_ver = (versionEl && versionEl.value) ? versionEl.value : '1.0.1';

        // Wait for window.xMidas (up to 15s).
        // With the route intercept + configurable:false lock, it should be
        // present immediately; this loop is a safety net.
        let xmWait = 0;
        while (typeof window.xMidas !== 'function' && xmWait < 150) {
            await new Promise(r => setTimeout(r, 100));
            xmWait++;
        }
        if (typeof window.xMidas !== 'function') return {
            error: 'no_xmidas_function',
            midasKeys: Object.keys(window).filter(k => k.toLowerCase().includes('midas')),
        };

        // Build publicParams — mirrors ei() in 91.79b63beb.bundle.js module 36453.
        // server validates the full merged payload; omitting these fields causes HTTP 500.
        const snapshot = window.__backendBootstrap || {};
        const liveServerData = window.SERVER_DATA || {};
        const sd = Object.assign({}, snapshot, liveServerData);
        sd.payInfo = Object.assign(
            {},
            snapshot.payInfo || {},
            liveServerData.payInfo || {}
        );
        window.SERVER_DATA = sd;
        const payInfo = sd.payInfo;
        const shopInfo = sd.shopInfo || {};
        const ri = window.__Report_INFO || {};
        const rp = sd.reportParams || {};
        const urlParams = new URLSearchParams(location.search);
        const queryString = (obj) => Object.keys(obj)
            .filter(k => obj[k] !== undefined && obj[k] !== null)
            .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(obj[k]))
            .join('&');
        let storedUser = {};
        try {
            storedUser = JSON.parse(sessionStorage.getItem('user_login_data') || '{}');
        } catch(e) {}
        let actualPayload = JSON.parse(payloadJson);
        const verifiedPlayerStorageKey = 'midasbuy_backend_verified_players';
        let verifiedPlayers = {};
        let verifiedPlayer = null;
        let verifiedPlayerApplied = false;
        try {
            verifiedPlayers = JSON.parse(
                sessionStorage.getItem(verifiedPlayerStorageKey) || '{}'
            );
        } catch(e) {}
        if (endpoint.endsWith('/QueryRedeemCodeInfo')) {
            verifiedPlayer = verifiedPlayers[actualPayload.open_id] || null;
            if (verifiedPlayer) {
                Object.assign(payInfo, verifiedPlayer);
                verifiedPlayerApplied = true;
            }
        }

        const deviceMatch = document.cookie.match(/midasbuyDeviceId=([^;]*)/);
        const device_id = (
            rp.midasbuyDeviceId ||
            ri.midasbuyDeviceId ||
            (deviceMatch ? deviceMatch[1] : '')
        );
        const muid = (
            rp.midasuid ||
            ri.midasuid ||
            sd.muid ||
            sd.user?.uid ||
            payInfo.midasUser?.uid ||
            storedUser.uid ||
            ''
        );

        // tdrc_fp is the UUID cookie value — NOT a Forter token
        const uuidMatch = document.cookie.match(/UUID=([^;]*)/);
        const tdrc_fp   = uuidMatch ? uuidMatch[1] : '';

        const pageOpenId = (
            payInfo.openid ||
            actualPayload.openid ||
            actualPayload.open_id ||
            ''
        );
        let serverTimeOffset = Number(window._SERVER_TIME_OFFSET || 0);
        if (serverTimeOffset > 0 && serverTimeOffset <= 15000) {
            serverTimeOffset = 0;
        }
        const pageTime = Date.now() - serverTimeOffset;
        const pagetoken = btoa(`${location.hostname}_${pageTime}_${pageOpenId}`);
        const cgi_extend_obj = {device_id, pagetoken, tdrc_fp, muid};
        const cgi_extend     = queryString(cgi_extend_obj);
        const drm_info       = queryString(payInfo.drm_info || {});
        const buyType        = sd.buyType || (location.pathname.includes('/redeem/') ? 'REDEEM' : '');

        const publicParams = {
            appid:         payInfo.appid || sd.appid || '1450015065',
            pf:            payInfo.pf || 'mds_pc_browser-yy-android-midasweb-midasbuy-self.midasbuy_saas',
            zoneid:        String(payInfo.zoneid || payInfo.zone_id || payInfo.currentBindUser?.zoneid || '1'),
            country:       (payInfo.country || sd.country || 'BD').toUpperCase(),
            cgi_extend,
            drm_info,
            midasbuyArea:  payInfo.midasbuyArea || sd.midasbuyArea || '',
            shopcode:      payInfo.shopcode || payInfo.shop_id || shopInfo.shopcode || '',
            buyType,
            midas_sdk:     '0',
            currency_type: payInfo.currency_type || sd.currency_type || 'USD',
            _id:           Math.random(),
            sc:            urlParams.get('sc') || '',
            from:          urlParams.get('from') || '',
            task_token:    urlParams.get('task_token') || '',
            cgi_extend_obj,
        };
        Object.assign(publicParams, sd._Exp_DATA || {});

        const initExtendParams = urlParams.get('initExtendParams');
        if (initExtendParams) {
            try {
                Object.assign(publicParams, JSON.parse(atob(initExtendParams)));
            } catch(e) {}
        }

        // Merge: actualPayload fields win over publicParams on overlap (e.g. country, appid)
        if (endpoint.endsWith('/QueryRedeemCodeInfo')) {
            const verificationPayload = actualPayload;
            const playerUserId = (
                verificationPayload.role_id ||
                verifiedPlayer?.userid ||
                verificationPayload.open_id ||
                payInfo.userid ||
                ''
            );
            const redeemOpenId = (
                verifiedPlayer?.openid ||
                payInfo.openid ||
                payInfo.currentBindUser?.openid ||
                verificationPayload.openid ||
                verificationPayload.open_id ||
                ''
            );
            const serverId = String(
                verifiedPlayer?.zoneid ||
                actualPayload.zone_id ||
                payInfo.zoneid ||
                payInfo.zone_id ||
                payInfo.currentBindUser?.zoneid ||
                '1'
            );
            const language = (
                sd.countryInfo?.iso?.language ||
                (Array.isArray(sd.countryInfo?.lang) ? sd.countryInfo.lang[0] : sd.countryInfo?.lang) ||
                payInfo.cgi_language ||
                document.documentElement.lang ||
                navigator.language ||
                'en'
            ).split('-')[0];
            const user = sd.user || payInfo.midasUser || storedUser;

            actualPayload = {
                redeem_code: actualPayload.redeem_code,
                subchannel: 'MIDASBUY_REDEEM',
                direct_redeem: '1',
                offer_id: payInfo.appid || sd.appid || '1450015065',
                platform: payInfo.platform || 'android',
                server_id: serverId,
                region: payInfo.country || sd.country || 'BD',
                open_id: redeemOpenId,
                muid: user.uid || actualPayload.muid || sd.muid || '',
                flexible_return_url: (
                    `https://${location.hostname}/h5/overseah5/views/riskcontrol/landing.html`
                ),
                user_ip: payInfo.ipInfo?.mall_ip || '',
                role_id: playerUserId,
                language,
                shop_code: payInfo.shopcode || payInfo.shop_id || shopInfo.shopcode || '',
            };
            if (verificationPayload.rc_token && verificationPayload.rc_uuid) {
                actualPayload.rc_token = verificationPayload.rc_token;
                actualPayload.rc_uuid = verificationPayload.rc_uuid;
                actualPayload.channel = verificationPayload.channel || 'os_midaspay_v2';
            }
        }
        const fullPayload   = Object.assign({}, publicParams, actualPayload);
        for (const k of Object.keys(fullPayload)) {
            if (fullPayload[k] !== undefined && typeof fullPayload[k] !== 'object') {
                fullPayload[k] = String(fullPayload[k]);
            }
        }
        const fullJson      = JSON.stringify(fullPayload);

        try { window.xMidas(); } catch(e) {}
        const hexResult = window.xMidas({d: fullJson});
        if (!hexResult || typeof hexResult !== 'string' || hexResult.length === 0)
            return {error: 'xmidas_empty', got: JSON.stringify(hexResult)};

        const bytes       = (hexResult.match(/../g) || []).map(h => parseInt(h, 16));
        const encrypt_msg = btoa(String.fromCharCode(...bytes));

        const resp = await fetch('https://www.midasbuy.com' + endpoint, {
            method:      method || 'POST',
            headers:     {'Content-Type': 'application/json', 'Accept': 'application/json, text/plain, */*'},
            body:        JSON.stringify({encrypt_msg, ctoken_ver, ctoken}),
            credentials: 'include',
        });

        const text = await resp.text();
        let data;
        try { data = JSON.parse(text); }
        catch(e) {
            return {error: 'invalid_json', status: resp.status,
                    encrypt_msg_len: encrypt_msg.length, text: text.substring(0, 300)};
        }
        if (endpoint.endsWith('/getCharac') && Number(data?.ret) === 0 && data?.info) {
            const info = data.info;
            const verifiedPlayer = {
                openid: info.openid || '',
                charac_name: info.charac_name || '',
                zoneid: info.zoneid || actualPayload.zoneid || '',
                userid: actualPayload.openid || '',
                is_ban: !!info.is_ban,
                register_country: info.register_country || '',
                active_country: info.active_country || '',
                region: info.region || '',
            };
            Object.assign(payInfo, verifiedPlayer);
            verifiedPlayers[verifiedPlayer.userid] = verifiedPlayer;
            try {
                sessionStorage.setItem(
                    verifiedPlayerStorageKey,
                    JSON.stringify(verifiedPlayers)
                );
            } catch(e) {}
        }
        return {
            ok: true,
            status: resp.status,
            data,
            encrypt_msg_len: encrypt_msg.length,
            request_field_names: Object.keys(actualPayload).sort(),
            request_debug: endpoint.endsWith('/QueryRedeemCodeInfo') ? {
                open_id: actualPayload.open_id || '',
                role_id: actualPayload.role_id || '',
                server_id: actualPayload.server_id || '',
                region: actualPayload.region || '',
                shop_code: actualPayload.shop_code || '',
                has_rc_token: !!actualPayload.rc_token,
                has_rc_uuid: !!actualPayload.rc_uuid,
            } : {},
            public_field_names: Object.keys(publicParams).sort(),
            full_json_length: fullJson.length,
            cgi_extend_length: cgi_extend.length,
            drm_info_length: drm_info.length,
            exp_data_length: JSON.stringify(sd._Exp_DATA || {}).length,
            pagetoken_length: pagetoken.length,
            has_device_id: !!device_id,
            has_muid: !!muid,
            has_ip_info: !!payInfo.ipInfo?.mall_ip,
            has_drm_info: !!Object.keys(payInfo.drm_info || {}).length,
            has_exp_data: !!Object.keys(sd._Exp_DATA || {}).length,
            verified_player_count: Object.keys(verifiedPlayers).length,
            verified_player_applied: verifiedPlayerApplied,
        };
    } catch(e) {
        return {error: 'js_exception', detail: String(e), stack: (e.stack||'').substring(0,500)};
    }
}
"""

_JS_ENCRYPT_ONLY = """
async ({payloadJson}) => {
    try {
        let tokenWait = 0;
        while ((!document.getElementById('xMidasToken')?.value) && tokenWait < 150) {
            await new Promise(r => setTimeout(r, 100));
            tokenWait++;
        }
        const tokenEl   = document.getElementById('xMidasToken');
        const versionEl = document.getElementById('xMidasVersion');
        if (!tokenEl || !tokenEl.value) return {error: 'no_xmidas_token'};

        const ctoken     = tokenEl.value;
        const ctoken_ver = (versionEl && versionEl.value) ? versionEl.value : '1.0.1';

        let xmWait = 0;
        while (typeof window.xMidas !== 'function' && xmWait < 150) {
            await new Promise(r => setTimeout(r, 100));
            xmWait++;
        }
        if (typeof window.xMidas !== 'function') return {error: 'no_xmidas_function'};

        const snapshot = window.__backendBootstrap || {};
        const liveServerData = window.SERVER_DATA || {};
        const sd = Object.assign({}, snapshot, liveServerData);
        sd.payInfo = Object.assign(
            {},
            snapshot.payInfo || {},
            liveServerData.payInfo || {}
        );
        window.SERVER_DATA = sd;
        const payInfo = sd.payInfo;
        const shopInfo = sd.shopInfo || {};
        const ri = window.__Report_INFO || {};
        const rp = sd.reportParams || {};
        const urlParams = new URLSearchParams(location.search);
        const queryString = (obj) => Object.keys(obj)
            .filter(k => obj[k] !== undefined && obj[k] !== null)
            .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(obj[k]))
            .join('&');
        let storedUser = {};
        try {
            storedUser = JSON.parse(sessionStorage.getItem('user_login_data') || '{}');
        } catch(e) {}

        const deviceMatch = document.cookie.match(/midasbuyDeviceId=([^;]*)/);
        const device_id = (
            rp.midasbuyDeviceId ||
            ri.midasbuyDeviceId ||
            (deviceMatch ? deviceMatch[1] : '')
        );
        const muid = (
            rp.midasuid ||
            ri.midasuid ||
            sd.muid ||
            sd.user?.uid ||
            payInfo.midasUser?.uid ||
            storedUser.uid ||
            ''
        );
        const uuidMatch = document.cookie.match(/UUID=([^;]*)/);
        const tdrc_fp   = uuidMatch ? uuidMatch[1] : '';
        const actualPayload = JSON.parse(payloadJson);
        const pageOpenId = (
            payInfo.openid ||
            actualPayload.openid ||
            actualPayload.open_id ||
            ''
        );
        let serverTimeOffset = Number(window._SERVER_TIME_OFFSET || 0);
        if (serverTimeOffset > 0 && serverTimeOffset <= 15000) {
            serverTimeOffset = 0;
        }
        const pageTime = Date.now() - serverTimeOffset;
        const pagetoken = btoa(`${location.hostname}_${pageTime}_${pageOpenId}`);
        const cgi_extend_obj = {device_id, pagetoken, tdrc_fp, muid};
        const buyType = sd.buyType || (location.pathname.includes('/redeem/') ? 'REDEEM' : '');

        const publicParams = {
            appid: payInfo.appid || sd.appid || '1450015065',
            pf: payInfo.pf || 'mds_pc_browser-yy-android-midasweb-midasbuy-self.midasbuy_saas',
            zoneid: String(payInfo.zoneid || payInfo.zone_id || payInfo.currentBindUser?.zoneid || '1'),
            country: (payInfo.country || sd.country || 'BD').toUpperCase(),
            cgi_extend: queryString(cgi_extend_obj),
            drm_info: queryString(payInfo.drm_info || {}),
            midasbuyArea: payInfo.midasbuyArea || sd.midasbuyArea || '',
            shopcode: shopInfo.shopcode || '',
            buyType,
            midas_sdk: '0',
            currency_type: payInfo.currency_type || sd.currency_type || 'USD',
            _id: Math.random(),
            sc: urlParams.get('sc') || '',
            from: urlParams.get('from') || '',
            task_token: urlParams.get('task_token') || '',
            cgi_extend_obj,
        };
        Object.assign(publicParams, sd._Exp_DATA || {});

        const initExtendParams = urlParams.get('initExtendParams');
        if (initExtendParams) {
            try {
                Object.assign(publicParams, JSON.parse(atob(initExtendParams)));
            } catch(e) {}
        }
        const fullPayload   = Object.assign({}, publicParams, actualPayload);
        for (const k of Object.keys(fullPayload)) {
            if (fullPayload[k] !== undefined && typeof fullPayload[k] !== 'object') {
                fullPayload[k] = String(fullPayload[k]);
            }
        }
        const fullJson      = JSON.stringify(fullPayload);

        try { window.xMidas(); } catch(e) {}
        const hexResult = window.xMidas({d: fullJson});
        if (!hexResult || typeof hexResult !== 'string' || hexResult.length === 0)
            return {error: 'xmidas_empty'};

        const bytes       = (hexResult.match(/../g) || []).map(h => parseInt(h, 16));
        const encrypt_msg = btoa(String.fromCharCode(...bytes));
        return {ok: true, ctoken, ctoken_ver, encrypt_msg};
    } catch(e) {
        return {error: 'js_exception', detail: String(e)};
    }
}
"""

_JS_REDEEM_RESULT_PAGE = """
async ({payloadJson}) => {
    try {
        let tokenWait = 0;
        while ((!document.getElementById('xMidasToken')?.value) && tokenWait < 150) {
            await new Promise(r => setTimeout(r, 100));
            tokenWait++;
        }
        const tokenEl = document.getElementById('xMidasToken');
        if (!tokenEl || !tokenEl.value) return {error: 'no_xmidas_token'};

        const ctoken = tokenEl.value;
        const versionEl = document.getElementById('xMidasVersion');
        const ctoken_ver = (versionEl && versionEl.value) ? versionEl.value : '1.0.1';

        let xmWait = 0;
        while (typeof window.xMidas !== 'function' && xmWait < 150) {
            await new Promise(r => setTimeout(r, 100));
            xmWait++;
        }
        if (typeof window.xMidas !== 'function') return {error: 'no_xmidas_function'};

        const payload = JSON.parse(payloadJson);
        const snapshot = window.__backendBootstrap || {};
        const liveServerData = window.SERVER_DATA || {};
        const sd = Object.assign({}, snapshot, liveServerData);
        sd.payInfo = Object.assign(
            {},
            snapshot.payInfo || {},
            liveServerData.payInfo || {}
        );
        window.SERVER_DATA = sd;

        const payInfo = sd.payInfo || {};
        let storedUser = {};
        try {
            storedUser = JSON.parse(sessionStorage.getItem('user_login_data') || '{}');
        } catch(e) {}

        let verifiedPlayers = {};
        try {
            verifiedPlayers = JSON.parse(
                sessionStorage.getItem('midasbuy_backend_verified_players') || '{}'
            );
        } catch(e) {}

        const verifiedPlayer = verifiedPlayers[payload.player_id] || {};
        if (verifiedPlayer.openid) {
            Object.assign(payInfo, verifiedPlayer);
        }

        const resultOpenId = (
            payload.openid ||
            verifiedPlayer.openid ||
            payInfo.openid ||
            payInfo.currentBindUser?.openid ||
            payload.player_id ||
            ''
        );
        if (!resultOpenId) return {error: 'missing_result_openid'};

        const buyType = (
            new URLSearchParams(location.search).get('buyType') ||
            sd.buyType ||
            'REDEEM'
        ).toUpperCase();
        let pageId = String(payInfo.pageid || '').trim();
        if (!pageId) {
            pageId = `page_${String(Math.random()).slice(2, 19)}`;
        }
        const buyTypeKey = payload.buy_type_key || `CURRENT_BUY_ITEM_${buyType}_${pageId}`;

        const country = String(payload.country_code || sd.country || 'bd').toLowerCase();
        const gameShortUrl = sd.gameConfig?.gameShortUrl || payload.game_short_url || 'pubgm';
        const resultParams = {
            appid: String(payInfo.appid || sd.appid || payload.appid || '1450015065'),
            type: 'redeem',
            resultPageType: 'redeem',
            openid: resultOpenId,
            buy_type_key: buyTypeKey,
            gameShortUrl,
            isFromJsx: 'true',
        };
        const fullJson = JSON.stringify(resultParams);

        let serverTimeOffset = Number(window._SERVER_TIME_OFFSET || 0);
        if (serverTimeOffset > 0 && serverTimeOffset <= 15000) {
            serverTimeOffset = 0;
        }
        const pageTime = Date.now() - serverTimeOffset;
        const pagetoken = btoa(`${location.hostname}_${pageTime}_${resultOpenId}`);

        try { window.xMidas(); } catch(e) {}
        const hexResult = window.xMidas({d: fullJson});
        if (!hexResult || typeof hexResult !== 'string' || hexResult.length === 0) {
            return {error: 'xmidas_empty'};
        }

        const bytes = (hexResult.match(/../g) || []).map(h => parseInt(h, 16));
        const encrypt_msg = btoa(String.fromCharCode(...bytes));
        document.cookie = `pagetoken=${pagetoken}; path=/`;

        const url = new URL(
            `https://${location.hostname}/midasbuy/${country}/result/${gameShortUrl}`
        );
        for (const [key, value] of Object.entries(resultParams)) {
            url.searchParams.set(key, value);
        }
        url.searchParams.set('encrypt_msg', encrypt_msg);
        url.searchParams.set('ctoken_ver', ctoken_ver);
        url.searchParams.set('ctoken', ctoken);

        const resp = await fetch(url.toString(), {
            method: 'GET',
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'X-Requested-With': 'XMLHttpRequest',
            },
            credentials: 'include',
        });
        const text = await resp.text();
        let data;
        try {
            data = JSON.parse(text);
        } catch(e) {
            return {
                error: 'invalid_json',
                status: resp.status,
                text: text.substring(0, 300),
                result_url: url.toString(),
                encrypt_msg_len: encrypt_msg.length,
            };
        }

        return {
            ok: true,
            status: resp.status,
            data,
            result_url: url.toString(),
            result_openid: resultOpenId,
            buy_type_key: buyTypeKey,
            encrypt_msg_len: encrypt_msg.length,
            full_json_length: fullJson.length,
            pagetoken_length: pagetoken.length,
            request_field_names: Object.keys(resultParams).sort(),
            verified_player_applied: !!verifiedPlayer.openid,
        };
    } catch(e) {
        return {
            error: 'js_exception',
            detail: String(e),
            stack: (e.stack || '').substring(0, 500),
        };
    }
}
"""


# ── Helpers ───────────────────────────────────────────────────────────────────

_JS_REDEEM_ORDER = """
async ({payloadJson, sdkScript}) => {
    const messages = [];
    const pushMessage = (kind, value) => {
        try { messages.push({kind, value}); } catch(e) {}
    };
    const queryString = (obj) => Object.keys(obj)
        .filter(k => obj[k] !== undefined && obj[k] !== null && obj[k] !== '')
        .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(obj[k]))
        .join('&');
    const parseMaybeJson = (value) => {
        if (typeof value !== 'string') return value;
        try { return JSON.parse(value); } catch(e) { return value; }
    };
    const extractOrder = (value) => {
        const data = parseMaybeJson(value) || {};
        if (typeof data !== 'object') return {};
        const url = data.url || data.successUrl || data.link || '';
        let queryOrder = {};
        if (url && typeof url === 'string') {
            try {
                const parsed = new URL(url, location.href);
                queryOrder = {
                    order_no: parsed.searchParams.get('order_no') || '',
                    order_no_hash: parsed.searchParams.get('order_no_hash') || '',
                    portal_serial_no: parsed.searchParams.get('portal_serial_no') || '',
                };
            } catch(e) {}
        }
        return {
            order_no: data.order_no || data.orderNo || data.orderInfo?.order_no || queryOrder.order_no || '',
            order_no_hash: data.order_no_hash || data.orderNoHash || queryOrder.order_no_hash || '',
            portal_serial_no: data.portal_serial_no || data.portalNo || data.orderInfo?.portal_serial_no || queryOrder.portal_serial_no || '',
            status: data.status || data.orderStatus || '',
            action: data.action || data._cmd__ || data.type || '',
            raw: data,
        };
    };
    const buildDecouplingExtra = (channelId, queryContext, browserParams) => {
        try {
            let webpackRequire = null;
            const chunks = window.webpackChunkjsxui;
            if (Array.isArray(chunks)) {
                chunks.push([
                    [`backend_redeem_${Date.now()}`],
                    {},
                    require => { webpackRequire = require; },
                ]);
            }
            const helpers = webpackRequire ? webpackRequire(16984) : null;
            if (typeof helpers?.Pl === 'function') {
                return {
                    source: 'official_webpack_helper',
                    value: helpers.Pl(channelId, queryContext || {}, browserParams || {}),
                };
            }
        } catch(e) {
            pushMessage('decoupling_helper_error', String(e));
        }

        const payInfo = window.SERVER_DATA?.payInfo || {};
        const ipInfo = payInfo.ipInfo || {};
        const user = window.SERVER_DATA?.user || {};
        const reportParams = window.SERVER_DATA?.reportParams || {};
        const uuidMatch = document.cookie.match(/UUID=([^;]*)/);
        let fingerId = '';
        try {
            fingerId = JSON.parse(localStorage.getItem('midasbuy_fingerid') || '""') || '';
        } catch(e) {}
        return {
            source: 'local_fallback',
            value: {
                from: browserParams?.from || reportParams.from || 'self.midasbuy_saas',
                shelf_debug_id: queryContext?.debug_id || '',
                loss_level: queryContext?.loss_level || '',
                active_country: '',
                register_country: '',
                ...ipInfo,
                mall_country: ipInfo.mall_ipcountry || '',
                referrer_domain: 'self',
                has_back_btn: '1',
                midasbuy_login_type: user.providerType || 'not_logged_in',
                pay_platform: 'pc',
                midasbuy_adtag: reportParams.adtag || 'no_adtag',
                live_id: '',
                ad_id: '',
                web_language_code: String(payInfo.cgi_language || 'EN').toUpperCase(),
                charac_seq_id: crypto.randomUUID().replace(/-/g, ''),
                midasbuy_fingerid: fingerId,
                if_robot: '0',
                if_agent: '0',
                if_traceless: '0',
                temp_req: JSON.stringify({orderFromUrl: location.href}),
                tdrc_fp: uuidMatch ? uuidMatch[1] : '',
                is_set_passkey: '0',
                is_support_passkey: window.supportPasskey ? '1' : '0',
                game_player_info: JSON.stringify({
                    charac_name: payInfo.charac_name || payInfo.currentBindUser?.charac_name || '',
                    userid: payInfo.userid || payInfo.currentBindUser?.userid || '',
                }),
                is_vip_product: '1',
            },
        };
    };

    try {
        const input = JSON.parse(payloadJson);
        const cleanCode = String(input.pin_code || input.redeem_code || '').replace(/\\s+/g, '');
        if (!cleanCode) return {error: 'missing_redeem_code'};

        if (!window.midas?.buyGame && sdkScript) {
            const script = document.createElement('script');
            script.text = sdkScript;
            document.head.appendChild(script);
            script.remove();
        }
        let midasWait = 0;
        while (!window.midas?.buyGame && midasWait < 10) {
            await new Promise(r => setTimeout(r, 100));
            midasWait++;
        }
        if (!window.midas?.buyGame) {
            return {
                error: 'no_midas_buy_game',
                midasKeys: Object.keys(window).filter(k => k.toLowerCase().includes('midas')),
            };
        }

        let tokenWait = 0;
        while ((!document.getElementById('xMidasToken')?.value) && tokenWait < 150) {
            await new Promise(r => setTimeout(r, 100));
            tokenWait++;
        }
        if (!document.getElementById('xMidasToken')?.value) return {error: 'no_xmidas_token'};

        let storedUser = {};
        try { storedUser = JSON.parse(sessionStorage.getItem('user_login_data') || '{}'); } catch(e) {}
        let verifiedPlayers = {};
        try {
            verifiedPlayers = JSON.parse(sessionStorage.getItem('midasbuy_backend_verified_players') || '{}');
        } catch(e) {}

        const snapshot = window.__backendBootstrap || {};
        const liveServerData = window.SERVER_DATA || {};
        const sd = Object.assign({}, snapshot, liveServerData);
        sd.payInfo = Object.assign({}, snapshot.payInfo || {}, liveServerData.payInfo || {});
        window.SERVER_DATA = sd;

        const payInfo = sd.payInfo;
        const playerId = String(input.player_id || '');
        const verifiedPlayer = verifiedPlayers[playerId] || {};
        if (verifiedPlayer.openid) Object.assign(payInfo, verifiedPlayer);

        const ri = window.__Report_INFO || {};
        const rp = sd.reportParams || {};
        const shopInfo = sd.shopInfo || {};
        const appid = String(input.appid || payInfo.appid || sd.appid || '1450015065');
        const openid = String(verifiedPlayer.openid || payInfo.openid || payInfo.currentBindUser?.openid || '');
        const userid = String(verifiedPlayer.userid || payInfo.userid || payInfo.currentBindUser?.userid || playerId);
        const zoneid = String(verifiedPlayer.zoneid || payInfo.zoneid || payInfo.zone_id || payInfo.currentBindUser?.zoneid || '1');
        const productId = String(input.product_id || '');
        if (!openid) return {error: 'missing_verified_openid', player_id: playerId};
        if (!productId) return {error: 'missing_product_id'};

        const user = sd.user || payInfo.midasUser || storedUser || {};
        const muid = rp.midasuid || ri.midasuid || sd.muid || user.uid || payInfo.midasUser?.uid || storedUser.uid || '';
        const deviceMatch = document.cookie.match(/midasbuyDeviceId=([^;]*)/);
        const deviceId = rp.midasbuyDeviceId || ri.midasbuyDeviceId || (deviceMatch ? deviceMatch[1] : '');
        const uuidMatch = document.cookie.match(/UUID=([^;]*)/);
        const tdrcFp = uuidMatch ? uuidMatch[1] : '';
        let serverTimeOffset = Number(window._SERVER_TIME_OFFSET || 0);
        if (serverTimeOffset > 0 && serverTimeOffset <= 15000) serverTimeOffset = 0;
        const pageTime = Date.now() - serverTimeOffset;
        const pagetoken = btoa(`${location.hostname}_${pageTime}_${openid}`);
        const pf = 'mds_hkweb_pc-v2-android-midasweb-midasbuy';
        const country = String(payInfo.country || sd.country || input.country_code || 'BD').toUpperCase();
        const currencyType = String(payInfo.currency_type || sd.currency_type || 'BDT');
        const localPageId = String(payInfo.pageid || `page_${String(Math.random()).slice(2, 19)}`);
        const orderPageId = String(ri.pageid || rp.pageid || localPageId.replace(/^page_/, ''));
        const buyTypeKey = `CURRENT_BUY_ITEM_REDEEM_${localPageId}`;
        const callbackBase = `${location.protocol}//${location.hostname}:${location.port}/callback/`;
        const messageBase = `${location.protocol}//${location.hostname}:${location.port}`;

        payInfo.appid = appid;
        payInfo.openid = openid;
        payInfo.userid = userid;
        payInfo.zoneid = zoneid;
        payInfo.country = country;
        payInfo.currency_type = currencyType;
        payInfo.pf = pf;
        payInfo.platform = payInfo.platform || 'android';
        payInfo.shop_id = payInfo.shop_id || payInfo.shopcode || shopInfo.shopcode || 'midasbuy';
        payInfo.shopcode = payInfo.shopcode || payInfo.shop_id || shopInfo.shopcode || 'midasbuy';
        payInfo.currentBindUser = Object.assign({}, payInfo.currentBindUser || {}, {openid, userid, zoneid});

        let iframe = document.getElementById('redeemCodeChannelIframe');
        if (!iframe) {
            iframe = document.createElement('iframe');
            iframe.id = 'redeemCodeChannelIframe';
            iframe.setAttribute('frameborder', '0');
            document.body.appendChild(iframe);
        }
        Object.assign(iframe.style, {
            display: 'block',
            visibility: 'visible',
            width: '0px',
            height: '0px',
            position: 'fixed',
            left: '-9999px',
            top: '-9999px',
        });

        const cgiExtend = {
            pagetoken,
            device_id: deviceId,
        };
        const queryContext = input.query_context || {};
        const decoupling = buildDecouplingExtra(
            'MIDASBUY_REDEEM',
            queryContext,
            {from: rp.from || 'self.midasbuy_saas'},
        );
        decoupling.value.game_player_info = JSON.stringify({
            charac_name: verifiedPlayer.charac_name || payInfo.charac_name ||
                payInfo.currentBindUser?.charac_name || '',
            userid,
        });
        decoupling.value.is_vip_product = '1';

        const params = {
            appid,
            shop_id: payInfo.shop_id || 'midasbuy',
            channel: 'os_midaspay_v2',
            subchannel: 'MIDASBUY_REDEEM',
            muid,
            openid,
            country,
            shelf_product_id: productId,
            zoneid,
            currency_type: currencyType,
            platform: payInfo.platform || 'android',
            redeem_code: cleanCode,
            direct_redeem: '1',
            newtab: '0',
            productid: '',
            msgUrl: `${messageBase}/receivemsg?buy_type_key=${buyTypeKey}`,
            pendingUrl: `${callbackBase}pending?buy_type_key:REDEEM`,
            successUrl: `${callbackBase}success?buy_type_key=REDEEM`,
            failUrl: `${callbackBase}fail?buy_type_key=REDEEM`,
            sandbox: '0',
            pf,
            is_vip_product: 'true',
            charac_no: userid,
            drm_info: encodeURIComponent(queryString(payInfo.drm_info || {})),
            pageid: orderPageId,
            decouplingExtraParams: queryString(decoupling.value),
            cgi_extend: queryString(cgiExtend),
            buytype: 'save',
            lan: (sd.countryInfo?.iso?.language || 'en').split('-')[0],
            usePost: '1',
            target: iframe.contentWindow,
        };

        const result = await new Promise(resolve => {
            let done = false;
            const finish = (value) => {
                if (done) return;
                done = true;
                clearTimeout(timer);
                window.removeEventListener('message', onWindowMessage);
                resolve(value);
            };
            const onWindowMessage = (event) => {
                const parsed = parseMaybeJson(event.data);
                pushMessage('window_message', {origin: event.origin, data: parsed});
                const order = extractOrder(parsed);
                if (order.order_no || order.portal_serial_no) {
                    finish(Object.assign({ok: true, source: 'window_message'}, order));
                }
                if (order.action === 'error' || order.status === 'error') {
                    finish({error: 'sdk_window_error', source: 'window_message', data: parsed});
                }
            };
            const timer = setTimeout(() => {
                finish({
                    error: 'sdk_order_timeout',
                    iframe_src: iframe.getAttribute('src') || '',
                    messages,
                });
            }, 12000);

            window.addEventListener('message', onWindowMessage);
            try {
                window.midas.buyGame(params, {
                    onMessage(value) {
                        pushMessage('onMessage', parseMaybeJson(value));
                        const order = extractOrder(value);
                        if (order.order_no || order.portal_serial_no) {
                            finish(Object.assign({ok: true, source: 'onMessage'}, order));
                        }
                        if (order.action === 'error' || order.status === 'error') {
                            finish({error: 'sdk_on_message_error', source: 'onMessage', data: value});
                        }
                    },
                    onSuccess(value) {
                        pushMessage('onSuccess', parseMaybeJson(value));
                        const order = extractOrder(value);
                        finish(Object.assign({ok: true, source: 'onSuccess'}, order));
                    },
                    onError(value) {
                        pushMessage('onError', parseMaybeJson(value));
                        finish({error: 'sdk_on_error', source: 'onError', data: value});
                    },
                });
            } catch(e) {
                finish({
                    error: 'sdk_exception',
                    detail: String(e),
                    stack: (e.stack || '').substring(0, 500),
                });
            }
        });

        const iframeSrc = iframe.getAttribute('src') || '';
        return Object.assign({}, result, {
            order_param_names: Object.keys(params).filter(k => k !== 'target').sort(),
            request_debug: {
                appid,
                openid,
                userid,
                zoneid,
                product_id: productId,
                currency_type: currencyType,
                buy_type_key: buyTypeKey,
                channel: params.channel,
                subchannel: params.subchannel,
                pageid: params.pageid,
                pf: params.pf,
                productid: params.productid,
                shelf_product_id: params.shelf_product_id,
                direct_redeem: params.direct_redeem,
                decoupling_source: decoupling.source,
                decoupling_length: params.decouplingExtraParams.length,
                has_redeem_code: !!cleanCode,
                has_target: !!params.target,
                cgi_extend_len: params.cgi_extend.length,
                has_midas_buy_game: !!window.midas?.buyGame,
            },
            iframe_src: iframeSrc.split('encrypt_msg=', 1)[0],
            messages,
        });
    } catch(e) {
        return {
            error: 'js_exception',
            detail: String(e),
            stack: (e.stack || '').substring(0, 500),
            messages,
        };
    }
}
"""


def _setup_chaos_vm_protection(page) -> None:
    """
    Register a page.route intercept for the Chaos VM CDN URL BEFORE page.goto.

    Serves the local JS file (or fetches from CDN as fallback) with
    _CHAOS_VM_PROTECTION appended.  The protection runs synchronously during
    script execution — before any React hydration task — so window.xMidas
    is locked with configurable:false and can never be deleted by the SPA.
    """
    def handle_route(route):
        try:
            with open(_CHAOS_VM_LOCAL_PATH, "rb") as f:
                original = f.read()
            route.fulfill(
                status=200,
                headers={
                    "content-type": "application/javascript; charset=utf-8",
                    "cache-control": "no-cache",
                },
                body=original + _CHAOS_VM_PROTECTION,
            )
            logger.info(
                "[CRYPTO] chaos VM served from local file + protection (%d bytes total)",
                len(original) + len(_CHAOS_VM_PROTECTION),
            )
        except Exception as e:
            logger.warning("[CRYPTO] local chaos VM unavailable (%s) — fetching from CDN", e)
            try:
                response = route.fetch()
                body = response.body() + _CHAOS_VM_PROTECTION
                hdrs = dict(response.headers)
                hdrs.pop("content-length", None)
                route.fulfill(status=response.status, headers=hdrs, body=body)
                logger.info("[CRYPTO] chaos VM fetched from CDN + protection appended")
            except Exception as e2:
                logger.error("[CRYPTO] CDN fetch also failed (%s) — no protection", e2)
                route.continue_()

    page.route("**cdn.midasbuy.com/js/x-midas/**", handle_route)
    logger.info("[CRYPTO] chaos VM route intercept registered")


def _setup_lightweight_routes(page) -> None:
    """Skip heavy resources that are not needed for hidden tokens or xMidas."""
    def handle_route(route):
        try:
            if route.request.resource_type in {"image", "font", "media"}:
                route.abort()
            else:
                route.continue_()
        except Exception:
            try:
                route.continue_()
            except Exception:
                pass

    page.route("**/*", handle_route)
    logger.info("[CRYPTO] lightweight resource route registered")


def _load_session_storage(storage_state_path: str) -> dict:
    ss_path = os.path.join(os.path.dirname(storage_state_path), "session_storage.json")
    if not os.path.exists(ss_path):
        return {}
    try:
        with open(ss_path, encoding="utf-8") as f:
            data = json.load(f)
        logger.info("[CRYPTO] loaded %d sessionStorage keys", len(data))
        return data
    except Exception as e:
        logger.warning("[CRYPTO] could not load session_storage.json: %s", e)
        return {}


def _select_server_data_snapshot(data: dict) -> dict:
    keys = (
        "country",
        "appid",
        "muid",
        "payInfo",
        "reportParams",
        "_Exp_DATA",
        "user",
        "shopInfo",
        "countryInfo",
        "buyType",
        "gameConfig",
        "newRiskCtrlComponentOptions",
    )
    return {key: data.get(key) for key in keys if key in data}


def _server_data_snapshot_is_complete(data: dict) -> bool:
    pay_info = data.get("payInfo") or {}
    ip_info = pay_info.get("ipInfo") or {}
    return bool(
        ip_info.get("mall_ip")
        and pay_info.get("drm_info")
        and data.get("_Exp_DATA")
    )


def _load_server_data_snapshot(storage_state_path: str) -> dict:
    session_dir = os.path.dirname(storage_state_path)
    snapshot_path = os.path.join(session_dir, "server_data.json")

    if os.path.exists(snapshot_path):
        try:
            with open(snapshot_path, encoding="utf-8") as f:
                data = json.load(f)
            snapshot = _select_server_data_snapshot(data)
            if _server_data_snapshot_is_complete(snapshot):
                logger.info("[CRYPTO] loaded complete SERVER_DATA snapshot")
                return snapshot
            logger.warning(
                "[CRYPTO] SERVER_DATA snapshot is incomplete; recovering from browser_page.html"
            )
        except Exception as exc:
            logger.warning("[CRYPTO] could not load server_data.json: %s", exc)

    html_path = os.path.join(session_dir, "browser_page.html")
    if not os.path.exists(html_path):
        return {}

    try:
        with open(html_path, encoding="utf-8") as f:
            html = f.read()
        marker = "var SERVER_DATA = "
        start = html.find(marker)
        if start < 0:
            return {}
        start += len(marker)
        data, _ = json.JSONDecoder().raw_decode(html[start:])
        snapshot = _select_server_data_snapshot(data)
        if not _server_data_snapshot_is_complete(snapshot):
            logger.warning(
                "[CRYPTO] browser_page.html SERVER_DATA bootstrap is incomplete"
            )
            return {}
        with open(snapshot_path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=4)
        logger.info(
            "[CRYPTO] recovered complete SERVER_DATA snapshot from browser_page.html"
        )
        return snapshot
    except Exception as exc:
        logger.warning("[CRYPTO] could not recover SERVER_DATA snapshot: %s", exc)
        return {}


def _restore_server_data_snapshot(page, storage_state_path: str) -> None:
    snapshot = _load_server_data_snapshot(storage_state_path)
    if not snapshot:
        logger.warning("[CRYPTO] no SERVER_DATA snapshot available")
        return

    try:
        result = page.evaluate("""
            (snapshot) => {
                window.__backendBootstrap = snapshot;
                const live = window.SERVER_DATA || {};
                const merged = Object.assign({}, snapshot, live);
                merged.payInfo = Object.assign(
                    {},
                    snapshot.payInfo || {},
                    live.payInfo || {}
                );
                window.SERVER_DATA = merged;
                return {
                    pay: !!Object.keys(merged.payInfo || {}).length,
                    ip: !!merged.payInfo?.ipInfo?.mall_ip,
                    drm: !!Object.keys(merged.payInfo?.drm_info || {}).length,
                    exp: !!Object.keys(merged._Exp_DATA || {}).length,
                };
            }
        """, snapshot)
        logger.info("[CRYPTO] restored SERVER_DATA snapshot: %s", result)
    except Exception as exc:
        logger.warning("[CRYPTO] SERVER_DATA snapshot restore failed: %s", exc)


def _launch_context(p, storage_state_path: str, country_code: str, bypass_csp: bool = False,
                    headless: Optional[bool] = None):
    from django.conf import settings

    ss_data = _load_session_storage(storage_state_path)
    server_data = _load_server_data_snapshot(storage_state_path)

    if headless is None:
        headless = getattr(settings, "MIDASBUY_CRYPTO_BROWSER_HEADLESS", True)
    browser = p.chromium.launch(
        headless=headless,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled",
        ],
    )

    timezone_by_country = {
        "bd": "Asia/Dhaka",
        "br": "America/Sao_Paulo",
        "id": "Asia/Jakarta",
        "in": "Asia/Kolkata",
        "my": "Asia/Kuala_Lumpur",
        "ph": "Asia/Manila",
        "pk": "Asia/Karachi",
        "sa": "Asia/Riyadh",
        "tr": "Europe/Istanbul",
        "us": "America/New_York",
    }
    context = browser.new_context(
        storage_state=storage_state_path,
        viewport=getattr(settings, "MIDASBUY_BROWSER_VIEWPORT", {"width": 1440, "height": 900}),
        locale="en-US",
        timezone_id=timezone_by_country.get(country_code.lower(), "UTC"),
        bypass_csp=bypass_csp,
    )

    context.add_init_script(_STEALTH_JS)

    if ss_data:
        ss_json = json.dumps(ss_data)
        context.add_init_script(f"""
            (() => {{
                const data = {ss_json};
                for (const [k,v] of Object.entries(data)) {{
                    try {{ sessionStorage.setItem(k, v); }} catch(e) {{}}
                }}
            }})();
        """)

    if server_data:
        server_data_json = json.dumps(server_data, separators=(",", ":"))
        context.add_init_script(f"""
            (() => {{
                const snapshot = {server_data_json};
                window.__backendBootstrap = snapshot;
                const live = window.SERVER_DATA || {{}};
                window.SERVER_DATA = Object.assign({{}}, snapshot, live);
                window.SERVER_DATA.payInfo = Object.assign(
                    {{}},
                    snapshot.payInfo || {{}},
                    live.payInfo || {{}}
                );
            }})();
        """)

    return browser, context


def _storage_mtime(storage_state_path: str) -> float:
    try:
        return os.path.getmtime(storage_state_path)
    except OSError:
        return 0.0


def _session_cache_key(storage_state_path: str, country_code: str) -> Tuple[str, str, int]:
    # Playwright sync objects are thread-affine, so cache per worker thread.
    return (os.path.abspath(storage_state_path), country_code.lower(), get_ident())


def _session_is_usable(session: _CachedBrowserSession, storage_mtime: float) -> bool:
    if session.storage_mtime != storage_mtime:
        return False
    try:
        if session.page.is_closed():
            return False
        if hasattr(session.browser, "is_connected") and not session.browser.is_connected():
            return False
    except Exception:
        return False
    return True


def _close_cached_session(session: _CachedBrowserSession) -> None:
    for obj, method_name in (
        (session.context, "close"),
        (session.browser, "close"),
    ):
        try:
            getattr(obj, method_name)()
        except Exception:
            pass
    try:
        session.manager.__exit__(None, None, None)
    except Exception:
        pass


def _stop_playwright_manager(manager) -> None:
    if manager is None:
        return
    try:
        manager.__exit__(None, None, None)
    except Exception:
        pass


def _discard_cached_session(session: _CachedBrowserSession) -> None:
    with _SESSION_CACHE_LOCK:
        for key, cached in list(_SESSION_CACHE.items()):
            if cached is session:
                _SESSION_CACHE.pop(key, None)
    _close_cached_session(session)


def close_cached_browser_sessions() -> None:
    """Best-effort shutdown hook for warmed browser sessions."""
    with _SESSION_CACHE_LOCK:
        sessions = list(_SESSION_CACHE.values())
        _SESSION_CACHE.clear()

    for session in sessions:
        with session.lock:
            _close_cached_session(session)


def _create_cached_session(
    storage_state_path: str,
    country_code: str,
    timeout_ms: int,
) -> _CachedBrowserSession:
    sync_playwright, PWTimeout = _get_playwright()

    storage_state_path = os.path.abspath(storage_state_path)
    redeem_url = (
        f"https://www.midasbuy.com/midasbuy/{country_code}/redeem/pubgm"
        "?from=self.midasbuy_saas"
    )
    session_dir = os.path.dirname(storage_state_path)
    manager = None
    browser = None
    context = None

    try:
        manager = sync_playwright()
        p = manager.start()
        browser, context = _launch_context(p, storage_state_path, country_code, bypass_csp=True)
        page = context.new_page()

        _setup_lightweight_routes(page)
        _setup_chaos_vm_protection(page)

        logger.info("[CRYPTO] warming cached page %s", redeem_url)
        page.goto(redeem_url, wait_until="domcontentloaded", timeout=timeout_ms)
        try:
            page.wait_for_load_state("load", timeout=20_000)
        except PWTimeout:
            logger.warning("[CRYPTO] page load event timed out; continuing with initialized DOM")
        page.wait_for_timeout(2_000)
        _restore_server_data_snapshot(page, storage_state_path)
        logger.info("[CRYPTO] cached page ready url=%s", page.url)

        if not _wait_for_xmidas(page, session_dir, timeout_ms):
            raise RuntimeError("xMidas did not become ready")

        now = time.time()
        return _CachedBrowserSession(
            manager=manager,
            browser=browser,
            context=context,
            page=page,
            storage_state_path=storage_state_path,
            country_code=country_code.lower(),
            storage_mtime=_storage_mtime(storage_state_path),
            created_at=now,
            last_used=now,
        )
    except Exception:
        logger.exception("[CRYPTO] cached page warm-up timed out")
        if context:
            try:
                _save_debug(context.pages[0], session_dir, "crypto_cache_timeout")
            except Exception:
                pass
        if context:
            try:
                context.close()
            except Exception:
                pass
        if browser:
            try:
                browser.close()
            except Exception:
                pass
        _stop_playwright_manager(manager)
        raise


def _get_or_create_cached_session(
    storage_state_path: str,
    country_code: str,
    timeout_ms: int,
) -> _CachedBrowserSession:
    key = _session_cache_key(storage_state_path, country_code)
    storage_mtime = _storage_mtime(os.path.abspath(storage_state_path))

    with _SESSION_CACHE_LOCK:
        session = _SESSION_CACHE.get(key)
        if session and _session_is_usable(session, storage_mtime):
            session.last_used = time.time()
            logger.info("[CRYPTO] reusing cached browser session")
            return session

        if session:
            _SESSION_CACHE.pop(key, None)
            _close_cached_session(session)

        session = _create_cached_session(storage_state_path, country_code, timeout_ms)
        _SESSION_CACHE[key] = session
        return session


def _wait_for_xmidas(page, session_dir: str, timeout_ms: int) -> bool:
    from playwright.sync_api import TimeoutError as PWTimeout
    try:
        from patchright.sync_api import TimeoutError as PWTimeout
    except ImportError:
        pass

    try:
        page.wait_for_function(
            "() => !!document.getElementById('xMidasToken')?.value",
            timeout=timeout_ms,
        )
        logger.info("[CRYPTO] xMidasToken ready")
    except PWTimeout:
        logger.error("[CRYPTO] timeout waiting for xMidasToken")
        _save_debug(page, session_dir, "crypto_no_token")
        return False

    try:
        has_xmidas = page.evaluate("() => typeof window.xMidas === 'function'")
    except Exception:
        has_xmidas = False

    if not has_xmidas:
        try:
            page.wait_for_function(
                "() => typeof window.xMidas === 'function'",
                timeout=10_000,
            )
            has_xmidas = page.evaluate(
                "() => typeof window.xMidas === 'function'"
            )
            if has_xmidas:
                logger.info("[CRYPTO] native window.xMidas became ready")
        except PWTimeout:
            pass

    if not has_xmidas:
        try:
            logger.info("[CRYPTO] window.xMidas missing - injecting local Chaos VM")
            with open(_CHAOS_VM_LOCAL_PATH, "r", encoding="utf-8") as f:
                vm_source = f.read() + _CHAOS_VM_PROTECTION.decode("ascii")
            page.evaluate("(source) => { (0, eval)(source); }", vm_source)
            has_xmidas = page.evaluate("() => typeof window.xMidas === 'function'")
            logger.info("[CRYPTO] local Chaos VM injection xMidas=%s", has_xmidas)
        except Exception as exc:
            logger.warning("[CRYPTO] local Chaos VM injection failed: %s", exc)

    try:
        has_xmidas = page.evaluate("() => typeof window.xMidas === 'function'")
    except PWTimeout:
        logger.warning("[CRYPTO] window.xMidas not detected after 30s — JS evaluate will poll")

    if not has_xmidas:
        try:
            logger.info("[CRYPTO] transient xMidas disappeared - injecting locked local VM")
            with open(_CHAOS_VM_LOCAL_PATH, "r", encoding="utf-8") as f:
                vm_source = f.read() + _CHAOS_VM_PROTECTION.decode("ascii")
            page.evaluate("(source) => { (0, eval)(source); }", vm_source)
            has_xmidas = page.evaluate(
                "() => typeof window.xMidas === 'function'"
            )
        except Exception as exc:
            logger.warning("[CRYPTO] final local Chaos VM injection failed: %s", exc)

    try:
        diag = page.evaluate("""
            () => ({
                xMidasType:  typeof window.xMidas,
                xMidasToken: !!document.getElementById('xMidasToken')?.value,
                url:         location.href,
                readyState:  document.readyState,
                deviceIdReady: !!(
                    window.SERVER_DATA?.reportParams?.midasbuyDeviceId ||
                    window.__Report_INFO?.midasbuyDeviceId ||
                    /(?:^|; )midasbuyDeviceId=/.test(document.cookie)
                ),
                muidReady: !!(
                    window.SERVER_DATA?.reportParams?.midasuid ||
                    window.__Report_INFO?.midasuid ||
                    window.SERVER_DATA?.muid ||
                    window.SERVER_DATA?.user?.uid ||
                    window.SERVER_DATA?.payInfo?.midasUser?.uid ||
                    sessionStorage.getItem('user_login_data')
                ),
                uuidReady: /(?:^|; )UUID=/.test(document.cookie),
                userAgent: navigator.userAgent,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                midasKeys:   Object.keys(window).filter(k => k.toLowerCase().includes('midas')),
            })
        """)
        logger.info("[CRYPTO] pre-call diag: %s", diag)
        has_xmidas = diag.get("xMidasType") == "function"
    except Exception as _e:
        logger.warning("[CRYPTO] diag failed: %s", _e)

    if not has_xmidas:
        logger.error("[CRYPTO] window.xMidas is not stable after initialization")
        _save_debug(page, session_dir, "crypto_unstable_xmidas")

    return has_xmidas


# ── Public API ────────────────────────────────────────────────────────────────

def _extract_browser_result(result: Optional[dict], endpoint: str) -> Optional[dict]:
    if not result:
        logger.error("[CRYPTO] evaluate returned None")
        return None

    if result.get("error"):
        logger.error(
            "[CRYPTO] fetch failed  endpoint=%s  error=%s  status=%s  encrypt_msg_len=%s  midasKeys=%s",
            endpoint,
            result.get("error"),
            result.get("status"),
            result.get("encrypt_msg_len", "?"),
            result.get("midasKeys"),
        )
        return None

    logger.info(
        "[CRYPTO] ok  status=%s  encrypt_msg_len=%s  full_json_len=%s  "
        "cgi_len=%s  drm_len=%s  exp_len=%s  pagetoken_len=%s  "
        "device=%s  muid=%s  ip=%s  drm=%s  exp=%s  verified_players=%s  "
        "verified_player_applied=%s  "
        "request_fields=%s  request_debug=%s  public_fields=%s",
        result.get("status"),
        result.get("encrypt_msg_len"),
        result.get("full_json_length"),
        result.get("cgi_extend_length"),
        result.get("drm_info_length"),
        result.get("exp_data_length"),
        result.get("pagetoken_length"),
        result.get("has_device_id"),
        result.get("has_muid"),
        result.get("has_ip_info"),
        result.get("has_drm_info"),
        result.get("has_exp_data"),
        result.get("verified_player_count"),
        result.get("verified_player_applied"),
        result.get("request_field_names"),
        result.get("request_debug"),
        result.get("public_field_names"),
    )
    return result.get("data")


def _call_api_in_cached_browser(
    payload: dict,
    endpoint: str,
    storage_state_path: str,
    country_code: str,
    method: str,
    timeout_ms: int,
) -> Optional[dict]:
    payload_json = json.dumps(payload, separators=(",", ":"))

    for attempt in (1, 2):
        try:
            session = _get_or_create_cached_session(storage_state_path, country_code, timeout_ms)
        except Exception:
            logger.exception("[CRYPTO] could not create cached browser session")
            return None

        with session.lock:
            try:
                logger.info("[CRYPTO] cached in-browser fetch endpoint=%s attempt=%d", endpoint, attempt)
                result = session.page.evaluate(_JS_CALL_API, {
                    "payloadJson": payload_json,
                    "endpoint":    endpoint,
                    "method":      method,
                })
                session.last_used = time.time()
            except Exception:
                logger.exception("[CRYPTO] cached page evaluate failed")
                _discard_cached_session(session)
                if attempt == 1:
                    continue
                return None

            if result and result.get("error") in {
                "no_xmidas_token",
                "no_xmidas_function",
                "xmidas_empty",
                "js_exception",
            }:
                logger.warning("[CRYPTO] cached page stale (%s), rebuilding", result.get("error"))
                _discard_cached_session(session)
                if attempt == 1:
                    continue

            return _extract_browser_result(result, endpoint)

    return None


def _sdk_redeem_error_message(result: dict) -> str:
    error = str(result.get("error") or "sdk_order_failed")
    if error == "sdk_order_timeout":
        return (
            "Midasbuy did not return an order confirmation from the redeem "
            "iframe. The code has not been confirmed as redeemed."
        )
    if error == "no_midas_buy_game":
        return "Midasbuy redeem SDK did not initialize in the browser session."
    if error == "missing_product_id":
        return "Redeem product information was missing before final confirmation."
    if error == "missing_verified_openid":
        return "Player lookup data was missing before final confirmation."
    if error.startswith("sdk_on_error") or error.startswith("sdk_window_error"):
        data = result.get("data")
        if isinstance(data, dict):
            return data.get("msg") or data.get("message") or error
    return error


def _eval_main_world_async(page, fn_source: str, args: dict, timeout_ms: int) -> Optional[dict]:
    """
    Run an async arrow function (fn_source, e.g. _JS_REDEEM_ORDER) in the page
    MAIN world — where window.midas lives — instead of patchright's isolated
    world, and poll the JSON result back via a DOM element. Requires bypass_csp.
    """
    nonce = os.urandom(6).hex()
    page.evaluate(
        """(a) => {
            const inEl = document.createElement('div');
            inEl.id = '__ro_in_' + a.nonce; inEl.style.display = 'none';
            inEl.textContent = a.input;
            inEl.setAttribute('data-fn', a.fn);
            document.documentElement.appendChild(inEl);
            const outEl = document.createElement('div');
            outEl.id = '__ro_out_' + a.nonce; outEl.style.display = 'none';
            document.documentElement.appendChild(outEl);
            const s = document.createElement('script');
            s.textContent =
                '(function(){var i=document.getElementById("__ro_in_' + a.nonce + '");' +
                'var o=document.getElementById("__ro_out_' + a.nonce + '");try{' +
                'var fn=(0,eval)("(" + i.getAttribute("data-fn") + ")");' +
                'Promise.resolve(fn(JSON.parse(i.textContent))).then(function(r){' +
                'o.textContent=JSON.stringify(r===undefined?null:r);}).catch(function(e){' +
                'o.textContent=JSON.stringify({error:"mainworld_exception",detail:String(e)});});' +
                '}catch(e){o.textContent=JSON.stringify({error:"mainworld_eval",detail:String(e)});}})();';
            document.documentElement.appendChild(s);
            s.remove();
        }""",
        {"nonce": nonce, "input": json.dumps(args), "fn": fn_source},
    )

    import time as _t
    deadline = _t.time() + timeout_ms / 1000.0
    while _t.time() < deadline:
        raw = page.evaluate(
            "(n) => { const o = document.getElementById('__ro_out_' + n); return o && o.textContent ? o.textContent : null; }",
            nonce,
        )
        if raw:
            try:
                return json.loads(raw)
            except Exception:
                return {"error": "mainworld_bad_json"}
        page.wait_for_timeout(500)
    return {"error": "mainworld_timeout"}


def call_redeem_order_in_browser(
    payload: dict,
    storage_state_path: str,
    country_code: str = "bd",
    timeout_ms: int = 60_000,
) -> Optional[dict]:
    """
    Submit the actual Midasbuy redeem transaction through the official SDK.

    QueryRedeemCodeInfo only validates the code. A real successful redemption
    emits /callback/success with order_no/order_no_hash through the hidden
    MIDASBUY_REDEEM iframe. This function invokes window.midas.buyGame and
    returns only the SDK/order message, not the result-page JSON.
    """
    payload_json = json.dumps(payload, separators=(",", ":"))
    sdk_script = ""
    try:
        with open(_MIDAS_SDK_LOCAL_PATH, encoding="utf-8") as file:
            sdk_script = file.read()
    except OSError as exc:
        logger.warning("[CRYPTO] local Midas SDK unavailable: %s", exc)

    for attempt in (1, 2):
        try:
            session = _get_or_create_cached_session(
                storage_state_path,
                country_code,
                timeout_ms,
            )
        except Exception:
            logger.exception("[CRYPTO] could not create cached browser session")
            return None

        with session.lock:
            network_events = []

            def _record_network_event(kind, obj):
                try:
                    url = obj.url
                    if not (
                        "midasbuy.com" in url
                        or "harvestsharp.com" in url
                        or "api.unipay.qq.com" in url
                    ):
                        return

                    event = {
                        "kind": kind,
                        "method": getattr(obj, "method", None),
                        "url": url.split("encrypt_msg=", 1)[0],
                    }
                    if kind == "response":
                        event["status"] = obj.status
                        event["method"] = obj.request.method
                    if len(network_events) < 60:
                        network_events.append(event)
                except Exception:
                    pass

            def _on_request(req):
                _record_network_event("request", req)

            def _on_response(resp):
                _record_network_event("response", resp)
                # Save the result-page / callback bodies for debugging the commit.
                try:
                    u = resp.url.lower()
                    if "/result/" in u or "/callback/" in u:
                        body = None
                        try:
                            body = resp.text()
                        except Exception:
                            body = None
                        dbg = os.path.join(os.path.dirname(storage_state_path), "redeem_commit_debug.txt")
                        with open(dbg, "a", encoding="utf-8") as f:
                            f.write(f"\n<< {resp.status} {resp.url.split('encrypt_msg=',1)[0]}\n")
                            if body:
                                f.write(body[:60000] + "\n")
                        logger.info("[CRYPTO] redeem commit %s %s (saved to redeem_commit_debug.txt)",
                                    resp.status, resp.url.split("encrypt_msg=", 1)[0][:110])
                except Exception:
                    pass

            try:
                logger.info("[CRYPTO] cached redeem SDK order attempt=%d (main world)", attempt)
                session.page.on("request", _on_request)
                session.page.on("response", _on_response)
                # window.midas lives in the MAIN world; patchright evaluate is
                # isolated, so run the order there via the main-world bridge.
                result = _eval_main_world_async(
                    session.page,
                    _JS_REDEEM_ORDER,
                    {"payloadJson": payload_json, "sdkScript": sdk_script},
                    18_000,
                )
                session.last_used = time.time()
            except Exception:
                logger.exception("[CRYPTO] cached redeem SDK order evaluate failed")
                _discard_cached_session(session)
                if attempt == 1:
                    continue
                return None
            finally:
                try:
                    session.page.remove_listener("request", _on_request)
                    session.page.remove_listener("response", _on_response)
                except Exception:
                    pass

            if not result:
                logger.error("[CRYPTO] redeem SDK order evaluate returned None")
                return None

            success_callback = next(
                (
                    event for event in network_events
                    if event.get("kind") == "response"
                    and event.get("status") == 200
                    and "/callback/success" in event.get("url", "")
                ),
                None,
            )
            if success_callback:
                callback_query = parse_qs(urlparse(success_callback["url"]).query)
                order_no = (callback_query.get("order_no") or [""])[0]
                order_no_hash = (callback_query.get("order_no_hash") or [""])[0]
                if order_no and order_no_hash:
                    result.update(
                        {
                            "ok": True,
                            "error": None,
                            "source": "callback_success",
                            "order_no": order_no,
                            "order_no_hash": order_no_hash,
                            "callback_url": success_callback["url"],
                        }
                    )

            if result.get("error") in {
                "no_xmidas_token",
                "js_exception",
            }:
                logger.warning(
                    "[CRYPTO] cached page stale during redeem SDK order (%s), rebuilding",
                    result.get("error"),
                )
                _discard_cached_session(session)
                if attempt == 1:
                    continue

            logger.info(
                "[CRYPTO] redeem SDK order result ok=%s error=%s source=%s "
                "order_no=%s portal_serial_no=%s iframe_src=%s",
                result.get("ok"),
                result.get("error"),
                result.get("source"),
                result.get("order_no"),
                result.get("portal_serial_no"),
                result.get("iframe_src"),
            )
            logger.info(
                "[CRYPTO] redeem SDK order debug=%s",
                json.dumps(result.get("request_debug") or {}, ensure_ascii=False),
            )
            logger.debug(
                "[CRYPTO] redeem SDK order messages=%s",
                json.dumps(result.get("messages") or [], ensure_ascii=False, default=str)[:5000],
            )
            logger.debug(
                "[CRYPTO] redeem SDK order network events=%s",
                json.dumps(network_events, ensure_ascii=False),
            )

            if result.get("error"):
                return {
                    "ret": 1,
                    "err_code": result.get("error"),
                    "msg": _sdk_redeem_error_message(result),
                    "sdk_result": result,
                    "network_events": network_events,
                }

            result["network_events"] = network_events
            return result

    return None


def call_redeem_result_in_browser(
    payload: dict,
    storage_state_path: str,
    country_code: str = "bd",
    timeout_ms: int = 60_000,
) -> Optional[dict]:
    """
    Confirm a valid redeem code by loading Midasbuy's encrypted result route.

    The official redeem confirmation does not POST another JSON API in the
    captured HAR. It navigates/fetches:
        /midasbuy/<country>/result/pubgm?...&encrypt_msg=...&ctoken=...
    where encrypt_msg is generated from {t, h, o}, not the full redeem payload.
    """
    payload_json = json.dumps(payload, separators=(",", ":"))

    for attempt in (1, 2):
        try:
            session = _get_or_create_cached_session(
                storage_state_path,
                country_code,
                timeout_ms,
            )
        except Exception:
            logger.exception("[CRYPTO] could not create cached browser session")
            return None

        with session.lock:
            network_events = []

            def _record_network_event(kind, obj):
                try:
                    url = obj.url
                    if not (
                        "midasbuy.com" in url
                        or "harvestsharp.com" in url
                        or "tencent.com" in url
                    ):
                        return

                    event = {
                        "kind": kind,
                        "method": getattr(obj, "method", None),
                        "url": url.split("encrypt_msg=", 1)[0],
                    }
                    if kind == "response":
                        event["status"] = obj.status
                        event["method"] = obj.request.method
                    if len(network_events) < 30:
                        network_events.append(event)
                except Exception:
                    pass

            def _on_request(req):
                _record_network_event("request", req)

            def _on_response(resp):
                _record_network_event("response", resp)

            try:
                logger.info("[CRYPTO] cached redeem result GET attempt=%d", attempt)
                session.page.on("request", _on_request)
                session.page.on("response", _on_response)
                result = session.page.evaluate(_JS_REDEEM_RESULT_PAGE, {
                    "payloadJson": payload_json,
                })
                session.last_used = time.time()
            except Exception:
                logger.exception("[CRYPTO] cached redeem result evaluate failed")
                _discard_cached_session(session)
                if attempt == 1:
                    continue
                return None
            finally:
                try:
                    session.page.remove_listener("request", _on_request)
                    session.page.remove_listener("response", _on_response)
                except Exception:
                    pass

            if result and result.get("error") in {
                "no_xmidas_token",
                "no_xmidas_function",
                "xmidas_empty",
                "js_exception",
            }:
                logger.warning(
                    "[CRYPTO] cached page stale during redeem result (%s), rebuilding",
                    result.get("error"),
                )
                _discard_cached_session(session)
                if attempt == 1:
                    continue

            if not result:
                logger.error("[CRYPTO] redeem result evaluate returned None")
                return None

            if result.get("error"):
                logger.error(
                    "[CRYPTO] redeem result failed error=%s status=%s detail=%s text=%s",
                    result.get("error"),
                    result.get("status"),
                    result.get("detail"),
                    result.get("text"),
                )
                return None

            logger.info(
                "[CRYPTO] redeem result ok status=%s encrypt_msg_len=%s "
                "full_json_len=%s pagetoken_len=%s openid=%s buy_type_key=%s "
                "verified_player_applied=%s result_url=%s",
                result.get("status"),
                result.get("encrypt_msg_len"),
                result.get("full_json_length"),
                result.get("pagetoken_length"),
                result.get("result_openid"),
                result.get("buy_type_key"),
                result.get("verified_player_applied"),
                result.get("result_url", "").split("encrypt_msg=", 1)[0],
            )

            data = result.get("data")
            if isinstance(data, dict):
                pay_info = data.get("payInfo") if isinstance(data.get("payInfo"), dict) else {}
                current_bind_user = (
                    pay_info.get("currentBindUser")
                    if isinstance(pay_info.get("currentBindUser"), dict)
                    else {}
                )
                logger.info(
                    "[CRYPTO] redeem result markers pageHandlerName=%s type=%s "
                    "isRedeem=%s appid=%s bind_openid=%s bind_userid=%s",
                    data.get("pageHandlerName"),
                    data.get("type"),
                    data.get("isRedeem"),
                    data.get("appid"),
                    current_bind_user.get("openid"),
                    current_bind_user.get("userid"),
                )
            logger.debug(
                "[CRYPTO] redeem result network events=%s",
                json.dumps(network_events, ensure_ascii=False),
            )
            return data

    return None


def call_api_in_browser(
    payload: dict,
    endpoint: str,
    storage_state_path: str,
    country_code: str = "bd",
    method: str = "POST",
    timeout_ms: int = 60_000,
) -> Optional[dict]:
    """
    Navigate to the Midasbuy redeem page, run window.xMidas and fetch()
    entirely inside the browser, return the parsed JSON response.
    """
    if endpoint.rstrip("/") in _CACHED_ENDPOINTS:
        cached_data = _call_api_in_cached_browser(
            payload,
            endpoint,
            storage_state_path,
            country_code,
            method,
            timeout_ms,
        )
        if cached_data is not None:
            return cached_data
        logger.warning("[CRYPTO] cached call failed; falling back to a fresh browser endpoint=%s", endpoint)

    sync_playwright, PWTimeout = _get_playwright()

    redeem_url  = f"https://www.midasbuy.com/midasbuy/{country_code}/redeem/pubgm"
    session_dir = os.path.dirname(storage_state_path)

    try:
        with sync_playwright() as p:
            browser, context = _launch_context(p, storage_state_path, country_code)
            page = context.new_page()

            # Route intercept must be registered BEFORE page.goto
            _setup_chaos_vm_protection(page)

            logger.info("[CRYPTO] navigating to %s", redeem_url)
            try:
                page.goto(redeem_url, wait_until="load", timeout=timeout_ms)
            except PWTimeout:
                logger.error("[CRYPTO] page.goto timed out")
                _save_debug(page, session_dir, "crypto_timeout")
                browser.close()
                return None

            _restore_server_data_snapshot(page, storage_state_path)
            logger.info("[CRYPTO] page loaded  url=%s", page.url)

            if not _wait_for_xmidas(page, session_dir, timeout_ms):
                browser.close()
                return None

            payload_json = json.dumps(payload, separators=(",", ":"))
            logger.info("[CRYPTO] calling in-browser fetch  endpoint=%s", endpoint)

            result = page.evaluate(_JS_CALL_API, {
                "payloadJson": payload_json,
                "endpoint":    endpoint,
                "method":      method,
            })

            _save_debug(page, session_dir, "crypto_done")
            browser.close()

            return _extract_browser_result(result, endpoint)

    except Exception:
        logger.exception("[CRYPTO] call_api_in_browser crashed")
        return None


def get_browser_payload(
    payload: dict,
    storage_state_path: str,
    country_code: str = "bd",
    timeout_ms: int = 45_000,
) -> Optional[dict]:
    """Return {encrypt_msg, ctoken, ctoken_ver, fresh_cookies} or None."""
    sync_playwright, PWTimeout = _get_playwright()

    redeem_url  = f"https://www.midasbuy.com/midasbuy/{country_code}/redeem/pubgm"
    session_dir = os.path.dirname(storage_state_path)

    try:
        with sync_playwright() as p:
            browser, context = _launch_context(p, storage_state_path, country_code)
            page = context.new_page()

            _setup_chaos_vm_protection(page)

            logger.info("[CRYPTO] navigating to %s", redeem_url)
            try:
                page.goto(redeem_url, wait_until="load", timeout=timeout_ms)
            except PWTimeout:
                logger.error("[CRYPTO] page.goto timed out")
                _save_debug(page, session_dir, "crypto_timeout")
                browser.close()
                return None

            _restore_server_data_snapshot(page, storage_state_path)
            if not _wait_for_xmidas(page, session_dir, timeout_ms):
                browser.close()
                return None

            payload_json = json.dumps(payload, separators=(",", ":"))
            result = page.evaluate(_JS_ENCRYPT_ONLY, {"payloadJson": payload_json})

            fresh_cookies = {
                c["name"]: c["value"]
                for c in context.cookies()
                if c.get("name") and c.get("value")
            }

            _save_debug(page, session_dir, "crypto_done")
            browser.close()

            if not result or result.get("error"):
                logger.error("[CRYPTO] JS error: %s", result)
                return None

            logger.info(
                "[CRYPTO] ok  ctoken_prefix=%s  encrypt_msg_len=%d",
                result["ctoken"][:20],
                len(result["encrypt_msg"]),
            )
            return {
                "encrypt_msg":   result["encrypt_msg"],
                "ctoken":        result["ctoken"],
                "ctoken_ver":    result["ctoken_ver"],
                "fresh_cookies": fresh_cookies,
            }

    except Exception:
        logger.exception("[CRYPTO] get_browser_payload crashed")
        return None


def _save_debug(page, session_dir: str, name: str) -> None:
    try:
        page.screenshot(path=os.path.join(session_dir, f"{name}.png"), full_page=True)
        with open(os.path.join(session_dir, f"{name}.html"), "w", encoding="utf-8") as f:
            f.write(page.content())
        logger.info("[CRYPTO] debug artifacts saved: %s/%s.*", session_dir, name)
    except Exception as e:
        logger.debug("[CRYPTO] could not save debug artifacts: %s", e)


# ── Captcha auto-solve: obtain rc_token / rc_uuid via a paid provider ────────────
#
# Replaces the manual slider solve. Drives window.midas.newRiskControl(challenge)
# headlessly, hooks window.TencentCaptcha in every frame to capture the slider's
# success callback, solves the TCaptcha off-box via 2Captcha, fires the callback
# with {ticket, randstr} inside the (cross-origin) harvestsharp slider frame —
# the slider then submits to harvestsharp itself and newRiskControl resolves with
# {rc_token, rc_uuid}, which the backend feeds into QueryRedeemCodeInfo.

_JS_TCAPTCHA_HOOK = r"""
() => {
  try {
    if (window.__tcapHookInstalled) return;
    window.__tcapHookInstalled = true;
    function _grab(args) {
      for (var i = 0; i < args.length; i++) {
        var a = args[i];
        if (typeof a === 'function') { window.__tcaptchaCallback = a; return; }
        if (a && typeof a === 'object') {
          for (var k in a) {
            try { if (typeof a[k] === 'function' && /call|cb|verif|success|done|ready/i.test(k)) { window.__tcaptchaCallback = a[k]; return; } } catch(e) {}
          }
        }
      }
    }
    var _real = null;
    function Wrapped() {
      var args = Array.prototype.slice.call(arguments);
      _grab(args);
      var inst = Object.create(_real && _real.prototype ? _real.prototype : Object.prototype);
      try { var r = _real.apply(inst, args); if (r && typeof r === 'object') inst = r; } catch(e) {}
      return inst;
    }
    Object.defineProperty(window, 'TencentCaptcha', {
      configurable: true, enumerable: true,
      get: function () { return _real ? Wrapped : undefined; },
      set: function (v) { _real = v; },
    });
  } catch (e) {}
}
"""

_JS_TRIGGER_RC = r"""
(function(){
  var me = document.currentScript;
  var nonce = me && me.getAttribute('data-nonce');
  function out(o){ var el = document.getElementById('__rc_out_'+nonce); if (el) el.textContent = JSON.stringify(o); }
  try {
    var challenge = JSON.parse(document.getElementById('__rc_in_'+nonce).textContent).challenge;
    if (!window.midas || typeof window.midas.newRiskControl !== 'function') { out({error:'no_newRiskControl', midas: typeof window.midas}); return; }
    window.midas.newRiskControl(challenge).then(function(r){
      out({ok:true, rc_token: r && r.rc_token, rc_uuid: r && r.rc_uuid});
    }).catch(function(e){ out({error:'rc_rejected', detail: String(e)}); });
  } catch(e) { out({error:'js_exception', detail: String(e)}); }
})();
"""

_RC_SLIDER_SELECTORS = (
    "#riskControlComponent",
    "iframe[src*='harvestsharp']",
    "iframe[src*='slider']",
    "iframe[src*='captcha']",
)


def _frame_main_eval(fr, body_js: str, data=None):
    """
    Run JS in a frame's MAIN world (not patchright's isolated world) by injecting a
    <script> element, and read the JSON result back via a DOM element. `body_js` is
    a function body that may use `DATA` (a JSON string of `data`) and `return` a
    JSON-able value. Requires bypass_csp for cross-origin frames.
    """
    rid = "__mw_" + os.urandom(5).hex()
    fr.evaluate(
        """(a) => {
            const r = document.createElement('div');
            r.id = a.rid; r.style.display = 'none';
            r.setAttribute('data-in', a.data || '');
            document.documentElement.appendChild(r);
            const s = document.createElement('script');
            s.textContent =
                '(function(){var __el=document.getElementById("' + a.rid + '");' +
                'var DATA=__el.getAttribute("data-in");try{' +
                'var __v=(function(DATA){' + a.body + '})(DATA);' +
                '__el.textContent=JSON.stringify(__v===undefined?null:__v);' +
                '}catch(e){__el.textContent=JSON.stringify("ERR:"+e);}})();';
            document.documentElement.appendChild(s);
            s.remove();
        }""",
        {"rid": rid, "body": body_js, "data": json.dumps(data) if data is not None else ""},
    )
    raw = fr.evaluate(
        "(rid) => { const r = document.getElementById(rid); const t = r ? r.textContent : null; if (r) r.remove(); return t; }",
        rid,
    )
    return json.loads(raw) if raw else None


def _rc_inject_token(page, token: dict) -> bool:
    body = (
        "var t = JSON.parse(DATA);"
        "if (typeof window.__tcaptchaCallback === 'function') {"
        "  window.__tcaptchaCallback({ret: 0, ticket: t.ticket, randstr: t.randstr,"
        "    CaptchaAppId: t.appid, appid: t.appid, errorCode: 0, errorMessage: 'OK',"
        "    verifyDuration: 1200, actionDuration: 1000, sid: ''});"
        "  return 'ok';"
        "} return 'no_cb';"
    )
    for fr in page.frames:
        try:
            if _frame_main_eval(fr, body, data=token) == "ok":
                logger.info("[CAPTCHA] token injected (main world) into frame %s", (fr.url or "")[:90])
                return True
        except Exception:
            continue
    return False


def _rc_slider_present(page) -> bool:
    for sel in _RC_SLIDER_SELECTORS:
        try:
            el = page.query_selector(sel)
            if el:
                box = el.bounding_box()
                if box and box["width"] > 30 and box["height"] > 30:
                    return True
        except Exception:
            continue
    return False


# Appended to TCaptcha-global.js (served via page.route) so window.TencentCaptcha
# is wrapped before the slider calls it — captures the success callback into
# window.__tcaptchaCallback even in the cross-origin iframe add_init_script misses.
_TCAPTCHA_WRAP = b"""
;(function(){
  function wrap(_real){
    function W(){
      var args=[].slice.call(arguments);
      for(var i=0;i<args.length;i++){
        var a=args[i];
        if(typeof a==='function'){window.__tcaptchaCallback=a;}
        else if(a&&typeof a==='object'){for(var k in a){try{if(typeof a[k]==='function'&&/call|cb|verif|success|done|ready/i.test(k)){window.__tcaptchaCallback=a[k];}}catch(e){}}}
      }
      try{return new (Function.prototype.bind.apply(_real,[null].concat(args)))();}
      catch(e){var o=Object.create(_real.prototype);try{_real.apply(o,args);}catch(e2){}return o;}
    }
    try{for(var k in _real){try{W[k]=_real[k];}catch(e){}}}catch(e){}
    try{W.prototype=_real.prototype;}catch(e){}
    return W;
  }
  try{
    var cur=window.TencentCaptcha;
    if(typeof cur==='function'){window.TencentCaptcha=wrap(cur);window.__tcapHookInstalled=true;}
    else{
      var _w=null;
      Object.defineProperty(window,'TencentCaptcha',{configurable:true,enumerable:true,
        get:function(){return _w;},
        set:function(v){_w=(typeof v==='function')?wrap(v):v;window.__tcapHookInstalled=true;}});
    }
  }catch(e){}
})();
"""


def _setup_tcaptcha_hook_route(page) -> None:
    def handle(route):
        try:
            resp = route.fetch()
            headers = dict(resp.headers)
            headers.pop("content-length", None)
            headers["content-type"] = "application/javascript; charset=utf-8"
            route.fulfill(status=resp.status, headers=headers, body=resp.body() + _TCAPTCHA_WRAP)
            logger.info("[CAPTCHA] TCaptcha-global.js hook injected via route")
        except Exception as exc:
            # Common + harmless: the browser closed (we already have rc_token) while
            # a background fetch was mid-flight.
            if "disposed" in str(exc).lower() or "closed" in str(exc).lower():
                logger.debug("[CAPTCHA] TCaptcha route hook skipped (context closed)")
            else:
                logger.warning("[CAPTCHA] TCaptcha route hook failed (%s) — continuing", exc)
            try:
                route.continue_()
            except Exception:
                pass

    page.route("**TCaptcha-global*", handle)


def obtain_rc_token_via_provider(
    challenge_url: str,
    storage_state_path: str,
    country_code: str = "bd",
    timeout_ms: int = 75_000,
) -> Optional[dict]:
    """
    Produce {rc_token, rc_uuid} for a graphic risk-control challenge using the
    configured paid solver. Returns None if no provider key, solve fails, or the
    challenge does not resolve. Runs its own browser (call from a dedicated
    thread, not the cached-session executor).
    """
    from . import captcha_provider

    if not captcha_provider.is_enabled():
        return None

    sync_playwright, PWTimeout = _get_playwright()
    redeem_url = f"https://www.midasbuy.com/midasbuy/{country_code}/redeem/pubgm"
    session_dir = os.path.dirname(storage_state_path)

    try:
        with sync_playwright() as p:
            browser, context = _launch_context(p, storage_state_path, country_code, bypass_csp=True)
            context.add_init_script(_JS_TCAPTCHA_HOOK)
            page = context.new_page()
            _setup_chaos_vm_protection(page)
            _setup_tcaptcha_hook_route(page)

            # Capture the post-callback traffic (PAValidate / Tencent verify) so we
            # can see whether/why the ticket is accepted. Full bodies (incl. the
            # slider JS) are dumped to rc_network.txt for offline inspection.
            dump_path = os.path.join(session_dir, "rc_network.txt")
            try:
                open(dump_path, "w", encoding="utf-8").close()
            except Exception:
                pass

            def _dump(line):
                try:
                    with open(dump_path, "a", encoding="utf-8") as f:
                        f.write(line + "\n")
                except Exception:
                    pass

            _verify_hints = ("pavalidate", "paenroll", "paidentify", "pasetup",
                             "cap_union_new_verify", "secondary")
            _capture_hints = _verify_hints + ("/v1/rc/3ds/assets/", "/v1/rc/3ds/api/")

            def _on_req(req):
                try:
                    u = req.url.lower()
                    if any(h in u for h in _verify_hints):
                        pd = None
                        try:
                            pd = req.post_data
                        except Exception:
                            pd = None
                        _dump(f"\n>> {req.method} {req.url}")
                        if pd:
                            _dump("POST_DATA: " + pd[:8000])
                        logger.info("[CAPTCHA][NET] >> %s %s", req.method, req.url[:120])
                except Exception:
                    pass

            def _on_resp(resp):
                try:
                    u = resp.url.lower()
                    if any(h in u for h in _capture_hints):
                        body = None
                        try:
                            body = resp.text()
                        except Exception:
                            body = None
                        _dump(f"\n<< {resp.status} {resp.url}")
                        if body:
                            _dump(body[:60000])
                        if any(h in u for h in _verify_hints):
                            logger.info("[CAPTCHA][NET] << %s %s body=%s", resp.status, resp.url[:120], (body or "")[:300])
                except Exception:
                    pass

            page.on("request", _on_req)
            page.on("response", _on_resp)

            logger.info("[CAPTCHA] obtaining rc_token via provider (challenge ready)")
            try:
                page.goto(redeem_url, wait_until="load", timeout=timeout_ms)
            except PWTimeout:
                logger.error("[CAPTCHA] page.goto timed out")
                browser.close()
                return None

            try:
                page.wait_for_function(
                    "() => window.midas && typeof window.midas.newRiskControl === 'function'",
                    timeout=40_000,
                )
            except Exception:
                logger.error("[CAPTCHA] window.midas.newRiskControl not available")
                _save_debug(page, session_dir, "rc_no_sdk")
                browser.close()
                return None

            # Trigger newRiskControl in the page main world.
            nonce = os.urandom(8).hex()
            page.evaluate(
                """(a) => {
                    const inEl = document.createElement('div');
                    inEl.id = '__rc_in_' + a.nonce; inEl.style.display = 'none';
                    inEl.textContent = JSON.stringify({challenge: a.challenge});
                    document.documentElement.appendChild(inEl);
                    const outEl = document.createElement('div');
                    outEl.id = '__rc_out_' + a.nonce; outEl.style.display = 'none';
                    document.documentElement.appendChild(outEl);
                    const s = document.createElement('script');
                    s.setAttribute('data-nonce', a.nonce);
                    s.textContent = a.code;
                    document.documentElement.appendChild(s);
                }""",
                {"nonce": nonce, "challenge": challenge_url, "code": _JS_TRIGGER_RC},
            )

            # Wait for the slider frame to render (we POST CommonCheck from inside
            # it so the request carries the harvestsharp cookies + origin).
            for _ in range(60):
                if _rc_find_slider_frame(page) is not None:
                    break
                page.wait_for_timeout(250)

            token = captcha_provider.solve_tencent(redeem_url)
            if not token or not token.get("ticket"):
                logger.error("[CAPTCHA] provider returned no token: %s", token)
                _save_debug(page, session_dir, "rc_no_token")
                browser.close()
                return None
            logger.info("[CAPTCHA] provider token acquired; submitting CommonCheck")

            import re as _re
            m = _re.search(r"rc_uuid=([^&]+)", challenge_url)
            rc_uuid = m.group(1) if m else None
            result = None
            if rc_uuid:
                resp = _rc_submit_commoncheck(page, rc_uuid, token, timeout_s=30)
                result = _rc_extract_token(resp, rc_uuid)
                if result:
                    logger.info("[CAPTCHA] rc_token obtained via CommonCheck")
                else:
                    logger.warning("[CAPTCHA] CommonCheck did not yield rc_token: %s",
                                   json.dumps(resp)[:400] if resp else resp)
            else:
                logger.error("[CAPTCHA] could not parse rc_uuid from challenge url")

            if result is None:
                _save_debug(page, session_dir, "rc_unresolved")
            browser.close()
            return result

    except Exception:
        logger.exception("[CAPTCHA] obtain_rc_token_via_provider crashed")
        return None


def _rc_find_slider_frame(page):
    for fr in page.frames:
        u = fr.url or ""
        if "harvestsharp" in u and ("slider" in u or "/rc/3ds/" in u):
            return fr
    return None


def _rc_extract_token(resp, rc_uuid: str):
    """Pull {rc_token, rc_uuid} out of a CommonCheck response (flat or under .data)."""
    if not isinstance(resp, dict):
        return None
    for obj in (resp, resp.get("data") if isinstance(resp.get("data"), dict) else {}):
        if isinstance(obj, dict) and obj.get("rc_token"):
            return {"rc_token": obj["rc_token"], "rc_uuid": obj.get("rc_uuid") or rc_uuid}
    return None


def _rc_submit_commoncheck(page, rc_uuid: str, token: dict, timeout_s: int = 30):
    """
    POST CommonCheck inside the harvestsharp slider frame (same origin → cookies)
    with the paid-solver ticket, and return the parsed JSON response.

        POST /v1/rc/3ds/api/trpc.tdrc.rc_verification_go.Verification/CommonCheck
        {rc_uuid, ticket, rand_str, verify_state:"0", verify_type:"graphic"}
    """
    fr = _rc_find_slider_frame(page)
    if fr is None:
        logger.warning("[CAPTCHA] no harvestsharp slider frame for CommonCheck")
        return None

    rid = "__cc_" + os.urandom(5).hex()
    body = {
        "rc_uuid": rc_uuid,
        "ticket": token.get("ticket"),
        "rand_str": token.get("randstr"),
        "verify_state": "0",
        "verify_type": "graphic",
    }
    fr.evaluate(
        """(a) => {
            const r = document.createElement('div');
            r.id = a.rid; r.style.display = 'none';
            r.setAttribute('data-body', a.body);
            document.documentElement.appendChild(r);
            const s = document.createElement('script');
            s.textContent =
                '(function(){var el=document.getElementById("' + a.rid + '");' +
                'fetch("/v1/rc/3ds/api/trpc.tdrc.rc_verification_go.Verification/CommonCheck",' +
                '{method:"POST",headers:{"content-type":"application/json"},credentials:"include",' +
                'body:el.getAttribute("data-body")})' +
                '.then(function(x){return x.text();})' +
                '.then(function(b){el.textContent=b||"{}";})' +
                '.catch(function(e){el.textContent=JSON.stringify({__err:String(e)});});})();';
            document.documentElement.appendChild(s);
            s.remove();
        }""",
        {"rid": rid, "body": json.dumps(body)},
    )

    deadline = time.time() + timeout_s
    while time.time() < deadline:
        raw = fr.evaluate(
            "(rid) => { const r = document.getElementById(rid); return r ? r.textContent : null; }",
            rid,
        )
        if raw:
            try:
                return json.loads(raw)
            except Exception:
                logger.warning("[CAPTCHA] CommonCheck non-JSON response: %s", raw[:300])
                return None
        page.wait_for_timeout(500)
    logger.warning("[CAPTCHA] CommonCheck timed out")
    return None


def _rc_log_frame_diagnostics(page) -> None:
    """Log, per frame (MAIN world), how TCaptcha is exposed."""
    body = (
        "return {url: location.href.slice(0,120),"
        " tcaptcha: typeof window.TencentCaptcha,"
        " hookInstalled: !!window.__tcapHookInstalled,"
        " callbackCaptured: typeof window.__tcaptchaCallback,"
        " captchaKeys: Object.keys(window).filter(function(k){return /captcha|tcap|cap_|tdc|verif/i.test(k);}).slice(0,25)};"
    )
    for fr in page.frames:
        try:
            info = _frame_main_eval(fr, body)
            logger.info("[CAPTCHA][DIAG] %s", json.dumps(info))
        except Exception as exc:
            logger.info("[CAPTCHA][DIAG] frame %s probe failed: %s", (fr.url or "")[:80], exc)
