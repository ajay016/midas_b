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
        let verifiedPlayerApplied = false;
        try {
            verifiedPlayers = JSON.parse(
                sessionStorage.getItem(verifiedPlayerStorageKey) || '{}'
            );
        } catch(e) {}
        if (endpoint.endsWith('/QueryRedeemCodeInfo')) {
            const verifiedPlayer = verifiedPlayers[actualPayload.open_id];
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
            const zoneParts = String(
                actualPayload.zone_id ||
                payInfo.zoneid ||
                payInfo.zone_id ||
                payInfo.currentBindUser?.zoneid ||
                '1'
            ).split('_');
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
                server_id: zoneParts[0] || '',
                region: payInfo.country || sd.country || 'BD',
                open_id: actualPayload.open_id || '',
                muid: user.uid || actualPayload.muid || sd.muid || '',
                flexible_return_url: (
                    `https://${location.hostname}/h5/overseah5/views/riskcontrol/landing.html`
                ),
                user_ip: payInfo.ipInfo?.mall_ip || '',
                role_id: zoneParts[1] || '',
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


# ── Helpers ───────────────────────────────────────────────────────────────────

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


def _launch_context(p, storage_state_path: str, country_code: str):
    from django.conf import settings

    ss_data = _load_session_storage(storage_state_path)
    server_data = _load_server_data_snapshot(storage_state_path)

    browser = p.chromium.launch(
        headless=getattr(settings, "MIDASBUY_CRYPTO_BROWSER_HEADLESS", True),
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
        browser, context = _launch_context(p, storage_state_path, country_code)
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
        "request_fields=%s  public_fields=%s",
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
