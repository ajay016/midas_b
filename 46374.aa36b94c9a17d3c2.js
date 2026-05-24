(window[
    "webpackJsonp_impage_materials_name_gems_midasbuy_activity_materials@1778240049"
] =
    window[
        "webpackJsonp_impage_materials_name_gems_midasbuy_activity_materials@1778240049"
    ] || []).push([
    ["46374"],
    {
        84472: function (e) {
            e.exports = {
                libType: "independent",
                libName: "gems-midasbuy_activity_materials",
                libFramework: "react",
                dir: ".",
                author: "yandeng",
                outputType: ["dist"],
                isFlat: !1,
                extendMaterials: "",
                libWebpackConfig: (e) => e,
            };
        },
        22448: function (e, t, n) {
            "use strict";
            n.d(t, {
                L: function () {
                    return i;
                },
            });
            var r = n(74740);
            async function i(e) {
                return r.H1.request(e, "Background:getNeedBalanceVerify");
            }
        },
        53167: function (e, t, n) {
            "use strict";
            (n.d(t, {
                BC: function () {
                    return o;
                },
                le: function () {
                    return a;
                },
                y_: function () {
                    return l;
                },
            }),
                n(616));
            var r = n(74740),
                i = n(14603);
            function o(e, t) {
                e.emit("basePopup:show", t);
            }
            function a(e, t) {
                e.emit("activityErrorPopup:show", t);
            }
            async function l(e, t) {
                return (await (0, i.Wt)("base_popup"))
                    ? r.H1.request(e, "basePopup:withGlobalLoading", {
                          task: t,
                      })
                    : t();
            }
        },
        52363: function (e, t, n) {
            "use strict";
            function r(e) {
                var t;
                return (
                    (null == e
                        ? void 0
                        : null === (t = e.mp_model_conf) || void 0 === t
                          ? void 0
                          : t.mp_sub_activity_id) ||
                    (null == e ? void 0 : e.mp_sub_activity_id) ||
                    ""
                );
            }
            n.d(t, {
                n: function () {
                    return r;
                },
            });
        },
        14866: function (e, t, n) {
            "use strict";
            n.d(t, {
                l3: function () {
                    return P;
                },
                SV: function () {
                    return w;
                },
            });
            var r = n("66339"),
                i = n("75865"),
                o = n("11972"),
                a = n("65317"),
                l = n("80430"),
                u = n("616"),
                s = n.n(u),
                c = n("13476"),
                d = n("21635"),
                p = n("63821"),
                f = n("29628");
            let m = new (n("9825").m)();
            m.register({ propagator: new f.jf() });
            let y = m.getTracer("midasbuy_activity_materials");
            var v = n("14603"),
                g = n("20640"),
                b = n.n(g);
            function _(e) {
                let { userId: t } = e;
                return s().createElement(
                    "div",
                    { style: { pointerEvents: "initial" } },
                    s().createElement(
                        "p",
                        null,
                        `You're not in white list！${t ? `Your user ID: ${t}` : ""}`,
                    ),
                    t &&
                        s().createElement(
                            "button",
                            {
                                type: "button",
                                style: {
                                    color: "#4a9ee7",
                                    marginTop: 12,
                                    background: "none",
                                    border: 0,
                                    appearance: "none",
                                    textDecoration: "underline",
                                    cursor: "pointer",
                                },
                                onClick: () => {
                                    var e;
                                    (b()(t),
                                        null ===
                                            (e = document.querySelector(
                                                "#pagedoo-toast-container",
                                            )) ||
                                            void 0 === e ||
                                            e.remove(),
                                        (0, c.A)({
                                            text: "Copied!",
                                            duration: 3e3,
                                        }));
                                },
                            },
                            "Copy user ID",
                        ),
                );
            }
            let h = 0;
            function w() {
                let e = location.hostname.includes("sandbox")
                    ? location.pathname.includes("act/verify-pagedoo") ||
                      "1" === (0, a.jS)("verify")
                        ? "sandbox-verify"
                        : "sandbox"
                    : location.pathname.includes("act/verify-pagedoo") ||
                        "1" === (0, a.jS)("verify")
                      ? "release-verify"
                      : "release";
                return {
                    "release-verify": "verify-pagedooapi.midasbuy.com",
                    "sandbox-verify": "sandbox-verify-pagedooapi.midasbuy.com",
                    release: "pagedooapi.midasbuy.com",
                    sandbox: "sandbox-pagedooapi.midasbuy.com",
                }[e];
            }
            let O = (e) => {
                    let [t, n] = e.split("/").filter(Boolean);
                    if ("trpc.osmp.page.QualificationSvr" === t)
                        return `osmidas_eventcall/${n}`;
                    let r = t.split(".").slice(-2)[0];
                    return `${r}/${n}`;
                },
                P = (e, t, n, s = {}) => {
                    if (e.startsWith("/trpc.midasuser.vip.Vip"))
                        return p.RV.shelfProto(e, n);
                    if (
                        d.$.get("activityEnded") &&
                        !e.startsWith(
                            "/trpc.mpgo.dd_prize_service.Greeter/QueryPrizeInfoList",
                        )
                    )
                        throw { result_code: -1, msg: "ACTIVITY_END" };
                    let { acctId: f = "osmidas" } = s || {},
                        m = (null == s ? void 0 : s.loginState) || {},
                        g = O(e);
                    return new Promise((e, t) => {
                        let s = `/api/CallMpgo/${f}/${g}`,
                            p = y.startSpan(s),
                            b = (0, v.yR)("getSessionId");
                        r.D.with(i.g.setSpan(r.D.active(), p), () => {
                            var s, y, v;
                            let O = {
                                "x-request-id":
                                    "function" == typeof b
                                        ? `${b()}-${h}`
                                        : (0, a.Vj)(),
                                "x-tencent-login-check": JSON.stringify({
                                    accountType: "midasbuy",
                                    appid: m.appid,
                                    endpoint_type: "mpgo_activity",
                                    offer_id:
                                        null === (s = m.currentBindUser) ||
                                        void 0 === s
                                            ? void 0
                                            : s.appid,
                                    openid:
                                        null === (y = m.currentBindUser) ||
                                        void 0 === y
                                            ? void 0
                                            : y.openid,
                                    openkey: "nokey",
                                    pf:
                                        null === (v = m.currentBindUser) ||
                                        void 0 === v
                                            ? void 0
                                            : v.pf,
                                    session_id: "hy_gameid",
                                    session_type: "st_dummy",
                                    token: m.token || d.$.get("userToken"),
                                    userType: "hy_gameid",
                                }),
                            };
                            return (
                                (h += 1),
                                location.host.includes("sandbox") &&
                                    o.u.inject(r.D.active(), O),
                                O.traceparent &&
                                    ((O["Trpc-Trans-Info"] = JSON.stringify({
                                        traceparent: O.traceparent,
                                    })),
                                    delete O.traceparent),
                                l.Z.post(`/api/CallMpgo/${f}/${g}`, n, {
                                    baseURL: "https://".concat(w()),
                                    headers: O,
                                    withCredentials: !0,
                                })
                                    .then((e) => e.data)
                                    .then((o) => {
                                        var a, l;
                                        if (
                                            "0" == `${o.result_code}` ||
                                            !o.result_code
                                        )
                                            return (
                                                null ===
                                                    (l = i.g.getSpan(
                                                        r.D.active(),
                                                    )) ||
                                                    void 0 === l ||
                                                    l.addEvent(
                                                        "fetch-completed",
                                                    ),
                                                e(o)
                                            );
                                        if (
                                            (null ===
                                                (a = i.g.getSpan(
                                                    r.D.active(),
                                                )) ||
                                                void 0 === a ||
                                                a.addEvent(
                                                    "fetch-business-error",
                                                ),
                                            "1311" === o.result_code)
                                        ) {
                                            let e =
                                                null == n ? void 0 : n.user_id;
                                            (0, c.A)({
                                                text: (0, u.createElement)(_, {
                                                    userId: e,
                                                }),
                                                duration: 1e4,
                                            });
                                        }
                                        t(o);
                                    })
                                    .catch((e) => {
                                        var n;
                                        (null ===
                                            (n = i.g.getSpan(r.D.active())) ||
                                            void 0 === n ||
                                            n.addEvent("fetch-error"),
                                            t(e));
                                    })
                                    .finally(() => {
                                        p.end();
                                    })
                            );
                        });
                    });
                };
        },
        13476: function (e, t, n) {
            "use strict";
            n.d(t, {
                A: function () {
                    return i;
                },
            });
            var r = n(86651);
            function i({ text: e, duration: t }) {
                let n = "pagedoo-toast-container";
                if (!document.getElementById(n)) {
                    let e = document.createElement("div");
                    ((e.id = n),
                        (e.style.fontSize = "16px"),
                        document.body.appendChild(e));
                }
                return r.F.show(e, {
                    duration: t,
                    container: document.getElementById(n),
                });
            }
        },
        94263: function (e, t, n) {
            "use strict";
            n.d(t, {
                DH: function () {
                    return r;
                },
                bY: function () {
                    return i;
                },
                vj: function () {
                    return o;
                },
            });
            let r = {
                    CallType: "dd_task_model",
                    CallFuncs: {
                        GrabTaskPrize: "TaskPrizeNotify",
                        QueryTask: "QueryUserModelInfo",
                        TaskExec: "TaskExec",
                        TaskPrizeNotify: "TaskPrizeNotify",
                    },
                    protocol: { protocol: "trpc" },
                },
                i = {
                    CallType: "dd_buy_model",
                    CallFuncs: { QueryUserCard: "QueryUserCard" },
                    protocol: { protocol: "trpc" },
                },
                o = {
                    CallType: "dd_buy_model",
                    CallFuncs: { QueryUserCard: "QueryGiftRule" },
                    protocol: { protocol: "trpc" },
                };
        },
        21635: function (e, t, n) {
            "use strict";
            n.d(t, {
                $: function () {
                    return i;
                },
            });
            let r = window;
            if (
                (void 0 === r.__gems_regsitry &&
                    (r.__gems_regsitry = new Map()),
                "object" == typeof r.__gems_regsitry &&
                    r.__gems_regsitry &&
                    !(r.__gems_regsitry instanceof Map))
            ) {
                let e = new Map();
                (Object.entries(r.__gems_regsitry).forEach(([t, n]) => {
                    e.set(t, n);
                }),
                    (r.__gems_regsitry = e));
            }
            let i = new (class e {
                set(e, t) {
                    return !this.store.has(e) && (this.store.set(e, t), !0);
                }
                overwrite(e, t) {
                    return this.store.set(e, t);
                }
                has(e) {
                    return this.store.has(e);
                }
                get(e) {
                    return this.store.get(e);
                }
                constructor() {
                    var e, t, n;
                    ((e = this),
                        (t = "store"),
                        (n = r.__gems_regsitry),
                        t in e
                            ? Object.defineProperty(e, t, {
                                  value: n,
                                  enumerable: !0,
                                  configurable: !0,
                                  writable: !0,
                              })
                            : (e[t] = n));
                }
            })();
        },
        33086: function (e, t, n) {
            "use strict";
            n.d(t, {
                e: function () {
                    return i;
                },
            });
            var r,
                i =
                    (((r = {}).LOGIN = "login"),
                    (r.TASK = "task"),
                    (r.CARD = "card"),
                    (r.INIT = "init"),
                    (r.REPORT = "report"),
                    (r.BUYCARE = "buycard"),
                    (r.ANY_STATE = "ANY_STATE"),
                    (r.LUCK_DRAW_PRODUCTS = "LUCK_DRAW_PRODUCTS"),
                    (r.MODEL_MAP = "MODEL_MAP"),
                    (r.PRODUCT_MAP = "PRODUCT_MAP"),
                    (r.GLOBAL_POPUP_CONFIG = "GLOBAL_POPUP_CONFIG"),
                    (r.METADATA = "METADATA"),
                    (r.USER_BALANCE = "USER_BALANCE"),
                    (r.VERIFIED_USER = "VERIFIED_USER"),
                    (r.MESSENGER = "MESSENGER"),
                    (r.SIMULATE_DATA = "SIMULATE_DATA"),
                    (r.PAGE_VISIBLE = "PAGE_VISIBLE"),
                    r);
        },
        19639: function (e, t, n) {
            "use strict";
            n.d(t, {
                w: function () {
                    return r;
                },
            });
            function r(e, t, n, r) {
                var i;
                let o =
                    e.activityInfo ||
                    (null === (i = e.global) || void 0 === i
                        ? void 0
                        : i.activityInfo);
                if (void 0 !== o && "" !== o && void 0 !== t) {
                    if ("activityId" === t && o.activityId) return o.activityId;
                    if ("modelId" === t && n && o.modelList)
                        return (function (e, t) {
                            var n;
                            let r = JSON.parse(e).find(
                                (e) => e.model_key === t,
                            );
                            return null !==
                                (n = null == r ? void 0 : r.model_id) &&
                                void 0 !== n
                                ? n
                                : "";
                        })(o.modelList, n);
                    if ("modelId" === t && r && o.modelList)
                        return (function (e, t) {
                            var n;
                            let r = JSON.parse(e).find(
                                (e) => e.model_type === t,
                            );
                            return null !==
                                (n = null == r ? void 0 : r.model_id) &&
                                void 0 !== n
                                ? n
                                : "";
                        })(o.modelList, r);
                }
            }
        },
        48251: function (e, t, n) {
            "use strict";
            n.d(t, {
                Hl: function () {
                    return T;
                },
                i1: function () {
                    return C;
                },
                aE: function () {
                    return k;
                },
                dv: function () {
                    return E;
                },
                Ri: function () {
                    return D;
                },
            });
            var r = n("65317"),
                i = n("74125"),
                o = n("30399"),
                a = n("66540"),
                l = n("99045"),
                u = n("9553"),
                s = n("3930"),
                c = n("616"),
                d = n("63821"),
                p = n("14603"),
                f = n("55137"),
                m = n("49567"),
                y = n("29872"),
                v = n("89601"),
                g = n("75889"),
                b = n("31661"),
                _ = n("38905"),
                h = n("19639"),
                w = n("44342");
            let O = "console",
                P = () => {
                    var e;
                    return `
${null === (e = Error().stack) || void 0 === e ? void 0 : e.split("\n")[3]}`;
                };
            class j {
                debug(...e) {
                    d.TQ &&
                        window[O].debug(
                            this.tag,
                            "color: #5520e2",
                            "color: initial",
                            ...e,
                            P(),
                        );
                }
                log(...e) {
                    d.TQ &&
                        window[O].log(
                            this.tag,
                            "color: #5520e2",
                            "color: initial",
                            ...e,
                            P(),
                        );
                }
                warn(...e) {
                    d.TQ &&
                        window[O].warn(
                            this.tag,
                            "color: #5520e2",
                            "color: initial",
                            ...e,
                            P(),
                        );
                }
                error(...e) {
                    d.TQ &&
                        window[O].error(
                            this.tag,
                            "color: #5520e2",
                            "color: initial",
                            ...e,
                            P(),
                        );
                }
                constructor(e) {
                    var t, n, r;
                    ((t = this),
                        (n = "tag"),
                        (r = void 0),
                        "tag" in t
                            ? Object.defineProperty(t, n, {
                                  value: r,
                                  enumerable: !0,
                                  configurable: !0,
                                  writable: !0,
                              })
                            : (t[n] = r),
                        (this.tag = `%c[素材库]${e}%c`));
                }
            }
            let S = (e) => {
                if ("string" != typeof e) return "[unknown]";
                let [, , t = ""] = e.split("/");
                return `[${t}]`;
            };
            var I = n("35235");
            let E = () => {
                    if ("string" == typeof sessionStorage.shortLinkFrom)
                        return {
                            chan_share: sessionStorage.shortLinkFrom,
                            chan_custom_id: sessionStorage.shortLink,
                            pf: `${sessionStorage.shortLinkFrom}.${sessionStorage.shortLink}`,
                        };
                    let e = new Set(d.GA.map((e) => e.id)),
                        t = (0, r.jS)("from") || "",
                        n = t.split("."),
                        i = n[n.length - 1],
                        o = e.has(i),
                        a = o ? i : "false",
                        l = o ? n.slice(0, -1).join(".") : t,
                        u = `${a}.${l}`;
                    return { chan_share: a, chan_custom_id: l, pf: u };
                },
                k = "1450027575";
            function D(e) {
                var t, n, r, i, o, a;
                let l = e.global.eventBus,
                    u =
                        null !== (i = (0, w.v)(e, "appId")) && void 0 !== i
                            ? i
                            : "",
                    s =
                        (0, h.w)(e, "activityId") ||
                        (null === (t = e.global.appInfo) || void 0 === t
                            ? void 0
                            : t.activityId) ||
                        (null === (n = e.global.appInfo) || void 0 === n
                            ? void 0
                            : n.activityInfo) ||
                        "",
                    c =
                        null !== (o = (0, w.v)(e, "payOfferId")) && void 0 !== o
                            ? o
                            : "",
                    m =
                        null !== (a = (0, w.v)(e, "merchantId")) && void 0 !== a
                            ? a
                            : "",
                    { metadata: y } = (0, d.B9)(l, c),
                    v =
                        (null == y
                            ? void 0
                            : null === (r = y.payInfo) || void 0 === r
                              ? void 0
                              : r.country) || "",
                    g = m === k,
                    b =
                        [f.ro].includes(c) ||
                        (0, p.QR)(e, "GameLipassLogin") ||
                        (g && c !== k);
                return {
                    appId: u,
                    activityId: s,
                    platformOfferId: k,
                    isPlatformActivity: g,
                    payOfferId: c,
                    metadata: y,
                    country: v,
                    needVerify: b,
                };
            }
            function C(e) {
                var t;
                let n = e.global.eventBus,
                    { getModel: r, setModel: i } = (0, y.ZP)(n),
                    { getProduct: o, setProduct: a } = (0, v.ZP)(n),
                    l = (0, _.s)(e),
                    {
                        domAction: u,
                        reportItemClick: s,
                        reportItemVisible: d,
                        reportOtherEvent: p,
                    } = (0, I.Y)(e);
                let f =
                        ((t = e),
                        (0, c.useMemo)(
                            () => new j(S(t.instance.id)),
                            [t.instance.id],
                        )),
                    { messenger: g } = (0, m.ZP)(n);
                return {
                    wrapComponent: l,
                    domAction: u,
                    reportItemClick: s,
                    reportItemVisible: d,
                    reportOtherEvent: p,
                    getModel: r,
                    setModel: i,
                    getProduct: o,
                    setProduct: a,
                    logger: f,
                    messenger: g,
                    store: n,
                };
            }
            function T(e) {
                var t, n;
                let p = C(e),
                    f = D(e),
                    m = (function (e) {
                        var t, n, i, o, a, l, u, s, p;
                        let f = e.global.eventBus,
                            m =
                                null !== (p = (0, w.v)(e, "payOfferId")) &&
                                void 0 !== p
                                    ? p
                                    : "",
                            { metadata: y } = (0, d.B9)(f, m),
                            v =
                                null === (t = (0, g.ZP)(f)) || void 0 === t
                                    ? void 0
                                    : t.verifiedUser,
                            _ = (0, c.useMemo)(
                                () =>
                                    (null == v ? void 0 : v.state) === "INITIAL"
                                        ? {
                                              state: (0, g.V_)(
                                                  null == y
                                                      ? void 0
                                                      : y.userData,
                                              ),
                                              user:
                                                  null == y
                                                      ? void 0
                                                      : y.userData,
                                          }
                                        : v,
                                [null == y ? void 0 : y.userData, v],
                            ),
                            h =
                                (null == _
                                    ? void 0
                                    : null === (n = _.user) || void 0 === n
                                      ? void 0
                                      : n.currentBindUser) ||
                                (null == y
                                    ? void 0
                                    : null === (i = y.userData) || void 0 === i
                                      ? void 0
                                      : i.currentBindUser),
                            O = String((null == h ? void 0 : h.zoneid) || "1"),
                            P = (y && (null == h ? void 0 : h.openid)) || "",
                            j = (null == h ? void 0 : h.platId) || "",
                            S = (null == h ? void 0 : h.areaId) || "",
                            I = (0, b.X)(y, _),
                            k = !!(null == y
                                ? void 0
                                : null === (o = y.gameData) || void 0 === o
                                  ? void 0
                                  : o.mutipZoneidCharac),
                            D = (0, b.H)(O),
                            { shortZoneId: C, serverId: T } = D,
                            B = I || D.roleId,
                            A =
                                (null === (a = _.user) || void 0 === a
                                    ? void 0
                                    : a.uid) ||
                                (null == y
                                    ? void 0
                                    : null === (l = y.userData) || void 0 === l
                                      ? void 0
                                      : l.uid) ||
                                "",
                            U =
                                (null === (u = _.user) || void 0 === u
                                    ? void 0
                                    : u.token) ||
                                (null == y
                                    ? void 0
                                    : null === (s = y.userData) || void 0 === s
                                      ? void 0
                                      : s.token) ||
                                "",
                            x = (0, g.E_)(null == h ? void 0 : h.verifytype),
                            $ = (0, c.useMemo)(
                                () => (k ? `${T}_${B}` : T),
                                [k, B, T],
                            ),
                            { pf: L } = E(),
                            N = (0, c.useMemo)(() => {
                                var e;
                                return {
                                    ori_zoneid: $,
                                    client_ver: "android",
                                    server_id: T,
                                    role_id: k ? B : "",
                                    muid: A,
                                    player_id:
                                        (null == h ? void 0 : h.userid) || "",
                                    pf: L,
                                    adtag:
                                        (0, r.jS)("adtag", location.href) ||
                                        (0, r.jS)(
                                            "adtag",
                                            null === (e = top) || void 0 === e
                                                ? void 0
                                                : e.location.href,
                                        ),
                                };
                            }, [
                                A,
                                k,
                                $,
                                B,
                                T,
                                L,
                                null == h ? void 0 : h.userid,
                            ]);
                        return {
                            muid: A,
                            userToken: U,
                            verifiedUser: _,
                            currentBindUser: h,
                            isBalanceVerified: x,
                            zoneid: O,
                            openid: P,
                            roleId: B,
                            needRoleId: k,
                            oriZoneId: $,
                            serverId: T,
                            shortZoneId: C,
                            platId: j,
                            areaId: S,
                            gameUserMetadata: N,
                        };
                    })(e),
                    y = (function (e, t) {
                        let n = e.global.eventBus,
                            { userInfo: r, setUserInfo: s } = (0, l.b)(n),
                            { extendScene: c, setExtendScene: d } = (0, a.a)(n),
                            { getProductInfo: p, setProductMap: f } = (0, i.AM)(
                                n,
                                t.appId,
                                r,
                            ),
                            {
                                getProductProvide: m,
                                getProductProvideKey: y,
                                setProductProvide: v,
                            } = (0, o.x)(n, t.appId, r);
                        return {
                            pagedooUserInfo: r,
                            setPagedooUserInfo: s,
                            pagedooExtendScene: c,
                            setPagedooExtendScene: d,
                            getPagedooProductInfo: p,
                            setPagedooProductMap: f,
                            getPagedooProductProvide: m,
                            getPagedooProductProvideKey: y,
                            setPagedooProductProvide: v,
                            pagedooEventBus: u.Z,
                        };
                    })(e, f),
                    v = !!(
                        f.metadata &&
                        m.openid &&
                        f.appId &&
                        f.activityId &&
                        (!f.needVerify || m.isBalanceVerified) &&
                        (!m.needRoleId || m.roleId)
                    ),
                    _ = f.isPlatformActivity
                        ? { user_id: m.muid, user_id_type: "midasbuy" }
                        : { user_id: m.openid, user_id_type: "hy_gameid" };
                return (0, s.Z)(
                    ((t = (function (e) {
                        for (var t = 1; t < arguments.length; t++) {
                            var n = null != arguments[t] ? arguments[t] : {},
                                r = Object.keys(n);
                            ("function" ==
                                typeof Object.getOwnPropertySymbols &&
                                (r = r.concat(
                                    Object.getOwnPropertySymbols(n).filter(
                                        function (e) {
                                            return Object.getOwnPropertyDescriptor(
                                                n,
                                                e,
                                            ).enumerable;
                                        },
                                    ),
                                )),
                                r.forEach(function (t) {
                                    var r, i, o;
                                    ((r = e),
                                        (i = t),
                                        (o = n[t]),
                                        i in r
                                            ? Object.defineProperty(r, i, {
                                                  value: o,
                                                  enumerable: !0,
                                                  configurable: !0,
                                                  writable: !0,
                                              })
                                            : (r[i] = o));
                                }));
                        }
                        return e;
                    })({}, p, f, m, y)),
                    (n = ((n = { isUserReady: v, userIdAndType: _ }), n)),
                    Object.getOwnPropertyDescriptors
                        ? Object.defineProperties(
                              t,
                              Object.getOwnPropertyDescriptors(n),
                          )
                        : (function (e, t) {
                              var n = Object.keys(e);
                              if (Object.getOwnPropertySymbols) {
                                  var r = Object.getOwnPropertySymbols(e);
                                  n.push.apply(n, r);
                              }
                              return n;
                          })(Object(n)).forEach(function (e) {
                              Object.defineProperty(
                                  t,
                                  e,
                                  Object.getOwnPropertyDescriptor(n, e),
                              );
                          }),
                    t),
                ).current;
            }
        },
        44342: function (e, t, n) {
            "use strict";
            n.d(t, {
                v: function () {
                    return i;
                },
            });
            var r = n(65317);
            function i(e, t) {
                var n;
                let i =
                    e.appInfo ||
                    (null === (n = e.global) || void 0 === n
                        ? void 0
                        : n.appInfo);
                if (void 0 === i) return "";
                let {
                        appId: o,
                        payOfferId: a,
                        resourceInfo: l,
                        appInfoDetail: u,
                        contentId: s,
                    } = i,
                    {
                        offerId: c,
                        authOfferId: d,
                        extend: p,
                        merchant_id: f,
                    } = u;
                return {
                    appInfo: i,
                    appId: o,
                    payOfferId: (0, r.jS)("appid") || a || f,
                    merchantId: f,
                    resourceInfo: l,
                    appInfoDetail: u,
                    contentId: s,
                    offerId: c,
                    authOfferId: d,
                    extend: p,
                }[t];
            }
        },
        35235: function (e, t, n) {
            "use strict";
            n.d(t, {
                Y: function () {
                    return u;
                },
                n: function () {
                    return l;
                },
            });
            var r = n(16520),
                i = n(22638),
                o = n(616);
            function a(e) {
                for (var t = 1; t < arguments.length; t++) {
                    var n = null != arguments[t] ? arguments[t] : {},
                        r = Object.keys(n);
                    ("function" == typeof Object.getOwnPropertySymbols &&
                        (r = r.concat(
                            Object.getOwnPropertySymbols(n).filter(
                                function (e) {
                                    return Object.getOwnPropertyDescriptor(n, e)
                                        .enumerable;
                                },
                            ),
                        )),
                        r.forEach(function (t) {
                            var r, i, o;
                            ((r = e),
                                (i = t),
                                (o = n[t]),
                                i in r
                                    ? Object.defineProperty(r, i, {
                                          value: o,
                                          enumerable: !0,
                                          configurable: !0,
                                          writable: !0,
                                      })
                                    : (r[i] = o));
                        }));
                }
                return e;
            }
            function l(e) {
                return (0, r.o2)(e, "domAction");
            }
            function u(e) {
                let t = (0, r.o2)(e.global.eventBus, "domAction"),
                    [n, l] = (0, o.useState)({}),
                    u = (0, i.Z)((n) => {
                        var r;
                        return t.emit(
                            "ItemClick",
                            a(
                                {
                                    module_id:
                                        null !== (r = e.instance.id) &&
                                        void 0 !== r
                                            ? r
                                            : "",
                                },
                                n,
                            ),
                        );
                    }),
                    s = (0, i.Z)((r, i) => {
                        var o;
                        (!n[e.instance.id] || null == i || !i.once) &&
                            (t.emit(
                                "ItemVisible",
                                a(
                                    {
                                        module_id:
                                            null !== (o = e.instance.id) &&
                                            void 0 !== o
                                                ? o
                                                : "",
                                    },
                                    r,
                                ),
                            ),
                            l((t) => {
                                var n, r;
                                return (
                                    (n = a({}, t)),
                                    (r = ((r = { [e.instance.id]: !0 }), r)),
                                    Object.getOwnPropertyDescriptors
                                        ? Object.defineProperties(
                                              n,
                                              Object.getOwnPropertyDescriptors(
                                                  r,
                                              ),
                                          )
                                        : (function (e, t) {
                                              var n = Object.keys(e);
                                              if (
                                                  Object.getOwnPropertySymbols
                                              ) {
                                                  var r =
                                                      Object.getOwnPropertySymbols(
                                                          e,
                                                      );
                                                  n.push.apply(n, r);
                                              }
                                              return n;
                                          })(Object(r)).forEach(function (e) {
                                              Object.defineProperty(
                                                  n,
                                                  e,
                                                  Object.getOwnPropertyDescriptor(
                                                      r,
                                                      e,
                                                  ),
                                              );
                                          }),
                                    n
                                );
                            }));
                    });
                return {
                    reportItemClick: u,
                    reportItemVisible: s,
                    reportOtherEvent: (0, i.Z)((n, r) => {
                        var i;
                        return t.emit(
                            n,
                            a(
                                {
                                    module_id:
                                        null !== (i = e.instance.id) &&
                                        void 0 !== i
                                            ? i
                                            : "",
                                },
                                r,
                            ),
                        );
                    }),
                    domAction: t,
                };
            }
        },
        61230: function (e, t, n) {
            "use strict";
            n.d(t, {
                Q: function () {
                    return o;
                },
            });
            var r = n(45780),
                i = n(21635);
            i.$.set("ahooksUseRequest", r.default);
            let o = i.$.get("ahooksUseRequest");
        },
        78181: function (e, t, n) {
            "use strict";
            n.d(t, {
                H: function () {
                    return u;
                },
                RV: function () {
                    return p;
                },
                dJ: function () {
                    return c;
                },
            });
            var r = n(65317),
                i = n(80430),
                o = n(17078),
                a = n(90609);
            function l(e) {
                for (var t = 1; t < arguments.length; t++) {
                    var n = null != arguments[t] ? arguments[t] : {},
                        r = Object.keys(n);
                    ("function" == typeof Object.getOwnPropertySymbols &&
                        (r = r.concat(
                            Object.getOwnPropertySymbols(n).filter(
                                function (e) {
                                    return Object.getOwnPropertyDescriptor(n, e)
                                        .enumerable;
                                },
                            ),
                        )),
                        r.forEach(function (t) {
                            var r, i, o;
                            ((r = e),
                                (i = t),
                                (o = n[t]),
                                i in r
                                    ? Object.defineProperty(r, i, {
                                          value: o,
                                          enumerable: !0,
                                          configurable: !0,
                                          writable: !0,
                                      })
                                    : (r[i] = o));
                        }));
                }
                return e;
            }
            let u =
                    {
                        "sandbox-admin.midasbuy.com": "sandbox.midasbuy.com",
                        "admin.midasbuy.com": "www.midasbuy.com",
                    }[location.host] || location.host,
                s = `${location.protocol}//${u}`,
                c = i.Z.create({
                    baseURL: s,
                    timeout: 2e4,
                    withCredentials: !0,
                });
            (c.interceptors.request.use(
                async (e) => {
                    var t;
                    return (
                        await (0, o.IS)(),
                        null === (t = e.url) ||
                            void 0 === t ||
                            t.replace("/interface/", ""),
                        "get" === e.method &&
                            !e.notEncrypt &&
                            (e.params = (0, a.f)(e.params)),
                        "post" === e.method &&
                            !e.notEncrypt &&
                            (e.data = (0, a.f)(e.data)),
                        e
                    );
                },
                (e) => Promise.reject(e),
            ),
                c.interceptors.response.use(
                    (e) => {
                        var t, n, r;
                        let i =
                            null == e
                                ? void 0
                                : null === (t = e.data) || void 0 === t
                                  ? void 0
                                  : t.ret;
                        if (
                            null === (r = e.config) || void 0 === r
                                ? void 0
                                : null === (n = r.url) || void 0 === n
                                  ? void 0
                                  : n.includes("/interface/shelfProto")
                        )
                            return "number" == typeof i && 0 !== i
                                ? Promise.reject({ response: e })
                                : e.data;
                        return 0 !== i
                            ? Promise.reject({ response: e })
                            : e.data.data;
                    },
                    (e) => Promise.reject(e),
                ),
                location.pathname.includes("act/verify-pagedoo") ||
                "1" === (0, r.jS)("verify")
                    ? r.pR.set("midas_p_test", "1", {
                          path: "/",
                          time: 36e5,
                          domain: "*",
                      })
                    : r.pR.del("midas_p_test", { domain: "*" }));
            let d = new Map(),
                p = {
                    instance: c,
                    initializeXMidas: (e) =>
                        i.Z.get(
                            `${location.protocol}//${u}/apps/activity/api/v1/x-midas/init`,
                            { params: e },
                        ).then((e) => e.data.data),
                    getEventMetadata: (e) =>
                        c.get(
                            "/apps/activity/api/activity-initialize/metadata",
                            { params: e },
                        ),
                    getChannelManifest(e) {
                        let t = `getChannelManifest_${JSON.stringify(e)}`,
                            n = d.get(t);
                        if (n) return n;
                        let r = c.post(
                            "/apps/activity/api/v1/manifest/getChannelManifest",
                            e,
                        );
                        return (d.set(t, r), r);
                    },
                    idipQueryQualification: (e) =>
                        c.post(
                            "/apps/activity/api/v1/go/mp/ea/idipQueryQualification",
                            e,
                        ),
                    idipCollectGift: (e) =>
                        c.post(
                            "/apps/activity/api/v1/go/mp/ea/idipCollectGift",
                            e,
                        ),
                    queryVip: (e) =>
                        c.get("/interface/queryVip", { params: e }),
                    shelfProto(e, t) {
                        let n = (0, r.fQ)((0, r.jS)("presandbox")),
                            i =
                                location.pathname.includes(
                                    "act/verify-pagedoo",
                                ) || "1" === (0, r.jS)("verify"),
                            o =
                                Number((0, r.jS)("sandbox")) ||
                                (location.hostname.includes("sandbox") ? 1 : 0),
                            a =
                                n && i && o
                                    ? `${location.protocol}//presandbox.midasbuy.com`
                                    : "";
                        return c.post(`${a}/interface/shelfProto${e}`, t);
                    },
                    createShareUrl(e) {
                        var t, n;
                        let r = e.image.startsWith("//")
                            ? `https:${e.image}`
                            : e.image;
                        let i = encodeURIComponent(
                            btoa(
                                unescape(
                                    encodeURIComponent(
                                        JSON.stringify(
                                            ((t = l({}, e)),
                                            (n =
                                                ((n = {
                                                    image: r,
                                                    t: Date.now(),
                                                }),
                                                n)),
                                            Object.getOwnPropertyDescriptors
                                                ? Object.defineProperties(
                                                      t,
                                                      Object.getOwnPropertyDescriptors(
                                                          n,
                                                      ),
                                                  )
                                                : (function (e, t) {
                                                      var n = Object.keys(e);
                                                      if (
                                                          Object.getOwnPropertySymbols
                                                      ) {
                                                          var r =
                                                              Object.getOwnPropertySymbols(
                                                                  e,
                                                              );
                                                          n.push.apply(n, r);
                                                      }
                                                      return n;
                                                  })(Object(n)).forEach(
                                                      function (e) {
                                                          Object.defineProperty(
                                                              t,
                                                              e,
                                                              Object.getOwnPropertyDescriptor(
                                                                  n,
                                                                  e,
                                                              ),
                                                          );
                                                      },
                                                  ),
                                            t),
                                        ),
                                    ),
                                ),
                            ),
                        );
                        return Promise.resolve(
                            `${s}/apps/activity/share/og?token=${i}`,
                        );
                    },
                    queryVipV2: (e) =>
                        c.post(
                            "/interface/shelfProto",
                            l(
                                {
                                    trpcPath:
                                        "/trpc.midasuser.vip.Vip/QueryVipV2",
                                },
                                e,
                            ),
                        ),
                    queryCouponInfo: (e) =>
                        c.get("/interface/queryCouponInfo", e),
                    queryRedeemCode: (e) =>
                        c.post(
                            "/apps/activity/api/v1/midasuser/vip/queryRedeemCode",
                            e,
                        ),
                    sendEmail: (e) => c.post("/interface/sendEmail", e),
                    querySubscribe: (e) =>
                        c.post("/interface/querySubscribe", e),
                    subscribeNotifications: (e) =>
                        c.post("/interface/subscribeNotifications", e),
                    mobileOverseasCommonInfo: (e) =>
                        c.post(
                            "/apps/activity/api/v1/cgi/mobileOverseasCommonInfo",
                            e,
                        ),
                    getCharacByOpenid: (e) =>
                        c.get("/interface/getCharacByOpenid", { params: e }),
                    verifyBalance: (e) => c.post("/interface/verifyBalance", e),
                    queryRoleIsOnline: (e) =>
                        c.get("/interface/easy_access/check_online", {
                            params: e,
                        }),
                    queryRoleDetail: (e) =>
                        c.get("/interface/queryRoleDetail", { params: e }),
                    gameLink: (e, t, n) =>
                        (0, i.Z)({
                            method: "post",
                            data: e,
                            headers: t,
                            url: `/midas/usc/v1/${n}/gameLink`,
                        }),
                    getLipByEmail(e) {
                        let t = location.host.includes("sandbox")
                            ? { appid: "332651" }
                            : { appid: "123123" };
                        return c.post(
                            `/midas/usc/v1/${t.appid}/getLipByEmail`,
                            e,
                        );
                    },
                    shelvesQuery: (e) =>
                        c.post(
                            "/apps/activity/api/v1/go/midasbuy/shelvesQuery",
                            e,
                        ),
                    queryRoleInfoByOpenid: (e) =>
                        c
                            .post(
                                "/apps/activity/api/v1/go/midasbuy/proxy/easy_access/query_role_info_by_openid",
                                e,
                            )
                            .then((e) => JSON.parse(e.data)),
                    querySubscribeActivityStatus: (e) =>
                        c.get("/interface/querySubscribeActivityStatus", {
                            params: e,
                        }),
                    subscribeActivity: (e) =>
                        c.post("/interface/subscribeActivity", e),
                    querySubscribeActivityTotal: (e) =>
                        c.get("/interface/querySubscribeActivityTotal", {
                            params: e,
                        }),
                };
        },
        77468: function (e, t, n) {
            "use strict";
            n.d(t, {
                o: function () {
                    return m;
                },
                k: function () {
                    return f;
                },
            });
            var r = n("616"),
                i = n("89879"),
                o = n("19639"),
                a = n("65317"),
                l = n("80430"),
                u = n("14866");
            let s = async ({ call_param: e, acct_id: t, params: n = {} }) => {
                let r = await (0, l.Z)({
                    method: "post",
                    baseURL: `https://${(0, u.SV)()}`,
                    url: "/api/CommonCallMpgo",
                    headers: { "x-request-id": (0, a.Vj)() },
                    data: { acct_id: null != t ? t : "1", call_param: e },
                    params: n,
                });
                return 200 !== r.status
                    ? { result_code: "-1", result_info: "network error" }
                    : "0" !== r.data.result_code
                      ? r.data
                      : JSON.parse(r.data.data.call_reply);
            };
            var c = n("29564");
            function d(e) {
                for (var t = 1; t < arguments.length; t++) {
                    var n = null != arguments[t] ? arguments[t] : {},
                        r = Object.keys(n);
                    ("function" == typeof Object.getOwnPropertySymbols &&
                        (r = r.concat(
                            Object.getOwnPropertySymbols(n).filter(
                                function (e) {
                                    return Object.getOwnPropertyDescriptor(n, e)
                                        .enumerable;
                                },
                            ),
                        )),
                        r.forEach(function (t) {
                            var r, i, o;
                            ((r = e),
                                (i = t),
                                (o = n[t]),
                                i in r
                                    ? Object.defineProperty(r, i, {
                                          value: o,
                                          enumerable: !0,
                                          configurable: !0,
                                          writable: !0,
                                      })
                                    : (r[i] = o));
                        }));
                }
                return e;
            }
            let p = (e) => {
                    var t, n, r, i, o, a;
                    return e
                        ? {
                              appid:
                                  (null == e
                                      ? void 0
                                      : null === (t = e.userData) ||
                                          void 0 === t
                                        ? void 0
                                        : t.appid) || "",
                              token:
                                  (null == e
                                      ? void 0
                                      : null === (n = e.userData) ||
                                          void 0 === n
                                        ? void 0
                                        : n.token) || "",
                              endpoint_type: "mpgo_activity",
                              session_id: "hy_gameid",
                              session_type: "st_dummy",
                              openid:
                                  (null == e
                                      ? void 0
                                      : null === (i = e.userData) ||
                                          void 0 === i
                                        ? void 0
                                        : null === (r = i.currentBindUser) ||
                                            void 0 === r
                                          ? void 0
                                          : r.openid) || "",
                              openkey: "nokey",
                              offer_id:
                                  (null == e
                                      ? void 0
                                      : null === (o = e.payInfo) || void 0 === o
                                        ? void 0
                                        : o.appid) || "",
                              pf:
                                  (null == e
                                      ? void 0
                                      : null === (a = e.payInfo) || void 0 === a
                                        ? void 0
                                        : a.pf) || "",
                              userType: "hy_gameid",
                              accountType: "midasbuy",
                              userData: null == e ? void 0 : e.userData,
                          }
                        : {
                              appid: "",
                              token: "",
                              endpoint_type: "mpgo_activity",
                              session_id: "hy_gameid",
                              session_type: "st_dummy",
                              openid: "",
                              openkey: "",
                              pf: "",
                              offer_id: "",
                              userType: "hy_gameid",
                              accountType: "midasbuy",
                              userData: null,
                          };
                },
                f = (e, t, n, l, u = !1) => {
                    var f, m, y, v, g, b, _;
                    let h = null !== (_ = (0, i.rh)()) && void 0 !== _ ? _ : "",
                        w =
                            (null == e
                                ? void 0
                                : null === (y = e.data) || void 0 === y
                                  ? void 0
                                  : null === (m = y.dataConf) || void 0 === m
                                    ? void 0
                                    : null === (f = m.callParamJson) ||
                                        void 0 === f
                                      ? void 0
                                      : f.mp_activity_id) || "",
                        O =
                            null === (v = e.data) || void 0 === v
                                ? void 0
                                : v.__modelKey;
                    (0, o.w)(e.global, "modelId", O);
                    let P = w,
                        j = (0, c.useTShareAtom)(l, n.storeKey, n.stateKey),
                        [S, I] = (0, c.useTState)(j),
                        E = (0, r.useCallback)(async () => {
                            let e = async () => {
                                var e, r, i;
                                let o = {},
                                    l = {
                                        mp_app_id: h,
                                        mp_activity_id: P,
                                        mp_sub_activity_id:
                                            (null == n ? void 0 : n.modelId) ||
                                            "",
                                        user_id:
                                            (null == t
                                                ? void 0
                                                : null === (r = t.userData) ||
                                                    void 0 === r
                                                  ? void 0
                                                  : null ===
                                                          (e =
                                                              r.currentBindUser) ||
                                                      void 0 === e
                                                    ? void 0
                                                    : e.openid) ||
                                            "34133663436637488",
                                        user_id_type: "hy_gameid",
                                    };
                                (null == n ? void 0 : n.mpTaskId) &&
                                    (null == n ? void 0 : n.subTaskId) &&
                                    (null == n
                                        ? void 0
                                        : null === (i = n.subTaskId) ||
                                            void 0 === i
                                          ? void 0
                                          : i.length) > 0 &&
                                    d({}, l, {
                                        mp_task_id:
                                            null == n ? void 0 : n.mpTaskId,
                                        mp_activity_trade_no: (0, a.Vj)(),
                                        mp_task_exec_subtask_list:
                                            null == n
                                                ? void 0
                                                : n.subTaskId.map((e) => ({
                                                      mp_task_subtask_id: e,
                                                      mp_task_completion_timestamp:
                                                          Math.round(
                                                              Date.now() / 1e3,
                                                          ),
                                                      mp_task_subtask_meta_data:
                                                          { is_login: "1" },
                                                  })),
                                    });
                                let u = n.httpProtocol,
                                    c = p(t);
                                return await s({
                                    acct_id: null == n ? void 0 : n.acctId,
                                    call_param: {
                                        context_map_json: JSON.stringify(u),
                                        call_type:
                                            null == n ? void 0 : n.call_type,
                                        call_func:
                                            null == n ? void 0 : n.call_func,
                                        call_param_json: JSON.stringify(l),
                                        login_check_param_json:
                                            JSON.stringify(c),
                                    },
                                });
                            };
                            I(await e());
                        }, [
                            P,
                            h,
                            null == t
                                ? void 0
                                : null === (b = t.userData) || void 0 === b
                                  ? void 0
                                  : null === (g = b.currentBindUser) ||
                                      void 0 === g
                                    ? void 0
                                    : g.openid,
                            null == n ? void 0 : n.acctId,
                            null == n ? void 0 : n.call_func,
                            null == n ? void 0 : n.call_type,
                            n.httpProtocol,
                            null == n ? void 0 : n.modelId,
                            null == n ? void 0 : n.mpTaskId,
                            null == n ? void 0 : n.subTaskId,
                            I,
                        ]);
                    return (
                        (0, r.useEffect)(() => {
                            t && !S && !u && E();
                        }, [E, t, u, S]),
                        [E, S]
                    );
                },
                m = async (e, t, n, r) => {
                    var o, l, u, c;
                    let f = null !== (c = (0, i.rh)()) && void 0 !== c ? c : "",
                        m =
                            (null == n ? void 0 : n.mpActivityId) ||
                            (null == e
                                ? void 0
                                : null === (u = e.data) || void 0 === u
                                  ? void 0
                                  : null === (l = u.dataConf) || void 0 === l
                                    ? void 0
                                    : null === (o = l.callParamJson) ||
                                        void 0 === o
                                      ? void 0
                                      : o.mp_activity_id) ||
                            "",
                        y = async () => {
                            var e, i, o;
                            let l = {},
                                u = {
                                    mp_app_id: f,
                                    mp_activity_id: m,
                                    mp_sub_activity_id: n.modelId || "",
                                    mp_model_type: 106,
                                    user_id:
                                        (null == t
                                            ? void 0
                                            : null === (i = t.userData) ||
                                                void 0 === i
                                              ? void 0
                                              : null ===
                                                      (e = i.currentBindUser) ||
                                                  void 0 === e
                                                ? void 0
                                                : e.openid) ||
                                        "34133663436637488",
                                    user_id_type: "hy_gameid",
                                };
                            if (
                                (null == n ? void 0 : n.mpTaskId) &&
                                (null == n ? void 0 : n.subTaskId) &&
                                (null == n
                                    ? void 0
                                    : null === (o = n.subTaskId) || void 0 === o
                                      ? void 0
                                      : o.length) > 0
                            ) {
                                let e = n.subTaskId.find(
                                        (e, t) => t === n.taskIndex,
                                    ),
                                    t = [
                                        {
                                            mp_task_subtask_id: e,
                                            mp_task_completion_timestamp:
                                                Math.round(Date.now() / 1e3),
                                            mp_task_subtask_meta_data: {
                                                is_login: "1",
                                            },
                                        },
                                    ],
                                    i = {
                                        mp_task_id:
                                            null == n ? void 0 : n.mpTaskId,
                                        mp_activity_trade_no: (0, a.Vj)(),
                                        mp_task_exec_subtask_list: t,
                                    };
                                (r &&
                                    (i = {
                                        mp_task_id:
                                            null == n ? void 0 : n.mpTaskId,
                                        mp_activity_trade_no: (0, a.Vj)(),
                                        mp_task_subtask_id: e,
                                        mp_task_meta_data: { is_login: "1" },
                                    }),
                                    (l = d({}, u, i)));
                            } else l = u;
                            let c = n.httpProtocol,
                                y = p(t);
                            return await s({
                                acct_id: null == n ? void 0 : n.acctId,
                                call_param: {
                                    context_map_json: JSON.stringify(c),
                                    call_type: null == n ? void 0 : n.call_type,
                                    call_func: null == n ? void 0 : n.call_func,
                                    call_param_json: JSON.stringify(l),
                                    login_check_param_json: JSON.stringify(y),
                                },
                            });
                        };
                    return await y();
                };
        },
        89879: function (e, t, n) {
            "use strict";
            n.d(t, {
                Jg: function () {
                    return g;
                },
                Q1: function () {
                    return u;
                },
                RD: function () {
                    return v;
                },
                TQ: function () {
                    return a;
                },
                Um: function () {
                    return _;
                },
                Xi: function () {
                    return p;
                },
                _v: function () {
                    return d;
                },
                a9: function () {
                    return h;
                },
                b9: function () {
                    return c;
                },
                bm: function () {
                    return b;
                },
                cv: function () {
                    return s;
                },
                n5: function () {
                    return f;
                },
                nX: function () {
                    return m;
                },
                rh: function () {
                    return y;
                },
                yi: function () {
                    return l;
                },
            });
            var r = n(65317),
                i = n(94263),
                o = n(77468);
            let a = !!(0, r.jS)("debug") && !(0, r.X0)((0, r.jS)("debug")),
                l = (() => {
                    let e =
                        location.pathname.includes("act/verify-pagedoo") ||
                        "1" === (0, r.jS)("verify");
                    return (
                        a || e || "sandbox.midasbuy.com" === location.hostname
                    );
                })(),
                u = (e) =>
                    e / parseInt(document.documentElement.style.fontSize, 10),
                s = (e) =>
                    e * parseInt(document.documentElement.style.fontSize, 10),
                c = () =>
                    document.body.clientWidth >= 768 ||
                    window.matchMedia("(orientation: landscape)").matches,
                d = (e) => new Promise((t) => setTimeout(t, e)),
                p = (e = 0) =>
                    c() ? e / 2 : (e * document.body.clientWidth) / 750,
                f = () =>
                    `trade-${+new Date()}-${Math.floor(9e5 * Math.random() + 1e5)}`,
                m = async (e, t, n = "", r = "", a = "") => {
                    let l = {
                        call_type: i.bY.CallType,
                        call_func: i.bY.CallFuncs.QueryUserCard,
                        acctId: r,
                        modelId: n,
                        httpProtocol: i.bY.protocol,
                        mpActivityId: a,
                    };
                    return await (0, o.o)(e, t, l);
                },
                y = () => {
                    var e;
                    let t =
                        null !== (e = (0, r.jS)("appid")) && void 0 !== e
                            ? e
                            : "";
                    if ("" !== t) return t;
                    try {
                        return localStorage.getItem("AppcationId");
                    } catch (e) {
                        return "";
                    }
                },
                v =
                    "//pagedoo.midasbuy.com/material/202307101225411091064960/3511261f2219959016bf0a8e8b9f9fcd.png",
                g = {
                    BuyGift: 114,
                    LuckDraw: 105,
                    Task: 106,
                    DynamicBuyGift: 108,
                    Help: 3,
                    Exchange: 4,
                    Coupon: 123,
                    Team: 22,
                },
                b = (e) =>
                    ({ pt: "pu", es: "sp", "zh-hant": "hk", ms: "my" })[
                        e.toLowerCase()
                    ] || e,
                _ = (e) =>
                    ({ pu: "pt", sp: "es", hk: "zh-Hant" })[e.toLowerCase()] ||
                    e,
                h = (e) => {
                    document.body.style.overflow = e ? "" : "hidden";
                };
        },
        84624: function (e, t, n) {
            "use strict";
            function r() {
                return !/(iPhone|iPad|iPod|iOS|Android)/i.test(
                    window.navigator.userAgent,
                );
            }
            function i() {
                return /iPhone|iPad|iPod/i.test(window.navigator.userAgent);
            }
            function o() {
                return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
                    window.navigator.userAgent,
                );
            }
            n.d(t, {
                Ro: function () {
                    return r;
                },
                gn: function () {
                    return i;
                },
                tq: function () {
                    return o;
                },
                uf: function () {
                    return a;
                },
            });
            let a = () => {
                let e = navigator.language;
                return !("object" != typeof Intl || !Intl.NumberFormat || !e);
            };
        },
        81962: function (e, t, n) {
            "use strict";
            function r(e, t, n) {
                return (
                    t in e
                        ? Object.defineProperty(e, t, {
                              value: n,
                              enumerable: !0,
                              configurable: !0,
                              writable: !0,
                          })
                        : (e[t] = n),
                    e
                );
            }
            n.d(t, {
                dn: function () {
                    return u;
                },
                K2: function () {
                    return y;
                },
                G$: function () {
                    return c;
                },
                yM: function () {
                    return f;
                },
                yV: function () {
                    return d;
                },
                xY: function () {
                    return l;
                },
                x1: function () {
                    return p;
                },
                Jm: function () {
                    return s;
                },
                Ug: function () {
                    return m;
                },
                UV: function () {
                    return v;
                },
                gs: function () {
                    return a;
                },
            });
            class i extends Error {
                constructor(e, t, n) {
                    (super(t),
                        r(this, "name", void 0),
                        r(this, "stack", void 0),
                        r(this, "extra", void 0),
                        (this.name = e),
                        (this.stack = Error().stack || ""),
                        (null == n ? void 0 : n.extra) &&
                            (this.extra = n.extra));
                }
            }
            let o = (e) => {
                    class t extends i {
                        static is(n) {
                            return n instanceof t && n.name === e;
                        }
                        toString() {
                            let e = this.extra
                                    ? `<${JSON.stringify(this.extra)}>`
                                    : "",
                                t = this.message ? `: ${this.message}` : "";
                            return `${this.name}${e}${t}`;
                        }
                        constructor(t, n) {
                            super(e, t || "", n);
                        }
                    }
                    return t;
                },
                a = o("VIP_LEVEL_NOT_ENOUGH"),
                l = o("BALANCE_NOT_ENOUGH"),
                u = o("COUPON_NOT_ENOUGH"),
                s = o("NOT_VERIFIED_ERROR"),
                c = o("NO_OPENID_ERROR"),
                d = o("BACKEND_ERROR"),
                p = o("CONFIG_ERROR"),
                f = o("NO_PAY_RECORD"),
                m = o("TASK_NOT_ELIGIBLE"),
                y = o("LimitQuotaExceededError"),
                v = o("USER_CLOSED_ERROR");
        },
        74740: function (e, t, n) {
            "use strict";
            n.d(t, {
                H1: function () {
                    return a;
                },
                J5: function () {
                    return u;
                },
                Q7: function () {
                    return s;
                },
                ZM: function () {
                    return c;
                },
                wE: function () {
                    return l;
                },
            });
            var r = n(99744);
            let i = (0, r.R)("REQUEST_RESPONSE"),
                o = (0, r.R)("RESPONSE_REQUEST");
            class a {
                static async request(e, t, n) {
                    let r = `${performance.now().toFixed(0)}_${Math.random().toString(36).slice(-4)}`;
                    return (
                        await this.waitForEventHandler(e, i),
                        e.emit(i, { eventName: t, requestId: r, params: n }),
                        new Promise((t) => {
                            let n = e.on(o, ({ requestId: e, result: i }) => {
                                e === r && (t(i), n());
                            });
                        })
                    );
                }
                static respondTo(e, t, n) {
                    return e.on(
                        i,
                        async ({ eventName: r, requestId: i, params: a }) => {
                            if (r !== t) return;
                            let l = await n(a);
                            e.emit(o, { requestId: i, result: l });
                        },
                    );
                }
                static waitForEventHandler(e, t) {
                    return new Promise((n) => {
                        let r = setInterval(() => {
                            e.eventMap.has(t) && (n(), clearInterval(r));
                        }, 16);
                    });
                }
            }
            let l = {
                    statusChange: "commonEvents.statusChange",
                    userChange: "commonEvents.userChange",
                },
                u = {
                    setActiveModelId: "luckDrawModel.setActiveModelId",
                    setLuckDrawMetaData: "luckDrawModel.setLuckDrawMetaData",
                    playLotteryAnimation: "luckDrawModel.playLotteryAnimation",
                    isAnimationPlaying: "luckDrawModel.isAnimationPlaying",
                },
                s = {
                    setPointsExchangeMetaData:
                        "exchangeEvents.setPointsExchangeMetaData",
                },
                c = { modifyVipInfo: "midasbuyEvents.modifyVipInfo" };
        },
        68187: function (e, t, n) {
            "use strict";
            n.d(t, {
                Z: function () {
                    return a;
                },
            });
            let r = {
                BRL: {
                    currencySymbol: "R$ ",
                    decimalPoint: ",",
                    leftSymbol: !0,
                    thousandPoint: ".",
                    zeroPadding: "2",
                },
                IDR: {
                    currencySymbol: "Rp ",
                    leftSymbol: !0,
                    thousandPoint: ".",
                },
                JPY: { currencySymbol: "円" },
                MMK: { currencySymbol: " MMK", thousandPoint: "," },
                MYR: { currencySymbol: "RM ", leftSymbol: !0 },
                PHP: { currencySymbol: "₱ ", leftSymbol: !0 },
                THB: { currencySymbol: "฿ ", leftSymbol: !0 },
                VND: { currencySymbol: " ₫", leftSymbol: !1 },
                ZAR: { currencySymbol: "R ", leftSymbol: !0 },
            };
            function i(e) {
                let t = String(e).split("."),
                    n = t[0],
                    r = t.length > 1 ? `.${t[1]}` : "",
                    i = /(\d+)(\d{3})/;
                for (; i.test(n); ) n = n.replace(i, "$1,$2");
                return n + r;
            }
            function o(e) {
                return e.replace(".", "#").replace(/,/g, ".").replace("#", ",");
            }
            var a = function (e, t) {
                var n;
                let a;
                let l = ((n = e), (a = parseInt(`${n}`, 10) / 100).toString()),
                    u = i(l),
                    s = r[t];
                if (s) {
                    let e = s.decimalPoint || ".",
                        n = s.thousandPoint || ",",
                        r = s.currencySymbol || t,
                        o = s.leftSymbol || !1,
                        a = s.zeroPadding
                            ? parseInt(`${s.zeroPadding}`, 10)
                            : 0,
                        l = !!s.rounding,
                        c = u;
                    return (
                        a &&
                            (c = (function (e, t, n) {
                                if (t <= 0) return e;
                                let r = e.split(".");
                                if (r.length > 1) {
                                    let o = t - r[1].length;
                                    if (o >= 0)
                                        return `${r[0]}.${r[1]}${Array(o).fill("0").join("")}`;
                                    if (n) {
                                        let [e, n] = parseFloat(`0.${r[1]}`)
                                            .toFixed(t)
                                            .split(".");
                                        if ("1" === e) {
                                            let e = i(
                                                parseInt(
                                                    r[0]
                                                        .toString()
                                                        .replace(/,/g, ""),
                                                    10,
                                                ) + 1,
                                            );
                                            return `${e}.${n}`;
                                        }
                                        return `${r[0]}.${n}`;
                                    }
                                    return e;
                                }
                                return `${e}.${Array(t).fill("0").join("")}`;
                            })(c, a, l)),
                        (c = c
                            .replace(".", "d")
                            .replace(/,/g, n)
                            .replace("d", e)),
                        o ? (c = r + c) : (c += r),
                        c
                    );
                }
                let c = `${l} ${t}`;
                switch (t) {
                    case "IDR":
                        c = `Rp ${o(u)}`;
                        break;
                    case "THB":
                        c = `฿${u}`;
                        break;
                    case "PHP":
                        c = `₱${u}`;
                        break;
                    case "VND":
                        c = `${o(u)}₫`;
                        break;
                    case "MYR":
                        c = `RM${u}`;
                }
                return c;
            };
        },
        31661: function (e, t, n) {
            "use strict";
            n.d(t, {
                H: function () {
                    return r;
                },
                X: function () {
                    return i;
                },
            });
            let r = (e = "") => {
                    let t = e.split("_"),
                        n = "",
                        r = "";
                    return (
                        1 === t.length ? (n = e) : ([n, r] = t),
                        { serverId: n, roleId: r, shortZoneId: t[0] }
                    );
                },
                i = (e, t) => {
                    var n, r, i;
                    if (
                        !t ||
                        !e ||
                        !(null == e
                            ? void 0
                            : null === (n = e.payInfo) || void 0 === n
                              ? void 0
                              : n.needSelectPf)
                    )
                        return "";
                    let o =
                        (null == t
                            ? void 0
                            : null === (r = t.user) || void 0 === r
                              ? void 0
                              : r.currentBindUser) ||
                        (null == e
                            ? void 0
                            : null === (i = e.userData) || void 0 === i
                              ? void 0
                              : i.currentBindUser);
                    return (null == o ? void 0 : o.roleId)
                        ? o.roleId
                        : (null == o ? void 0 : o.userid)
                          ? o.userid
                          : "";
                };
        },
        48620: function (e, t, n) {
            "use strict";
            n.d(t, {
                V: function () {
                    return i;
                },
            });
            var r = n(65317);
            let i = () =>
                (0, r.jS)("country") || r.pR.get("select_country") || "";
        },
        99744: function (e, t, n) {
            "use strict";
            n.d(t, {
                H: function () {
                    return a;
                },
                R: function () {
                    return o;
                },
            });
            var r = n(84472),
                i = n.n(r);
            let o = (e) => `${i().libName}_${e}Store`,
                a = (e) => `${i().libName}_${e}State`;
        },
        63821: function (e, t, n) {
            "use strict";
            n.d(t, {
                Xi: function () {
                    return i.Xi;
                },
                gn: function () {
                    return o.gn;
                },
                tq: function () {
                    return o.tq;
                },
                V_: function () {
                    return l;
                },
                m1: function () {
                    return h;
                },
                ji: function () {
                    return c;
                },
                Q1: function () {
                    return i.Q1;
                },
                cv: function () {
                    return i.cv;
                },
                _v: function () {
                    return i._v;
                },
                bm: function () {
                    return i.bm;
                },
                Um: function () {
                    return i.Um;
                },
                a9: function () {
                    return i.a9;
                },
                B9: function () {
                    return _.B;
                },
                Ro: function () {
                    return o.Ro;
                },
                b9: function () {
                    return i.b9;
                },
                Yl: function () {
                    return a;
                },
                GA: function () {
                    return d;
                },
                RV: function () {
                    return r.RV;
                },
                JE: function () {
                    return b;
                },
                n5: function () {
                    return i.n5;
                },
                TQ: function () {
                    return i.TQ;
                },
                Jg: function () {
                    return i.Jg;
                },
                RD: function () {
                    return i.RD;
                },
                Vc: function () {
                    return w.V;
                },
            });
            var r = n("78181"),
                i = n("89879"),
                o = n("84624");
            function a(e) {
                return "object" == typeof FB
                    ? window.FB
                    : new Promise((t) => {
                          let n = {
                              init_FB_Button(e) {},
                              getToken() {},
                              login(e) {
                                  FB.login((t) => {
                                      "connected" === t.status && e();
                                  });
                              },
                              logout(e) {
                                  var t;
                                  (null === (t = FB) || void 0 === t
                                      ? void 0
                                      : t.logout) &&
                                      FB.logout(() => {
                                          e();
                                      });
                              },
                          };
                          ((window.fbAsyncInit = function () {
                              (FB.init({
                                  appId: e || "855538431298982",
                                  cookie: !0,
                                  xfbml: !0,
                                  version: "v15.0",
                              }),
                                  FB.AppEvents.logPageView(),
                                  FB.getLoginStatus((e) => {
                                      n.init_FB_Button(
                                          "connected" === e.status,
                                      );
                                  }),
                                  t(FB));
                          }),
                              !(function (e, t, n) {
                                  let r = e.getElementsByTagName(t)[0];
                                  if (e.getElementById(n)) return;
                                  let i = e.createElement(t);
                                  ((i.id = n),
                                      (i.src =
                                          "//connect.facebook.net/en_US/sdk.js"),
                                      r.parentNode.insertBefore(i, r));
                              })(document, "script", "facebook-jssdk"));
                      });
            }
            let l = {
                createLoadingEle() {
                    let e = document.createElement("div");
                    return (
                        (e.innerHTML =
                            "<div id='global_loading'        style='width: 100%; height: 100%; position: fixed; z-index: 10000; top: 0; left: 0; width: 100%; height: 100%; background: rgba(000, 000, 000, .8); '>        <div          style='position: absolute; z-index: 10001; box-sizing: border-box; top: 50%; left: 50%; transform: translateX(-50%); color: #fff; font-weight: bold; text-align: center;'>          <svg style='display: block; margin: 0 auto' id='loader-1' version='1.1' xmlns='http://www.w3.org/2000/svg'            xmlns:xlink='http://www.w3.org/1999/xlink' x='0px' y='0px' width='40px' height='40px' viewBox='0 0 40 40'            enable-background='new 0 0 40 40' xml:space='preserve'>            <path opacity='0.2' fill='#fff' d='M20.201,5.169c-8.254,0-14.946,6.692-14.946,14.946c0,8.255,6.692,14.946,14.946,14.946s14.946-6.691,14.946-14.946C35.146,11.861,28.455,5.169,20.201,5.169z M20.201,31.749c-6.425,0-11.634-5.208-11.634-11.634c0-6.425,5.209-11.634,11.634-11.634c6.425,0,11.633,5.209,11.633,11.634C31.834,26.541,26.626,31.749,20.201,31.749z' />            <path id='loader-spin' fill='#fff' d='M26.013,10.047l1.654-2.866c-2.198-1.272-4.743-2.012-7.466-2.012h0v3.312h0C22.32,8.481,24.301,9.057,26.013,10.047z' style='animation: 0.5s linear infinite loadingrotate; transform-origin: 20px 20px;'>            </path>          </svg>        </div>        <style>@keyframes loadingrotate {          from {            transform: rotate(0);          }          to {            transform: rotate(360deg);          }        }</style>      </div>"),
                        e.childNodes[0]
                    );
                },
                show(e) {
                    let t = document.getElementById("global_loading");
                    (t
                        ? (t.style.display = "block")
                        : document.body.appendChild(this.createLoadingEle()),
                        e &&
                            setTimeout(() => {
                                l.hide();
                            }, e));
                },
                hide() {
                    let e = document.getElementById("global_loading");
                    e && (e.style.display = "none");
                },
            };
            var u = n("68187");
            let s = (e) => {
                var t;
                return null == e
                    ? void 0
                    : null === (t = e.prices) || void 0 === t
                      ? void 0
                      : t.some((e) => "" !== e.payment_channel_id);
            };
            function c(e, t) {
                var n, r, i, o, a, l;
                let c = (function (e) {
                        if (e.lowest_price) return e.lowest_price;
                        let { prices: t = [], promotion_info: n } = e;
                        if (null == n ? void 0 : n.promotion_id) {
                            let e = t.find(
                                (e) =>
                                    e.promotion_id ===
                                    (null == n ? void 0 : n.promotion_id),
                            );
                            if (e) return e;
                        }
                        let r = [...t].filter((e) => !e.promotion_id);
                        return (null == n ? void 0 : n.promotion_id) || s(e)
                            ? null == t
                                ? void 0
                                : t.reduce((e, t) => {
                                      let n = parseFloat(e.amount);
                                      return parseFloat(t.amount) < n ? t : e;
                                  }, r[0])
                            : null == r
                              ? void 0
                              : r.find(
                                    (e) =>
                                        "" === e.payment_channel_id &&
                                        "" === e.promotion_id,
                                );
                    })(e),
                    d = c ? `${Math.round(100 * Number(c.amount))}` : "0",
                    p = parseFloat(
                        (null === (r = e.main_channel_promotions) ||
                        void 0 === r
                            ? void 0
                            : null === (n = r.taxed_final_price) || void 0 === n
                              ? void 0
                              : n.amount) ||
                            (null === (o = e.main_channel_promotions) ||
                            void 0 === o
                                ? void 0
                                : null === (i = o.final_price) || void 0 === i
                                  ? void 0
                                  : i.amount) ||
                            "",
                    ),
                    f = p ? `${Math.round(100 * Number(p))}` : d,
                    m = c ? c.currency : t || "USD",
                    y = (null == c ? void 0 : c.display_amount)
                        ? `${Math.round(100 * Number(c.display_amount))}`
                        : 0;
                return (
                    (a = (function (e) {
                        for (var t = 1; t < arguments.length; t++) {
                            var n = null != arguments[t] ? arguments[t] : {},
                                r = Object.keys(n);
                            ("function" ==
                                typeof Object.getOwnPropertySymbols &&
                                (r = r.concat(
                                    Object.getOwnPropertySymbols(n).filter(
                                        function (e) {
                                            return Object.getOwnPropertyDescriptor(
                                                n,
                                                e,
                                            ).enumerable;
                                        },
                                    ),
                                )),
                                r.forEach(function (t) {
                                    var r, i, o;
                                    ((r = e),
                                        (i = t),
                                        (o = n[t]),
                                        i in r
                                            ? Object.defineProperty(r, i, {
                                                  value: o,
                                                  enumerable: !0,
                                                  configurable: !0,
                                                  writable: !0,
                                              })
                                            : (r[i] = o));
                                }));
                        }
                        return e;
                    })({}, e)),
                    (l =
                        ((l = {
                            calculatePriceView: (0, u.Z)(f, m),
                            calculateDisplayPriceView: (0, u.Z)(y || 0, m),
                            calculatePrice: c,
                        }),
                        l)),
                    Object.getOwnPropertyDescriptors
                        ? Object.defineProperties(
                              a,
                              Object.getOwnPropertyDescriptors(l),
                          )
                        : (function (e, t) {
                              var n = Object.keys(e);
                              if (Object.getOwnPropertySymbols) {
                                  var r = Object.getOwnPropertySymbols(e);
                                  n.push.apply(n, r);
                              }
                              return n;
                          })(Object(l)).forEach(function (e) {
                              Object.defineProperty(
                                  a,
                                  e,
                                  Object.getOwnPropertyDescriptor(l, e),
                              );
                          }),
                    a
                );
            }
            let d = [
                {
                    id: "copy",
                    icon: "https://cdn.midasbuy.com/events/public/icon-copy.png",
                    name: "Copy Link",
                    url: "#",
                },
                {
                    id: "email",
                    icon: "https://cdn.midasbuy.com/events/public/icon-email.png",
                    isLink: !0,
                    name: "Email",
                    params: { body: "text", subject: "title" },
                    url: "mailto:",
                },
                {
                    id: "fb",
                    customProperty: ["hashtag", "quote"],
                    icon: "https://cdn.midasbuy.com/events/public/icon-fb.png",
                    name: "Facebook",
                    params: { u: "url" },
                    url: "https://www.facebook.com/sharer/sharer.php",
                },
                {
                    id: "pinterest",
                    name: "Pinterest",
                    params: { description: "text", media: "image", url: "url" },
                    url: "https://www.pinterest.com/pin/create/button/",
                },
                {
                    id: "reddit",
                    name: "Reddit",
                    params: { title: "title", url: "url" },
                    url: "https://www.reddit.com/submit",
                },
                {
                    id: "sms",
                    icon: "https://cdn.midasbuy.com/events/public/icon-sms.png",
                    isLink: !0,
                    name: "SMS",
                    url: "sms://",
                },
                {
                    id: "twitter",
                    customProperty: ["hashtags", "via"],
                    icon: "https://cdn.midasbuy.com/events/public/icon-twitter.png",
                    name: "Twitter",
                    params: { text: "text", url: "url" },
                    url: "https://twitter.com/intent/tweet?",
                },
                {
                    id: "whatsapp",
                    name: "Whatsapp",
                    params: { text: "text" },
                    url: "https://wa.me",
                },
                {
                    id: "ins",
                    icon: "https://cdn.midasbuy.com/events/register/20230515/images/icon-instagram.png",
                    name: "Instagram",
                    url: "https://www.instagram.com/midasbuy_top_up/",
                },
                {
                    id: "yt",
                    icon: "https://cdn.midasbuy.com/events/register/20230515/images/icon-youtube.png",
                    name: "Youtube",
                    url: "https://www.youtube.com/channel/UCVP9bUAXwBkYHcLHBA71zng",
                },
            ];
            var p = n("55974"),
                f = n("67411"),
                m = n("37504"),
                y = n("92889"),
                v = n("17078");
            function g(e) {
                for (var t = 1; t < arguments.length; t++) {
                    var n = null != arguments[t] ? arguments[t] : {},
                        r = Object.keys(n);
                    ("function" == typeof Object.getOwnPropertySymbols &&
                        (r = r.concat(
                            Object.getOwnPropertySymbols(n).filter(
                                function (e) {
                                    return Object.getOwnPropertyDescriptor(n, e)
                                        .enumerable;
                                },
                            ),
                        )),
                        r.forEach(function (t) {
                            var r, i, o;
                            ((r = e),
                                (i = t),
                                (o = n[t]),
                                i in r
                                    ? Object.defineProperty(r, i, {
                                          value: o,
                                          enumerable: !0,
                                          configurable: !0,
                                          writable: !0,
                                      })
                                    : (r[i] = o));
                        }));
                }
                return e;
            }
            async function b(e, t, n, r) {
                var i, a, l, u;
                let s = new y.TinyEmitter();
                window.__CALLBACKINTERFACE = function (e) {
                    let t = (0, f.default)(e),
                        n = (function (e) {
                            return c[e];
                        })(t.buy_type_key);
                    s.emit(t.status, g({ result: t }, n));
                };
                let c = {};
                function d(e) {
                    return c[e];
                }
                await (0, v.wu)();
                let b = t.id;
                n.payParams = n.payParams || {};
                let { payParams: _ } = n,
                    h = {
                        muid: r.uid || "",
                        currency_type: null == e ? void 0 : e.currency_type,
                        productid: b,
                    };
                (0, o.tq)()
                    ? (_.newtab = _.pc_newtab)
                    : (_.newtab = _.h5_newtab);
                let w = `Activity_${Date.now()}_${Math.random().toString().replace(".", "")}`;
                c[w] = { product: t, channel: n };
                let O = {
                    msgUrl: `https://${location.hostname}/oversea_web/static/receiveMsg.html?buy_type_key=${w}`,
                    failUrl: `https://${location.hostname}/callback/fail?buy_type_key=${w}`,
                    pendingUrl: `https://${location.hostname}/callback/pending?buy_type_key=${w}`,
                    successUrl: `https://${location.hostname}/callback/success?buy_type_key=${w}`,
                };
                if (
                    "game_coin" === n.channel ||
                    "os_midasbuy_redeem" === n.channel
                ) {
                    document.querySelector("#checkout_iframe") &&
                        (null ===
                            (a = document.querySelector("#checkout_iframe")) ||
                            void 0 === a ||
                            a.remove());
                    let e = document.createElement("iframe");
                    ((e.id = "checkout_iframe"),
                        (e.src = "about:blank"),
                        (e.style.display = "none"),
                        document.body.appendChild(e),
                        (_.target =
                            document.querySelector(
                                "#checkout_iframe",
                            ).contentWindow),
                        (_.newtab = 0),
                        (_.usePost = 1),
                        (O = {}),
                        window.addEventListener("message", (e) => {
                            let t;
                            try {
                                t = JSON.parse(e.data);
                            } catch (e) {}
                            if (!/\.midasbuy\.com$/.test(e.origin) || !t)
                                return;
                            let n = c[w];
                            s.emit(t._cmd__, g({ result: t }, n));
                        }));
                }
                let P = location.pathname.split("/")[3] || "";
                let j = g(
                    ((l = g(
                        {
                            cgi_extend: (0, m.default)(h, !0),
                            session_id: "hy_gameid",
                            channel: n.channel,
                            subchannel: n.subchannel,
                            session_type: "st_dummy",
                            shopcode: "all",
                        },
                        n.payParams,
                    )),
                    (u =
                        ((u = {
                            newtab: "0" == `${_.newtab}` ? 0 : 1,
                            app_metadata: encodeURIComponent(
                                `muid=${r.uid || ""}`,
                            ),
                            appid: null == e ? void 0 : e.appid,
                            country:
                                null == e
                                    ? void 0
                                    : null === (i = e.country) || void 0 === i
                                      ? void 0
                                      : i.toUpperCase(),
                            currency_type: null == e ? void 0 : e.currency_type,
                            drm_info: encodeURIComponent(`activity_tag=${P}`),
                            openid: null == e ? void 0 : e.openid,
                            pf: null == e ? void 0 : e.pf,
                            id: n.id,
                            productid: b,
                            sandbox:
                                (0, p.default)("sandbox") ||
                                (/sandbox/.test(location.hostname) ? 1 : ""),
                            sessionToken:
                                Date.now() +
                                Math.random().toString().replace(".", ""),
                            version: "midasbuy_v2",
                            zoneid: null == e ? void 0 : e.zoneid,
                            type: "save",
                        }),
                        u)),
                    Object.getOwnPropertyDescriptors
                        ? Object.defineProperties(
                              l,
                              Object.getOwnPropertyDescriptors(u),
                          )
                        : (function (e, t) {
                              var n = Object.keys(e);
                              if (Object.getOwnPropertySymbols) {
                                  var r = Object.getOwnPropertySymbols(e);
                                  n.push.apply(n, r);
                              }
                              return n;
                          })(Object(u)).forEach(function (e) {
                              Object.defineProperty(
                                  l,
                                  e,
                                  Object.getOwnPropertyDescriptor(u, e),
                              );
                          }),
                    l),
                    O,
                    r,
                );
                return (
                    window.midas.buyGame(j, { onMessage(e) {} }),
                    new Promise((e, t) => {
                        (s.once("success", e), s.once("error", t));
                    })
                );
            }
            (0, v.wu)();
            var _ = n("67398");
            let h = () => {
                try {
                    var e;
                    (null === (e = top) || void 0 === e
                        ? void 0
                        : e.location) && top.location.reload();
                } catch (e) {
                    location.reload();
                }
            };
            var w = n("48620");
        },
        17078: function (e, t, n) {
            "use strict";
            let r, i;
            n.d(t, {
                D7: function () {
                    return u;
                },
                IS: function () {
                    return p;
                },
                Sg: function () {
                    return s;
                },
                oJ: function () {
                    return d;
                },
                wu: function () {
                    return c;
                },
            });
            var o,
                a = n(78181),
                l = n(90609);
            let u = (e, t) =>
                    new Promise((n, r) => {
                        if (t) {
                            let e = document.getElementById(t);
                            if (e instanceof HTMLScriptElement) {
                                e.addEventListener("load", () => n());
                                return;
                            }
                        }
                        let i = document.createElement("script");
                        return (
                            i.addEventListener("load", () => n()),
                            i.addEventListener("error", r),
                            (i.src = e),
                            t && (i.id = t),
                            document.head.appendChild(i),
                            i
                        );
                    }),
                s = (e, t) =>
                    new Promise((n) => {
                        let r = document.createElement("link");
                        (t && (r.id = t),
                            (r.rel = "stylesheet"),
                            (r.type = "text/css"),
                            (r.href = e),
                            document
                                .getElementsByTagName("head")[0]
                                .appendChild(r),
                            n());
                    }),
                c = async () =>
                    window.midas
                        ? Promise.resolve(window.midas)
                        : (await u(
                              "https://cdn.midasbuy.com/h5/overseah5/js/midas-oversea-h5page.js",
                              "h5page",
                          ),
                          window.midas);
            let d =
                    ((o = async () => {
                        if (!document.getElementById("xMidasToken"))
                            (await u(`//${a.H}/xmidas-sdk.js`), await p());
                    }),
                    (i = 2),
                    function () {
                        return (
                            --i > 0 && (r = o.apply(this, arguments)),
                            i <= 1 && (o = null),
                            r
                        );
                    }),
                p = () =>
                    new Promise((e) => {
                        if (window.xMidas) return ((0, l.L)(), e());
                        let t = setInterval(async () => {
                            window.xMidas &&
                                (clearInterval(t), (0, l.L)(), e());
                        }, 50);
                    });
        },
        75937: function (e, t, n) {
            "use strict";
            n.d(t, {
                M: function () {
                    return l;
                },
                s: function () {
                    return a;
                },
            });
            let r = (e, t) => {
                    let n = Math.max(t || 1, 0),
                        r = null === e ? 0 : e.length;
                    if (!r || n < 1) return [];
                    let i = 0,
                        o = 0,
                        a = Array(Math.ceil(r / n));
                    for (; i < r; ) a[(o += 1)] = e.slice(i, (i += n));
                    return a;
                },
                i = (e, t) => {
                    let n = (null == t ? void 0 : t.serialNumberSize) || 10;
                    return Object.fromEntries(
                        r(e, n).map((e, t) => [
                            `${n * t + 1}-${n * t + e.length}`,
                            e,
                        ]),
                    );
                },
                o = (e, t) => {
                    let { dataLayers: n = 2, disableSerialNumber: r = !1 } = t,
                        i = n;
                    !r && (i += 1);
                    let o = {};
                    switch (i) {
                        case 1:
                            o.default = { default: e };
                            break;
                        case 3:
                            o = e;
                            break;
                        default:
                            o.default = e;
                    }
                    return o;
                },
                a = (e) => {
                    let { data: t, config: n } = e,
                        r = {},
                        { dataLayers: a = 2 } = n;
                    return (
                        Object.keys(t).forEach((e) => {
                            if (a <= 2) {
                                var o;
                                let a =
                                    (null === (o = t[e]) || void 0 === o
                                        ? void 0
                                        : o.partition) || [];
                                r[e] = n.disableSerialNumber ? a : i(a, n);
                            } else
                                ((r[e] = {}),
                                    (Object.keys(t[e]) || []).forEach((n) => {
                                        var i;
                                        let o =
                                            (null === (i = t[e][n]) ||
                                            void 0 === i
                                                ? void 0
                                                : i.partition) || [];
                                        r[e][n] = o;
                                    }));
                        }),
                        o(r, n)
                    );
                },
                l = (e, t) => {
                    let { data: n, config: r } = e;
                    if (
                        (null == r ? void 0 : r.type) === "partition" &&
                        r.groups
                    ) {
                        if (!t) return e;
                        let i = null == t ? void 0 : t.toLowerCase(),
                            o = r.groups.find(
                                (e) =>
                                    "*" === e.country ||
                                    e.country === i ||
                                    e.country.includes(i),
                            );
                        if (!o) return e;
                        let { zoneid: a } = o,
                            { selectedZoneid: l } = o;
                        if (
                            ("string" == typeof a && (a = [a]),
                            l && a.includes(l))
                        ) {
                            r.selectedZoneid = l;
                            let e = {};
                            return (
                                Object.keys(n).forEach((t) => {
                                    e[t] = {};
                                    let { partition: r } = n[t];
                                    r
                                        ? (e[t].partition = r.filter((e) =>
                                              a.includes(e.zoneid),
                                          ))
                                        : Object.keys(n[t]).forEach((r) => {
                                              e[t][r] = {};
                                              let { partition: i } = n[t][r];
                                              e[t][r].partition = i.filter(
                                                  (e) => a.includes(e.zoneid),
                                              );
                                          });
                                }),
                                { data: e, config: r }
                            );
                        }
                    }
                    return e;
                };
        },
        13047: function (e, t, n) {
            "use strict";
            n.d(t, {
                TV: function () {
                    return o;
                },
                mN: function () {
                    return a;
                },
                v7: function () {
                    return r;
                },
                vZ: function () {
                    return function e(t, n) {
                        if (Object.is(t, n)) return !0;
                        if (
                            "object" != typeof t ||
                            null === t ||
                            "object" != typeof n ||
                            null === n ||
                            Object.keys(t).length !== Object.keys(n).length
                        )
                            return !1;
                        let r = Object.keys(t).sort(),
                            i = Object.keys(n).sort();
                        if (r.toString() !== i.toString()) return !1;
                        for (let r in t) {
                            var o, a;
                            if (
                                ((o = n),
                                (a = r),
                                !Object.prototype.hasOwnProperty.call(o, a) ||
                                    !e(t[r], n[r]))
                            )
                                return !1;
                        }
                        return !0;
                    };
                },
                yo: function () {
                    return i;
                },
            });
            function r(e, t) {
                let n = {};
                return (
                    Object.keys(e).forEach((r) => {
                        t(e[r], r, e) && (n[r] = e[r]);
                    }),
                    n
                );
            }
            function i(e, t) {
                if (null == t || t < 1) return [];
                let n = [],
                    r = 0,
                    { length: i } = e;
                for (; r < i; ) n.push(e.slice(r, (r += t)));
                return n;
            }
            function o(e) {
                let t = [...e];
                for (let e = t.length - 1; e > 0; e--) {
                    let n = Math.floor(Math.random() * (e + 1));
                    [t[e], t[n]] = [t[n], t[e]];
                }
                return t;
            }
            function a(e, t) {
                let n = new Set(),
                    r = [];
                return (
                    e.forEach((e, i, o) => {
                        let a = t(e, i, o);
                        !n.has(a) && (n.add(a), r.push(e));
                    }),
                    r
                );
            }
        },
        14603: function (e, t, n) {
            "use strict";
            let r;
            n.d(t, {
                NY: function () {
                    return g;
                },
                Q0: function () {
                    return y;
                },
                QR: function () {
                    return f;
                },
                ST: function () {
                    return w;
                },
                WF: function () {
                    return O;
                },
                Wt: function () {
                    return p;
                },
                Ym: function () {
                    return s;
                },
                ZY: function () {
                    return b;
                },
                eC: function () {
                    return _;
                },
                hv: function () {
                    return h;
                },
                iL: function () {
                    return m;
                },
                uy: function () {
                    return v;
                },
                yR: function () {
                    return P;
                },
            });
            var i,
                o = n(65317),
                a = n(89879);
            let l = window;
            async function u() {
                if (Array.isArray(l.__initPage))
                    try {
                        return JSON.parse(l.__initPage[2].pages[0].data);
                    } catch (e) {
                        return l.__initPage[2].pages[0].data;
                    }
                let e = (function () {
                    try {
                        if (window.handler) return window.handler;
                        if (window.parent !== window)
                            return window.parent.handler;
                        return null;
                    } catch (e) {
                        return null;
                    }
                })();
                if (e) return e.getPageContent();
                if ("object" == typeof l.__gems_preview)
                    return r
                        ? Promise.resolve(r)
                        : fetch("/__getStore", {
                              method: "POST",
                              body: '{"key":"gems-dev|preview"}',
                              headers: { "content-type": "application/json" },
                          })
                              .then((e) => e.json())
                              .then((e) => {
                                  try {
                                      return JSON.parse(e.data.global.pages);
                                  } catch (t) {
                                      return e.data.global.pages;
                                  }
                              })
                              .then((e) => ((r = e), e));
                return null;
            }
            async function s() {
                return (
                    await window.handler.getPageContent()
                ).components[0].children.sort((e, t) => {
                    var n, r, i, o;
                    let a =
                            null == e
                                ? void 0
                                : null === (r = e.commonStyle) || void 0 === r
                                  ? void 0
                                  : null === (n = r.position) || void 0 === n
                                    ? void 0
                                    : n.type,
                        l =
                            null == t
                                ? void 0
                                : null === (o = t.commonStyle) || void 0 === o
                                  ? void 0
                                  : null === (i = o.position) || void 0 === i
                                    ? void 0
                                    : i.type;
                    return a === l
                        ? 0
                        : "absolute" === a
                          ? 1
                          : "absolute" === l
                            ? -1
                            : 0;
                });
            }
            async function c() {
                let e = await u();
                return (Array.isArray(e) ? e.map((e) => e.data) : [e]).flatMap(
                    (e) => {
                        var t, n, r, i;
                        return (
                            (null == e
                                ? void 0
                                : null === (i = e.components) || void 0 === i
                                  ? void 0
                                  : null === (r = i[0]) || void 0 === r
                                    ? void 0
                                    : null === (n = r.children) || void 0 === n
                                      ? void 0
                                      : null ===
                                              (t = n.map((e) => {
                                                  var t;
                                                  return null ===
                                                      (t = e.data.dataConf) ||
                                                      void 0 === t
                                                      ? void 0
                                                      : t.ruleConf;
                                              })) || void 0 === t
                                        ? void 0
                                        : t.filter(Boolean)) || []
                        );
                    },
                );
            }
            async function d() {
                var e, t, n;
                let r =
                    (null === (e = await u()) || void 0 === e
                        ? void 0
                        : e.components) || [];
                return new Date(
                    1e3 *
                        Math.max(
                            ...((null == r
                                ? void 0
                                : null === (n = r[0]) || void 0 === n
                                  ? void 0
                                  : null === (t = n.children) || void 0 === t
                                    ? void 0
                                    : t.map((e) => {
                                          var t;
                                          return Number(
                                              null ===
                                                  (t = `${e.id}`.match(
                                                      /@([^/]+)/,
                                                  )) || void 0 === t
                                                  ? void 0
                                                  : t[1],
                                          );
                                      })) || []),
                        ),
                ).toLocaleString();
            }
            async function p(e) {
                let t = await u();
                if (!t) throw Error("Unable to get schema!");
                let n = (Array.isArray(t) ? t[0].data : t).components[0]
                    .children;
                return (
                    !!Array.isArray(n) &&
                    n.some((t) => String(t.id).endsWith(`/${e}`))
                );
            }
            function f(e, t) {
                try {
                    let n = e.global.pages;
                    if (!n) throw Error("Unable to get schema!");
                    let r = (Array.isArray(n) ? n[0].data : n).components[0]
                        .children;
                    if (!Array.isArray(r)) return !1;
                    return r.some((e) => String(e.id).endsWith(`/${t}`));
                } catch (e) {
                    return !1;
                }
            }
            function m(e) {
                return document.querySelectorAll(
                    `.__impage-component-actions-proxy > div > [data-module-id="${e}"], .__impage-component-actions-proxy > [data-module-id="${e}"]`,
                ).length;
            }
            function y(e) {
                try {
                    let t = null == e ? void 0 : e.editorSettingData,
                        n = JSON.parse(t);
                    return new Date(
                        (null == n ? void 0 : n.activityDate[0]) * 1e3,
                    );
                } catch (n) {
                    try {
                        var t;
                        return new Date(
                            (null == e
                                ? void 0
                                : null === (t = e.activityBasicInfo) ||
                                    void 0 === t
                                  ? void 0
                                  : t.activityBeginTime) * 1e3,
                        );
                    } catch (e) {
                        return new Date();
                    }
                }
            }
            function v(e) {
                try {
                    let t = null == e ? void 0 : e.editorSettingData,
                        n = JSON.parse(t);
                    return new Date(
                        (null == n ? void 0 : n.activityDate[1]) * 1e3,
                    );
                } catch (t) {
                    try {
                        return new Date(
                            1e3 * e.activityBasicInfo.activityEndTime,
                        );
                    } catch (e) {
                        return new Date();
                    }
                }
            }
            var g =
                (((i = {}).ActivityEnd = "ActivityEnd"),
                (i.Custom = "Custom"),
                i);
            let b = (e, t, n) => {
                    if ("ActivityEnd" === t || !t)
                        return v(null == e ? void 0 : e.global);
                    if (Number(n)) {
                        if (13 === `${n}`.length) return new Date(1 * n);
                        if (10 === `${n}`.length) return new Date(1e3 * n);
                    }
                    return "string" == typeof n
                        ? new Date(n.replace(/-/g, "/"))
                        : new Date();
                },
                _ = [
                    {
                        id: "ar",
                        name: "العربية",
                        conf_name: "阿拉伯语 ar",
                        desc: "",
                    },
                    {
                        id: "de",
                        name: "Deutsch",
                        conf_name: "德语 de",
                        desc: "",
                    },
                    {
                        id: "es",
                        name: "Espa\xf1ol",
                        conf_name: "西班牙语 es",
                        desc: "",
                    },
                    {
                        id: "fa",
                        name: "فارسی",
                        conf_name: "波斯语 fa",
                        desc: "",
                    },
                    {
                        id: "fr",
                        name: "Fran\xe7ais",
                        conf_name: "法语 fr",
                        desc: "",
                    },
                    {
                        id: "id",
                        name: "Bahasa Indonesia",
                        conf_name: "印度尼西亚语 id",
                        desc: "",
                    },
                    {
                        id: "it",
                        name: "Italiano",
                        conf_name: "意大利语 it",
                        desc: "",
                    },
                    {
                        id: "ja",
                        name: "日本語",
                        conf_name: "日语 ja",
                        desc: "",
                    },
                    {
                        id: "ko",
                        name: "한국어",
                        conf_name: "韩语 ko",
                        desc: "",
                    },
                    {
                        id: "my",
                        name: "Melayu",
                        conf_name: "马来语 my",
                        desc: "",
                    },
                    {
                        id: "pt",
                        name: "Portugu\xeas",
                        conf_name: "葡萄牙语 pt",
                        desc: "",
                    },
                    {
                        id: "pt-br",
                        name: "Portugu\xeas do Brasil",
                        conf_name: "巴西葡语 pt-br",
                        desc: "",
                    },
                    {
                        id: "en",
                        name: "English",
                        conf_name: "英语 en",
                        desc: "",
                    },
                    {
                        id: "ru",
                        name: "Русский",
                        conf_name: "俄语 ru",
                        desc: "",
                    },
                    { id: "th", name: "ไทย", conf_name: "泰语 th", desc: "" },
                    {
                        id: "tr",
                        name: "T\xfcrk\xe7e",
                        conf_name: "土耳其语 tr",
                        desc: "",
                    },
                    {
                        id: "vi",
                        name: "Tiếng Việt",
                        conf_name: "越南语 vi",
                        desc: "",
                    },
                    {
                        id: "zh-Hans",
                        name: "简体中文",
                        conf_name: "简体中文 zh-Hans",
                        desc: "",
                    },
                    {
                        id: "zh-Hant",
                        name: "繁體中文",
                        conf_name: "繁体中文 zh-Hant",
                        desc: "",
                    },
                ],
                h = new Map(_.map((e) => [e.id, e]));
            function w(e) {
                let t = (e) =>
                    e
                        .filter(
                            (e) =>
                                ![
                                    "component_id",
                                    "description",
                                    "key_id",
                                ].includes(e),
                        )
                        .filter((e) => 2 === e.split("-")[0].length);
                try {
                    try {
                        e.global.pages[0].data = JSON.parse(
                            e.global.pages[0].data,
                        );
                    } catch (e) {}
                    return t(
                        e.global.pages[0].data.components[0].data.dataConf
                            .i18nData.headers,
                    );
                } catch (e) {}
                try {
                    var n, r, i, o, a, l, u, s, c, d;
                    let { headers: e = [] } =
                        (null === (d = window) || void 0 === d
                            ? void 0
                            : null === (c = d.__initPage) || void 0 === c
                              ? void 0
                              : null === (s = c[2]) || void 0 === s
                                ? void 0
                                : null === (u = s.pages) || void 0 === u
                                  ? void 0
                                  : null === (l = u[0]) || void 0 === l
                                    ? void 0
                                    : null === (a = l.data) || void 0 === a
                                      ? void 0
                                      : null === (o = a.components) ||
                                          void 0 === o
                                        ? void 0
                                        : null === (i = o[0]) || void 0 === i
                                          ? void 0
                                          : null === (r = i.data) ||
                                              void 0 === r
                                            ? void 0
                                            : null === (n = r.dataConf) ||
                                                void 0 === n
                                              ? void 0
                                              : n.i18nData) || {};
                    if (0 === e.length) return ["en"];
                    return t(e);
                } catch (e) {
                    return ["en"];
                }
            }
            function O(e, t) {
                ((l.__pagedoo_helper = l.__pagedoo_helper || {}),
                    (l.__pagedoo_helper[e] = t));
            }
            function P(e) {
                return l.__pagedoo_helper[e];
            }
            if (
                ((0, o.jS)("silentIframe") &&
                    setInterval(() => {
                        for (let e of Array.from(
                            document.getElementsByTagName("iframe"),
                        )) {
                            let t = e.contentWindow;
                            if (!t) continue;
                            let n = () => {};
                            ((t.console.log = n),
                                (t.console.warn = n),
                                (t.console.debug = n),
                                (t.console.error = n),
                                (t.console.group = n),
                                (t.console.groupEnd = n));
                        }
                    }, 100),
                (l.__pagedoo_helper = l.__pagedoo_helper || {}),
                (l.__pagedoo_helper.getSchema = u),
                (l.__pagedoo_helper.getRules = c),
                (l.__pagedoo_helper.getVersion = d),
                location.pathname.startsWith("/preview.html") &&
                    (0, o.jS)("hot"))
            ) {
                let e;
                ((e = ""),
                    (async () => {
                        for (;;) {
                            try {
                                ((e = (
                                    await fetch(
                                        `/__ping_gems_dev?msg=${encodeURIComponent(e)}`,
                                        {},
                                    ).then((e) => e.json())
                                ).msg),
                                    "reload" === e &&
                                        setTimeout(() => {
                                            location.reload();
                                        }, 500));
                            } catch (t) {
                                (console.error(t), (e = "disconnect"));
                            }
                            await (0, a._v)(1e3);
                        }
                    })());
            }
        },
        32937: function (e, t, n) {
            "use strict";
            n.d(t, {
                D: function () {
                    return r;
                },
                y: function () {
                    return i;
                },
            });
            let r = (e) => new Promise((t) => setTimeout(t, e)),
                i = (e, t) => {
                    let n = (null == t ? void 0 : t.retryUntil) || (() => !0),
                        i = (null == t ? void 0 : t.interval) || 500,
                        o =
                            (null == t ? void 0 : t.backOffStrategy) ||
                            "exponential",
                        a = (e) => {
                            if (0 === e) return i;
                            if ("linear" === o) return e + i;
                            if ("exponential" === o) return 2 * e;
                            throw Error(`Invalid backOffStrategy: ${o}`);
                        },
                        l = async (t) => {
                            let i;
                            await r(t);
                            let o = !1;
                            try {
                                ((i = await e()), (o = await n(i)));
                            } catch (e) {
                                console.log(
                                    "Request failed, continue polling...",
                                    e,
                                );
                            }
                            return o ? i : l(a(t));
                        };
                    return l(0);
                };
        },
        38905: function (e, t, n) {
            "use strict";
            n.d(t, {
                s: function () {
                    return s;
                },
            });
            var r = n("616"),
                i = n.n(r),
                o = n("22638");
            let a = () => {
                    let e = () =>
                            parseFloat(
                                window.getComputedStyle(
                                    document.documentElement,
                                ).fontSize,
                            ),
                        [t, n] = (0, r.useState)(e);
                    return (
                        (0, r.useEffect)(() => {
                            let t = () => {
                                requestAnimationFrame(() => n(e()));
                            };
                            return (
                                window.addEventListener("resize", t),
                                () => window.removeEventListener("resize", t)
                            );
                        }, []),
                        t
                    );
                },
                l = (e, t) => {
                    if (!e) return 0;
                    if (e.endsWith("%")) return 0.075 * parseFloat(e);
                    if (e.endsWith("rem")) return parseFloat(e);
                    if (e.endsWith("px")) return parseFloat(e) / t;
                    throw Error("unknown width unit");
                },
                u = (0, r.forwardRef)((e, t) => {
                    var n, u;
                    let {
                            p: s,
                            children: c,
                            width: d,
                            height: p,
                            autoHeight: f,
                        } = e,
                        m = (function (e, t) {
                            if (null == e) return {};
                            var n,
                                r,
                                i = (function (e, t) {
                                    if (null == e) return {};
                                    var n,
                                        r,
                                        i = {},
                                        o = Object.keys(e);
                                    for (r = 0; r < o.length; r++)
                                        ((n = o[r]),
                                            !(t.indexOf(n) >= 0) &&
                                                (i[n] = e[n]));
                                    return i;
                                })(e, t);
                            if (Object.getOwnPropertySymbols) {
                                var o = Object.getOwnPropertySymbols(e);
                                for (r = 0; r < o.length; r++) {
                                    if (((n = o[r]), !(t.indexOf(n) >= 0)))
                                        Object.prototype.propertyIsEnumerable.call(
                                            e,
                                            n,
                                        ) && (i[n] = e[n]);
                                }
                            }
                            return i;
                        })(e, [
                            "p",
                            "children",
                            "width",
                            "height",
                            "autoHeight",
                        ]),
                        [y, v] = (0, r.useState)(null),
                        [g, b] = (0, r.useState)(null),
                        _ = a(),
                        h = (0, r.useMemo)(
                            () => l(s.commonStyle.width, _),
                            [s.commonStyle.width, _],
                        );
                    (0, r.useImperativeHandle)(t, () => y, [y]);
                    let w = (0, o.Z)(async () => {
                        if (!g || !y) return;
                        let e = await g.getBoundingClientRect();
                        y.style.height = `${e.height / _}rem`;
                    });
                    return (
                        (0, r.useLayoutEffect)(() => {
                            if (!y || !g) return;
                            let e = h / parseFloat(d);
                            ((y.style.position = "relative"),
                                (y.style.width = `${parseFloat(d) * e}rem`),
                                (g.style.position = "absolute"),
                                (g.style.transform = `scale(${e})`),
                                (g.style.transformOrigin = "0 0"),
                                p
                                    ? (y.style.height = `${parseFloat(p) * e}rem`)
                                    : w());
                        }, [y, g, d, h]),
                        (0, r.useLayoutEffect)(() => {
                            if (!g || !f) return;
                            if ("undefined" != typeof ResizeObserver) {
                                let e = new ResizeObserver(w);
                                return (e.observe(g), () => e.disconnect());
                            }
                            (setTimeout(w, 100),
                                setTimeout(w, 200),
                                setTimeout(w, 500));
                            let e = setInterval(w, 1e3);
                            return () => clearInterval(e);
                        }, [g, f, w]),
                        (0, r.useEffect)(() => {
                            var e;
                            (null == g
                                ? void 0
                                : null === (e = g.parentElement) || void 0 === e
                                  ? void 0
                                  : e.parentElement) &&
                                g.parentElement.parentElement.setAttribute(
                                    "dir",
                                    "ltr",
                                );
                        }, [g]),
                        i().createElement(
                            "div",
                            ((n = (function (e) {
                                for (var t = 1; t < arguments.length; t++) {
                                    var n =
                                            null != arguments[t]
                                                ? arguments[t]
                                                : {},
                                        r = Object.keys(n);
                                    ("function" ==
                                        typeof Object.getOwnPropertySymbols &&
                                        (r = r.concat(
                                            Object.getOwnPropertySymbols(
                                                n,
                                            ).filter(function (e) {
                                                return Object.getOwnPropertyDescriptor(
                                                    n,
                                                    e,
                                                ).enumerable;
                                            }),
                                        )),
                                        r.forEach(function (t) {
                                            var r, i, o;
                                            ((r = e),
                                                (i = t),
                                                (o = n[t]),
                                                i in r
                                                    ? Object.defineProperty(
                                                          r,
                                                          i,
                                                          {
                                                              value: o,
                                                              enumerable: !0,
                                                              configurable: !0,
                                                              writable: !0,
                                                          },
                                                      )
                                                    : (r[i] = o));
                                        }));
                                }
                                return e;
                            })({}, m)),
                            (u = ((u = { ref: v }), u)),
                            Object.getOwnPropertyDescriptors
                                ? Object.defineProperties(
                                      n,
                                      Object.getOwnPropertyDescriptors(u),
                                  )
                                : (function (e, t) {
                                      var n = Object.keys(e);
                                      if (Object.getOwnPropertySymbols) {
                                          var r =
                                              Object.getOwnPropertySymbols(e);
                                          n.push.apply(n, r);
                                      }
                                      return n;
                                  })(Object(u)).forEach(function (e) {
                                      Object.defineProperty(
                                          n,
                                          e,
                                          Object.getOwnPropertyDescriptor(u, e),
                                      );
                                  }),
                            n),
                            i().createElement(
                                "div",
                                {
                                    dir:
                                        document.body.getAttribute("dir") ||
                                        "ltr",
                                    ref: b,
                                    style: { width: d, height: p },
                                },
                                c,
                            ),
                        )
                    );
                }),
                s = (e) =>
                    function (t) {
                        var n, r;
                        return i().createElement(
                            u,
                            {
                                "data-module-id": t.props["data-module-id"],
                                width:
                                    null === (n = t.props.style) || void 0 === n
                                        ? void 0
                                        : n.width,
                                p: e,
                                height:
                                    null === (r = t.props.style) || void 0 === r
                                        ? void 0
                                        : r.height,
                                autoHeight: !0,
                            },
                            t,
                        );
                    };
        },
        67398: function (e, t, n) {
            "use strict";
            (n.d(t, {
                B: function () {
                    return U;
                },
            }),
                n("10189"));
            var r,
                i,
                o,
                a,
                l = n("65317"),
                u = n("616"),
                s = n("21635"),
                c = n("61230"),
                d = n("13783"),
                p = n.n(d),
                f = n("55974"),
                m = n("48620");
            function y() {
                let e = (0, l.xn)("encodeparam", location.href).split("#")[0];
                return location.pathname.endsWith("preview.html") &&
                    !(0, l.fQ)((0, f.default)("enableAegis"))
                    ? "https://midasbuy.local/preview.html"
                    : location.pathname.endsWith("/pagedoo-s/one")
                      ? `${location.origin}${location.pathname}/${(0, f.default)("s")}`
                      : location.pathname.endsWith("pc/index.html")
                        ? e.replace("pc/index.html", "*/index.html")
                        : location.pathname.endsWith("mobile/index.html")
                          ? e.replace("mobile/index.html", "*/index.html")
                          : e;
            }
            if (!window.aegis) {
                window.aegis = new (p())({
                    id: "SDK-b3bd5765f52e0790495e",
                    hostUrl: {
                        url: "https://sg.galileotelemetry.tencent.com/collect",
                    },
                    uid: l.pR.get("midasbuyDeviceId"),
                    env: location.pathname.endsWith("preview.html")
                        ? p().environment.LOCAL
                        : location.hostname.includes("sandbox") ||
                            location.hostname.includes("admin")
                          ? p().environment.TEST
                          : p().environment.PROD,
                    urlHandler: y,
                    plugin: {
                        apiSpeed: !0,
                        assetSpeed: !0,
                        device: !0,
                        close: !0,
                        aid: !0,
                        fId: !1,
                        ie: !1,
                        pv: !0,
                        spa: !0,
                        error: !0,
                        webVitals: !0,
                        session: !0,
                        pagePerformance: { urlHandler: y },
                        api: {
                            apiDetail: !0,
                            injectTraceHeader: "traceparent",
                            injectTraceUrls: [/midasbuy.com/],
                            injectTraceIgnoreUrls: [
                                /playapi.midasbuy.com/,
                                /cdn.midasbuy.com/,
                            ],
                            resourceTypeHandler(e) {
                                if (
                                    null == e
                                        ? void 0
                                        : e.includes("log_data.fcg")
                                )
                                    return "fetch";
                            },
                            retCodeHandler(e, t) {
                                try {
                                    e = JSON.parse(e);
                                } catch (e) {}
                                return (null == t
                                    ? void 0
                                    : t.includes("/api/CallMpgo")) ||
                                    (null == t
                                        ? void 0
                                        : t.includes("/api/CommonCallMpgo"))
                                    ? {
                                          isErr: "0" != `${e.result_code}`,
                                          code: e.result_code,
                                      }
                                    : (
                                            null == t
                                                ? void 0
                                                : t.includes(
                                                      "/apps/activity/api",
                                                  )
                                        )
                                      ? {
                                            isErr: "0" != `${e.ret}`,
                                            code: e.code,
                                        }
                                      : void 0;
                            },
                        },
                    },
                    onBeforeSend: (e) =>
                        e.filter(
                            (e) =>
                                !e.url ||
                                (!(
                                    e.url.includes("/api/pagereport") ||
                                    e.url.includes("log_data.fcg")
                                ) &&
                                    !0),
                        ),
                    extField: {
                        ext1: (
                            null === (a = window) || void 0 === a
                                ? void 0
                                : null === (o = a.__initPage) || void 0 === o
                                  ? void 0
                                  : null === (i = o[2]) || void 0 === i
                                    ? void 0
                                    : null === (r = i.appInfo) || void 0 === r
                                      ? void 0
                                      : r.payOfferId
                        )
                            ? window.__initPage[2].appInfo.payOfferId
                            : (0, f.default)("appid"),
                        ext2: (0, m.V)(),
                        ext3: (0, f.default)("from"),
                    },
                });
            }
            let { aegis: v } = window;
            var g = n("78181"),
                b = n("89879"),
                _ = n("74740"),
                h = n("17078"),
                w = n("14603"),
                O = n("49567"),
                P = n("16520"),
                j = n("33086"),
                S = n("99744"),
                I = n("25808"),
                E = n("14831"),
                k = n("75889");
            function D(e) {
                for (var t = 1; t < arguments.length; t++) {
                    var n = null != arguments[t] ? arguments[t] : {},
                        r = Object.keys(n);
                    ("function" == typeof Object.getOwnPropertySymbols &&
                        (r = r.concat(
                            Object.getOwnPropertySymbols(n).filter(
                                function (e) {
                                    return Object.getOwnPropertyDescriptor(n, e)
                                        .enumerable;
                                },
                            ),
                        )),
                        r.forEach(function (t) {
                            var r, i, o;
                            ((r = e),
                                (i = t),
                                (o = n[t]),
                                i in r
                                    ? Object.defineProperty(r, i, {
                                          value: o,
                                          enumerable: !0,
                                          configurable: !0,
                                          writable: !0,
                                      })
                                    : (r[i] = o));
                        }));
                }
                return e;
            }
            function C(e, t) {
                return (
                    (t = null != t ? t : {}),
                    Object.getOwnPropertyDescriptors
                        ? Object.defineProperties(
                              e,
                              Object.getOwnPropertyDescriptors(t),
                          )
                        : (function (e, t) {
                              var n = Object.keys(e);
                              if (Object.getOwnPropertySymbols) {
                                  var r = Object.getOwnPropertySymbols(e);
                                  n.push.apply(n, r);
                              }
                              return n;
                          })(Object(t)).forEach(function (n) {
                              Object.defineProperty(
                                  e,
                                  n,
                                  Object.getOwnPropertyDescriptor(t, n),
                              );
                          }),
                    e
                );
            }
            (0, u.createContext)(void 0);
            let T = window;
            T.__gems_custom_has_initialized = !1;
            let B = function (e) {
                let t = e;
                try {
                    t = decodeURIComponent(e);
                } catch (e) {}
                return t.replace(/>/g, "&gt;");
            };
            function A(e) {
                let t = `${e.split("midasweb")[0]}midasweb`;
                try {
                    let e =
                            (function () {
                                try {
                                    if ("string" != typeof document.referrer)
                                        return "";
                                    let e = new URL(document.referrer);
                                    if (!e.hostname.endsWith(".midasbuy.com"))
                                        return "";
                                    return e.pathname.split("/")[0];
                                } catch (e) {
                                    return "";
                                }
                            })() || "midasbuy",
                        n = (0, l.jS)("from") || "";
                    return [t, e, n].filter(Boolean).join("-");
                } catch (e) {
                    return t;
                }
            }
            let U = (e, t) => {
                let { metadata: n, setMetadata: r } = (function (e) {
                        let t = (0, S.R)(j.e.METADATA),
                            n = (0, S.H)(j.e.METADATA),
                            r = (0, P.vZ)(e, t, n),
                            [i, o] = (0, P.Dr)(r);
                        return { metadata: i, setMetadata: o };
                    })(e),
                    { setVerifiedUser: i } = (0, k.ZP)(e),
                    { simulateData: o } = (0, E.ZP)(e),
                    a = (0, I.Z)((e) => e.setIsPageVisible),
                    { messenger: d } = (0, O.ZP)(e),
                    { runAsync: p } = (0, c.Q)(
                        () =>
                            (0, h.oJ)().then(() =>
                                g.RV.getEventMetadata({
                                    appid: t,
                                    country: (
                                        (0, m.V)() ||
                                        (null == o ? void 0 : o.country) ||
                                        ""
                                    ).toUpperCase(),
                                    from: (0, l.jS)("from") || "",
                                }),
                            ),
                        {
                            cacheKey:
                                "gems:useRequest:activityCgi.getEventMetadata",
                            manual: !0,
                        },
                    );
                return (
                    (0, u.useEffect)(() => {
                        if (window === top || !d) {
                            a(!0);
                            return;
                        }
                        a(!1);
                        let e = (e) => {
                            ("show" === e && a(!0), "hide" === e && a(!1));
                        };
                        return (
                            d.on("report", e),
                            () => {
                                d.off("report", e);
                            }
                        );
                    }, [d, a]),
                    (0, u.useEffect)(() => {
                        if (!T.__gems_custom_has_initialized && !!o)
                            ((T.__gems_custom_has_initialized = !0),
                                (window.__gems_store = e),
                                (window.__gems_eventBusUtil = _.H1),
                                i({ state: "INITIAL" }),
                                v.reportEvent("before:metadata"),
                                p().then(async (e) => {
                                    var t, n, o;
                                    if (
                                        (v.reportEvent("after:metadata"),
                                        (null === (t = e.userData) ||
                                        void 0 === t
                                            ? void 0
                                            : t.token) &&
                                            (s.$.set(
                                                "userToken",
                                                null === (n = e.userData) ||
                                                    void 0 === n
                                                    ? void 0
                                                    : n.token,
                                            ),
                                            i((t) => {
                                                var n;
                                                return {
                                                    state:
                                                        (null == t
                                                            ? void 0
                                                            : t.state) ||
                                                        "INITIAL",
                                                    user: C(
                                                        D(
                                                            {},
                                                            null == t
                                                                ? void 0
                                                                : t.user,
                                                        ),
                                                        {
                                                            token:
                                                                null ===
                                                                    (n =
                                                                        e.userData) ||
                                                                void 0 === n
                                                                    ? void 0
                                                                    : n.token,
                                                        },
                                                    ),
                                                };
                                            })),
                                        r(e),
                                        document.body.setAttribute(
                                            "data-country",
                                            e.payInfo.country || "",
                                        ),
                                        e.userData)
                                    ) {
                                        (e.userData.currentBindUser &&
                                            ((e.userData.currentBindUser.charac_name =
                                                B(
                                                    e.userData.currentBindUser
                                                        .charac_name,
                                                )),
                                            "string" ==
                                                typeof e.userData
                                                    .currentBindUser.pf &&
                                                (e.userData.currentBindUser.pf =
                                                    A(
                                                        e.userData
                                                            .currentBindUser.pf,
                                                    )),
                                            "string" == typeof e.payInfo.pf &&
                                                (e.payInfo.pf = A(
                                                    e.payInfo.pf,
                                                ))),
                                            b.yi &&
                                                ((null == e
                                                    ? void 0
                                                    : e.userData) &&
                                                    (0, l.jS)("muid") &&
                                                    (e.userData.uid = (0, l.jS)(
                                                        "muid",
                                                    )),
                                                (null == e
                                                    ? void 0
                                                    : null ===
                                                            (o = e.userData) ||
                                                        void 0 === o
                                                      ? void 0
                                                      : o.currentBindUser) &&
                                                    (0, l.jS)("openid") &&
                                                    (e.userData.currentBindUser.openid =
                                                        (0, l.jS)("openid"))));
                                        let t = await (0, w.Wt)(
                                            "base_midasbuy_embed",
                                        );
                                        i((n) => {
                                            if (window.parent !== window && t) {
                                                var r;
                                                return {
                                                    state:
                                                        (null == n
                                                            ? void 0
                                                            : n.state) ||
                                                        "INITIAL",
                                                    user: C(
                                                        D(
                                                            {},
                                                            null == n
                                                                ? void 0
                                                                : n.user,
                                                        ),
                                                        {
                                                            token:
                                                                null ===
                                                                    (r =
                                                                        e.userData) ||
                                                                void 0 === r
                                                                    ? void 0
                                                                    : r.token,
                                                        },
                                                    ),
                                                };
                                            }
                                            return {
                                                user: e.userData,
                                                state: (0, k.V_)(e.userData),
                                            };
                                        });
                                    }
                                }));
                    }, [t, p, r, i, e, o]),
                    { metadata: n }
                );
            };
        },
        25997: function (e, t, n) {
            "use strict";
            let r;
            n.d(t, {
                D: function () {
                    return l;
                },
                w: function () {
                    return a;
                },
            });
            var i = n(84624);
            let o = window;
            function a(e) {
                let t = JSON.stringify({ INTLMethod: e });
                (0, i.gn)()
                    ? "function" == typeof r && r("INTLCallNative", t, null)
                    : (0, i.Ro)()
                      ? window.tbs_external.nativeCall(e, [t])
                      : t.includes("nativeCallJS")
                        ? alert(t)
                        : prompt(t);
            }
            function l() {
                return window.navigator.userAgent.includes("INTLBrowser");
            }
            l() &&
                !(function (e) {
                    if (o.WebViewJavascriptBridge)
                        return e(o.WebViewJavascriptBridge);
                    if (o.WVJBCallbacks) return o.WVJBCallbacks.push(e);
                    o.WVJBCallbacks = [e];
                    let t = document.createElement("iframe");
                    ((t.style.display = "none"),
                        (t.src = "https://__bridge_loaded__"),
                        document.documentElement.appendChild(t),
                        setTimeout(function () {
                            document.documentElement.removeChild(t);
                        }, 0));
                })(function (e) {
                    e &&
                        "object" == typeof e &&
                        "callHandler" in e &&
                        (r = e.callHandler);
                });
        },
        36424: function (e, t, n) {
            "use strict";
            n.d(t, {
                vI: function () {
                    return u;
                },
                x_: function () {
                    return d;
                },
                yA: function () {
                    return c;
                },
            });
            var r = n(65317),
                i = n(72499),
                o = n(17078),
                a = n(25997),
                l = n(55137);
            let u = async () =>
                    window.midasLogin
                        ? window.midasLogin
                        : (await (0, o.D7)(
                              `https://cdn.midasbuy.com/oversea_web/static/js/loginSdk.latest.js?t=${Date.now()}`,
                              "login-sdk",
                          ),
                          new Promise((e) => {
                              let t = () => {
                                  if (window.midasLogin)
                                      return e(window.midasLogin);
                                  setTimeout(t, 100);
                              };
                              t();
                          })),
                s = async () => {
                    if (window.midasLogin) return window.midasLogin;
                    try {
                        let e = await (0, i.w)();
                        return ((window.midasLogin = e), window.midasLogin);
                    } catch (e) {
                        return e;
                    }
                },
                c = async (e) => {
                    await p(e);
                    let { midasLogin: t } = window;
                    if (!t) return;
                    let {
                        appid: n,
                        hash: i = "#login",
                        country: o = "ot",
                        bindAfterLogin: u = 1,
                        noBindAfterLogin: s,
                        activityId: c,
                        hideThirdPartyList: d,
                    } = e;
                    return (
                        t.login({
                            country: o,
                            hash: i,
                            host: location.hostname,
                            pageConfig: {
                                hideThirdPartyList: d,
                                bindAfterLogin: u,
                                noBindAfterLogin: s,
                                appid: n,
                                from: `pagedoo-${c}`,
                                hideThirdParty: (function () {
                                    return (
                                        (0, a.D)() ||
                                        (0, r.fQ)((0, r.jS)("inApp"))
                                    );
                                })()
                                    ? 1
                                    : 0,
                            },
                        }),
                        new Promise((e, n) => {
                            let r = async (t) => {
                                (await (0, l.Zc)(c), e(t));
                            };
                            (t.on("logined", r),
                                t.on("loginSuccess", r),
                                t.on("facebookLoginSuccess", r),
                                t.on("registerSuccess", r),
                                t.on("closeIframe", () => {
                                    setTimeout(() => n(), 1e3);
                                }));
                        })
                    );
                },
                d = (e) => {
                    var t, n, r, i;
                    let o = document.getElementById("login-iframe");
                    if (
                        null == o
                            ? void 0
                            : null === (t = o.getAttribute("src")) ||
                                void 0 === t
                              ? void 0
                              : t.endsWith("#login")
                    )
                        try {
                            (null === (n = o.parentElement) ||
                                void 0 === n ||
                                n.removeChild(o),
                                (window.midasLogin.params.hasInit = !1));
                        } catch (e) {}
                    return c(
                        ((r = (function (e) {
                            for (var t = 1; t < arguments.length; t++) {
                                var n =
                                        null != arguments[t]
                                            ? arguments[t]
                                            : {},
                                    r = Object.keys(n);
                                ("function" ==
                                    typeof Object.getOwnPropertySymbols &&
                                    (r = r.concat(
                                        Object.getOwnPropertySymbols(n).filter(
                                            function (e) {
                                                return Object.getOwnPropertyDescriptor(
                                                    n,
                                                    e,
                                                ).enumerable;
                                            },
                                        ),
                                    )),
                                    r.forEach(function (t) {
                                        var r, i, o;
                                        ((r = e),
                                            (i = t),
                                            (o = n[t]),
                                            i in r
                                                ? Object.defineProperty(r, i, {
                                                      value: o,
                                                      enumerable: !0,
                                                      configurable: !0,
                                                      writable: !0,
                                                  })
                                                : (r[i] = o));
                                    }));
                            }
                            return e;
                        })({}, e)),
                        (i = ((i = { hash: "#bind-openid" }), i)),
                        Object.getOwnPropertyDescriptors
                            ? Object.defineProperties(
                                  r,
                                  Object.getOwnPropertyDescriptors(i),
                              )
                            : (function (e, t) {
                                  var n = Object.keys(e);
                                  if (Object.getOwnPropertySymbols) {
                                      var r = Object.getOwnPropertySymbols(e);
                                      n.push.apply(n, r);
                                  }
                                  return n;
                              })(Object(i)).forEach(function (e) {
                                  Object.defineProperty(
                                      r,
                                      e,
                                      Object.getOwnPropertyDescriptor(i, e),
                                  );
                              }),
                        r),
                    );
                },
                p = async ({
                    appid: e,
                    hash: t = "#login",
                    country: n = "ot",
                    bindAfterLogin: r = 1,
                    noBindAfterLogin: i,
                    activityId: o,
                    hideThirdPartyList: a,
                }) => {
                    await s();
                    let { midasLogin: l } = window;
                    l.init({
                        host: location.hostname,
                        country: n,
                        hash: t,
                        pageConfig: {
                            appid: e,
                            bindAfterLogin: r,
                            noBindAfterLogin: i,
                            hideThirdPartyList: a,
                            from: `pagedoo-${o}`,
                        },
                        preload: !0,
                    });
                };
        },
        92724: function (e, t, n) {
            "use strict";
            n.d(t, {
                Bh: function () {
                    return D;
                },
                qF: function () {
                    return E;
                },
                a8: function () {
                    return $;
                },
                zS: function () {
                    return L;
                },
                LH: function () {
                    return T;
                },
            });
            var r = n("65317"),
                i = n("80430"),
                o = n("99560"),
                a = n.n(o),
                l = n("52153"),
                u = n.n(l),
                s = n("48620"),
                c = n("53167");
            async function d(e, t) {
                e.emit("baseSelectZone:show", t);
            }
            var p = n("75889"),
                f = n("78181"),
                m = n("63821"),
                y = n("17078"),
                v = n("75937"),
                g = n("32937"),
                b = n("98818"),
                _ = n("25997");
            let h = {
                0x5705d605: {
                    env: "aws-na",
                    needRoleId: !0,
                    inAppSigKey: "1311fcd5dd2326a37a1ad2a9124e7f87",
                    inAppSource: 18,
                    userOpenidCustomKey: "toweroffantasy-openid",
                    userType: "toweroffantasy",
                    lipassGameID: 29093,
                    lipassAppID: "a0ca7921668f7d18c096ad85011589fd",
                    lipassSocialMedia: [
                        "facebook",
                        "line",
                        "twitter",
                        "google",
                        "apple",
                    ],
                },
                0x5705d61d: {
                    env: "aws-na",
                    needRoleId: !1,
                    inAppSigKey: "",
                    inAppSource: -1,
                    userOpenidCustomKey: "game-lipass-29080-openid",
                    userType: "game-lipass",
                    lipassGameID: 29080,
                    lipassAppID: "09af79d65d6e4fdf2d2569f0d365739d",
                    lipassSocialMedia: [
                        "facebook",
                        "line",
                        "twitter",
                        "google",
                        "apple",
                    ],
                },
                0x5705d61e: {
                    env: "sg",
                    needRoleId: !1,
                    inAppSigKey: "",
                    inAppSource: -1,
                    userOpenidCustomKey: "game-lipass-29157-openid",
                    userType: "game-lipass",
                    lipassGameID: 29157,
                    lipassAppID: "153011f55ca99902901dbea68fc00cb0",
                    lipassSocialMedia: [
                        "facebook",
                        "line",
                        "twitter",
                        "google",
                        "apple",
                    ],
                },
            };
            var w = n("36424");
            function O(e) {
                for (var t = 1; t < arguments.length; t++) {
                    var n = null != arguments[t] ? arguments[t] : {},
                        r = Object.keys(n);
                    ("function" == typeof Object.getOwnPropertySymbols &&
                        (r = r.concat(
                            Object.getOwnPropertySymbols(n).filter(
                                function (e) {
                                    return Object.getOwnPropertyDescriptor(n, e)
                                        .enumerable;
                                },
                            ),
                        )),
                        r.forEach(function (t) {
                            var r, i, o;
                            ((r = e),
                                (i = t),
                                (o = n[t]),
                                i in r
                                    ? Object.defineProperty(r, i, {
                                          value: o,
                                          enumerable: !0,
                                          configurable: !0,
                                          writable: !0,
                                      })
                                    : (r[i] = o));
                        }));
                }
                return e;
            }
            function P(e, t) {
                return (
                    (t = null != t ? t : {}),
                    Object.getOwnPropertyDescriptors
                        ? Object.defineProperties(
                              e,
                              Object.getOwnPropertyDescriptors(t),
                          )
                        : (function (e, t) {
                              var n = Object.keys(e);
                              if (Object.getOwnPropertySymbols) {
                                  var r = Object.getOwnPropertySymbols(e);
                                  n.push.apply(n, r);
                              }
                              return n;
                          })(Object(t)).forEach(function (n) {
                              Object.defineProperty(
                                  e,
                                  n,
                                  Object.getOwnPropertyDescriptor(t, n),
                              );
                          }),
                    e
                );
            }
            let j = () => {
                    let e = "correctLipassLoginToastStyle",
                        t = document.getElementById(e);
                    if (!t) {
                        let n =
                            document.getElementById("root") ||
                            document.getElementById("app");
                        (((t = document.createElement("style")).id = e),
                            (t.innerHTML =
                                ".ant-message {z-index: 10010 !important;}"),
                            document.body.insertBefore(t, n));
                    }
                },
                S = location.host.includes("sandbox")
                    ? {
                          secretKey: "9ch8L1CpTRZgi6W0ym9Yvuz53c48QRVj",
                          appid: "332651",
                      }
                    : {
                          secretKey: "WwwaKu5kbLeEHYvUO8C71ObfsBpP6ypf",
                          appid: "123123",
                      };
            async function I() {
                try {
                    let e = Math.floor(Date.now() / 1e3),
                        {
                            gameid: t,
                            channelid: n,
                            sdk_version: o = "",
                            os: l = "1",
                            seq: u = Math.random().toString(36).slice(2),
                            encodeparam: s,
                        } = (0, r.Qf)();
                    if (!t || !n || !s) return null;
                    let c = [e, s, "1311fcd5dd2326a37a1ad2a9124e7f87"].join(""),
                        d = a()(c),
                        p = (0, b.a3)(
                            P(
                                O(
                                    {},
                                    {
                                        gameid: t,
                                        channelid: n,
                                        os: l,
                                        source: "18",
                                        ts: e,
                                        sdk_version: o,
                                        seq: u,
                                        encodeparam: s,
                                    },
                                ),
                                { sig: d },
                            ),
                            "https://aws-na.intlgame.com/v2/auth/decrypt_aes",
                        ),
                        { data: f } = await i.Z.post(p);
                    return {
                        openid: (0, r.jS)("openid", f),
                        token: (0, r.jS)("token", f),
                        gameId: t,
                        channelId: n,
                    };
                } catch (e) {
                    return null;
                }
            }
            async function E() {
                (await (0, w.vI)(),
                    await Promise.race([
                        new Promise((e) => {
                            var t, n;
                            null === (n = window) ||
                                void 0 === n ||
                                null === (t = n.midasLogin) ||
                                void 0 === t ||
                                t.on("initLoginSuccess", e);
                        }),
                        (0, g.D)(2e3),
                    ]));
            }
            let k = "HIDE_ZONE_SELECT";
            async function D(e, t, n) {
                return new Promise((n, r) => {
                    if (!!t)
                        (d(t, e),
                            t.on("baseSelectZone:success", (t) => {
                                var r;
                                n(
                                    P(O({}, e.user), {
                                        currentBindUser: O(
                                            {},
                                            null === (r = e.user) ||
                                                void 0 === r
                                                ? void 0
                                                : r.currentBindUser,
                                            t,
                                        ),
                                    }),
                                );
                            }),
                            t.on("baseSelectZone:close", () => {
                                r(Error(k));
                            }));
                }).then(async (e) => {
                    var t;
                    let { zoneName: r } = await L(
                        `${null == e ? void 0 : null === (t = e.currentBindUser) || void 0 === t ? void 0 : t.zoneid}`,
                        n,
                    );
                    return P(O({}, e), {
                        currentBindUser: P(
                            O({}, null == e ? void 0 : e.currentBindUser),
                            { zoneName: r },
                        ),
                    });
                });
            }
            let C = async ({
                    openid: e,
                    token: t,
                    gameId: n,
                    channelId: r,
                }) => {
                    var i;
                    let o = await (null === (i = window.midasLogin) ||
                    void 0 === i
                        ? void 0
                        : i.createMidasbuyUser({
                              openid: e,
                              token: t,
                              gameId: n,
                              channelId: r,
                              browser_info: "",
                              rc_extra: "",
                              csrftoken: "",
                              keyVersion: "",
                          }));
                    if (0 === o.ret) return o.data;
                    throw o;
                },
                T = (e) => {
                    var t;
                    return (
                        "string" ==
                        typeof (null == e
                            ? void 0
                            : null === (t = e.other) || void 0 === t
                              ? void 0
                              : t["toweroffantasy-openid"])
                    );
                },
                B = (e, t) => {
                    var n, r;
                    return (
                        (!!(0, p.E_)(
                            null == e
                                ? void 0
                                : null === (n = e.currentBindUser) ||
                                    void 0 === n
                                  ? void 0
                                  : n.verifytype,
                        ) &&
                            ((null == e
                                ? !!void 0
                                : null === (r = e.currentBindUser) ||
                                    void 0 === r
                                  ? !!void 0
                                  : !!r.roleId) ||
                                !t.needRoleId)) ||
                        !1
                    );
                };
            async function A(e, t, n) {
                try {
                    let { appid: i, country: o, language: a, pf: l } = e,
                        u = h[i];
                    if (t) {
                        var r;
                        let s = await C(t);
                        if (!s) return null;
                        let c = {
                            ErrorCode: s.ErrorCode,
                            appid: i,
                            avatarUrl: "",
                            country: o,
                            email: s.email,
                            other: s.other,
                            providerType: s.providerType,
                            uid: s.uid,
                            language: a,
                            token: s.token,
                        };
                        if (
                            null == s
                                ? void 0
                                : null === (r = s.other) || void 0 === r
                                  ? void 0
                                  : r[u.userOpenidCustomKey]
                        )
                            try {
                                return await D(
                                    {
                                        appid: i,
                                        country: o,
                                        openid: s.other[u.userOpenidCustomKey],
                                        pf: l,
                                        user: s,
                                    },
                                    n,
                                    e,
                                );
                            } catch (e) {
                                if ((null == e ? void 0 : e.message) === k)
                                    return c;
                            }
                    }
                    return null;
                } catch (e) {
                    return (console.error("getInAppUserData", e), null);
                }
            }
            let U = async (e, t, n) => {
                    var r;
                    let i = h[t],
                        o =
                            null === (r = window.GameBindPopConfig) ||
                            void 0 === r
                                ? void 0
                                : r.bindTipsPop;
                    return (
                        o &&
                            (await new Promise((t) => {
                                (0, c.BC)(e, {
                                    title: o.title,
                                    content: o.content,
                                    primaryButtonText: o.buttonText,
                                    disableCloseButton: !0,
                                    onClickPrimaryButton: () => {
                                        (null == n ||
                                            n.emit("ItemClick", {
                                                module_id: "",
                                                components_id:
                                                    "game_login_prompt_close",
                                            }),
                                            t());
                                    },
                                });
                            })),
                        new Promise(async (t, r) => {
                            j();
                            let o = document.createElement("div"),
                                a = document.createElement("div"),
                                l = document.createElement("div"),
                                s = document.createElement("div"),
                                d = document.createElement("div");
                            ((d.style.position = "fixed"),
                                (d.style.zIndex = "10000"),
                                (d.style.width = "100%"),
                                (d.style.height = "100%"),
                                (d.style.background = "#000"),
                                (d.style.opacity = "0.7"),
                                o.appendChild(d),
                                o.appendChild(a),
                                a.appendChild(l),
                                a.appendChild(s));
                            let p =
                                document.getElementById("root") ||
                                document.getElementById("app");
                            ((l.id = "infinite-pass-component"),
                                l.classList.add("infinite-pass-component"),
                                (a.style.position = "fixed"),
                                (a.style.zIndex = "10000"),
                                (a.style.transformOrigin = "left top"),
                                (a.style.top = "50%"),
                                (a.style.left = "50%"),
                                (a.style.margin = "0px"),
                                (a.style.transform =
                                    "scale(1) translate(-50%, -50%)"),
                                (s.style.position = "absolute"),
                                (s.style.zIndex = "1000"),
                                (s.style.width = "20px"),
                                (s.style.height = "20px"),
                                (s.style.right = "20px"),
                                (s.style.top = "0px"),
                                (s.style.backgroundImage =
                                    "url(https://cdn.midasbuy.com/events/ucGasStation/images/delete_icon.png?imageMogr2/thumbnail/128x128)"),
                                (s.style.backgroundRepeat = "no-repeat"),
                                (s.style.backgroundSize = "100% 100%"),
                                (s.style.marginTop = "20px"),
                                (s.style.cursor = "pointer"),
                                !(0, m.b9)() &&
                                    ((s.style.width = "15px"),
                                    (s.style.height = "15px"),
                                    (s.style.right = "0px"),
                                    (s.style.marginRight = "12px"),
                                    (s.style.marginTop = "12px")),
                                (s.onclick = () => {
                                    (r(),
                                        null == n ||
                                            n.emit("ItemClick", {
                                                module_id: "",
                                                components_id:
                                                    "game_login_close",
                                            }),
                                        p.parentNode.removeChild(o));
                                }),
                                p.parentNode.insertBefore(o, p),
                                await (0, y.Sg)(
                                    "https://common-web.intlgame.com/sdk-cdn/infinite-pass/latest/index.css",
                                ),
                                await (0, y.D7)(
                                    "https://common-web.intlgame.com/sdk-cdn/infinite-pass/latest/index.umd.js",
                                ));
                            let v = {
                                env: i.env,
                                gameID: i.lipassGameID,
                                appID: i.lipassAppID,
                                config: {
                                    langType:
                                        document.body.getAttribute(
                                            "data-lang",
                                        ) || "en",
                                    isMobile: !(0, m.Ro)(),
                                    socialList: (0, _.D)()
                                        ? []
                                        : i.lipassSocialMedia || [
                                              "facebook",
                                              "line",
                                              "twitter",
                                              "google",
                                              "apple",
                                          ],
                                },
                            };
                            new window.PassFactory.Pass(v)
                                .start(".infinite-pass-component")
                                .then((a) => {
                                    if (
                                        (p.parentNode.removeChild(o),
                                        (null == a ? void 0 : a.openid) &&
                                            (null == a ? void 0 : a.token))
                                    ) {
                                        var l, s, d;
                                        let o = {
                                                appid: S.appid || "",
                                                type: i.userType,
                                                game_id: `${i.lipassGameID}`,
                                                game_open_id:
                                                    (null == a
                                                        ? void 0
                                                        : a.openid) || "",
                                                game_token:
                                                    (null == a
                                                        ? void 0
                                                        : a.token) || "",
                                                game_channel_id: (
                                                    null == a
                                                        ? void 0
                                                        : null ===
                                                                (l =
                                                                    a.channel_info) ||
                                                            void 0 === l
                                                          ? void 0
                                                          : l.channelId
                                                )
                                                    ? JSON.stringify(
                                                          null == a
                                                              ? void 0
                                                              : null ===
                                                                      (s =
                                                                          a.channel_info) ||
                                                                  void 0 === s
                                                                ? void 0
                                                                : s.channelId,
                                                      )
                                                    : "",
                                            },
                                            p = {},
                                            m = Math.floor(Date.now() / 1e3);
                                        p.Csrftokentime = m;
                                        let y = `${JSON.stringify(o)}${S.secretKey}${m}`,
                                            v =
                                                null === u() || void 0 === u()
                                                    ? void 0
                                                    : null === (d = u()(y)) ||
                                                        void 0 === d
                                                      ? void 0
                                                      : d.toString();
                                        ((p.Csrftokenv2 = v),
                                            f.RV.gameLink(o, p, S.appid).then(
                                                (i) => {
                                                    var o, a, l, u, s;
                                                    (null == i
                                                        ? void 0
                                                        : null ===
                                                                (o = i.data) ||
                                                            void 0 === o
                                                          ? void 0
                                                          : o.ret) === 0
                                                        ? (t(
                                                              null == i
                                                                  ? void 0
                                                                  : null ===
                                                                          (l =
                                                                              i.data) ||
                                                                      void 0 ===
                                                                          l
                                                                    ? void 0
                                                                    : l.ret,
                                                          ),
                                                          location.reload())
                                                        : (null == i
                                                                ? void 0
                                                                : null ===
                                                                        (a =
                                                                            i.data) ||
                                                                    void 0 === a
                                                                  ? void 0
                                                                  : a.ret) ===
                                                                10041 &&
                                                            window.GameBindPopConfig
                                                          ? (null == n ||
                                                                n.emit(
                                                                    "ItemClick",
                                                                    {
                                                                        module_id:
                                                                            "",
                                                                        components_id:
                                                                            "game_login_already_bind",
                                                                    },
                                                                ),
                                                            (0, c.BC)(e, {
                                                                title: " ",
                                                                content:
                                                                    null ===
                                                                        (u =
                                                                            window.GameBindPopConfig) ||
                                                                    void 0 === u
                                                                        ? void 0
                                                                        : u.alreadyBindText,
                                                            }),
                                                            r(
                                                                Error(
                                                                    "Account has been bound",
                                                                ),
                                                            ))
                                                          : window.GameBindPopConfig &&
                                                            (null == n ||
                                                                n.emit(
                                                                    "ItemClick",
                                                                    {
                                                                        module_id:
                                                                            "",
                                                                        components_id:
                                                                            "game_login_link_error",
                                                                    },
                                                                ),
                                                            (0, c.BC)(e, {
                                                                title:
                                                                    null ===
                                                                        (s =
                                                                            window.GameBindPopConfig) ||
                                                                    void 0 === s
                                                                        ? void 0
                                                                        : s.errLoginText,
                                                            }),
                                                            r(
                                                                Error(
                                                                    "Bind error",
                                                                ),
                                                            ));
                                                },
                                            ));
                                    }
                                });
                        })
                    );
                },
                x = async (e, t, n, i, o, a = !1) => {
                    var l, u, s, c;
                    let d = h[e.appid],
                        p = await I(),
                        f =
                            !p ||
                            p.openid ===
                                (null == n
                                    ? void 0
                                    : null === (l = n.currentBindUser) ||
                                        void 0 === l
                                      ? void 0
                                      : l.openid);
                    if (B(n, d) && f) {
                        let {
                            zoneName: t,
                            areaId: r,
                            platId: i,
                        } = await L(
                            `${null == n ? void 0 : null === (s = n.currentBindUser) || void 0 === s ? void 0 : s.zoneid}`,
                            e,
                        );
                        return {
                            state: "LOGGED_IN",
                            verifiedUser: P(O({}, n), {
                                currentBindUser: P(
                                    O(
                                        {},
                                        null == n ? void 0 : n.currentBindUser,
                                    ),
                                    { zoneName: t, areaId: r, platId: i },
                                ),
                            }),
                        };
                    }
                    let m = await A(e, p, t);
                    if (null == m ? void 0 : m.uid)
                        return ((null == m
                            ? void 0
                            : null === (c = m.currentBindUser) || void 0 === c
                              ? void 0
                              : c.roleId) &&
                            d.needRoleId) ||
                            !d.needRoleId
                            ? { state: "LOGGED_IN", verifiedUser: m }
                            : { state: "NO_ROLE_ID", verifiedUser: m };
                    if (null == p ? void 0 : p.openid)
                        return { state: "NOT_LOGIN", verifiedUser: null };
                    if (!(null == n ? void 0 : n.uid)) {
                        if (a)
                            return { state: "NOT_LOGIN", verifiedUser: null };
                        try {
                            let t = await (0, w.yA)({
                                appid: e.appid,
                                noBindAfterLogin: 1,
                                country: e.country,
                                activityId: o,
                            });
                            if (
                                ((null == t ? void 0 : t.status) === 200 &&
                                    (n = null == t ? void 0 : t.user),
                                B(n, d))
                            )
                                return { state: "LOGGED_IN", verifiedUser: n };
                        } catch (e) {
                            return { state: "NOT_LOGIN", verifiedUser: null };
                        }
                    }
                    if (
                        !(null == n
                            ? void 0
                            : null === (u = n.other) || void 0 === u
                              ? void 0
                              : u[d.userOpenidCustomKey])
                    ) {
                        if (a)
                            return {
                                state: "NOT_BIND",
                                verifiedUser: (0, r.CE)(n, ["currentBindUser"]),
                            };
                        i &&
                            i.emit("ItemClick", {
                                module_id: "",
                                components_id: "game_login_show",
                            });
                        try {
                            (await U(t, e.appid, i),
                                null == i ||
                                    i.emit("ItemClick", {
                                        module_id: "",
                                        components_id: "game_login_success",
                                    }));
                        } finally {
                            return {
                                state: "NOT_BIND",
                                verifiedUser: (0, r.CE)(n, ["currentBindUser"]),
                            };
                        }
                    }
                    return { state: "NO_ROLE_ID", verifiedUser: n };
                },
                $ = async (e, t, n, i, o, a = !1) => {
                    var l, u, c, d, p, m, y, v;
                    let g = h[e.appid],
                        b = await x(e, t, n, i, o, a);
                    if (b.verifiedUser && !b.verifiedUser.token) {
                        let t = await f.RV.getEventMetadata({
                            appid: e.appid,
                            country: ((0, s.V)() || "").toUpperCase(),
                            from: (0, r.jS)("from") || "",
                        });
                        if (
                            ((b.verifiedUser.token =
                                (null == t
                                    ? void 0
                                    : null === (c = t.userData) || void 0 === c
                                      ? void 0
                                      : c.token) || ""),
                            !b.verifiedUser.token && location.reload(),
                            (null == t
                                ? void 0
                                : null === (p = t.userData) || void 0 === p
                                  ? void 0
                                  : null === (d = p.currentBindUser) ||
                                      void 0 === d
                                    ? void 0
                                    : d.roleId) &&
                                (null == b
                                    ? void 0
                                    : null === (m = b.verifiedUser) ||
                                        void 0 === m
                                      ? void 0
                                      : m.currentBindUser))
                        ) {
                            ((b.verifiedUser.currentBindUser.roleId =
                                t.userData.currentBindUser.roleId),
                                (b.state = "LOGGED_IN"));
                            let {
                                zoneName: n,
                                areaId: r,
                                platId: i,
                            } = await L(
                                `${null === (v = b.verifiedUser) || void 0 === v ? void 0 : null === (y = v.currentBindUser) || void 0 === y ? void 0 : y.zoneid}`,
                                e,
                            );
                            ((b.verifiedUser.currentBindUser.zoneName = n),
                                (b.verifiedUser.currentBindUser.areaId = r),
                                (b.verifiedUser.currentBindUser.platId = i));
                        }
                    }
                    if (
                        (null === (u = b.verifiedUser) || void 0 === u
                            ? void 0
                            : null === (l = u.other) || void 0 === l
                              ? void 0
                              : l[g.userOpenidCustomKey]) &&
                        !B(b.verifiedUser, g) &&
                        t
                    )
                        try {
                            let n = await D(
                                {
                                    appid: e.appid,
                                    country: e.country,
                                    openid: b.verifiedUser.other[
                                        g.userOpenidCustomKey
                                    ],
                                    pf: e.pf,
                                    user: b.verifiedUser,
                                },
                                t,
                                e,
                            );
                            return { state: "LOGGED_IN", verifiedUser: n };
                        } catch (e) {
                            if ((null == e ? void 0 : e.message) === k)
                                return {
                                    state: "NO_ROLE_ID",
                                    verifiedUser: b.verifiedUser,
                                };
                        }
                    return b;
                };
            async function L(e, t) {
                try {
                    if (!t) return {};
                    let { needSelectPf: n, country: r } = t,
                        i = {
                            name: "",
                            area_id: "",
                            plat_id: "",
                            regionName: "",
                            zone_id: "",
                            zoneid: "",
                        };
                    if (n) {
                        let t = (0, v.M)(n, r),
                            o = (0, v.s)(t);
                        Object.keys(o).forEach((t) => {
                            Object.keys(o[t]).forEach((n) => {
                                o[t][n].forEach((t) => {
                                    `${e}` == `${t.zoneid}` &&
                                        ((i = t).regionName = n);
                                });
                            });
                        });
                    }
                    return {
                        zoneName: `${null == i ? void 0 : i.name}${(null == i ? void 0 : i.regionName) ? `(${null == i ? void 0 : i.regionName})` : null == i ? void 0 : i.regionName}`,
                        areaId: null == i ? void 0 : i.area_id,
                        platId: null == i ? void 0 : i.plat_id,
                    };
                } catch (e) {
                    return (console.error("getZoneName", e), {});
                }
            }
        },
        55137: function (e, t, n) {
            "use strict";
            n.d(t, {
                Gn: function () {
                    return y;
                },
                Zc: function () {
                    return m;
                },
                ro: function () {
                    return f;
                },
            });
            var r = n(15189),
                i = n(22638),
                o = n(616),
                a = n(22448),
                l = n(48251),
                u = n(75889),
                s = n(81962),
                c = n(14603),
                d = n(36424),
                p = n(92724);
            let f = "1460000261";
            async function m(e) {
                if (e)
                    return new Promise((t) => {
                        try {
                            e &&
                                parent !== window &&
                                localStorage.setItem(
                                    "EMBED_ACTIVITY_LOGIN_SUCC",
                                    e,
                                );
                        } catch (e) {}
                        setTimeout(() => {
                            t();
                        }, 200);
                    });
            }
            function y(e) {
                let {
                        metadata: t,
                        store: n,
                        domAction: y,
                        activityId: v,
                        oriZoneId: g,
                    } = (0, l.Hl)(e),
                    { verifiedUser: b, setVerifiedUser: _ } = (0, u.ZP)(n),
                    [h, w] = (0, o.useState)(!1),
                    O = (0, i.Z)(async () => {
                        if (!t) return Promise.reject(Error("no metadata"));
                        let i = await (0, c.Wt)("GameLipassLogin");
                        if (t.payInfo.appid === f || i) {
                            let r = await (0, p.a8)(
                                t.payInfo,
                                n,
                                (null == b ? void 0 : b.user) || t.userData,
                                y,
                                v,
                                !1,
                            );
                            return "NOT_LOGIN" === r.state
                                ? Promise.reject("NOT_LOGIN")
                                : (_({ state: r.state, user: r.verifiedUser }),
                                    "LOGGED_IN" !== r.state &&
                                        (0, c.QR)(e, "GameLipassLogin"))
                                  ? Promise.reject(r.state)
                                  : r;
                        }
                        let o = null == b ? void 0 : b.user;
                        if (await (0, a.L)(n)) {
                            var l, h;
                            let e = (null == o ? void 0 : o.currentBindUser)
                                    ? ((l = (function (e) {
                                          for (
                                              var t = 1;
                                              t < arguments.length;
                                              t++
                                          ) {
                                              var n =
                                                      null != arguments[t]
                                                          ? arguments[t]
                                                          : {},
                                                  r = Object.keys(n);
                                              ("function" ==
                                                  typeof Object.getOwnPropertySymbols &&
                                                  (r = r.concat(
                                                      Object.getOwnPropertySymbols(
                                                          n,
                                                      ).filter(function (e) {
                                                          return Object.getOwnPropertyDescriptor(
                                                              n,
                                                              e,
                                                          ).enumerable;
                                                      }),
                                                  )),
                                                  r.forEach(function (t) {
                                                      var r, i, o;
                                                      ((r = e),
                                                          (i = t),
                                                          (o = n[t]),
                                                          i in r
                                                              ? Object.defineProperty(
                                                                    r,
                                                                    i,
                                                                    {
                                                                        value: o,
                                                                        enumerable:
                                                                            !0,
                                                                        configurable:
                                                                            !0,
                                                                        writable:
                                                                            !0,
                                                                    },
                                                                )
                                                              : (r[i] = o));
                                                  }));
                                          }
                                          return e;
                                      })(
                                          {},
                                          null == o
                                              ? void 0
                                              : o.currentBindUser,
                                      )),
                                      (h = ((h = { zoneid: g }), h)),
                                      Object.getOwnPropertyDescriptors
                                          ? Object.defineProperties(
                                                l,
                                                Object.getOwnPropertyDescriptors(
                                                    h,
                                                ),
                                            )
                                          : (function (e, t) {
                                                var n = Object.keys(e);
                                                if (
                                                    Object.getOwnPropertySymbols
                                                ) {
                                                    var r =
                                                        Object.getOwnPropertySymbols(
                                                            e,
                                                        );
                                                    n.push.apply(n, r);
                                                }
                                                return n;
                                            })(Object(h)).forEach(function (e) {
                                                Object.defineProperty(
                                                    l,
                                                    e,
                                                    Object.getOwnPropertyDescriptor(
                                                        h,
                                                        e,
                                                    ),
                                                );
                                            }),
                                      l)
                                    : null,
                                { balanceVerify: n } = await (0,
                                r.loadMidasbuyCommonSdkApi)();
                            return (
                                null == n ||
                                    n.emit("setBaseInfo", {
                                        appid: t.payInfo.appid,
                                        country: t.payInfo.country,
                                        popConfig: {},
                                    }),
                                null == n || n.emit("setUserInfo", e),
                                null == n || n.emit("showPop"),
                                new Promise((e, t) => {
                                    n.on("loginSuccess", async (t) => {
                                        (await m(v), e(t));
                                    })
                                        .on(
                                            "balanceVerifySuccess",
                                            async (t) => {
                                                (await m(v), e(t));
                                            },
                                        )
                                        .on("hide", () => {
                                            t(new s.UV());
                                        });
                                })
                            );
                        }
                        return (
                            (!(null == o ? void 0 : o.currentBindUser) ||
                                !o.uid) &&
                                _({
                                    user: (o = await (0, d.yA)({
                                        appid: t.payInfo.appid,
                                        country: t.payInfo.country,
                                        bindAfterLogin: 1,
                                        activityId: v,
                                    }).then((e) =>
                                        null == e ? void 0 : e.user,
                                    )),
                                    state: (0, u.V_)(o),
                                }),
                            o
                        );
                    }),
                    P = (0, i.Z)(async () => {
                        if (!t) return Promise.reject(Error("no metadata"));
                        let e = await (0, d.yA)({
                            appid: t.payInfo.appid,
                            country: t.payInfo.country,
                            noBindAfterLogin: 1,
                            activityId: v,
                            hash: "#lipass-joint-redirect",
                            hideThirdPartyList: ["lipass"],
                        }).then((e) => (null == e ? void 0 : e.user));
                        return (_({ user: e, state: (0, u.V_)(e) }), e);
                    }),
                    j = (0, i.Z)(async () =>
                        h
                            ? Promise.reject(Error("loading"))
                            : (w(!0), P().finally(() => w(!1))),
                    );
                return {
                    unifiedLogin: (0, i.Z)(async () =>
                        h
                            ? Promise.reject(Error("loading"))
                            : (w(!0), O().finally(() => w(!1))),
                    ),
                    unifiedLipassBind: j,
                };
            }
        },
        98818: function (e, t, n) {
            "use strict";
            n.d(t, {
                a3: function () {
                    return o;
                },
                of: function () {
                    return i;
                },
                vV: function () {
                    return a;
                },
            });
            var r = n(65317);
            function i(e) {
                let [t, n] = e.split("@"),
                    r = Math.min(5, Math.floor(t.length / 2));
                return `${t.slice(0, r)}${"*".repeat(t.length - r)}@${n}`;
            }
            function o(e, t) {
                let [n, i] = t.split("#");
                return `${(0, r.b1)(e, n)}${i ? `#${i}` : ""}`;
            }
            function a(e) {
                return (
                    !!(
                        null != e &&
                        "" !== e &&
                        "string" == typeof e &&
                        /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(
                            e,
                        )
                    ) || !1
                );
            }
        },
        90609: function (e, t, n) {
            "use strict";
            n.d(t, {
                L: function () {
                    return r;
                },
                f: function () {
                    return i;
                },
            });
            function r() {
                if (!!(document.getElementById("xMidasToken") || {}).value)
                    try {
                        window.xMidas();
                    } catch (e) {}
            }
            function i(e) {
                let t = JSON.stringify(e),
                    n = (document.getElementById("xMidasToken") || {}).value;
                if (!n) return e;
                let r = (document.getElementById("xMidasVersion") || {}).value,
                    i = (function (e) {
                        let t = Date.now(),
                            n = e();
                        return { times: Date.now() - t, result: n };
                    })(() => {
                        try {
                            return window.xMidas({ d: t });
                        } catch (t) {
                            return e;
                        }
                    });
                if (!i.result) return e;
                return {
                    encrypt_msg: btoa(
                        String.fromCharCode(
                            ...(i.result.match(/../g) || []).map((e) =>
                                parseInt(e, 16),
                            ),
                        ),
                    ),
                    ctoken_ver: r,
                    ctoken: n,
                };
            }
        },
        49567: function (e, t, n) {
            "use strict";
            n.d(t, {
                ZP: function () {
                    return u;
                },
            });
            var r = n(16520),
                i = n(33086),
                o = n(99744);
            let a = (0, o.R)(i.e.MESSENGER),
                l = (0, o.H)(i.e.MESSENGER);
            function u(e) {
                let t = (0, r.vZ)(e, a, l),
                    [n, i] = (0, r.Dr)(t);
                return { messenger: n, setMessenger: i };
            }
        },
        25808: function (e, t, n) {
            "use strict";
            var r = n(78812);
            let i = { isPageVisible: !1 },
                o = (0, r.Ue)()((e) => {
                    var t, n;
                    return (
                        (t = (function (e) {
                            for (var t = 1; t < arguments.length; t++) {
                                var n =
                                        null != arguments[t]
                                            ? arguments[t]
                                            : {},
                                    r = Object.keys(n);
                                ("function" ==
                                    typeof Object.getOwnPropertySymbols &&
                                    (r = r.concat(
                                        Object.getOwnPropertySymbols(n).filter(
                                            function (e) {
                                                return Object.getOwnPropertyDescriptor(
                                                    n,
                                                    e,
                                                ).enumerable;
                                            },
                                        ),
                                    )),
                                    r.forEach(function (t) {
                                        var r, i, o;
                                        ((r = e),
                                            (i = t),
                                            (o = n[t]),
                                            i in r
                                                ? Object.defineProperty(r, i, {
                                                      value: o,
                                                      enumerable: !0,
                                                      configurable: !0,
                                                      writable: !0,
                                                  })
                                                : (r[i] = o));
                                    }));
                            }
                            return e;
                        })({}, i)),
                        (n =
                            ((n = {
                                setIsPageVisible: (t) =>
                                    e(() => ({ isPageVisible: t })),
                            }),
                            n)),
                        Object.getOwnPropertyDescriptors
                            ? Object.defineProperties(
                                  t,
                                  Object.getOwnPropertyDescriptors(n),
                              )
                            : (function (e, t) {
                                  var n = Object.keys(e);
                                  if (Object.getOwnPropertySymbols) {
                                      var r = Object.getOwnPropertySymbols(e);
                                      n.push.apply(n, r);
                                  }
                                  return n;
                              })(Object(n)).forEach(function (e) {
                                  Object.defineProperty(
                                      t,
                                      e,
                                      Object.getOwnPropertyDescriptor(n, e),
                                  );
                              }),
                        t
                    );
                });
            t.Z = o;
        },
        29872: function (e, t, n) {
            "use strict";
            n.d(t, {
                ID: function () {
                    return m;
                },
                ZP: function () {
                    return y;
                },
            });
            var r = n(16520),
                i = n(22638),
                o = n(616),
                a = n(52363),
                l = n(13047),
                u = n(33086),
                s = n(99744);
            function c(e) {
                for (var t = 1; t < arguments.length; t++) {
                    var n = null != arguments[t] ? arguments[t] : {},
                        r = Object.keys(n);
                    ("function" == typeof Object.getOwnPropertySymbols &&
                        (r = r.concat(
                            Object.getOwnPropertySymbols(n).filter(
                                function (e) {
                                    return Object.getOwnPropertyDescriptor(n, e)
                                        .enumerable;
                                },
                            ),
                        )),
                        r.forEach(function (t) {
                            var r, i, o;
                            ((r = e),
                                (i = t),
                                (o = n[t]),
                                i in r
                                    ? Object.defineProperty(r, i, {
                                          value: o,
                                          enumerable: !0,
                                          configurable: !0,
                                          writable: !0,
                                      })
                                    : (r[i] = o));
                        }));
                }
                return e;
            }
            function d(e, t) {
                return (
                    (t = null != t ? t : {}),
                    Object.getOwnPropertyDescriptors
                        ? Object.defineProperties(
                              e,
                              Object.getOwnPropertyDescriptors(t),
                          )
                        : (function (e, t) {
                              var n = Object.keys(e);
                              if (Object.getOwnPropertySymbols) {
                                  var r = Object.getOwnPropertySymbols(e);
                                  n.push.apply(n, r);
                              }
                              return n;
                          })(Object(t)).forEach(function (n) {
                              Object.defineProperty(
                                  e,
                                  n,
                                  Object.getOwnPropertyDescriptor(t, n),
                              );
                          }),
                    e
                );
            }
            let p = (0, s.R)(u.e.MODEL_MAP),
                f = (0, s.H)(u.e.MODEL_MAP);
            function m(e, t) {
                var n, r, i;
                if (
                    "number" ==
                    typeof (null == e
                        ? void 0
                        : null === (n = e.__ruleConf) || void 0 === n
                          ? void 0
                          : n.model_type)
                )
                    return null == e
                        ? void 0
                        : null === (r = e.__ruleConf) || void 0 === r
                          ? void 0
                          : r.model_type;
                let o = e.__modelKey;
                try {
                    let e = JSON.parse(t.activityInfo.modelList);
                    return (
                        (null === (i = e.find((e) => e.model_key === o)) ||
                        void 0 === i
                            ? void 0
                            : i.model_type) || -1
                    );
                } catch (e) {
                    return -1;
                }
            }
            function y(e) {
                let t = (0, r.vZ)(e, p, f),
                    [n, u] = (0, r.Dr)(t),
                    s = (0, o.useMemo)(() => {
                        var e;
                        return (
                            (e = n),
                            function (t) {
                                if (!t) return;
                                if ("string" == typeof t)
                                    return null == e ? void 0 : e[t];
                                let n = {};
                                return (
                                    Object.values(e || {}).forEach((e) => {
                                        n[(0, a.n)(e)] = e;
                                    }),
                                    Object.values(n).filter(
                                        (e) => e.modelType === t,
                                    )
                                );
                            }
                        );
                    }, [n]);
                return {
                    getModel: s,
                    setModel: (0, i.Z)(function (e, t, n, r) {
                        u((i) => {
                            let o = null == i ? void 0 : i[e],
                                u = d(c({}, t), {
                                    modelType: n,
                                    modelKey: e,
                                    modelCustomConf: r,
                                });
                            return (0, l.vZ)(o, u)
                                ? i
                                : d(c({}, i), { [e]: u, [(0, a.n)(t)]: u });
                        });
                    }),
                };
            }
        },
        89601: function (e, t, n) {
            "use strict";
            n.d(t, {
                ZP: function () {
                    return p;
                },
            });
            var r = n(16520),
                i = n(22638),
                o = n(616),
                a = n(33086),
                l = n(99744),
                u = n(13047);
            function s(e) {
                for (var t = 1; t < arguments.length; t++) {
                    var n = null != arguments[t] ? arguments[t] : {},
                        r = Object.keys(n);
                    ("function" == typeof Object.getOwnPropertySymbols &&
                        (r = r.concat(
                            Object.getOwnPropertySymbols(n).filter(
                                function (e) {
                                    return Object.getOwnPropertyDescriptor(n, e)
                                        .enumerable;
                                },
                            ),
                        )),
                        r.forEach(function (t) {
                            var r, i, o;
                            ((r = e),
                                (i = t),
                                (o = n[t]),
                                i in r
                                    ? Object.defineProperty(r, i, {
                                          value: o,
                                          enumerable: !0,
                                          configurable: !0,
                                          writable: !0,
                                      })
                                    : (r[i] = o));
                        }));
                }
                return e;
            }
            let c = (0, l.R)(a.e.PRODUCT_MAP),
                d = (0, l.H)(a.e.PRODUCT_MAP);
            function p(e) {
                let t = (0, r.vZ)(e, c, d),
                    [n, a] = (0, r.Dr)(t),
                    l = (0, i.Z)(function (e) {
                        a((t) => {
                            let n = Array.isArray(e) ? e : Object.values(e);
                            if (
                                n.every((e) =>
                                    (0, u.vZ)(
                                        null == t
                                            ? void 0
                                            : t[e.uniqueId || e.id],
                                        e,
                                    ),
                                )
                            )
                                return t;
                            let r = n.reduce((e, t) => {
                                var n, r;
                                return (
                                    (n = s(
                                        {},
                                        e,
                                        t.uniqueId && { [t.uniqueId]: t },
                                    )),
                                    (r = ((r = { [t.id]: t }), r)),
                                    Object.getOwnPropertyDescriptors
                                        ? Object.defineProperties(
                                              n,
                                              Object.getOwnPropertyDescriptors(
                                                  r,
                                              ),
                                          )
                                        : (function (e, t) {
                                              var n = Object.keys(e);
                                              if (
                                                  Object.getOwnPropertySymbols
                                              ) {
                                                  var r =
                                                      Object.getOwnPropertySymbols(
                                                          e,
                                                      );
                                                  n.push.apply(n, r);
                                              }
                                              return n;
                                          })(Object(r)).forEach(function (e) {
                                              Object.defineProperty(
                                                  n,
                                                  e,
                                                  Object.getOwnPropertyDescriptor(
                                                      r,
                                                      e,
                                                  ),
                                              );
                                          }),
                                    n
                                );
                            }, {});
                            return s({}, t, r);
                        });
                    });
                return {
                    getProduct: (0, o.useCallback)(
                        function (e, t) {
                            if (!e) return n;
                            if (n) {
                                if (e.startsWith(`${t}`))
                                    return null == n ? void 0 : n[e];
                                if (t) {
                                    let r = Object.values(
                                        (0, u.v7)(
                                            n,
                                            (n, r) =>
                                                !t || r.startsWith(`${t}:${e}`),
                                        ),
                                    )[0];
                                    return r
                                        ? r
                                        : Object.values(
                                              (0, u.v7)(n, (t, n) => n === e),
                                          )[0];
                                }
                                return null == n ? void 0 : n[e];
                            }
                        },
                        [n],
                    ),
                    setProduct: l,
                };
            }
        },
        14831: function (e, t, n) {
            "use strict";
            n.d(t, {
                ZP: function () {
                    return u;
                },
            });
            var r = n(16520),
                i = n(33086),
                o = n(99744);
            let a = (0, o.R)(i.e.TASK),
                l = (0, o.H)(i.e.TASK);
            function u(e) {
                let t = (0, r.vZ)(e, a, l),
                    [n, i] = (0, r.Dr)(t);
                return { simulateData: n, setSimulateData: i };
            }
        },
        75889: function (e, t, n) {
            "use strict";
            n.d(t, {
                E_: function () {
                    return c;
                },
                V_: function () {
                    return d;
                },
                ZP: function () {
                    return p;
                },
            });
            var r = n(16520),
                i = n(92724),
                o = n(55137),
                a = n(33086),
                l = n(99744);
            let u = (0, l.R)(a.e.VERIFIED_USER),
                s = (0, l.H)(a.e.VERIFIED_USER);
            function c(e) {
                return !!e && "" !== e && "email" !== e;
            }
            function d(e) {
                return e
                    ? e.currentBindUser
                        ? c(e.currentBindUser.verifytype)
                            ? "LOGGED_IN"
                            : e.currentBindUser.appid !== o.ro || (0, i.LH)(e)
                              ? "NOT_VERIFIED"
                              : "NOT_BIND"
                        : "NOT_BIND"
                    : "NOT_LOGIN";
            }
            function p(e) {
                let t = (0, r.vZ)(e, u, s),
                    [n, i] = (0, r.Dr)(t);
                return {
                    verifiedUser: n || { state: "INITIAL" },
                    setVerifiedUser: i,
                };
            }
        },
        77761: function () {},
    },
]);
//# sourceMappingURL=46374.aa36b94c9a17d3c2.js.map
