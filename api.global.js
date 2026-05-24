!(function () {
    "use strict";
    function e(e, t) {
        if (t == null || t > e.length) t = e.length;
        for (var r = 0, n = new Array(t); r < t; r++) n[r] = e[r];
        return n;
    }
    function t(e) {
        if (Array.isArray(e)) return e;
    }
    function r(t) {
        if (Array.isArray(t)) return e(t);
    }
    function n(e) {
        if (e === void 0) {
            throw new ReferenceError(
                "this hasn't been initialised - super() hasn't been called",
            );
        }
        return e;
    }
    function a(e, t) {
        if (!(e instanceof t)) {
            throw new TypeError("Cannot call a class as a function");
        }
    }
    function o(e, t) {
        for (var r = 0; r < t.length; r++) {
            var n = t[r];
            n.enumerable = n.enumerable || false;
            n.configurable = true;
            if ("value" in n) n.writable = true;
            Object.defineProperty(e, n.key, n);
        }
    }
    function u(e, t, r) {
        if (t) o(e.prototype, t);
        if (r) o(e, r);
        return e;
    }
    function c(e, t, r) {
        if (t in e) {
            Object.defineProperty(e, t, {
                value: r,
                enumerable: true,
                configurable: true,
                writable: true,
            });
        } else {
            e[t] = r;
        }
        return e;
    }
    function l(e) {
        l = Object.setPrototypeOf
            ? Object.getPrototypeOf
            : function l(e) {
                  return e.__proto__ || Object.getPrototypeOf(e);
              };
        return l(e);
    }
    function s(e, t) {
        if (typeof t !== "function" && t !== null) {
            throw new TypeError(
                "Super expression must either be null or a function",
            );
        }
        e.prototype = Object.create(t && t.prototype, {
            constructor: { value: e, writable: true, configurable: true },
        });
        if (t) P(e, t);
    }
    function f(e, t) {
        if (
            t != null &&
            typeof Symbol !== "undefined" &&
            t[Symbol.hasInstance]
        ) {
            return !!t[Symbol.hasInstance](e);
        } else {
            return e instanceof t;
        }
    }
    function v(e) {
        if (
            (typeof Symbol !== "undefined" && e[Symbol.iterator] != null) ||
            e["@@iterator"] != null
        )
            return Array.from(e);
    }
    function p(e, t) {
        var r =
            e == null
                ? null
                : (typeof Symbol !== "undefined" && e[Symbol.iterator]) ||
                  e["@@iterator"];
        if (r == null) return;
        var n = [];
        var a = true;
        var o = false;
        var u, c;
        try {
            for (r = r.call(e); !(a = (u = r.next()).done); a = true) {
                n.push(u.value);
                if (t && n.length === t) break;
            }
        } catch (l) {
            o = true;
            c = l;
        } finally {
            try {
                if (!a && r["return"] != null) r["return"]();
            } finally {
                if (o) throw c;
            }
        }
        return n;
    }
    function d() {
        throw new TypeError(
            "Invalid attempt to destructure non-iterable instance.\\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
        );
    }
    function h() {
        throw new TypeError(
            "Invalid attempt to spread non-iterable instance.\\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.",
        );
    }
    function y(e) {
        for (var t = 1; t < arguments.length; t++) {
            var r = arguments[t] != null ? arguments[t] : {};
            var n = Object.keys(r);
            if (typeof Object.getOwnPropertySymbols === "function") {
                n = n.concat(
                    Object.getOwnPropertySymbols(r).filter(function (e) {
                        return Object.getOwnPropertyDescriptor(r, e).enumerable;
                    }),
                );
            }
            n.forEach(function (t) {
                c(e, t, r[t]);
            });
        }
        return e;
    }
    function m(e, t) {
        var r = Object.keys(e);
        if (Object.getOwnPropertySymbols) {
            var n = Object.getOwnPropertySymbols(e);
            if (t) {
                n = n.filter(function (t) {
                    return Object.getOwnPropertyDescriptor(e, t).enumerable;
                });
            }
            r.push.apply(r, n);
        }
        return r;
    }
    function g(e, t) {
        t = t != null ? t : {};
        if (Object.getOwnPropertyDescriptors) {
            Object.defineProperties(e, Object.getOwnPropertyDescriptors(t));
        } else {
            m(Object(t)).forEach(function (r) {
                Object.defineProperty(
                    e,
                    r,
                    Object.getOwnPropertyDescriptor(t, r),
                );
            });
        }
        return e;
    }
    function $(e, t) {
        if (e == null) return {};
        var r = w(e, t);
        var n, a;
        if (Object.getOwnPropertySymbols) {
            var o = Object.getOwnPropertySymbols(e);
            for (a = 0; a < o.length; a++) {
                n = o[a];
                if (t.indexOf(n) >= 0) continue;
                if (!Object.prototype.propertyIsEnumerable.call(e, n)) continue;
                r[n] = e[n];
            }
        }
        return r;
    }
    function w(e, t) {
        if (e == null) return {};
        var r = {};
        var n = Object.keys(e);
        var a, o;
        for (o = 0; o < n.length; o++) {
            a = n[o];
            if (t.indexOf(a) >= 0) continue;
            r[a] = e[a];
        }
        return r;
    }
    function b(e, t) {
        if (t && (S(t) === "object" || typeof t === "function")) {
            return t;
        }
        return n(e);
    }
    function P(e, t) {
        P =
            Object.setPrototypeOf ||
            function P(e, t) {
                e.__proto__ = t;
                return e;
            };
        return P(e, t);
    }
    function k(e, r) {
        return t(e) || p(e, r) || R(e, r) || d();
    }
    function _(e) {
        return t(e) || v(e) || R(e, i) || d();
    }
    function x(e) {
        return r(e) || v(e) || R(e) || h();
    }
    var S = function (e) {
        "@swc/helpers - typeof";
        return e && typeof Symbol !== "undefined" && e.constructor === Symbol
            ? "symbol"
            : typeof e;
    };
    function R(t, r) {
        if (!t) return;
        if (typeof t === "string") return e(t, r);
        var n = Object.prototype.toString.call(t).slice(8, -1);
        if (n === "Object" && t.constructor) n = t.constructor.name;
        if (n === "Map" || n === "Set") return Array.from(n);
        if (
            n === "Arguments" ||
            /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)
        )
            return e(t, r);
    }
    function T() {
        if (typeof Reflect === "undefined" || !Reflect.construct) return false;
        if (Reflect.construct.sham) return false;
        if (typeof Proxy === "function") return true;
        try {
            Boolean.prototype.valueOf.call(
                Reflect.construct(Boolean, [], function () {}),
            );
            return true;
        } catch (e) {
            return false;
        }
    }
    function C(e) {
        var t = T();
        return function r() {
            var n = l(e),
                a;
            if (t) {
                var o = l(this).constructor;
                a = Reflect.construct(n, arguments, o);
            } else {
                a = n.apply(this, arguments);
            }
            return b(this, a);
        };
    }
    var midasbuyActivity = (function () {
        var e = function e() {
            return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
                window.navigator.userAgent,
            );
        };
        var t = function t() {
            var e =
                    arguments.length > 0 && arguments[0] !== void 0
                        ? arguments[0]
                        : {},
                r = e.method,
                n = r === void 0 ? "GET" : r,
                a = e.url,
                o = e.param,
                u = o === void 0 ? {} : o;
            var c = new XMLHttpRequest();
            return (
                n === "GET"
                    ? ((a = (0, eE.default)(u, a)), c.open(n, a, !0))
                    : (c.open(n, a, !0),
                      c.setRequestHeader(
                          "Content-Type",
                          "application/x-www-form-urlencoded",
                      )),
                new Promise(function (e, t) {
                    c.onreadystatechange = function () {
                        if (c.readyState === 4)
                            if (c.status >= 200 && c.status < 300)
                                try {
                                    return e(JSON.parse(c.responseText));
                                } catch (r) {
                                    return t({
                                        ret: -9999,
                                        path: a,
                                        msg: "System busy, please try again later！(-9999)",
                                    });
                                }
                            else
                                c.status >= 300
                                    ? t({
                                          ret: -9998,
                                          path: a,
                                          msg: "System busy, please try again later！(-9998-".concat(
                                              c.status,
                                              ")",
                                          ),
                                      })
                                    : t({
                                          ret: -9996,
                                          path: a,
                                          msg: "System busy, please try again later！(-9996)",
                                      });
                    };
                    var r = n === "POST" ? (0, eC.default)(u) : void 0;
                    c.send(r);
                })
            );
        };
        var r = Object.create;
        var n = Object.defineProperty;
        var o = Object.getOwnPropertyDescriptor;
        var c = Object.getOwnPropertyNames;
        var l = Object.getPrototypeOf,
            v = Object.prototype.hasOwnProperty;
        var p = function (e, t) {
            return function () {
                return (t || e((t = { exports: {} }).exports, t), t.exports);
            };
        };
        var d = function (e, t, r, a) {
            var u = true,
                l = false,
                s = undefined;
            if ((t && typeof t == "object") || typeof t == "function")
                try {
                    var f = function () {
                        var u = d.value;
                        !v.call(e, u) &&
                            u !== r &&
                            n(e, u, {
                                get: function () {
                                    return t[u];
                                },
                                enumerable: !(a = o(t, u)) || a.enumerable,
                            });
                    };
                    for (
                        var p = c(t)[Symbol.iterator](), d;
                        !(u = (d = p.next()).done);
                        u = true
                    )
                        f();
                } catch (h) {
                    l = true;
                    s = h;
                } finally {
                    try {
                        if (!u && p.return != null) {
                            p.return();
                        }
                    } finally {
                        if (l) {
                            throw s;
                        }
                    }
                }
            return e;
        };
        var h = function (e, t, a) {
                return (
                    (a = e != null ? r(l(e)) : {}),
                    d(
                        t || !e || !e.__esModule
                            ? n(a, "default", { value: e, enumerable: !0 })
                            : a,
                        e,
                    )
                );
            },
            m = function (e) {
                return d(n({}, "__esModule", { value: !0 }), e);
            };
        var w = p(function (e) {
            "use strict";
            var t = function t(e, n, a) {
                (e === void 0 && (e = location.href),
                    n === void 0 && (n = "&"),
                    a === void 0 && (a = "="));
                var o = e.replace(/.+?\?/, "").replace(/#.*/, ""),
                    u = o.split(n);
                return (
                    r[o] ||
                        (r[o] = u.reduce(function (e, t) {
                            var r = t.indexOf(a);
                            if (r > -1) {
                                var n = t.substr(0, r);
                                if (n) {
                                    var o = t.substr(r + 1);
                                    try {
                                        e[n] = decodeURIComponent(o);
                                    } catch (u) {
                                        e[n] = o;
                                    }
                                }
                            }
                            return e;
                        }, {})),
                    r[o]
                );
            };
            Object.defineProperty(e, "__esModule", { value: !0 });
            var r = {};
            e.default = t;
        });
        var b = p(function (e) {
            "use strict";
            var t = function t(e, n) {
                return (0, r.default)(n)[e];
            };
            Object.defineProperty(e, "__esModule", { value: !0 });
            var r = w();
            e.default = t;
        });
        var P = p(function (e) {
            "use strict";
            var t = function t(e, r) {
                var n = Object.prototype.toString.call(r).slice(8, -1);
                return r != null && n === e;
            };
            Object.defineProperty(e, "__esModule", { value: !0 });
            e.default = t;
        });
        var R = p(function (e) {
            "use strict";
            var t = function t(e) {
                return (0, r.default)("Object", e) && e !== null;
            };
            Object.defineProperty(e, "__esModule", { value: !0 });
            var r = P();
            e.default = t;
        });
        var T = p(function (e) {
            "use strict";
            var t = function t(e, n) {
                if ((n === void 0 && (n = !0), !(0, r.default)(e))) return "";
                var a = [];
                for (var o in e)
                    if (
                        Object.prototype.hasOwnProperty.call(e, o) &&
                        S(e[o]) < "u" &&
                        e[o] !== null
                    ) {
                        var u = n ? encodeURIComponent(o) : o,
                            c = n ? encodeURIComponent(e[o]) : e[o];
                        a.push(u + "=" + c);
                    }
                return a.join("&");
            };
            Object.defineProperty(e, "__esModule", { value: !0 });
            var r = R();
            e.default = t;
        });
        var E = p(function (e) {
            "use strict";
            var t = function t(e) {
                return (0, r.default)("Array", e);
            };
            Object.defineProperty(e, "__esModule", { value: !0 });
            var r = P();
            e.default = t;
        });
        var M = p(function (e) {
            "use strict";
            var t = function t(e, n) {
                var a,
                    o = 0;
                if ((0, r.default)(e)) {
                    var u = e.length;
                    for (
                        a = e[0];
                        o < u && n.call(a, a, o, e) !== !1;
                        a = e[++o]
                    );
                } else
                    for (var c in e) if (n.call(e[c], e[c], c, e) === !1) break;
                return e;
            };
            Object.defineProperty(e, "__esModule", { value: !0 });
            var r = E();
            e.default = t;
        });
        var I = p(function (e) {
            "use strict";
            var t = function t(e, n) {
                return (
                    n === void 0 && (n = location.href),
                    f(e, Array) || (e = [e]),
                    (n = n.replace(/[\r\n]/g, "")),
                    (0, r.default)(e, function (e) {
                        ((n = n.replace(
                            new RegExp("(?:&" + e + "=[^&]*)", "g"),
                            "",
                        )),
                            (n = n.replace(
                                new RegExp("(?:\\?" + e + "=[^&]*&?)", "g"),
                                "?",
                            )));
                    }),
                    n
                );
            };
            Object.defineProperty(e, "__esModule", { value: !0 });
            var r = M();
            e.default = t;
        });
        var O = p(function (e) {
            "use strict";
            var t = function t(e) {
                if (!(0, n.default)(e)) return [];
                var a = [];
                return (
                    (0, r.default)(e, function (e, t) {
                        a.push(t);
                    }),
                    a
                );
            };
            Object.defineProperty(e, "__esModule", { value: !0 });
            var r = M(),
                n = R();
            e.default = t;
        });
        var A = p(function (e) {
            "use strict";
            var t = function t(e, u) {
                if (!(0, o.default)(e)) return u;
                var c = (0, a.default)(e);
                if (c.length === 0) return u;
                u = (0, n.default)(c, u);
                var l = (0, r.default)(e);
                return (
                    (u += /(\?|&)$/.test(u)
                        ? "" + l
                        : /\?/.test(u)
                          ? "&" + l
                          : "?" + l),
                    u
                );
            };
            Object.defineProperty(e, "__esModule", { value: !0 });
            var r = T(),
                n = I(),
                a = O(),
                o = R();
            e.default = t;
        });
        var U = p(function (e) {
            "use strict";
            Object.defineProperty(e, "__esModule", { value: !0 });
            var t = {
                get: function e(t) {
                    var r = document.cookie.match(
                        new RegExp("(?:^|;\\s)" + t + "=(.*?)(?:;\\s|$)"),
                    );
                    return r ? r[1] : "";
                },
                set: function e(t, r, n) {
                    n === void 0 && (n = {});
                    var a = new Date(),
                        o = n.domain === "*" ? "" : n.domain || "pay.qq.com",
                        u = n.path || "/",
                        c = 31536e7,
                        l = n.time || c;
                    a.setTime(a.getTime() + l);
                    var s = t + "=" + r + "; path=" + u;
                    (o && (s += "; domain=" + o),
                        !n.ignoreTime && (s += "; expires=" + a.toUTCString()),
                        (document.cookie = s));
                },
                del: function e(r, n) {
                    (n === void 0 && (n = {}),
                        (n.time = -new Date()),
                        t.set(r, "", n));
                },
            };
            e.default = t;
        });
        var N = p(function (e, t) {
            var r = function r() {};
            r.prototype = {
                on: function e(t, r, n) {
                    var a = this.e || (this.e = {});
                    return (
                        (a[t] || (a[t] = [])).push({ fn: r, ctx: n }),
                        this
                    );
                },
                once: function e(t, r, n) {
                    var a = this;
                    function o() {
                        (a.off(t, o), r.apply(n, arguments));
                    }
                    return ((o._ = r), this.on(t, o, n));
                },
                emit: function e(t) {
                    var r = [].slice.call(arguments, 1),
                        n = ((this.e || (this.e = {}))[t] || []).slice(),
                        a = 0,
                        o = n.length;
                    for (a; a < o; a++) n[a].fn.apply(n[a].ctx, r);
                    return this;
                },
                off: function e(t, r) {
                    var n = this.e || (this.e = {}),
                        a = n[t],
                        o = [];
                    if (a && r)
                        for (var u = 0, c = a.length; u < c; u++)
                            a[u].fn !== r && a[u].fn._ !== r && o.push(a[u]);
                    return (o.length ? (n[t] = o) : delete n[t], this);
                },
            };
            t.exports = r;
            t.exports.TinyEmitter = r;
        });
        var Q = {};
        var j = h(b());
        var D = h(A()),
            F = h(b()),
            L = h(U()),
            W = h(N());
        var V;
        (function (e) {
            ((e.Call = "call"),
                (e.Reply = "reply"),
                (e.Syn = "syn"),
                (e.SynAck = "synAck"),
                (e.Ack = "ack"));
        })(V || (V = {}));
        var H;
        (function (e) {
            ((e.Fulfilled = "fulfilled"), (e.Rejected = "rejected"));
        })(H || (H = {}));
        var q;
        (function (e) {
            ((e.ConnectionDestroyed = "ConnectionDestroyed"),
                (e.ConnectionTimeout = "ConnectionTimeout"),
                (e.NoIframeSrc = "NoIframeSrc"));
        })(q || (q = {}));
        var z;
        (function (e) {
            e.DataCloneError = "DataCloneError";
        })(z || (z = {}));
        var B;
        (function (e) {
            e.Message = "message";
        })(B || (B = {}));
        var K = function (e, t) {
            var r = [],
                n = !1;
            return {
                destroy: function a(o) {
                    n ||
                        ((n = !0),
                        t("".concat(e, ": Destroying connection")),
                        r.forEach(function (e) {
                            e(o);
                        }));
                },
                onDestroy: function e(t) {
                    n ? t() : r.push(t);
                },
            };
        };
        var Y = function (e) {
            return function () {
                for (
                    var t = arguments.length, r = new Array(t), n = 0;
                    n < t;
                    n++
                ) {
                    r[n] = arguments[n];
                }
                var a;
                e && (a = console).log.apply(a, ["[Penpal]"].concat(x(r)));
            };
        };
        var G = { "http:": "80", "https:": "443" },
            J = /^(https?:)?\/\/([^/:]+)?(:(\d+))?/,
            X = ["file:", "data:"],
            Z = function (e) {
                if (
                    e &&
                    X.find(function (t) {
                        return e.startsWith(t);
                    })
                )
                    return "null";
                var t = document.location,
                    r = J.exec(e),
                    n,
                    a,
                    o;
                r
                    ? ((n = r[1] ? r[1] : t.protocol), (a = r[2]), (o = r[4]))
                    : ((n = t.protocol), (a = t.hostname), (o = t.port));
                var u = o && o !== G[n] ? ":".concat(o) : "";
                return "".concat(n, "//").concat(a).concat(u);
            };
        var ee = function (e) {
                var t = e.name,
                    r = e.message,
                    n = e.stack;
                return { name: t, message: r, stack: n };
            },
            et = function (e) {
                var t = new Error();
                return (
                    Object.keys(e).forEach(function (r) {
                        return (t[r] = e[r]);
                    }),
                    t
                );
            };
        var er = function (e, t, r) {
            var n = e.localName,
                a = e.local,
                o = e.remote,
                u = e.originForSending,
                c = e.originForReceiving,
                l = !1,
                s = function (e) {
                    if (e.source !== o || e.data.penpal !== V.Call) return;
                    if (c !== "*" && e.origin !== c) {
                        r(
                            ""
                                .concat(n, " received message from origin ")
                                .concat(
                                    e.origin,
                                    " which did not match expected origin ",
                                )
                                .concat(c),
                        );
                        return;
                    }
                    var a = e.data,
                        s = a.methodName,
                        v = a.args,
                        p = a.id;
                    r("".concat(n, ": Received ").concat(s, "() call"));
                    var d = function (e) {
                        return function (t) {
                            if (
                                (r(
                                    ""
                                        .concat(n, ": Sending ")
                                        .concat(s, "() reply"),
                                ),
                                l)
                            ) {
                                r(
                                    ""
                                        .concat(n, ": Unable to send ")
                                        .concat(
                                            s,
                                            "() reply due to destroyed connection",
                                        ),
                                );
                                return;
                            }
                            var a = {
                                penpal: V.Reply,
                                id: p,
                                resolution: e,
                                returnValue: t,
                            };
                            e === H.Rejected &&
                                f(t, Error) &&
                                ((a.returnValue = ee(t)),
                                (a.returnValueIsError = !0));
                            try {
                                o.postMessage(a, u);
                            } catch (c) {
                                if (c.name === z.DataCloneError) {
                                    var v = {
                                        penpal: V.Reply,
                                        id: p,
                                        resolution: H.Rejected,
                                        returnValue: ee(c),
                                        returnValueIsError: !0,
                                    };
                                    o.postMessage(v, u);
                                }
                                throw c;
                            }
                        };
                    };
                    new Promise(function (e) {
                        return e(t[s].apply(t, v));
                    }).then(d(H.Fulfilled), d(H.Rejected));
                };
            return (
                a.addEventListener(B.Message, s),
                function () {
                    ((l = !0), a.removeEventListener(B.Message, s));
                }
            );
        };
        var en = 0,
            ei = function () {
                return ++en;
            };
        var ea = ".",
            eo = function (e) {
                return e ? e.split(ea) : [];
            },
            eu = function (e) {
                return e.join(ea);
            },
            ec = function (e, t) {
                var r = eo(t || "");
                return (r.push(e), eu(r));
            },
            el = function (e, t, r) {
                var n = eo(t);
                return (
                    n.reduce(function (e, t, a) {
                        return (
                            S(e[t]) > "u" && (e[t] = {}),
                            a === n.length - 1 && (e[t] = r),
                            e[t]
                        );
                    }, e),
                    e
                );
            },
            es = function (e, t) {
                var r = {};
                return (
                    Object.keys(e).forEach(function (n) {
                        var a = e[n],
                            o = ec(n, t);
                        (typeof a == "object" && Object.assign(r, es(a, o)),
                            typeof a == "function" && (r[o] = a));
                    }),
                    r
                );
            },
            ef = function (e) {
                var t = {};
                for (var r in e) el(t, r, e[r]);
                return t;
            };
        var ev = function (e, t, r, n, a) {
            var o = t.localName,
                u = t.local,
                c = t.remote,
                l = t.originForSending,
                s = t.originForReceiving,
                f = !1;
            a("".concat(o, ": Connecting call sender"));
            var v = function (e) {
                    return function () {
                        for (
                            var t = arguments.length, r = new Array(t), v = 0;
                            v < t;
                            v++
                        ) {
                            r[v] = arguments[v];
                        }
                        a("".concat(o, ": Sending ").concat(e, "() call"));
                        var p;
                        try {
                            c.closed && (p = !0);
                        } catch (d) {
                            p = !0;
                        }
                        if ((p && n(), f)) {
                            var h = new Error(
                                "Unable to send ".concat(
                                    e,
                                    "() call due to destroyed connection",
                                ),
                            );
                            throw ((h.code = q.ConnectionDestroyed), h);
                        }
                        return new Promise(function (t, n) {
                            var f = ei(),
                                v = function (r) {
                                    if (
                                        r.source !== c ||
                                        r.data.penpal !== V.Reply ||
                                        r.data.id !== f
                                    )
                                        return;
                                    if (s !== "*" && r.origin !== s) {
                                        a(
                                            ""
                                                .concat(
                                                    o,
                                                    " received message from origin ",
                                                )
                                                .concat(
                                                    r.origin,
                                                    " which did not match expected origin ",
                                                )
                                                .concat(s),
                                        );
                                        return;
                                    }
                                    var l = r.data;
                                    (a(
                                        ""
                                            .concat(o, ": Received ")
                                            .concat(e, "() reply"),
                                    ),
                                        u.removeEventListener(B.Message, v));
                                    var p = l.returnValue;
                                    (l.returnValueIsError && (p = et(p)),
                                        (l.resolution === H.Fulfilled ? t : n)(
                                            p,
                                        ));
                                };
                            u.addEventListener(B.Message, v);
                            var p = {
                                penpal: V.Call,
                                id: f,
                                methodName: e,
                                args: r,
                            };
                            c.postMessage(p, l);
                        });
                    };
                },
                p = r.reduce(function (e, t) {
                    return ((e[t] = v(t)), e);
                }, {});
            return (
                Object.assign(e, ef(p)),
                function () {
                    f = !0;
                }
            );
        };
        var ep = function (e, t, r, n, a) {
            var o = n.destroy,
                u = n.onDestroy,
                c,
                l,
                s = {};
            return function (n) {
                if (t !== "*" && n.origin !== t) {
                    a(
                        "Parent: Handshake - Received ACK message from origin "
                            .concat(
                                n.origin,
                                " which did not match expected origin ",
                            )
                            .concat(t),
                    );
                    return;
                }
                a("Parent: Handshake - Received ACK");
                var f = {
                    localName: "Parent",
                    local: window,
                    remote: n.source,
                    originForSending: r,
                    originForReceiving: t,
                };
                (c && c(),
                    (c = er(f, e, a)),
                    u(c),
                    l &&
                        l.forEach(function (e) {
                            delete s[e];
                        }),
                    (l = n.data.methodNames));
                var v = ev(s, f, l, o, a);
                return (u(v), s);
            };
        };
        var ed = function (e, t, r, n) {
            return function (a) {
                if (!a.source) return;
                if (r !== "*" && a.origin !== r) {
                    e(
                        "Parent: Handshake - Received SYN message from origin "
                            .concat(
                                a.origin,
                                " which did not match expected origin ",
                            )
                            .concat(r),
                    );
                    return;
                }
                e("Parent: Handshake - Received SYN, responding with SYN-ACK");
                var o = { penpal: V.SynAck, methodNames: Object.keys(t) };
                a.source.postMessage(o, n);
            };
        };
        var eh = function (e, t) {
            var r = t.destroy,
                n = t.onDestroy,
                a = setInterval(function () {
                    e.isConnected || (clearInterval(a), r());
                }, 6e4);
            n(function () {
                clearInterval(a);
            });
        };
        var ey = function (e, t) {
            var r;
            return (
                e !== void 0 &&
                    (r = window.setTimeout(function () {
                        var r = new Error(
                            "Connection timed out after ".concat(e, "ms"),
                        );
                        ((r.code = q.ConnectionTimeout), t(r));
                    }, e)),
                function () {
                    clearTimeout(r);
                }
            );
        };
        var em = function (e) {
            if (!e.src && !e.srcdoc) {
                var t = new Error(
                    "Iframe must have src or srcdoc property defined.",
                );
                throw ((t.code = q.NoIframeSrc), t);
            }
        };
        var eg = function (e) {
            var t = e.iframe,
                r = e.methods,
                n = r === void 0 ? {} : r,
                a = e.childOrigin,
                o = e.timeout,
                u = e.debug,
                c = u === void 0 ? !1 : u,
                l = Y(c),
                s = K("Parent", l),
                f = s.onDestroy,
                v = s.destroy;
            a || (em(t), (a = Z(t.src)));
            var p = a === "null" ? "*" : a,
                d = es(n),
                h = ed(l, d, a, p),
                y = ep(d, a, p, s, l);
            return {
                promise: new Promise(function (e, r) {
                    var n = ey(o, v),
                        a = function (r) {
                            if (!(r.source !== t.contentWindow || !r.data)) {
                                if (r.data.penpal === V.Syn) {
                                    h(r);
                                    return;
                                }
                                if (r.data.penpal === V.Ack) {
                                    var a = y(r);
                                    a && (n(), e(a));
                                    return;
                                }
                            }
                        };
                    (window.addEventListener(B.Message, a),
                        l("Parent: Awaiting handshake"),
                        eh(t, s),
                        f(function (e) {
                            (window.removeEventListener(B.Message, a),
                                e && r(e));
                        }));
                }),
                destroy: function a() {
                    v();
                },
            };
        };
        var e$ = function (e) {
                var t =
                        arguments.length > 1 && arguments[1] !== void 0
                            ? arguments[1]
                            : {},
                    r = arguments.length > 2 ? arguments[2] : void 0;
                var n = document.createElement(e),
                    a = t.style,
                    o = $(t, ["style"]);
                return (
                    a &&
                        Object.entries(a).forEach(function (e) {
                            var t = k(e, 2),
                                r = t[0],
                                a = t[1];
                            n.style[r] = a;
                        }),
                    Object.entries(o).forEach(function (e) {
                        var t = k(e, 2),
                            r = t[0],
                            a = t[1];
                        n[r] = a;
                    }),
                    r &&
                        r.forEach(function (e) {
                            n.appendChild(e);
                        }),
                    n
                );
            },
            ew = function (e) {
                var t = document.createElement("style");
                ((t.innerText = e), document.head.appendChild(t));
            };
        var eb = function (e) {
            return (
                Object.keys(e).forEach(function (t) {
                    e[t] || delete e[t];
                }),
                e
            );
        };
        var eP = function (e) {
            return function (t) {
                return e.replace(/{\s*(\w+)\s*}/g, function (e, r) {
                    if (r in t) return t[r];
                    throw new Error("Unknown placeholder ".concat(r));
                });
            };
        };
        ew(
            "\nhtml, body {\n  -webkit-overflow-scrolling: touch !important;\n}\nbody.activity-iframe-open {\n  position: fixed;\n  width: 100%;\n}\n.activity-iframe-wrapper {\n  width: 100%;\n  height: 100%;\n  visibility: hidden;\n  position: fixed;\n  left: -5000px;\n  top: 0;\n  z-index: 99999999;\n  border: 0;\n  -webkit-overflow-scrolling: touch !important;\n  overflow-y: scroll;\n}\n.activity-iframe-wrapper.open {\n  left: 0;\n  visibility: visible;\n}\n.activity-iframe-wrapper iframe {\n  width: 100%;\n  height: 101%;\n  min-height: calc(100% + 1px);\n  z-index: 99999999;\n}\n\n.activity-iframe-wrapper.pagedoo-pc {\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  background: rgba(0,0,0,0.7);\n}\n.activity-iframe-wrapper.pagedoo-pc iframe {\n  width: 880px;\n  height: 820px;\n  min-height: 820px;\n  z-index: 99999999;\n}\n",
        );
        var ek = (function (t) {
                s(n, t);
                var r = C(n);
                function n() {
                    a(this, n);
                    var e;
                    e = r.call.apply(
                        r,
                        [this].concat(Array.prototype.slice.call(arguments)),
                    );
                    e.emitter = new W.TinyEmitter();
                    e.messageQueue = [];
                    e.wrapperClassName = "activity-iframe-wrapper";
                    e.messageInterval = 0;
                    return e;
                }
                u(n, [
                    {
                        key: "preload",
                        value: function t(r) {
                            var n = this;
                            (this.beforePreload(r),
                                (this.messageQueue = []),
                                (this.emitter = new W.TinyEmitter()));
                            var a = r.debug,
                                o = r.mpgoConfig;
                            (o === null || o === void 0
                                ? void 0
                                : o.urlTemplate) &&
                                (this.urlTemplate =
                                    o === null || o === void 0
                                        ? void 0
                                        : o.urlTemplate);
                            var u = this.getActivityUrl(r);
                            ((this.activityUrl = u),
                                (this.iframeRef =
                                    this.iframeRef ||
                                    e$(
                                        "iframe",
                                        g(
                                            y(
                                                {
                                                    frameBorder: "0",
                                                    scrolling: "yes",
                                                    width: "100%",
                                                    height: "100%",
                                                },
                                                e()
                                                    ? {}
                                                    : o === null || o === void 0
                                                      ? void 0
                                                      : o.iframeProps,
                                            ),
                                            {
                                                style: e()
                                                    ? {}
                                                    : o === null || o === void 0
                                                      ? void 0
                                                      : o.iframeStyle,
                                            },
                                        ),
                                    )),
                                (this.iframeRef.src = u),
                                (this.iframeWrapper = e$(
                                    "div",
                                    {
                                        className: this.wrapperClassName,
                                        style:
                                            (o === null || o === void 0
                                                ? void 0
                                                : o.wrapperStyle) || {},
                                    },
                                    [this.iframeRef],
                                )),
                                document.body.appendChild(this.iframeWrapper));
                            var c = eg({
                                iframe: this.iframeRef,
                                methods: {
                                    notify: function (e) {
                                        for (
                                            var t = arguments.length,
                                                r = new Array(
                                                    t > 1 ? t - 1 : 0,
                                                ),
                                                o = 1;
                                            o < t;
                                            o++
                                        ) {
                                            r[o - 1] = arguments[o];
                                        }
                                        var u, c;
                                        (a &&
                                            (u = console).log.apply(
                                                u,
                                                [
                                                    "[MidasbuyActivity "
                                                        .concat(
                                                            n.name,
                                                            "] API received event: ",
                                                        )
                                                        .concat(e),
                                                ].concat(x(r)),
                                            ),
                                            (c = n.emitter).emit.apply(
                                                c,
                                                [e].concat(x(r)),
                                            ));
                                    },
                                },
                            });
                            return (
                                (this.connection = c),
                                this.startFlushMessageQueue(),
                                this.setupListeners(),
                                this
                            );
                        },
                    },
                    {
                        key: "on",
                        value: function e(t, r) {
                            return (this.emitter.on(t, r), this);
                        },
                    },
                    {
                        key: "once",
                        value: function e(t, r) {
                            return (this.emitter.once(t, r), this);
                        },
                    },
                    {
                        key: "off",
                        value: function e(t, r) {
                            return (this.emitter.off(t, r), this);
                        },
                    },
                    {
                        key: "emit",
                        value: function e(t) {
                            for (
                                var r = arguments.length,
                                    n = new Array(r > 1 ? r - 1 : 0),
                                    a = 1;
                                a < r;
                                a++
                            ) {
                                n[a - 1] = arguments[a];
                            }
                            return t === "show"
                                ? (this.show(), this)
                                : t === "hide"
                                  ? (this.hide(), this)
                                  : (this.pushToQueue.apply(
                                        this,
                                        [t].concat(x(n)),
                                    ),
                                    this);
                        },
                    },
                    {
                        key: "isVisible",
                        value: function e() {
                            return this.iframeRef
                                ? this.iframeRef.style.visibility === "visible"
                                : !1;
                        },
                    },
                    {
                        key: "show",
                        value: function e() {
                            !this.iframeWrapper ||
                                (document.body.classList.add(
                                    "activity-iframe-open",
                                ),
                                this.iframeWrapper.classList.add("open"),
                                this.pushToQueue("report", "show"));
                        },
                    },
                    {
                        key: "hide",
                        value: function e() {
                            !this.iframeWrapper ||
                                (document.body.classList.remove(
                                    "activity-iframe-open",
                                ),
                                this.iframeWrapper.classList.remove("open"),
                                this.pushToQueue("report", "hide"));
                        },
                    },
                    {
                        key: "close",
                        value: function e() {
                            var t;
                            !this.iframeWrapper ||
                                (document.body.classList.remove(
                                    "activity-iframe-open",
                                ),
                                this.iframeWrapper.classList.remove("open"),
                                (t = this.connection) === null || t === void 0
                                    ? void 0
                                    : t.destroy(),
                                this.stopFlushMessageQueue(),
                                (this.messageQueue = []),
                                (this.emitter = new W.TinyEmitter()),
                                Array.from(document.body.children).includes(
                                    this.iframeWrapper,
                                ) &&
                                    document.body.removeChild(
                                        this.iframeWrapper,
                                    ));
                        },
                    },
                    {
                        key: "reload",
                        value: function e() {
                            !this.iframeRef ||
                                (this.iframeRef.src = this.iframeRef.src);
                        },
                    },
                    { key: "beforePreload", value: function e(t) {} },
                    {
                        key: "getActivityUrl",
                        value: function e(t) {
                            throw new Error(
                                "getActivityUrl should be implemented!",
                            );
                        },
                    },
                    {
                        key: "pushToQueue",
                        value: function e() {
                            for (
                                var t = arguments.length,
                                    r = new Array(t),
                                    n = 0;
                                n < t;
                                n++
                            ) {
                                r[n] = arguments[n];
                            }
                            this.messageQueue.push(r);
                        },
                    },
                    {
                        key: "startFlushMessageQueue",
                        value: function e() {
                            var t = this;
                            var r;
                            (r = this.connection) === null || r === void 0
                                ? void 0
                                : r.promise.then(function (e) {
                                      t.messageInterval = window.setInterval(
                                          function () {
                                              if (t.messageQueue.length && e) {
                                                  var r = _(
                                                          t.messageQueue.shift(),
                                                      ),
                                                      n = r[0],
                                                      a = r.slice(1);
                                                  try {
                                                      var o;
                                                      (o = e).notify.apply(
                                                          o,
                                                          [n].concat(x(a)),
                                                      );
                                                  } catch (u) {}
                                              }
                                          },
                                          50,
                                      );
                                  });
                        },
                    },
                    {
                        key: "stopFlushMessageQueue",
                        value: function e() {
                            window.clearInterval(this.messageInterval);
                        },
                    },
                    {
                        key: "setupListeners",
                        value: function e() {
                            var t = this;
                            (this.on("hide", function () {
                                return t.hide();
                            }),
                                this.on("show", function () {
                                    return t.show();
                                }),
                                this.on("jump", function (e, t) {
                                    if (!!e) {
                                        if (t) return location.replace(e);
                                        location.href = e;
                                    }
                                }));
                        },
                    },
                ]);
                return n;
            })(W.TinyEmitter),
            e8 = (0, F.default)("debug") ? (0, F.default)("activity_url") : "",
            e_ = (function (e) {
                s(r, e);
                var t = C(r);
                function r() {
                    a(this, r);
                    var e;
                    e = t.call.apply(
                        t,
                        [this].concat(Array.prototype.slice.call(arguments)),
                    );
                    e.urlTemplate = e8 || "/apps/activity/views/{name}";
                    return e;
                }
                u(r, [
                    {
                        key: "getActivityUrl",
                        value: function e(t) {
                            var r = t.appid,
                                n = t.eventid,
                                a = t.from,
                                o = t.debug,
                                u = t.country,
                                c = t.urlQuery;
                            if (this.activityUrl) return this.activityUrl;
                            var l = eb(
                                y(
                                    {
                                        appid: r,
                                        eventid: n,
                                        from: a,
                                        debug: o,
                                        country: u,
                                    },
                                    c,
                                ),
                            );
                            return (0, D.default)(
                                l,
                                eP(this.urlTemplate)({ name: this.name }),
                            );
                        },
                    },
                ]);
                return r;
            })(ek),
            e7 = (function (e) {
                s(r, e);
                var t = C(r);
                function r() {
                    a(this, r);
                    var e;
                    e = t.call.apply(
                        t,
                        [this].concat(Array.prototype.slice.call(arguments)),
                    );
                    e.urlTemplate =
                        e8 ||
                        "https://{host}/act/{env}/{activity_id}/{terminal_id}-{language}/index.html?from={from}";
                    return e;
                }
                u(r, [
                    {
                        key: "getActivityUrl",
                        value: function e(t) {
                            var r = t.from,
                                n = t.activityId,
                                a = t.activityLanguage,
                                o = t.activityTerminalId,
                                u = t.debug,
                                c = t.country,
                                l = t.urlQuery;
                            if (this.activityUrl) return this.activityUrl;
                            if (n) {
                                var s =
                                        (0, F.default)("env") ||
                                        (L.default.get("midas_p_test")
                                            ? "verify"
                                            : "release"),
                                    f = eP(this.urlTemplate)({
                                        host: location.host,
                                        activity_id: n,
                                        from: r || "",
                                        env: s === "verify" ? "mpbox" : "mp",
                                        terminal_id: o || "mobile",
                                        language: a || "en",
                                    }),
                                    v = eb(
                                        y({ from: r, debug: u, country: c }, l),
                                    );
                                return (0, D.default)(v, f);
                            }
                            throw new Error(
                                "activityId is required for activity ".concat(
                                    this.name,
                                ),
                            );
                        },
                    },
                ]);
                return r;
            })(ek),
            ex = (function (t) {
                s(n, t);
                var r = C(n);
                function n() {
                    a(this, n);
                    var e;
                    e = r.call.apply(
                        r,
                        [this].concat(Array.prototype.slice.call(arguments)),
                    );
                    e.urlTemplate =
                        e8 ||
                        "https://{host}/act/{env}/{activity_id}/{terminal_id}/index.html?from={from}&lan={language}";
                    return e;
                }
                u(n, [
                    {
                        key: "beforePreload",
                        value: function t(r) {
                            var n;
                            (!e() || (0, F.default)("from_pc")) &&
                                ((this.wrapperClassName =
                                    "activity-iframe-wrapper pagedoo-pc"),
                                (this.iframeRef =
                                    this.iframeRef ||
                                    e$(
                                        "iframe",
                                        y(
                                            {
                                                frameBorder: "0",
                                                scrolling: "no",
                                                width: "880px",
                                                height: "820px",
                                            },
                                            (n = r.mpgoConfig) === null ||
                                                n === void 0
                                                ? void 0
                                                : n.iframeProps,
                                        ),
                                    )));
                        },
                    },
                    {
                        key: "getActivityUrl",
                        value: function e(t) {
                            var r = t.from,
                                n = t.activityId,
                                a = t.activityLanguage,
                                o = t.activityTerminalId,
                                u = t.debug,
                                c = t.country,
                                l = t.urlQuery,
                                s = t.mpgoConfig;
                            if (this.activityUrl) return this.activityUrl;
                            if (n) {
                                var f =
                                        (0, F.default)("env") ||
                                        (L.default.get("midas_p_test")
                                            ? "verify"
                                            : "release"),
                                    v = eP(this.urlTemplate)({
                                        host: location.host,
                                        activity_id: n,
                                        from: r || "",
                                        env:
                                            f === "verify"
                                                ? "verify-pagedoo"
                                                : "pagedoo",
                                        terminal_id: o || "mobile",
                                        language: a || "en",
                                    }),
                                    p = eb(
                                        y(
                                            { from: r, debug: u, country: c },
                                            l,
                                            s === null || s === void 0
                                                ? void 0
                                                : s.urlQuery,
                                        ),
                                    );
                                return (0, D.default)(p, v);
                            }
                            throw new Error(
                                "activityId is required for activity ".concat(
                                    this.name,
                                ),
                            );
                        },
                    },
                ]);
                return n;
            })(ek);
        var eS = (function (e) {
                s(r, e);
                var t = C(r);
                function r() {
                    a(this, r);
                    var e;
                    e = t.call.apply(
                        t,
                        [this].concat(Array.prototype.slice.call(arguments)),
                    );
                    e.name = "cumulativeRecharge";
                    return e;
                }
                return r;
            })(e_),
            eR = (function (e) {
                s(r, e);
                var t = C(r);
                function r() {
                    a(this, r);
                    var e;
                    e = t.call.apply(
                        t,
                        [this].concat(Array.prototype.slice.call(arguments)),
                    );
                    e.name = "cumulativeRecharge";
                    return e;
                }
                return r;
            })(ex),
            eT = (function (t) {
                s(n, t);
                var r = C(n);
                function n() {
                    a(this, n);
                    var e;
                    e = r.call.apply(
                        r,
                        [this].concat(Array.prototype.slice.call(arguments)),
                    );
                    e.name = "cumulativeRecharge";
                    return e;
                }
                u(n, [
                    {
                        key: "beforePreload",
                        value: function t(r) {
                            if (
                                "activityId" in r &&
                                (!e() || (0, j.default)("from_pc"))
                            ) {
                                var n, a;
                                var o = Math.round(window.innerWidth * 0.56),
                                    u =
                                        ((n = r.mpgoConfig) === null ||
                                        n === void 0
                                            ? void 0
                                            : n.width) || o,
                                    c =
                                        ((a = r.mpgoConfig) === null ||
                                        a === void 0
                                            ? void 0
                                            : a.height) || Math.round(u * 0.59);
                                ((this.wrapperClassName =
                                    "activity-iframe-wrapper pagedoo-pc"),
                                    (this.iframeRef =
                                        this.iframeRef ||
                                        e$("iframe", {
                                            frameBorder: "0",
                                            scrolling: "no",
                                            width: "".concat(u, "px"),
                                            height: "".concat(c, "px"),
                                            style: {
                                                width: "".concat(u, "px"),
                                                height: "".concat(c, "px"),
                                                minHeight: "".concat(c, "px"),
                                            },
                                        })));
                            }
                        },
                    },
                    {
                        key: "getActivityUrl",
                        value: function e(t) {
                            if ("activityId" in t)
                                return new eR().getActivityUrl(t);
                            if ("appid" in t) return new eS().getActivityUrl(t);
                            throw new Error("Invalid preload parameter.");
                        },
                    },
                ]);
                return n;
            })(ek);
        var eC = h(T()),
            eE = h(A());
        var eM = (function (e) {
            s(r, e);
            var t = C(r);
            function r() {
                a(this, r);
                var e;
                e = t.call.apply(
                    t,
                    [this].concat(Array.prototype.slice.call(arguments)),
                );
                e.name = "pubgmReturn";
                return e;
            }
            return r;
        })(e7);
        var eI = (function (e) {
            s(r, e);
            var t = C(r);
            function r() {
                a(this, r);
                var e;
                e = t.call(this);
                e.name = "PubgmSeasonTopup";
                e.on("jump", function (e, t) {
                    if (!!e) {
                        if (t) return location.replace(e);
                        location.href = e;
                    }
                });
                return e;
            }
            return r;
        })(e7);
        var eO = (function (e) {
            s(r, e);
            var t = C(r);
            function r() {
                a(this, r);
                var e;
                e = t.call.apply(
                    t,
                    [this].concat(Array.prototype.slice.call(arguments)),
                );
                e.name = "PagedooSeasonTopup";
                return e;
            }
            return r;
        })(ex);
        var eA = (function (e) {
            s(r, e);
            var t = C(r);
            function r() {
                a(this, r);
                var e;
                e = t.call.apply(
                    t,
                    [this].concat(Array.prototype.slice.call(arguments)),
                );
                e.name = "PagedooCommon";
                return e;
            }
            return r;
        })(ex);
        var eU = (function () {
                function e() {
                    a(this, e);
                }
                u(e, [
                    {
                        key: "getValidEvent",
                        value: function e(r) {
                            return t({
                                url: "/apps/activity/api/activity-initialize/valid-events",
                                param: r,
                            }).then(function (e) {
                                if (e.ret === 0) return e.data;
                                throw new Error(e.msg);
                            });
                        },
                    },
                    {
                        key: "getManyValidEvents",
                        value: function e(r) {
                            return t({
                                url: "/apps/activity/api/activity-initialize/many-valid-events",
                                param: r,
                            }).then(function (e) {
                                if (e.ret === 0) return e.data;
                                throw new Error(e.msg);
                            });
                        },
                    },
                ]);
                return e;
            })(),
            eN = {
                api: new eU(),
                cumulativeRecharge: new eT(),
                pubgmReturn: new eM(),
                pubgmSeasonTopup: new eI(),
                pagedooSeasonTopup: new eO(),
                pagedooCommon: new eA(),
            };
        window.midasbuyActivity = { default: eN };
        return m(Q);
    })();
})(); //# sourceMappingURL=api.global.js.map
