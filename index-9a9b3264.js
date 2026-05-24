function e() {
    (import.meta.url, import("_").catch(() => 1));
}
function t(e) {
    return e &&
        e.__esModule &&
        Object.prototype.hasOwnProperty.call(e, "default")
        ? e.default
        : e;
}
!(function () {
    const e = document.createElement("link").relList;
    if (!(e && e.supports && e.supports("modulepreload"))) {
        for (const e of document.querySelectorAll('link[rel="modulepreload"]'))
            t(e);
        new MutationObserver((e) => {
            for (const n of e)
                if ("childList" === n.type)
                    for (const e of n.addedNodes)
                        "LINK" === e.tagName &&
                            "modulepreload" === e.rel &&
                            t(e);
        }).observe(document, { childList: !0, subtree: !0 });
    }
    function t(e) {
        if (e.ep) return;
        e.ep = !0;
        const t = (function (e) {
            const t = {};
            return (
                e.integrity && (t.integrity = e.integrity),
                e.referrerPolicy && (t.referrerPolicy = e.referrerPolicy),
                "use-credentials" === e.crossOrigin
                    ? (t.credentials = "include")
                    : "anonymous" === e.crossOrigin
                      ? (t.credentials = "omit")
                      : (t.credentials = "same-origin"),
                t
            );
        })(e);
        fetch(e.href, t);
    }
})();
var n = { exports: {} },
    r = {},
    o = window.React,
    i = 60103;
if (((r.Fragment = 60107), "function" == typeof Symbol && Symbol.for)) {
    var a = Symbol.for;
    ((i = a("react.element")), (r.Fragment = a("react.fragment")));
}
var c = o.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner,
    s = Object.prototype.hasOwnProperty,
    u = { key: !0, ref: !0, __self: !0, __source: !0 };
function l(e, t, n) {
    var r,
        o = {},
        a = null,
        l = null;
    for (r in (void 0 !== n && (a = "" + n),
    void 0 !== t.key && (a = "" + t.key),
    void 0 !== t.ref && (l = t.ref),
    t))
        s.call(t, r) && !u.hasOwnProperty(r) && (o[r] = t[r]);
    if (e && e.defaultProps)
        for (r in (t = e.defaultProps)) void 0 === o[r] && (o[r] = t[r]);
    return {
        $$typeof: i,
        type: e,
        key: a,
        ref: l,
        props: o,
        _owner: c.current,
    };
}
((r.jsx = l), (r.jsxs = l), (n.exports = r));
var f = n.exports;
function p(e) {
    return (
        null != e &&
        "object" == typeof e &&
        !0 === e["@@functional/placeholder"]
    );
}
function d(e) {
    return function t(n) {
        return 0 === arguments.length || p(n) ? t : e.apply(this, arguments);
    };
}
function m(e) {
    return function t(n, r) {
        switch (arguments.length) {
            case 0:
                return t;
            case 1:
                return p(n)
                    ? t
                    : d(function (t) {
                          return e(n, t);
                      });
            default:
                return p(n) && p(r)
                    ? t
                    : p(n)
                      ? d(function (t) {
                            return e(t, r);
                        })
                      : p(r)
                        ? d(function (t) {
                              return e(n, t);
                          })
                        : e(n, r);
        }
    };
}
const h =
    Array.isArray ||
    function (e) {
        return (
            null != e &&
            e.length >= 0 &&
            "[object Array]" === Object.prototype.toString.call(e)
        );
    };
function v(e, t) {
    return Object.prototype.hasOwnProperty.call(t, e);
}
var y = Object.prototype.toString;
const g = (function () {
    return "[object Arguments]" === y.call(arguments)
        ? function (e) {
              return "[object Arguments]" === y.call(e);
          }
        : function (e) {
              return v("callee", e);
          };
})();
var w = !{ toString: null }.propertyIsEnumerable("toString"),
    b = [
        "constructor",
        "valueOf",
        "isPrototypeOf",
        "toString",
        "propertyIsEnumerable",
        "hasOwnProperty",
        "toLocaleString",
    ],
    _ = (function () {
        return arguments.propertyIsEnumerable("length");
    })(),
    E = function (e, t) {
        for (var n = 0; n < e.length; ) {
            if (e[n] === t) return !0;
            n += 1;
        }
        return !1;
    };
const O =
    "function" != typeof Object.keys || _
        ? d(function (e) {
              if (Object(e) !== e) return [];
              var t,
                  n,
                  r = [],
                  o = _ && g(e);
              for (t in e)
                  !v(t, e) || (o && "length" === t) || (r[r.length] = t);
              if (w)
                  for (n = b.length - 1; n >= 0; )
                      (v((t = b[n]), e) && !E(r, t) && (r[r.length] = t),
                          (n -= 1));
              return r;
          })
        : d(function (e) {
              return Object(e) !== e ? [] : Object.keys(e);
          });
const S = d(function (e) {
    return null == e;
});
const A = d(function (e) {
    return null === e
        ? "Null"
        : void 0 === e
          ? "Undefined"
          : Object.prototype.toString.call(e).slice(8, -1);
});
function P(e, t, n, r) {
    var o,
        i = function (o) {
            for (var i = t.length, a = 0; a < i; ) {
                if (e === t[a]) return n[a];
                a += 1;
            }
            for (var c in ((t[a + 1] = e), (n[a + 1] = o), e))
                o[c] = r ? P(e[c], t, n, !0) : e[c];
            return o;
        };
    switch (A(e)) {
        case "Object":
            return i({});
        case "Array":
            return i([]);
        case "Date":
            return new Date(e.valueOf());
        case "RegExp":
            return (
                (o = e),
                new RegExp(
                    o.source,
                    (o.global ? "g" : "") +
                        (o.ignoreCase ? "i" : "") +
                        (o.multiline ? "m" : "") +
                        (o.sticky ? "y" : "") +
                        (o.unicode ? "u" : ""),
                )
            );
        default:
            return e;
    }
}
const C = d(function (e) {
    return null != e && "function" == typeof e.clone
        ? e.clone()
        : P(e, [], [], !0);
});
function x(e) {
    for (var t, n = []; !(t = e.next()).done; ) n.push(t.value);
    return n;
}
function I(e, t, n) {
    for (var r = 0, o = n.length; r < o; ) {
        if (e(t, n[r])) return !0;
        r += 1;
    }
    return !1;
}
const T =
    "function" == typeof Object.is
        ? Object.is
        : function (e, t) {
              return e === t ? 0 !== e || 1 / e == 1 / t : e != e && t != t;
          };
function j(e, t, n, r) {
    var o = x(e);
    function i(e, t) {
        return k(e, t, n.slice(), r.slice());
    }
    return !I(
        function (e, t) {
            return !I(i, t, e);
        },
        x(t),
        o,
    );
}
function k(e, t, n, r) {
    if (T(e, t)) return !0;
    var o,
        i,
        a = A(e);
    if (a !== A(t)) return !1;
    if (null == e || null == t) return !1;
    if (
        "function" == typeof e["fantasy-land/equals"] ||
        "function" == typeof t["fantasy-land/equals"]
    )
        return (
            "function" == typeof e["fantasy-land/equals"] &&
            e["fantasy-land/equals"](t) &&
            "function" == typeof t["fantasy-land/equals"] &&
            t["fantasy-land/equals"](e)
        );
    if ("function" == typeof e.equals || "function" == typeof t.equals)
        return (
            "function" == typeof e.equals &&
            e.equals(t) &&
            "function" == typeof t.equals &&
            t.equals(e)
        );
    switch (a) {
        case "Arguments":
        case "Array":
        case "Object":
            if (
                "function" == typeof e.constructor &&
                "Promise" ===
                    ((o = e.constructor),
                    null == (i = String(o).match(/^function (\w*)/))
                        ? ""
                        : i[1])
            )
                return e === t;
            break;
        case "Boolean":
        case "Number":
        case "String":
            if (typeof e != typeof t || !T(e.valueOf(), t.valueOf())) return !1;
            break;
        case "Date":
            if (!T(e.valueOf(), t.valueOf())) return !1;
            break;
        case "Error":
            return e.name === t.name && e.message === t.message;
        case "RegExp":
            if (
                e.source !== t.source ||
                e.global !== t.global ||
                e.ignoreCase !== t.ignoreCase ||
                e.multiline !== t.multiline ||
                e.sticky !== t.sticky ||
                e.unicode !== t.unicode
            )
                return !1;
    }
    for (var c = n.length - 1; c >= 0; ) {
        if (n[c] === e) return r[c] === t;
        c -= 1;
    }
    switch (a) {
        case "Map":
            return (
                e.size === t.size &&
                j(e.entries(), t.entries(), n.concat([e]), r.concat([t]))
            );
        case "Set":
            return (
                e.size === t.size &&
                j(e.values(), t.values(), n.concat([e]), r.concat([t]))
            );
        case "Arguments":
        case "Array":
        case "Object":
        case "Boolean":
        case "Number":
        case "String":
        case "Date":
        case "Error":
        case "RegExp":
        case "Int8Array":
        case "Uint8Array":
        case "Uint8ClampedArray":
        case "Int16Array":
        case "Uint16Array":
        case "Int32Array":
        case "Uint32Array":
        case "Float32Array":
        case "Float64Array":
        case "ArrayBuffer":
            break;
        default:
            return !1;
    }
    var s = O(e);
    if (s.length !== O(t).length) return !1;
    var u = n.concat([e]),
        l = r.concat([t]);
    for (c = s.length - 1; c >= 0; ) {
        var f = s[c];
        if (!v(f, t) || !k(t[f], e[f], u, l)) return !1;
        c -= 1;
    }
    return !0;
}
const R = m(function (e, t) {
    return k(e, t, [], []);
});
const N = d(function (e) {
    return null != e && "function" == typeof e["fantasy-land/empty"]
        ? e["fantasy-land/empty"]()
        : null != e &&
            null != e.constructor &&
            "function" == typeof e.constructor["fantasy-land/empty"]
          ? e.constructor["fantasy-land/empty"]()
          : null != e && "function" == typeof e.empty
            ? e.empty()
            : null != e &&
                null != e.constructor &&
                "function" == typeof e.constructor.empty
              ? e.constructor.empty()
              : h(e)
                ? []
                : (function (e) {
                        return (
                            "[object String]" ===
                            Object.prototype.toString.call(e)
                        );
                    })(e)
                  ? ""
                  : (function (e) {
                          return (
                              "[object Object]" ===
                              Object.prototype.toString.call(e)
                          );
                      })(e)
                    ? {}
                    : g(e)
                      ? (function () {
                            return arguments;
                        })()
                      : void 0;
});
const M = d(function (e) {
    return null != e && R(e, N(e));
});
function L(e) {
    var t = typeof e;
    return (
        e &&
        "string" !== t &&
        "number" !== t &&
        "boolean" !== t &&
        "function" !== t &&
        !Array.isArray(e)
    );
}
function $(e) {
    return e + "px";
}
function H(e) {
    return "auto" === e ? "auto" : e + "px";
}
function D(e) {
    return e + "%";
}
function U(e, t) {
    return "string" != typeof t && t
        ? "percent" === e
            ? t.toFixed(2) + "%"
            : "px" !== e && e
              ? void 0
              : t.toFixed(0) + "px"
        : t;
}
function V(e) {
    return "__impage-component-wrapper-" + e;
}
function G(e) {
    return "__impage-hotarea-wrapper-" + e;
}
var W =
        (window && window.__assign) ||
        function () {
            return (
                (W =
                    Object.assign ||
                    function (e) {
                        for (var t, n = 1, r = arguments.length; n < r; n++)
                            for (var o in (t = arguments[n]))
                                Object.prototype.hasOwnProperty.call(t, o) &&
                                    (e[o] = t[o]);
                        return e;
                    }),
                W.apply(this, arguments)
            );
        },
    z =
        (window && window.__rest) ||
        function (e, t) {
            var n = {};
            for (var r in e)
                Object.prototype.hasOwnProperty.call(e, r) &&
                    t.indexOf(r) < 0 &&
                    (n[r] = e[r]);
            if (
                null != e &&
                "function" == typeof Object.getOwnPropertySymbols
            ) {
                var o = 0;
                for (r = Object.getOwnPropertySymbols(e); o < r.length; o++)
                    t.indexOf(r[o]) < 0 &&
                        Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
                        (n[r[o]] = e[r[o]]);
            }
            return n;
        };
function B(e) {
    var t,
        n = e.size,
        r = e.transform,
        o = e.text,
        i = e.border,
        a = e.background,
        c = e.margin,
        s = e.padding,
        u = e.zIndex,
        l = e.cursor,
        f = z(e, [
            "size",
            "transform",
            "text",
            "border",
            "background",
            "margin",
            "padding",
            "zIndex",
            "cursor",
        ]);
    if (
        (n &&
            (n.autoWidth
                ? (f.maxWidth = "100%")
                : (f.width = U(n.widthUnit, n.width)),
            n.autoHeight || (f.height = U(n.heightUnit, n.height))),
        r)
    ) {
        var p = r.rotate,
            d = r.opacity,
            m = r.scale,
            h = r.radius;
        (((p && 0 !== p) || (m && 1 !== m)) &&
            (f.transform =
                (p ? "rotate(" + p + "deg) " : "") +
                (m ? "scale(" + m + ")" : "")),
            d && d < 1 && (f.opacity = d),
            h && h > 0 && (f.borderRadius = h + "px"));
    }
    if (c) {
        var v = c.top,
            y = c.right,
            g = c.bottom,
            w = c.left;
        (0 === v && 0 === y && 0 === g && 0 === w) ||
            (f.margin = [v, y, g, w].map(H).join(" "));
    }
    if (s) {
        var b = s.top;
        ((y = s.right), (g = s.bottom), (w = s.left));
        (0 === b && 0 === y && 0 === g && 0 === w) ||
            (f.padding = [b, y, g, w].map($).join(" "));
    }
    if (
        ("number" == typeof u && (f.zIndex = u),
        "string" == typeof l && (f.cursor = l),
        o &&
            ((f.color = o.color),
            (f.fontSize = o.fontSize + "px"),
            (f.lineHeight = o.lineHeight + "px"),
            (f.textAlign = o.textAlign),
            (f.fontWeight = o.weight)),
        i)
    ) {
        var _ = i.type,
            E = i.color,
            O = i.width;
        O > 0 && (f.border = O + "px " + _ + " " + E);
    }
    if (a) {
        E = a.color;
        var A = a.image,
            P = a.size,
            C = a.repeat,
            x = a.position;
        ((f.backgroundColor = E),
            ("string" == typeof (t = A)
                ? !t.trim()
                : M(t) || S(t) || Number.isNaN(t)) ||
                (f.backgroundImage = "url(" + A + ")"),
            (f.backgroundRepeat = C),
            (f.backgroundSize = P),
            (f.backgroundPosition = x));
    }
    return f;
}
var F = { top: 0, left: 0, bottom: 0, right: 0 };
W(W({}, F), { left: "auto", right: "auto" });
var K = new Map();
function J(e) {
    return K.get(e) || document.getElementById(V(e));
}
"undefined" == typeof window ||
    window.__componentInstanceNodeMap ||
    Object.defineProperty(window, "__componentInstanceNodeMap", {
        get: function () {
            return K;
        },
    });
var q,
    X = new Map();
"undefined" == typeof window ||
    window.__hotAreaInstanceNodeMap ||
    Object.defineProperty(window, "__hotAreaInstanceNodeMap", {
        get: function () {
            return X;
        },
    });
var Y = new Map(),
    Q = new Map();
function Z(e, t, n) {
    var r,
        o = function (e, t) {
            null == e ||
                e.forEach(function (e, n) {
                    var r = e.key,
                        i = e.children,
                        a = e.actions;
                    (!(function (e, t, n) {
                        Y.set(e, { index: t, parentKey: n });
                    })(r, n, t),
                        a.forEach(function (e) {
                            !(function (e, t) {
                                Q.set(e, t);
                            })(e.key, e);
                        }),
                        i && o(i, r));
                });
        };
    ("number" == typeof n && ((r = n), Y.delete(r)), o(e, t));
}
function ee(e) {
    var t;
    ((q = e), (t = e), Y.clear(), Z(t));
}
function te(e, t) {
    var n,
        r = (function (e) {
            return Y.get(e);
        })(e);
    if (!r) return null;
    var o = r.index,
        i = r.parentKey,
        a = null != t ? t : q;
    if ("number" == typeof i) {
        var c = te(i, a);
        return null === (n = null == c ? void 0 : c.children) || void 0 === n
            ? void 0
            : n[o];
    }
    return a[o];
}
var ne, re, oe, ie, ae, ce;
(((re = ne || (ne = {})).INIT = "__impage_action_trigger_init"),
    (re.CLICK = "__impage_action_trigger_click"),
    (re.MOUSE_ENTER = "__impage_action_trigger_mouseEnter"),
    (re.MOUSE_LEAVE = "__impage_action_trigger_mouseLeave"),
    (re.DOUBLE_CLICK = "__impage_action_trigger_double_click"),
    (re.LONG_PRESS = "__impage_action_trigger_long_press"),
    (re.ENTER_VIEW = "__impage_action_trigger_enter_view"),
    (re.LEAVE_VIEW = "__impage_action_trigger_leave_view"),
    ((ie = oe || (oe = {})).COMMON = "common"),
    (ie.BUSINESS = "business"),
    (ie.COMPONENT = "component"),
    ((ce = ae || (ae = {})).INIT = "afterRender"),
    (ce.CLICK = "click"),
    (ce.MOUSE_ENTER = "mouseEnter"),
    (ce.MOUSE_LEAVE = "mouseLeave"),
    (ce.DOUBLE_CLICK = "doubleClick"),
    (ce.LONG_PRESS = "longPress"),
    (ce.ENTER_VIEW = "enterView"),
    (ce.LEAVE_VIEW = "leaveView"));
var se,
    ue,
    le,
    fe,
    pe,
    de,
    me = ae;
(((ue = se || (se = {})).PAGE = "page"),
    (ue.COMPONENT = "component"),
    (ue.HOT_AREA = "hotarea"),
    (ue.PLUGIN = "plugin"),
    (ue.ACTION = "action"),
    ((fe = le || (le = {})).INIT = "afterRender"),
    (fe.CLOSE = "close"),
    ((pe || (pe = {})).EXEC = "exec"),
    ((de || (de = {})).EXEC = "exec"));
var he =
        (window && window.__read) ||
        function (e, t) {
            var n = "function" == typeof Symbol && e[Symbol.iterator];
            if (!n) return e;
            var r,
                o,
                i = n.call(e),
                a = [];
            try {
                for (; (void 0 === t || t-- > 0) && !(r = i.next()).done; )
                    a.push(r.value);
            } catch (c) {
                o = { error: c };
            } finally {
                try {
                    r && !r.done && (n = i.return) && n.call(i);
                } finally {
                    if (o) throw o.error;
                }
            }
            return a;
        },
    ve =
        (window && window.__spreadArray) ||
        function (e, t) {
            for (var n = 0, r = t.length, o = e.length; n < r; n++, o++)
                e[o] = t[n];
            return e;
        },
    ye = function () {
        var e = this;
        ((this.proxies = {}),
            (this.onceProxies = {}),
            (this.on = function (t, n) {
                if (e.proxies[t]) return e.proxies[t].push(n);
                e.proxies[t] = [n];
            }),
            (this.only = function (t, n) {
                e.proxies[t] = [n];
            }),
            (this.once = function (t, n) {
                if (e.onceProxies[t]) return e.onceProxies[t].push(n);
                e.onceProxies[t] = [n];
            }),
            (this.emit = function (t) {
                for (var n = [], r = 1; r < arguments.length; r++)
                    n[r - 1] = arguments[r];
                (e.proxies[t] &&
                    e.proxies[t].forEach(function (e) {
                        return e.apply(void 0, ve([], he(n)));
                    }),
                    e.onceProxies[t] &&
                        (e.onceProxies[t].forEach(function (e) {
                            return e.apply(void 0, ve([], he(n)));
                        }),
                        (e.onceProxies[t] = [])));
            }),
            (this.cancel = function (t, n) {
                e.proxies[t] &&
                    (e.proxies[t] = e.proxies[t].filter(function (e) {
                        return e !== n;
                    }));
            }),
            (this.cancelOnce = function (t, n) {
                e.onceProxies[t] &&
                    (e.onceProxies[t] = e.onceProxies[t].filter(function (e) {
                        return e !== n;
                    }));
            }),
            (this.cancelAll = function (t) {
                e.proxies[t] && (e.proxies[t] = []);
            }),
            (this.cancelAllOnce = function (t) {
                e.onceProxies[t] && (e.onceProxies[t] = []);
            }),
            (this.clear = function () {
                ((e.proxies = {}), (e.onceProxies = {}));
            }));
    };
function ge(e) {
    var t = e.key,
        n = e.component,
        r = n.id,
        o = n.info,
        i = n.name,
        a = n.projId,
        c = n.projKey;
    return {
        key: t,
        id: r,
        info: o,
        name: i,
        projId: a,
        projKey: c,
        get node() {
            return J(t);
        },
    };
}
function we(e, t) {
    var n = e.key,
        r = e.position,
        o = e.size;
    return {
        key: n,
        position: r,
        size: o,
        parent: ge(t),
        get node() {
            return (function (e) {
                return X.get(e) || document.getElementById(G(e));
            })(n);
        },
    };
}
function be(e, t, n, r) {
    var o = e.data;
    return {
        key: e.key,
        data: o,
        triggerEventType: e.trigger.replace("__impage_action_trigger_", ""),
        trigger: { type: "component", component: ge(t) },
        meta: r,
        global: n,
        componentsMap: K,
        getComponentByKey: J,
    };
}
function _e(e, t, n, r, o) {
    var i = be(e, n, r, o);
    return ((i.trigger.type = "hotarea"), (i.trigger.hotarea = we(t, n)), i);
}
function Ee(e, t, n, r, o) {
    var i = ge(r),
        a = o ? we(o, r) : void 0;
    return {
        meta: n,
        global: t,
        triggerEventType: e,
        trigger: {
            type: o ? "hotarea" : "component",
            component: i,
            hotarea: a,
        },
        component: i,
        hotArea: a,
    };
}
var Oe = new ye();
var Se = new ye();
function Ae(e, t) {
    Se.emit(e, t);
}
var Pe = new ye();
var Ce = new ye();
var xe,
    Ie,
    Te = new ye();
((xe = function (e, t) {
    var n,
        r = new Ie();
    return Promise.race([
        e,
        new Promise(function (e, o) {
            n = setTimeout(function () {
                o(r);
            }, t);
        }),
    ]).then(
        function (e) {
            return (clearTimeout(n), e);
        },
        function (e) {
            throw (clearTimeout(n), e);
        },
    );
}),
    ((Ie = function () {
        (Error.call(this),
            (this.stack = Error().stack),
            (this.message = "Timeout"));
    }).prototype = Object.create(Error.prototype)),
    (Ie.prototype.name = "TimeoutError"));
var je,
    ke,
    Re,
    Ne =
        (window && window.__awaiter) ||
        function (e, t, n, r) {
            return new (n || (n = Promise))(function (o, i) {
                function a(e) {
                    try {
                        s(r.next(e));
                    } catch (t) {
                        i(t);
                    }
                }
                function c(e) {
                    try {
                        s(r.throw(e));
                    } catch (t) {
                        i(t);
                    }
                }
                function s(e) {
                    var t;
                    e.done
                        ? o(e.value)
                        : ((t = e.value),
                          t instanceof n
                              ? t
                              : new n(function (e) {
                                    e(t);
                                })).then(a, c);
                }
                s((r = r.apply(e, t || [])).next());
            });
        },
    Me =
        (window && window.__generator) ||
        function (e, t) {
            var n,
                r,
                o,
                i,
                a = {
                    label: 0,
                    sent: function () {
                        if (1 & o[0]) throw o[1];
                        return o[1];
                    },
                    trys: [],
                    ops: [],
                };
            return (
                (i = { next: c(0), throw: c(1), return: c(2) }),
                "function" == typeof Symbol &&
                    (i[Symbol.iterator] = function () {
                        return this;
                    }),
                i
            );
            function c(i) {
                return function (c) {
                    return (function (i) {
                        if (n)
                            throw new TypeError(
                                "Generator is already executing.",
                            );
                        for (; a; )
                            try {
                                if (
                                    ((n = 1),
                                    r &&
                                        (o =
                                            2 & i[0]
                                                ? r.return
                                                : i[0]
                                                  ? r.throw ||
                                                    ((o = r.return) &&
                                                        o.call(r),
                                                    0)
                                                  : r.next) &&
                                        !(o = o.call(r, i[1])).done)
                                )
                                    return o;
                                switch (
                                    ((r = 0),
                                    o && (i = [2 & i[0], o.value]),
                                    i[0])
                                ) {
                                    case 0:
                                    case 1:
                                        o = i;
                                        break;
                                    case 4:
                                        return (
                                            a.label++,
                                            { value: i[1], done: !1 }
                                        );
                                    case 5:
                                        (a.label++, (r = i[1]), (i = [0]));
                                        continue;
                                    case 7:
                                        ((i = a.ops.pop()), a.trys.pop());
                                        continue;
                                    default:
                                        if (
                                            !((o = a.trys),
                                            (o =
                                                o.length > 0 &&
                                                o[o.length - 1]) ||
                                                (6 !== i[0] && 2 !== i[0]))
                                        ) {
                                            a = 0;
                                            continue;
                                        }
                                        if (
                                            3 === i[0] &&
                                            (!o || (i[1] > o[0] && i[1] < o[3]))
                                        ) {
                                            a.label = i[1];
                                            break;
                                        }
                                        if (6 === i[0] && a.label < o[1]) {
                                            ((a.label = o[1]), (o = i));
                                            break;
                                        }
                                        if (o && a.label < o[2]) {
                                            ((a.label = o[2]), a.ops.push(i));
                                            break;
                                        }
                                        (o[2] && a.ops.pop(), a.trys.pop());
                                        continue;
                                }
                                i = t.call(e, a);
                            } catch (c) {
                                ((i = [6, c]), (r = 0));
                            } finally {
                                n = o = 0;
                            }
                        if (5 & i[0]) throw i[1];
                        return { value: i[0] ? i[1] : void 0, done: !0 };
                    })([i, c]);
                };
            }
        },
    Le =
        (window && window.__values) ||
        function (e) {
            var t = "function" == typeof Symbol && Symbol.iterator,
                n = t && e[t],
                r = 0;
            if (n) return n.call(e);
            if (e && "number" == typeof e.length)
                return {
                    next: function () {
                        return (
                            e && r >= e.length && (e = void 0),
                            { value: e && e[r++], done: !e }
                        );
                    },
                };
            throw new TypeError(
                t
                    ? "Object is not iterable."
                    : "Symbol.iterator is not defined.",
            );
        };
function $e(e, t, n, r) {
    var o = this;
    return function (i, a) {
        var c = a.meta,
            s = a.global;
        return Ne(o, void 0, void 0, function () {
            var o, a, u, l, f, p, d, m, h, v, y, g, w, b;
            return Me(this, function (_) {
                switch (_.label) {
                    case 0:
                        (_.trys.push([0, 10, 11, 12]),
                            (o = Le(e)),
                            (a = o.next()),
                            (_.label = 1));
                    case 1:
                        if (a.done) return [3, 9];
                        ((u = a.value),
                            (l = u.action),
                            (f = l.action),
                            (p = l.maxTimeout),
                            (d = void 0 === p ? 1e4 : p),
                            (m = u.target),
                            ((h = n
                                ? _e(u, n, t, s, c)
                                : be(u, t, s, c)).payload = r),
                            i && (h.originalEvent = i),
                            "number" == typeof m &&
                                (v = te(m)) &&
                                (h.target = ge(v)),
                            (y = "object" == typeof f ? f.action : f),
                            (_.label = 2));
                    case 2:
                        return (
                            _.trys.push([2, 7, , 8]),
                            "Infinity" !== d ? [3, 4] : [4, y(h)]
                        );
                    case 3:
                        return (_.sent(), [3, 6]);
                    case 4:
                        return [4, xe(Promise.resolve(y(h)), d)];
                    case 5:
                        (_.sent(), (_.label = 6));
                    case 6:
                        return [3, 8];
                    case 7:
                        return (_.sent(), [3, 8]);
                    case 8:
                        return ((a = o.next()), [3, 1]);
                    case 9:
                        return [3, 12];
                    case 10:
                        return ((g = _.sent()), (w = { error: g }), [3, 12]);
                    case 11:
                        try {
                            a && !a.done && (b = o.return) && b.call(o);
                        } finally {
                            if (w) throw w.error;
                        }
                        return [7];
                    case 12:
                        return [2];
                }
            });
        });
    };
}
function He(e, t, n, r) {
    if (e && e.length) {
        var o = e.filter(function (e) {
            return e.trigger === t;
        });
        if (o.length) return $e(o, n, r);
    }
}
function De(e, t, n) {
    var r = {},
        o = He(e, ne.INIT, t, n);
    o && (r.onInit = o);
    var i = He(e, ne.CLICK, t, n);
    i && (r.onClick = i);
    var a = He(e, ne.MOUSE_ENTER, t, n);
    a && (r.onMouseEnter = a);
    var c = He(e, ne.MOUSE_LEAVE, t, n);
    c && (r.onMouseLeave = c);
    var s = He(e, ne.DOUBLE_CLICK, t, n);
    s && (r.onDoubleClick = s);
    var u = He(e, ne.LONG_PRESS, t, n);
    u && (r.onLongPress = u);
    var l = He(e, ne.ENTER_VIEW, t, n);
    l && (r.onEnterView = l);
    var f = He(e, ne.LEAVE_VIEW, t, n);
    return (f && (r.onLeaveView = f), r);
}
(((ke = je || (je = {})).MANAGE_RESOURCE = "manage_resource"),
    (ke.MANAGE_HOT_AREA = "manage_hot_area"),
    (ke.MANAGE_HISTORY = "manage_history"),
    (ke.PREVIEW = "preview"),
    (ke.REFRESH_SIMULATOR = "refresh_simulator"),
    (ke.RELOAD_MATERIALS = "reload_materials"),
    (ke.SCROLL_TO_COMPONENT = "scroll_to_component"),
    (ke.JUMP_PROP_EDIT_TAB = "jump_prop_edit_tab"),
    (ke.COMPONENT_INTERSECTING_CHANGE = "component_intersecting_change"),
    (ke.HOT_AREA_INTERSECTING_CHANGE = "hot_area_intersecting_change"),
    (ke.CHANGE_PROP_EDIT_TAB = "change_prop_edit_tab"),
    (ke.SCROLL_SIMULATOR = "scroll_simulator"),
    (ke.SET_RULER_DISTANCE = "set_ruler_distance"),
    (ke.CAPTURE_COMPONENT_MASK_CLICK_CALLBACK =
        "capture_component_mask_click_handler"),
    (ke.ORIENTATION_CHANGE = "simulator_orientation_change"),
    ((Re || (Re = {})).ORIENTATION_CHANGE = "orientationchange"));
var Ue = new ye(),
    Ve = new Map();
function Ge(e) {
    return Ve.get(e);
}
var We = function (e) {
        var t,
            n,
            r,
            o = e.data,
            i = e.payload,
            a = e.target,
            c = o.actionName,
            s =
                ((t = null == a ? void 0 : a.key),
                (n = c),
                (r = Ge(t)) ? r.get(n) : null);
        return s
            ? Promise.all(
                  s.map(function (e) {
                      return Promise.resolve(e({ data: o, payload: i }));
                  }),
              )
            : Promise.resolve();
    },
    ze = Number.MAX_SAFE_INTEGER;
function Be(e, t, n) {
    switch (e) {
        case se.PAGE:
            return (function (e, t) {
                Se.on(e, t);
            })(t, n);
        case se.COMPONENT:
            return (function (e, t) {
                Oe.on(e, t);
            })(t, n);
        case se.HOT_AREA:
            return (function (e, t) {
                Pe.on(e, t);
            })(t, n);
        case se.PLUGIN:
            return (function (e, t) {
                Te.on(e, t);
            })(t, n);
        case se.ACTION:
            return (function (e, t) {
                Ce.on(e, t);
            })(t, n);
        default:
            throw new Error(
                "Invalid [target] " +
                    e +
                    ", must one of '" +
                    se.PAGE +
                    "', '" +
                    se.COMPONENT +
                    "', '" +
                    se.HOT_AREA +
                    "'",
            );
    }
}
function Fe(e) {
    return function (t) {
        return (t.persist(), e(t));
    };
}
var Ke = {},
    Je = function (e, t, n) {
        return (Ke[e] || (Ke[e] = n(t)), Ke[e]);
    };
function qe(e) {
    return "*" !== e && e
        ? {
              mainJS: `main.${e}.js`,
              mainCSS: `main.${e}.css`,
              metaJS: `meta.${e}.js`,
              metaCSS: `meta.${e}.css`,
          }
        : {
              mainJS: "main.js",
              mainCSS: "main.css",
              metaJS: "meta.js",
              metaCSS: "meta.css",
          };
}
var Xe,
    Ye,
    Qe =
        (window && window.__assign) ||
        function () {
            return (
                (Qe =
                    Object.assign ||
                    function (e) {
                        for (var t, n = 1, r = arguments.length; n < r; n++)
                            for (var o in (t = arguments[n]))
                                Object.prototype.hasOwnProperty.call(t, o) &&
                                    (e[o] = t[o]);
                        return e;
                    }),
                Qe.apply(this, arguments)
            );
        },
    Ze =
        (window && window.__rest) ||
        function (e, t) {
            var n = {};
            for (var r in e)
                Object.prototype.hasOwnProperty.call(e, r) &&
                    t.indexOf(r) < 0 &&
                    (n[r] = e[r]);
            if (
                null != e &&
                "function" == typeof Object.getOwnPropertySymbols
            ) {
                var o = 0;
                for (r = Object.getOwnPropertySymbols(e); o < r.length; o++)
                    t.indexOf(r[o]) < 0 &&
                        Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
                        (n[r[o]] = e[r[o]]);
            }
            return n;
        },
    et = function (e) {
        var t = e.action,
            n = Ze(e, ["action"]);
        return Qe(Qe({}, C(n)), { id: t.id });
    },
    tt = function (e) {
        var t = e.actions,
            n = Ze(e, ["actions"]);
        return Qe(Qe({}, C(n)), { actions: t.map(et) });
    },
    nt = function (e) {
        var t = e.children;
        e.parent;
        var n = e.component,
            r = e.actions,
            o = e.hotAreas,
            i = e.data,
            a = Ze(e, [
                "children",
                "parent",
                "component",
                "actions",
                "hotAreas",
                "data",
            ]),
            c = Qe(Qe({}, C(a)), { id: n.id, data: C(i), actions: r.map(et) });
        return (
            n.__implementHotArea &&
                o &&
                (c.data = Qe(Qe({}, i), {
                    hotAreas: o.map(tt),
                    __implementHotArea: !0,
                })),
            t &&
                (c.children = t.map(function (e) {
                    return nt(e);
                })),
            c
        );
    },
    rt = function (e) {
        e.plugin;
        var t = Ze(e, ["plugin"]);
        return C(t);
    },
    ot =
        (window && window.__assign) ||
        function () {
            return (
                (ot =
                    Object.assign ||
                    function (e) {
                        for (var t, n = 1, r = arguments.length; n < r; n++)
                            for (var o in (t = arguments[n]))
                                Object.prototype.hasOwnProperty.call(t, o) &&
                                    (e[o] = t[o]);
                        return e;
                    }),
                ot.apply(this, arguments)
            );
        },
    it =
        (window && window.__rest) ||
        function (e, t) {
            var n = {};
            for (var r in e)
                Object.prototype.hasOwnProperty.call(e, r) &&
                    t.indexOf(r) < 0 &&
                    (n[r] = e[r]);
            if (
                null != e &&
                "function" == typeof Object.getOwnPropertySymbols
            ) {
                var o = 0;
                for (r = Object.getOwnPropertySymbols(e); o < r.length; o++)
                    t.indexOf(r[o]) < 0 &&
                        Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
                        (n[r[o]] = e[r[o]]);
            }
            return n;
        };
(((Ye = Xe || (Xe = {})).ACTION = "actions"),
    (Ye.COMPONENT = "components"),
    (Ye.PLUGIN = "plugins"));
var at = function (e, t, n) {
        var r = n[e];
        return Array.isArray(r)
            ? r.find(function (e) {
                  return e.id === t;
              })
            : r instanceof Map
              ? r.get(t)
              : null == r
                ? void 0
                : r[t];
    },
    ct = function (e, t) {
        var n = e.id,
            r = e.name,
            o = at(Xe.ACTION, n, t) || at(Xe.ACTION, r, t);
        return (
            o ||
            ((function (e) {
                return e === ze;
            })(Number(n))
                ? { action: We, id: Number.MAX_SAFE_INTEGER }
                : void 0)
        );
    },
    st = function (e, t) {
        var n = e.id,
            r = e.name;
        return at(Xe.COMPONENT, n, t) || at(Xe.COMPONENT, r, t);
    },
    ut = function (e, t) {
        var n = e.id,
            r = e.name;
        return at(Xe.PLUGIN, n, t) || at(Xe.PLUGIN, r, t);
    },
    lt = function (e, t) {
        var n = e.commonStyle,
            r = e.wrapperStyle;
        if (!t) return { commonStyle: n, wrapperStyle: r };
        var o = {};
        if (n) {
            var i = (function (e) {
                var t = e.position;
                if ("object" != typeof t) return null;
                var n = {},
                    r = t,
                    o = r.outset,
                    i = r.top,
                    a = r.left,
                    c = r.bottom,
                    s = r.right,
                    u = r.unit,
                    l = r.type;
                n.position = "absolute" === l ? "absolute" : "fixed";
                var f = u || {};
                switch (o) {
                    case "TopLeft":
                        ((n.top = U(f.top, i)), (n.left = U(f.left, a)));
                        break;
                    case "TopRight":
                        ((n.top = U(f.top, i)), (n.right = U(f.right, s)));
                        break;
                    case "BottomRight":
                        ((n.bottom = U(f.bottom, c)),
                            (n.right = U(f.right, s)));
                        break;
                    case "BottomLeft":
                        ((n.bottom = U(f.bottom, c)), (n.left = U(f.left, a)));
                }
                return n;
            })(n);
            (i && (o = { position: i }),
                (o = ot(ot({}, o), { commonStyle: B(n) })));
        }
        return (r && (o = ot(ot({}, o), { wrapperStyle: B(r) })), o);
    },
    ft = function (e, t, n) {
        void 0 === n && (n = {});
        var r = n.renderStore,
            o = ct(e, t);
        if (!o) return null;
        var i = ot(ot({}, C(e)), { action: o });
        return (null == r || r.registerSchemaStore(o.store, i), i.key, i);
    },
    pt = function (e, t, n) {
        void 0 === n && (n = {});
        var r = e.actions,
            o = ot(ot({}, C(e)), {
                actions: r
                    .map(function (e) {
                        return ft(e, t, n);
                    })
                    .filter(function (e) {
                        return !!e;
                    }),
            });
        return (o.key, o);
    },
    dt = function (e, t, n) {
        var r;
        void 0 === n && (n = {});
        var o = e.actions,
            i = e.children,
            a = it(e, ["actions", "children"]),
            c = n.autoParseStyle,
            s = void 0 !== c && c,
            u = n.renderStore,
            l = n.parent,
            f = lt(e, s),
            p = st(e, t);
        if (!p) return null;
        var d = o
                .map(function (e) {
                    return ft(e, t, n);
                })
                .filter(function (e) {
                    return !!e;
                }),
            m = ot(ot(ot({}, C(a)), f), {
                parent: l,
                component: p,
                children: void 0,
                actions: d,
            });
        if (
            (Array.isArray(i) &&
                (m.children =
                    null !==
                        (r = i
                            .map(function (e) {
                                return dt(e, t, ot(ot({}, n), { parent: m }));
                            })
                            .filter(function (e) {
                                return !!e;
                            })) && void 0 !== r
                        ? r
                        : []),
            p.__implementHotArea)
        ) {
            var h = m.data.hotAreas;
            ((m.data.hotAreas =
                null == h
                    ? void 0
                    : h
                          .map(function (e) {
                              return pt(e, t, n);
                          })
                          .filter(function (e) {
                              return !!e;
                          })),
                (m.hotAreas = m.data.hotAreas));
        }
        return (null == u || u.registerSchemaStore(p.store, m), m.key, m);
    },
    mt = function (e, t) {
        var n = ut(e, t);
        if (!n) return null;
        var r = ot(ot({}, C(e)), { plugin: n });
        return (r.key, r);
    },
    ht = function (e, t, n) {
        void 0 === n && (n = {});
        var r = e.components,
            o = e.plugins,
            i = it(e, ["components", "plugins"]);
        return ot(
            {
                componentInstances: r
                    .map(function (e) {
                        return dt(e, t, n);
                    })
                    .filter(function (e) {
                        return !!e;
                    }),
                pluginInstances: o
                    .map(function (e) {
                        return mt(e, t);
                    })
                    .filter(function (e) {
                        return !!e;
                    }),
            },
            i,
        );
    },
    vt = function (e, t, n) {
        void 0 === n && (n = {});
        var r = n.renderStore,
            o = ct(e, t);
        return (
            o &&
                ((e.action = ot(ot({}, e.action), o)),
                null == r || r.registerSchemaStore(o.store, e)),
            e
        );
    },
    yt = function (e, t, n) {
        var r;
        void 0 === n && (n = {});
        var o = n.renderStore,
            i = st(e, t);
        return (
            i &&
                ((e.component = i),
                null == o || o.registerSchemaStore(i.store, e)),
            e.actions.length &&
                e.actions.forEach(function (e) {
                    return vt(e, t, n);
                }),
            (null === (r = e.children) || void 0 === r ? void 0 : r.length) &&
                e.children.forEach(function (e) {
                    return yt(e, t, n);
                }),
            e
        );
    },
    gt = function (e, t) {
        var n = ut(e, t);
        return (n && (e.plugin = n), e);
    };
const wt =
    "object" == typeof global && global && global.Object === Object && global;
var bt = "object" == typeof self && self && self.Object === Object && self;
const _t = wt || bt || Function("return this")();
const Et = _t.Symbol;
var Ot = Object.prototype,
    St = Ot.hasOwnProperty,
    At = Ot.toString,
    Pt = Et ? Et.toStringTag : void 0;
var Ct = Object.prototype.toString;
var xt = Et ? Et.toStringTag : void 0;
function It(e) {
    return null == e
        ? void 0 === e
            ? "[object Undefined]"
            : "[object Null]"
        : xt && xt in Object(e)
          ? (function (e) {
                var t = St.call(e, Pt),
                    n = e[Pt];
                try {
                    e[Pt] = void 0;
                    var r = !0;
                } catch (i) {}
                var o = At.call(e);
                return (r && (t ? (e[Pt] = n) : delete e[Pt]), o);
            })(e)
          : (function (e) {
                return Ct.call(e);
            })(e);
}
function Tt(e) {
    return (
        "symbol" == typeof e ||
        ((function (e) {
            return null != e && "object" == typeof e;
        })(e) &&
            "[object Symbol]" == It(e))
    );
}
const jt = Array.isArray;
var kt = Et ? Et.prototype : void 0,
    Rt = kt ? kt.toString : void 0;
function Nt(e) {
    if ("string" == typeof e) return e;
    if (jt(e))
        return (
            (function (e, t) {
                for (
                    var n = -1, r = null == e ? 0 : e.length, o = Array(r);
                    ++n < r;
                )
                    o[n] = t(e[n], n, e);
                return o;
            })(e, Nt) + ""
        );
    if (Tt(e)) return Rt ? Rt.call(e) : "";
    var t = e + "";
    return "0" == t && 1 / e == -Infinity ? "-0" : t;
}
function Mt(e) {
    var t = typeof e;
    return null != e && ("object" == t || "function" == t);
}
const Lt = _t["__core-js_shared__"];
var $t,
    Ht = ($t = /[^.]+$/.exec((Lt && Lt.keys && Lt.keys.IE_PROTO) || ""))
        ? "Symbol(src)_1." + $t
        : "";
var Dt = Function.prototype.toString;
var Ut = /^\[object .+?Constructor\]$/,
    Vt = Function.prototype,
    Gt = Object.prototype,
    Wt = Vt.toString,
    zt = Gt.hasOwnProperty,
    Bt = RegExp(
        "^" +
            Wt.call(zt)
                .replace(/[\\^$.*+?()[\]{}|]/g, "\\$&")
                .replace(
                    /hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g,
                    "$1.*?",
                ) +
            "$",
    );
function Ft(e) {
    if (!Mt(e) || ((t = e), Ht && Ht in t)) return !1;
    var t,
        n = (function (e) {
            if (!Mt(e)) return !1;
            var t = It(e);
            return (
                "[object Function]" == t ||
                "[object GeneratorFunction]" == t ||
                "[object AsyncFunction]" == t ||
                "[object Proxy]" == t
            );
        })(e)
            ? Bt
            : Ut;
    return n.test(
        (function (e) {
            if (null != e) {
                try {
                    return Dt.call(e);
                } catch (t) {}
                try {
                    return e + "";
                } catch (t) {}
            }
            return "";
        })(e),
    );
}
function Kt(e, t) {
    var n = (function (e, t) {
        return null == e ? void 0 : e[t];
    })(e, t);
    return Ft(n) ? n : void 0;
}
var Jt = (function () {
    try {
        var e = Kt(Object, "defineProperty");
        return (e({}, "", {}), e);
    } catch (t) {}
})();
const qt = Jt;
var Xt = /^(?:0|[1-9]\d*)$/;
function Yt(e, t) {
    var n = typeof e;
    return (
        !!(t = null == t ? 9007199254740991 : t) &&
        ("number" == n || ("symbol" != n && Xt.test(e))) &&
        e > -1 &&
        e % 1 == 0 &&
        e < t
    );
}
function Qt(e, t) {
    return e === t || (e != e && t != t);
}
var Zt = Object.prototype.hasOwnProperty;
function en(e, t, n) {
    var r = e[t];
    (Zt.call(e, t) && Qt(r, n) && (void 0 !== n || t in e)) ||
        (function (e, t, n) {
            "__proto__" == t && qt
                ? qt(e, t, {
                      configurable: !0,
                      enumerable: !0,
                      value: n,
                      writable: !0,
                  })
                : (e[t] = n);
        })(e, t, n);
}
var tn = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/,
    nn = /^\w*$/;
const rn = Kt(Object, "create");
var on = Object.prototype.hasOwnProperty;
var an = Object.prototype.hasOwnProperty;
function cn(e) {
    var t = -1,
        n = null == e ? 0 : e.length;
    for (this.clear(); ++t < n; ) {
        var r = e[t];
        this.set(r[0], r[1]);
    }
}
function sn(e, t) {
    for (var n = e.length; n--; ) if (Qt(e[n][0], t)) return n;
    return -1;
}
((cn.prototype.clear = function () {
    ((this.__data__ = rn ? rn(null) : {}), (this.size = 0));
}),
    (cn.prototype.delete = function (e) {
        var t = this.has(e) && delete this.__data__[e];
        return ((this.size -= t ? 1 : 0), t);
    }),
    (cn.prototype.get = function (e) {
        var t = this.__data__;
        if (rn) {
            var n = t[e];
            return "__lodash_hash_undefined__" === n ? void 0 : n;
        }
        return on.call(t, e) ? t[e] : void 0;
    }),
    (cn.prototype.has = function (e) {
        var t = this.__data__;
        return rn ? void 0 !== t[e] : an.call(t, e);
    }),
    (cn.prototype.set = function (e, t) {
        var n = this.__data__;
        return (
            (this.size += this.has(e) ? 0 : 1),
            (n[e] = rn && void 0 === t ? "__lodash_hash_undefined__" : t),
            this
        );
    }));
var un = Array.prototype.splice;
function ln(e) {
    var t = -1,
        n = null == e ? 0 : e.length;
    for (this.clear(); ++t < n; ) {
        var r = e[t];
        this.set(r[0], r[1]);
    }
}
((ln.prototype.clear = function () {
    ((this.__data__ = []), (this.size = 0));
}),
    (ln.prototype.delete = function (e) {
        var t = this.__data__,
            n = sn(t, e);
        return (
            !(n < 0) &&
            (n == t.length - 1 ? t.pop() : un.call(t, n, 1), --this.size, !0)
        );
    }),
    (ln.prototype.get = function (e) {
        var t = this.__data__,
            n = sn(t, e);
        return n < 0 ? void 0 : t[n][1];
    }),
    (ln.prototype.has = function (e) {
        return sn(this.__data__, e) > -1;
    }),
    (ln.prototype.set = function (e, t) {
        var n = this.__data__,
            r = sn(n, e);
        return (r < 0 ? (++this.size, n.push([e, t])) : (n[r][1] = t), this);
    }));
const fn = Kt(_t, "Map");
function pn(e, t) {
    var n,
        r,
        o = e.__data__;
    return (
        "string" == (r = typeof (n = t)) ||
        "number" == r ||
        "symbol" == r ||
        "boolean" == r
            ? "__proto__" !== n
            : null === n
    )
        ? o["string" == typeof t ? "string" : "hash"]
        : o.map;
}
function dn(e) {
    var t = -1,
        n = null == e ? 0 : e.length;
    for (this.clear(); ++t < n; ) {
        var r = e[t];
        this.set(r[0], r[1]);
    }
}
((dn.prototype.clear = function () {
    ((this.size = 0),
        (this.__data__ = {
            hash: new cn(),
            map: new (fn || ln)(),
            string: new cn(),
        }));
}),
    (dn.prototype.delete = function (e) {
        var t = pn(this, e).delete(e);
        return ((this.size -= t ? 1 : 0), t);
    }),
    (dn.prototype.get = function (e) {
        return pn(this, e).get(e);
    }),
    (dn.prototype.has = function (e) {
        return pn(this, e).has(e);
    }),
    (dn.prototype.set = function (e, t) {
        var n = pn(this, e),
            r = n.size;
        return (n.set(e, t), (this.size += n.size == r ? 0 : 1), this);
    }));
function mn(e, t) {
    if ("function" != typeof e || (null != t && "function" != typeof t))
        throw new TypeError("Expected a function");
    var n = function () {
        var r = arguments,
            o = t ? t.apply(this, r) : r[0],
            i = n.cache;
        if (i.has(o)) return i.get(o);
        var a = e.apply(this, r);
        return ((n.cache = i.set(o, a) || i), a);
    };
    return ((n.cache = new (mn.Cache || dn)()), n);
}
mn.Cache = dn;
var hn,
    vn,
    yn,
    gn =
        /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g,
    wn = /\\(\\)?/g,
    bn =
        ((hn = function (e) {
            var t = [];
            return (
                46 === e.charCodeAt(0) && t.push(""),
                e.replace(gn, function (e, n, r, o) {
                    t.push(r ? o.replace(wn, "$1") : n || e);
                }),
                t
            );
        }),
        (vn = mn(hn, function (e) {
            return (500 === yn.size && yn.clear(), e);
        })),
        (yn = vn.cache),
        vn);
const _n = bn;
function En(e, t) {
    return jt(e)
        ? e
        : (function (e, t) {
                if (jt(e)) return !1;
                var n = typeof e;
                return (
                    !(
                        "number" != n &&
                        "symbol" != n &&
                        "boolean" != n &&
                        null != e &&
                        !Tt(e)
                    ) ||
                    nn.test(e) ||
                    !tn.test(e) ||
                    (null != t && e in Object(t))
                );
            })(e, t)
          ? [e]
          : _n(
                (function (e) {
                    return null == e ? "" : Nt(e);
                })(e),
            );
}
function On(e) {
    if ("string" == typeof e || Tt(e)) return e;
    var t = e + "";
    return "0" == t && 1 / e == -Infinity ? "-0" : t;
}
function Sn(e, t, n) {
    var r =
        null == e
            ? void 0
            : (function (e, t) {
                  for (
                      var n = 0, r = (t = En(t, e)).length;
                      null != e && n < r;
                  )
                      e = e[On(t[n++])];
                  return n && n == r ? e : void 0;
              })(e, t);
    return void 0 === r ? n : r;
}
function An(e, t, n) {
    return null == e
        ? e
        : (function (e, t, n, r) {
              if (!Mt(e)) return e;
              for (
                  var o = -1, i = (t = En(t, e)).length, a = i - 1, c = e;
                  null != c && ++o < i;
              ) {
                  var s = On(t[o]),
                      u = n;
                  if (
                      "__proto__" === s ||
                      "constructor" === s ||
                      "prototype" === s
                  )
                      return e;
                  if (o != a) {
                      var l = c[s];
                      void 0 === (u = r ? r(l, s, c) : void 0) &&
                          (u = Mt(l) ? l : Yt(t[o + 1]) ? [] : {});
                  }
                  (en(c, s, u), (c = c[s]));
              }
              return e;
          })(e, t, n);
}
var Pn =
        (window && window.__assign) ||
        function () {
            return (
                (Pn =
                    Object.assign ||
                    function (e) {
                        for (var t, n = 1, r = arguments.length; n < r; n++)
                            for (var o in (t = arguments[n]))
                                Object.prototype.hasOwnProperty.call(t, o) &&
                                    (e[o] = t[o]);
                        return e;
                    }),
                Pn.apply(this, arguments)
            );
        },
    Cn =
        (window && window.__read) ||
        function (e, t) {
            var n = "function" == typeof Symbol && e[Symbol.iterator];
            if (!n) return e;
            var r,
                o,
                i = n.call(e),
                a = [];
            try {
                for (; (void 0 === t || t-- > 0) && !(r = i.next()).done; )
                    a.push(r.value);
            } catch (c) {
                o = { error: c };
            } finally {
                try {
                    r && !r.done && (n = i.return) && n.call(i);
                } finally {
                    if (o) throw o.error;
                }
            }
            return a;
        },
    xn =
        (window && window.__spreadArray) ||
        function (e, t) {
            for (var n = 0, r = t.length, o = e.length; n < r; n++, o++)
                e[o] = t[n];
            return e;
        },
    In = function (e) {
        return null == e ? void 0 : e.isCircleComp;
    },
    Tn = (function () {
        function e(e) {
            var t = this;
            ((this.actions = {}),
                (this.bindedActions = {}),
                (this.getSchemaStore = function (e, n) {
                    var r = t,
                        o = r.state,
                        i = r.bindedActions,
                        a = t.getIndexList(n);
                    return Pn(
                        Pn(
                            Pn({}, Sn(o, xn([e], Cn(a)))),
                            Sn(i, xn([e], Cn(a))),
                        ),
                        { key: e },
                    );
                }),
                (this.rootStore = e));
        }
        return (
            Object.defineProperty(e.prototype, "state", {
                get: function () {
                    return this.rootStore.getState();
                },
                enumerable: !1,
                configurable: !0,
            }),
            (e.prototype.bindAction = function (e, t, n) {
                var r = this.rootStore,
                    o = (0, this.getIndexList)(n),
                    i = {},
                    a = function () {
                        for (var a, c = [], s = 0; s < arguments.length; s++)
                            c[s] = arguments[s];
                        var u = r.getState(),
                            l = t.apply(void 0, xn([u[e]], Cn(c))),
                            f = (null == l ? void 0 : l.then) ? l.then() : l;
                        if (In(n)) {
                            i = Pn(Pn({}, u[e]), f);
                            var p = Sn(u, xn([e], Cn(o)));
                            An(i, o, Pn(Pn({}, p), f));
                        } else i = Pn(Pn({}, u[e]), f);
                        r.setState(Pn(Pn({}, u), (((a = {})[e] = i), a)));
                    };
                return function () {
                    for (var e = [], t = 0; t < arguments.length; t++)
                        e[t] = arguments[t];
                    return (a.apply(void 0, xn([], Cn(e))), i);
                };
            }),
            (e.prototype.registerSchemaStore = function (e, t) {
                var n = this.state,
                    r = this.actions,
                    o = t.key;
                if (!n[o])
                    try {
                        n[o] =
                            "function" == typeof e.state
                                ? e.state(t)
                                : JSON.parse(JSON.stringify(e.state));
                    } catch (i) {
                        n[o] = {};
                    }
                if (!r[o])
                    try {
                        r[o] =
                            "function" == typeof e.actions
                                ? e.actions(t)
                                : e.actions;
                    } catch (i) {
                        r[o] = {};
                    }
            }),
            (e.prototype.registerCircleSchemaStore = function (e, t, n) {
                var r = this.state,
                    o = this.getIndexList,
                    i = t.key,
                    a = o(n);
                if ((asc, r[i] && !Sn(r, xn([i], Cn(a)))))
                    try {
                        var c =
                            "function" == typeof e.state
                                ? e.state(t)
                                : JSON.parse(JSON.stringify(e.state));
                        An(r, xn([i], Cn(a)), c);
                    } catch (s) {
                        r[i][n.index] = {};
                    }
            }),
            (e.prototype.getIndexList = function (e) {
                var t;
                return (
                    (null === (t = null == e ? void 0 : e.indexList) ||
                    void 0 === t
                        ? void 0
                        : t.reduce(function (e, t) {
                              return (e.push(t.index), e);
                          }, [])) || []
                );
            }),
            (e.prototype.getStoreActionsByKey = function (e, t) {
                var n = this.getIndexList(t);
                return Sn(this.bindedActions, xn([e], Cn(n)));
            }),
            (e.prototype.getParentSchemaStores = function (e, t) {
                for (var n = [], r = new RegExp(t + "$"), o = e.parent; o; ) {
                    var i = o.key,
                        a = o.name,
                        c = o.iterator;
                    if (!t || r.test(a)) {
                        var s = this.getSchemaStore(i, c);
                        n.push(s);
                    }
                    o = o.parent;
                }
                return n;
            }),
            e
        );
    })(),
    jn =
        (window && window.__assign) ||
        function () {
            return (
                (jn =
                    Object.assign ||
                    function (e) {
                        for (var t, n = 1, r = arguments.length; n < r; n++)
                            for (var o in (t = arguments[n]))
                                Object.prototype.hasOwnProperty.call(t, o) &&
                                    (e[o] = t[o]);
                        return e;
                    }),
                jn.apply(this, arguments)
            );
        },
    kn =
        (window && window.__read) ||
        function (e, t) {
            var n = "function" == typeof Symbol && e[Symbol.iterator];
            if (!n) return e;
            var r,
                o,
                i = n.call(e),
                a = [];
            try {
                for (; (void 0 === t || t-- > 0) && !(r = i.next()).done; )
                    a.push(r.value);
            } catch (c) {
                o = { error: c };
            } finally {
                try {
                    r && !r.done && (n = i.return) && n.call(i);
                } finally {
                    if (o) throw o.error;
                }
            }
            return a;
        },
    Rn =
        (window && window.__spreadArray) ||
        function (e, t) {
            for (var n = 0, r = t.length, o = e.length; n < r; n++, o++)
                e[o] = t[n];
            return e;
        },
    Nn = function (e, t) {
        var n = null == t ? void 0 : t.indexList;
        if (!n || 0 === n.length) return e;
        var r = Rn([], kn(null == t ? void 0 : t.indexList)),
            o = e.match(/\.\$row/g);
        if (o && (null == o ? void 0 : o.length) > 0 && r.length > 1) {
            var i = null == o ? void 0 : o.length,
                a = i < n.length ? i : 0;
            r = r.slice(0, r.length - a);
        }
        for (var c = [], s = 0; s < r.length - 1; s++) {
            var u = r[s];
            c.push("[" + u.index + "]");
        }
        var l = r[r.length - 1],
            f =
                "stores[" +
                l.key +
                "]" +
                c.join("") +
                ".dataSource[" +
                l.index +
                "]";
        return e.replace(/\$row(.\$row)*/g, f);
    },
    Mn = function (e) {
        return e.indexOf("$row") >= 0;
    };
function Ln(e, t) {
    var n = t.rootStore,
        r = t.storeId,
        o = t.iterator,
        i = t.global,
        a = n.getState();
    if (!e || "string" != typeof e || !/\$\{(.)+\}/.test(e)) return e;
    var c = e;
    try {
        ((c = e.replace(/(?:#)(\d+)(\.|\[.+\])/g, function (e, t, n) {
            return "stores[" + t + "]" + n;
        })),
            (c = Mn(e)
                ? Nn(c, o)
                : (function (e, t) {
                      var n = e;
                      return (
                          (null == t ? void 0 : t.indexList) &&
                          t.indexList.length > 1
                              ? t.indexList.forEach(function (e) {
                                    var t = "#" + e.key + ".$index";
                                    ((t = n.indexOf(t) >= 0 ? t : "$index"),
                                        (n = n.replace(t, e.index)));
                                })
                              : t &&
                                !S(null == t ? void 0 : t.index) &&
                                (n = n.replace(
                                    /\$index/g,
                                    null == t ? void 0 : t.index.toString(),
                                )),
                          n
                      );
                  })(c, o)),
            (c = c.replace(/\$global/g, "global")));
        c = /^(\$\{)((?!\$\{).)*(\})$/g.test(c)
            ? c.slice(2, c.length - 1)
            : "`" + c + "`";
        var s = jn({ global: i, stores: a }, a[r]);
        return new Function("data", "with(data) {return " + c + "}")(s);
    } catch (u) {
        return "";
    }
}
function $n(e, t) {
    var n;
    if (Mn(e))
        return null === (n = null == t ? void 0 : t.indexList) || void 0 === n
            ? void 0
            : n.map(function (e) {
                  return e.key.toString();
              });
    return (e.match(/#(\d+)(?=\.|\[\d+\])/g) || []).map(function (e) {
        return e.replace("#", "");
    });
}
function Hn(e, t) {
    var n = t.storeId,
        r = t.parseExpression,
        o = t.iterator;
    if (!L(e)) return { data: e, storeIds: ["" + n] };
    var i = [],
        a = jn(jn({}, e), { iterator: o });
    return (
        Object.keys(e).forEach(function (n) {
            var o = e[n];
            if ("string" == typeof o) {
                var c = $n(o, t.iterator);
                return (
                    c && (i = i.concat(c)),
                    void (
                        /^(EXPR_)/.test(n) &&
                        ((a[n.slice(5)] = r ? Ln(o, t) : o), delete a[n])
                    )
                );
            }
            if (Array.isArray(o))
                a[n] = o.map(function (e) {
                    var n = Hn(e, t),
                        r = n.data,
                        o = n.storeIds;
                    return ((i = i.concat(o)), r);
                });
            else {
                if (L(o)) {
                    var s = Hn(o, t),
                        u = s.data,
                        l = s.storeIds;
                    return ((i = i.concat(l)), void (a[n] = u));
                }
                a[n] = o;
            }
        }),
        (i = Array.from(new Set(i.concat(["" + n])))),
        { data: a, storeIds: i }
    );
}
var Dn = [],
    Un = function (e, t, n, r) {
        if (
            (void 0 === r && (r = ""),
            r || (Dn.length = 0),
            null == e && null == t)
        )
            return !0;
        if ("object" != typeof e && "object" != typeof t && e === t) return !0;
        if (
            "object" != typeof e ||
            null === e ||
            "object" != typeof t ||
            null === t
        )
            return (Dn.push([r, !1, e, t]), !1);
        var o = Object.keys(e),
            i = Object.keys(t);
        if (o.length !== i.length) return (Dn.push([r, !1, e, t]), !1);
        var a = !0;
        if (
            !r ||
            n.some(function (e) {
                return e.test(r);
            })
        )
            for (var c = 0, s = void 0, u = void 0; c < o.length; c++)
                ((s = o[c]),
                    (u = r ? r + "." + s : s),
                    Un(e[s], t[s], n, u) || (a = !1));
        else {
            var l = [r, (a = e === t)];
            a || (l.push(e, t), Dn.push(l));
        }
        return a;
    },
    Vn = { compare: Un, loginfo: Dn },
    Gn =
        (window && window.__read) ||
        function (e, t) {
            var n = "function" == typeof Symbol && e[Symbol.iterator];
            if (!n) return e;
            var r,
                o,
                i = n.call(e),
                a = [];
            try {
                for (; (void 0 === t || t-- > 0) && !(r = i.next()).done; )
                    a.push(r.value);
            } catch (c) {
                o = { error: c };
            } finally {
                try {
                    r && !r.done && (n = i.return) && n.call(i);
                } finally {
                    if (o) throw o.error;
                }
            }
            return a;
        };
const Wn = window.React.useEffect,
    zn = window.React.useMemo;
var Bn,
    Fn,
    Kn =
        ((Bn = function (e) {
            return Object.entries(e).reduce(function (e, t) {
                var n = Gn(t, 2),
                    r = n[0],
                    o = n[1].inject;
                return o
                    ? ((Array.isArray(o) ? o : [o]).forEach(function (t) {
                          var n = t.attr,
                              o = t.selector,
                              i = t.format,
                              a = Array.isArray(n) ? n : [n || r],
                              c = Array.isArray(o) ? o.join(", ") : o,
                              s =
                                  "function" == typeof i
                                      ? i
                                      : function (e) {
                                            return e.toString();
                                        };
                          ("px" === i ? (s = H) : "percent" === i && (s = D),
                              e.push({
                                  key: r,
                                  attr: a,
                                  selector: c,
                                  format: s,
                              }));
                      }),
                      e)
                    : e;
            }, []);
        }),
        (Fn = []),
        Object.defineProperty(Bn, "__memo", {
            get: function () {
                return Fn;
            },
        }),
        function (e) {
            var t = Bn.__memo;
            if (t) {
                var n = t.find(function (t) {
                    return t.arg === e;
                });
                if (n) return n.result;
            }
            var r = Bn(e);
            return (
                t.push({ arg: e, result: r }),
                setTimeout(function () {
                    t.length > 20 && t.splice(0, t.length - 20);
                }, 10),
                r
            );
        });
function Jn(e) {
    var t = e.instance,
        n = t.key,
        r = t.component,
        o = r.styleForm,
        i = r.injectStyle,
        a = t.style,
        c = e.scope,
        s = e.children,
        u = zn(
            function () {
                return i
                    ? (function (e, t, n) {
                          return Kn(n)
                              .reduce(function (n, r) {
                                  var o = r.key,
                                      i = r.attr,
                                      a = r.selector,
                                      c = r.format,
                                      s = t[o];
                                  if (!s) return n;
                                  var u = c(s);
                                  return (
                                      n.push(
                                          "\t#" +
                                              e +
                                              " " +
                                              a +
                                              " { " +
                                              i
                                                  .map(function (e) {
                                                      return e + ": " + u;
                                                  })
                                                  .join("; ") +
                                              " }",
                                      ),
                                      n
                                  );
                              }, [])
                              .join("\n");
                      })(c, a, o)
                    : null;
            },
            [a],
        ),
        l = zn(
            function () {
                if (i) {
                    var e = document.createElement("style");
                    return (
                        e.setAttribute("type", "text/css"),
                        e.setAttribute(
                            "class",
                            "injected-styles-component-" + n,
                        ),
                        window.__iframeWindow.document.head.appendChild(e),
                        e
                    );
                }
            },
            [n],
        );
    return (
        Wn(
            function () {
                if (i)
                    return (
                        (l.innerHTML = u),
                        window.__iframeWindow.document.head.appendChild(l),
                        function () {
                            window.__iframeWindow.document.head.removeChild(l);
                        }
                    );
            },
            [u, l],
        ),
        s
    );
}
var qn,
    Xn =
        (window && window.__extends) ||
        ((qn = function (e, t) {
            return (qn =
                Object.setPrototypeOf ||
                ({ __proto__: [] } instanceof Array &&
                    function (e, t) {
                        e.__proto__ = t;
                    }) ||
                function (e, t) {
                    for (var n in t)
                        Object.prototype.hasOwnProperty.call(t, n) &&
                            (e[n] = t[n]);
                })(e, t);
        }),
        function (e, t) {
            if ("function" != typeof t && null !== t)
                throw new TypeError(
                    "Class extends value " +
                        String(t) +
                        " is not a constructor or null",
                );
            function n() {
                this.constructor = e;
            }
            (qn(e, t),
                (e.prototype =
                    null === t
                        ? Object.create(t)
                        : ((n.prototype = t.prototype), new n())));
        }),
    Yn =
        (window && window.__assign) ||
        function () {
            return (
                (Yn =
                    Object.assign ||
                    function (e) {
                        for (var t, n = 1, r = arguments.length; n < r; n++)
                            for (var o in (t = arguments[n]))
                                Object.prototype.hasOwnProperty.call(t, o) &&
                                    (e[o] = t[o]);
                        return e;
                    }),
                Yn.apply(this, arguments)
            );
        },
    Qn =
        (window && window.__rest) ||
        function (e, t) {
            var n = {};
            for (var r in e)
                Object.prototype.hasOwnProperty.call(e, r) &&
                    t.indexOf(r) < 0 &&
                    (n[r] = e[r]);
            if (
                null != e &&
                "function" == typeof Object.getOwnPropertySymbols
            ) {
                var o = 0;
                for (r = Object.getOwnPropertySymbols(e); o < r.length; o++)
                    t.indexOf(r[o]) < 0 &&
                        Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
                        (n[r[o]] = e[r[o]]);
            }
            return n;
        };
const Zn = window.React;
var er = (function (e) {
        function t(t) {
            var n = e.call(this, t) || this;
            return (
                (n.intersectionObserver = null),
                (n.handlerParams = {}),
                (n.handlers = {}),
                (n.containerRef = null),
                (n.longPressTimer = null),
                (n.preventClick = !1),
                (n.doubleClickTimer = null),
                (n.intersectionTimer = null),
                (n.wrapperStyleCache = []),
                (n.execActionHooks = function (e) {
                    e.forEach(function (e) {
                        if ("function" != typeof e.action.action) {
                            var t = e.action.action;
                            if (null == t ? void 0 : t.afterHandlerRender) {
                                var r = be(
                                    e,
                                    n.props.instance,
                                    n.props.global,
                                    n.props.meta,
                                );
                                try {
                                    t.afterHandlerRender(r);
                                } catch (o) {}
                            }
                        }
                    });
                }),
                (n.initIntersectionObserver = function () {
                    n.intersectionObserver = new window.IntersectionObserver(
                        function (e) {
                            e.forEach(function (e) {
                                var t = e.target,
                                    n = e.isIntersecting,
                                    r = parseInt(
                                        t.getAttribute("data-key"),
                                        10,
                                    );
                                Ue.emit(je.COMPONENT_INTERSECTING_CHANGE, n, r);
                            });
                        },
                    );
                }),
                (n.observeIntersection = function () {
                    return n.intersectionObserver.observe(n.containerRef);
                }),
                (n.unobserveIntersection = function () {
                    return n.intersectionObserver.unobserve(n.containerRef);
                }),
                (n.onComponentIntersectionChange = function (e, t) {
                    if (t === n.props.instance.key) {
                        n.intersectionTimer &&
                            (clearTimeout(n.intersectionTimer),
                            (n.intersectionTimer = null));
                        var r = e
                            ? n.onComponentEnterView
                            : n.onComponentLeaveView;
                        n.intersectionTimer = window.setTimeout(function () {
                            (r(),
                                clearTimeout(n.intersectionTimer),
                                (n.intersectionTimer = null));
                        }, 500);
                    }
                }),
                (n.onComponentEnterView = function () {
                    n.handlers.onEnterView && n.handlers.onEnterView(void 0);
                }),
                (n.onComponentLeaveView = function () {
                    n.handlers.onLeaveView && n.handlers.onLeaveView(void 0);
                }),
                (n.onComponentPress = Fe(function (e) {
                    e.target !== n.containerRef &&
                        n.handlers.onLongPress &&
                        (n.longPressTimer = window.setTimeout(function () {
                            return n.handlers.onLongPress(e);
                        }, 1e3));
                })),
                (n.onComponentPressRelease = function (e) {
                    e.target !== n.containerRef &&
                        (n.longPressTimer &&
                            window.clearTimeout(n.longPressTimer),
                        (n.longPressTimer = null));
                }),
                (n.onMouseEnter = Fe(function (e) {
                    e.target !== n.containerRef && n.handlers.onMouseEnter();
                })),
                (n.onMouseLeave = Fe(function (e) {
                    e.target !== n.containerRef && n.handlers.onMouseLeave();
                })),
                (n.onSingleClick = Fe(function (e) {
                    e.target !== n.containerRef &&
                        (n.doubleClickTimer = window.setTimeout(function () {
                            if (!n.preventClick)
                                try {
                                    n.handlers.onClick(e);
                                } catch (t) {}
                        }, 200));
                })),
                (n.onDoubleClick = Fe(function (e) {
                    if (e.target !== n.containerRef) {
                        (n.doubleClickTimer &&
                            (clearTimeout(n.doubleClickTimer),
                            (n.doubleClickTimer = null)),
                            (n.preventClick = !0));
                        try {
                            n.handlers.onDoubleClick(e);
                        } catch (t) {}
                        setTimeout(function () {
                            n.preventClick = !1;
                        }, 200);
                    }
                })),
                (n.emitComponentEvent = function (e, t) {
                    var r = n,
                        o = r.props.instance,
                        i = r.handlerParams,
                        a = i.global;
                    return (function (e, t, n, r, o) {
                        var i = Ee(t, o, r, n);
                        (e && (i.originalEvent = e),
                            delete i.hotArea,
                            Oe.emit(t, i));
                    })(e, t, o, i.meta, a);
                }),
                (n.withEmitComponentEvent = function (e, t) {
                    return function (r) {
                        if ((r && r.persist(), n.emitComponentEvent(r, e), t))
                            return t(r, n.handlerParams);
                    };
                }),
                (n.updateHandlerParams = function (e, t) {
                    ((n.handlerParams.meta = e), (n.handlerParams.global = t));
                }),
                (n.updateHandlersWithParams = function (e) {
                    var t = De(e, n.props.instance),
                        r = t.onInit,
                        o = t.onClick,
                        i = t.onMouseEnter,
                        a = t.onMouseLeave,
                        c = t.onDoubleClick,
                        s = t.onLongPress,
                        u = t.onEnterView,
                        l = t.onLeaveView,
                        f = n,
                        p = f.withEmitComponentEvent,
                        d = f.handlers;
                    ((d.onInit = p(ae.INIT, r)),
                        (d.onClick = p(ae.CLICK, o)),
                        (d.onMouseEnter = p(ae.MOUSE_ENTER, i)),
                        (d.onMouseLeave = p(ae.MOUSE_LEAVE, a)),
                        (d.onDoubleClick = p(ae.DOUBLE_CLICK, c)),
                        (d.onLongPress = p(ae.LONG_PRESS, s)),
                        (d.onEnterView = p(ae.ENTER_VIEW, u)),
                        (d.onLeaveView = p(ae.LEAVE_VIEW, l)));
                }),
                (n.setNode = function (e) {
                    ((n.containerRef = e),
                        (function (e, t) {
                            K.set(e, t);
                        })(n.props.instance.key, e));
                }),
                (n.handlerParams = { global: t.global, meta: t.meta }),
                n.updateHandlersWithParams(t.instance.actions),
                n
            );
        }
        return (
            Xn(t, e),
            (t.prototype.componentDidMount = function () {
                (this.initIntersectionObserver(),
                    this.observeIntersection(),
                    Ue.on(
                        je.COMPONENT_INTERSECTING_CHANGE,
                        this.onComponentIntersectionChange,
                    ),
                    this.handlers.onInit && this.handlers.onInit(void 0),
                    this.execActionHooks(this.props.instance.actions));
            }),
            (t.prototype.UNSAFE_componentWillReceiveProps = function (e) {
                ((e.global === this.props.global &&
                    e.meta === this.props.meta) ||
                    this.updateHandlerParams(e.meta, e.global),
                    e.instance.actions !== this.props.instance.actions &&
                        this.updateHandlersWithParams(e.instance.actions));
            }),
            (t.prototype.componentWillUnmount = function () {
                var e;
                (this.unobserveIntersection(),
                    Ue.cancel(
                        je.COMPONENT_INTERSECTING_CHANGE,
                        this.onComponentIntersectionChange,
                    ),
                    (e = this.props.instance.key),
                    K.delete(e),
                    this.longPressTimer &&
                        window.clearTimeout(this.longPressTimer));
            }),
            (t.prototype.render = function () {
                var e,
                    t = this.props,
                    n = t.children,
                    r = Qn(t, ["children"]),
                    o = r.instance.wrapperStyle,
                    i = r.instance.component.isContainer;
                (delete r.instance, delete r.meta, delete r.global);
                return Zn.createElement(
                    "div",
                    (((e = {}).className = "__impage-component-actions-proxy"),
                    (e.id = V(this.props.instance.key)),
                    (e.style = i ? Yn(Yn({}, o), { position: "relative" }) : o),
                    (e.ref = this.setNode),
                    (e["data-key"] = this.props.instance.key),
                    (e.onClick = this.onSingleClick),
                    (e.onDoubleClick = this.onDoubleClick),
                    (e.onMouseEnter = this.onMouseEnter),
                    (e.onMouseLeave = this.onMouseLeave),
                    (e.onTouchStart = this.onComponentPress),
                    (e.onTouchEnd = this.onComponentPressRelease),
                    (e.onMouseDown = this.onComponentPress),
                    (e.onMouseUp = this.onComponentPressRelease),
                    e),
                    M(r)
                        ? n
                        : Zn.Children.map(n, function (e) {
                              return Zn.cloneElement(e, r);
                          }),
                );
            }),
            t
        );
    })(Zn.PureComponent),
    tr =
        (window && window.__extends) ||
        (function () {
            var e = function (t, n) {
                return (e =
                    Object.setPrototypeOf ||
                    ({ __proto__: [] } instanceof Array &&
                        function (e, t) {
                            e.__proto__ = t;
                        }) ||
                    function (e, t) {
                        for (var n in t)
                            Object.prototype.hasOwnProperty.call(t, n) &&
                                (e[n] = t[n]);
                    })(t, n);
            };
            return function (t, n) {
                if ("function" != typeof n && null !== n)
                    throw new TypeError(
                        "Class extends value " +
                            String(n) +
                            " is not a constructor or null",
                    );
                function r() {
                    this.constructor = t;
                }
                (e(t, n),
                    (t.prototype =
                        null === n
                            ? Object.create(n)
                            : ((r.prototype = n.prototype), new r())));
            };
        })();
const nr = window.React;
var rr = (function (e) {
        function t(t) {
            var n = e.call(this, t) || this;
            return (
                (n.intersectionObserver = null),
                (n.handlerParams = {}),
                (n.handlers = {}),
                (n.containerRef = null),
                (n.longPressTimer = null),
                (n.preventClick = !1),
                (n.doubleClickTimer = null),
                (n.intersectionTimer = null),
                (n.execActionHooks = function (e) {
                    e.forEach(function (e) {
                        if ("function" != typeof e.action.action) {
                            var t = e.action.action;
                            if (t.afterHandlerRender) {
                                var r = _e(
                                    e,
                                    n.props.hotArea,
                                    n.props.instance,
                                    n.props.global,
                                    n.props.meta,
                                );
                                try {
                                    t.afterHandlerRender(r);
                                } catch (o) {}
                            }
                        }
                    });
                }),
                (n.initIntersectionObserver = function () {
                    n.intersectionObserver = new window.IntersectionObserver(
                        function (e) {
                            e.forEach(function (e) {
                                var t = e.target,
                                    n = e.isIntersecting,
                                    r = parseInt(
                                        t.getAttribute("data-key"),
                                        10,
                                    );
                                Ue.emit(je.HOT_AREA_INTERSECTING_CHANGE, n, r);
                            });
                        },
                    );
                }),
                (n.observeIntersection = function () {
                    return n.intersectionObserver.observe(n.containerRef);
                }),
                (n.unobserveIntersection = function () {
                    return n.intersectionObserver.unobserve(n.containerRef);
                }),
                (n.onHotAreaIntersectionChange = function (e, t) {
                    if (t === n.props.hotArea.key) {
                        n.intersectionTimer &&
                            (clearTimeout(n.intersectionTimer),
                            (n.intersectionTimer = null));
                        var r = e ? n.onHotAreaEnterView : n.onHotAreaLeaveView;
                        n.intersectionTimer = window.setTimeout(function () {
                            (r(),
                                clearTimeout(n.intersectionTimer),
                                (n.intersectionTimer = null));
                        }, 500);
                    }
                }),
                (n.onHotAreaEnterView = function () {
                    n.handlers.onEnterView && n.handlers.onEnterView(void 0);
                }),
                (n.onHotAreaLeaveView = function () {
                    n.handlers.onLeaveView && n.handlers.onLeaveView(void 0);
                }),
                (n.onHotAreaPress = Fe(function (e) {
                    n.handlers.onLongPress &&
                        (n.longPressTimer = window.setTimeout(function () {
                            return n.handlers.onLongPress(e);
                        }, 1e3));
                })),
                (n.onHotAreaPressRelease = function () {
                    (n.longPressTimer && window.clearTimeout(n.longPressTimer),
                        (n.longPressTimer = null));
                }),
                (n.onMouseEnter = Fe(function () {
                    n.handlers.onMouseEnter();
                })),
                (n.onMouseLeave = Fe(function () {
                    n.handlers.onMouseLeave();
                })),
                (n.onSingleClick = Fe(function (e) {
                    n.doubleClickTimer = window.setTimeout(function () {
                        if (!n.preventClick)
                            try {
                                n.handlers.onClick(e);
                            } catch (t) {}
                    }, 200);
                })),
                (n.onDoubleClick = Fe(function (e) {
                    (n.doubleClickTimer &&
                        (clearTimeout(n.doubleClickTimer),
                        (n.doubleClickTimer = null)),
                        (n.preventClick = !0));
                    try {
                        n.handlers.onDoubleClick(e);
                    } catch (t) {}
                    setTimeout(function () {
                        n.preventClick = !1;
                    }, 200);
                })),
                (n.emitHotAreaEvent = function (e, t) {
                    var r = n,
                        o = r.props,
                        i = o.hotArea,
                        a = o.instance,
                        c = r.handlerParams,
                        s = c.global;
                    return (function (e, t, n, r, o, i) {
                        var a = Ee(t, i, o, r, n);
                        (e && (a.originalEvent = e), Pe.emit(t, a));
                    })(e, t, i, a, c.meta, s);
                }),
                (n.withEmitHotAreaEvent = function (e, t) {
                    return function (r) {
                        if ((r && r.persist(), n.emitHotAreaEvent(r, e), t))
                            return t(r, n.handlerParams);
                    };
                }),
                (n.updateHandlerParams = function (e, t) {
                    ((n.handlerParams.meta = e), (n.handlerParams.global = t));
                }),
                (n.updateHandlersWithParams = function (e) {
                    var t = De(e, n.props.instance, n.props.hotArea),
                        r = t.onInit,
                        o = t.onClick,
                        i = t.onMouseEnter,
                        a = t.onMouseLeave,
                        c = t.onDoubleClick,
                        s = t.onLongPress,
                        u = t.onEnterView,
                        l = t.onLeaveView,
                        f = n,
                        p = f.withEmitHotAreaEvent,
                        d = f.handlers;
                    ((d.onInit = p(me.INIT, r)),
                        (d.onClick = p(me.CLICK, o)),
                        (d.onMouseEnter = p(me.MOUSE_ENTER, i)),
                        (d.onMouseLeave = p(me.MOUSE_LEAVE, a)),
                        (d.onDoubleClick = p(me.DOUBLE_CLICK, c)),
                        (d.onLongPress = p(me.LONG_PRESS, s)),
                        (d.onEnterView = p(me.ENTER_VIEW, u)),
                        (d.onLeaveView = p(me.LEAVE_VIEW, l)));
                }),
                (n.setNode = function (e) {
                    ((n.containerRef = e),
                        (function (e, t) {
                            X.set(e, t);
                        })(e));
                }),
                (n.handlerParams = { global: t.global, meta: t.meta }),
                n.updateHandlersWithParams(t.hotArea.actions),
                n
            );
        }
        return (
            tr(t, e),
            (t.prototype.componentDidMount = function () {
                (this.initIntersectionObserver(),
                    this.observeIntersection(),
                    Ue.on(
                        je.HOT_AREA_INTERSECTING_CHANGE,
                        this.onHotAreaIntersectionChange,
                    ),
                    this.handlers.onInit && this.handlers.onInit(void 0),
                    this.execActionHooks(this.props.hotArea.actions));
            }),
            (t.prototype.UNSAFE_componentWillReceiveProps = function (e) {
                ((e.global === this.props.global &&
                    e.meta === this.props.meta) ||
                    this.updateHandlerParams(e.meta, e.global),
                    e.hotArea.actions !== this.props.hotArea.actions &&
                        this.updateHandlersWithParams(e.hotArea.actions));
            }),
            (t.prototype.componentWillUnmount = function () {
                var e;
                (this.unobserveIntersection(),
                    Ue.cancel(
                        je.HOT_AREA_INTERSECTING_CHANGE,
                        this.onHotAreaIntersectionChange,
                    ),
                    (e = this.props.hotArea.kebabCase),
                    X.delete(e),
                    this.longPressTimer &&
                        window.clearTimeout(this.longPressTimer));
            }),
            (t.prototype.render = function () {
                var e,
                    t = this.props,
                    n = t.children,
                    r = t.style,
                    o = void 0 === r ? {} : r;
                return nr.createElement(
                    "div",
                    (((e = {}).className = "__impage-hot-area-actions-proxy"),
                    (e.id = G(this.props.hotArea.key)),
                    (e.ref = this.setNode),
                    (e["data-key"] = this.props.hotArea.key),
                    (e.onClick = this.onSingleClick),
                    (e.onDoubleClick = this.onDoubleClick),
                    (e.onMouseEnter = this.onMouseEnter),
                    (e.onMouseLeave = this.onMouseLeave),
                    (e.onTouchStart = this.onHotAreaPress),
                    (e.onTouchEnd = this.onHotAreaPressRelease),
                    (e.onMouseDown = this.onHotAreaPress),
                    (e.onMouseUp = this.onHotAreaPressRelease),
                    (e.style = o),
                    e),
                    n,
                );
            }),
            t
        );
    })(nr.PureComponent),
    or =
        (window && window.__assign) ||
        function () {
            return (
                (or =
                    Object.assign ||
                    function (e) {
                        for (var t, n = 1, r = arguments.length; n < r; n++)
                            for (var o in (t = arguments[n]))
                                Object.prototype.hasOwnProperty.call(t, o) &&
                                    (e[o] = t[o]);
                        return e;
                    }),
                or.apply(this, arguments)
            );
        };
const ir = window.React;
function ar(e) {
    var t = e.positionStyle,
        n = e.children,
        r = e.instance,
        o = r && r.fixedWrapperStyle && r.fixedWrapperStyle.width,
        i = r && r.fixedWrapperStyle && r.fixedWrapperStyle.height,
        a = r && r.commonStyle && r.commonStyle.width,
        c = or(or({}, t), {
            width: o || (a ? "auto" : "100%"),
            height: i || "auto",
            zIndex: 999,
        });
    return ir.createElement("div", { style: c }, n);
}
var cr = function () {
    return (
        (cr =
            Object.assign ||
            function (e) {
                for (var t, n = 1, r = arguments.length; n < r; n++)
                    for (var o in (t = arguments[n]))
                        Object.prototype.hasOwnProperty.call(t, o) &&
                            (e[o] = t[o]);
                return e;
            }),
        cr.apply(this, arguments)
    );
};
const sr = t(function (e, t) {
    (void 0 === e && (e = {}), void 0 === t && (t = null));
    var n = e || {},
        r = [];
    function o() {
        r.forEach(function (e) {
            return e(n);
        });
    }
    return {
        middleware: t,
        setState: function (e) {
            ((n = cr({}, n, "function" == typeof e ? e(n) : e)), o());
        },
        subscribe: function (e) {
            return (
                r.push(e),
                function () {
                    r.splice(r.indexOf(e), 1);
                }
            );
        },
        getState: function () {
            return n;
        },
        reset: function () {
            ((n = e), o());
        },
    };
});
var ur = {};
Object.defineProperty(ur, "__esModule", { value: !0 });
var lr = window.React,
    fr = function (e, t) {
        return (fr =
            Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array &&
                function (e, t) {
                    e.__proto__ = t;
                }) ||
            function (e, t) {
                for (var n in t) t.hasOwnProperty(n) && (e[n] = t[n]);
            })(e, t);
    };
function pr(e, t) {
    function n() {
        this.constructor = e;
    }
    (fr(e, t),
        (e.prototype =
            null === t
                ? Object.create(t)
                : ((n.prototype = t.prototype), new n())));
}
var dr = function () {
    return (
        (dr =
            Object.assign ||
            function (e) {
                for (var t, n = 1, r = arguments.length; n < r; n++)
                    for (var o in (t = arguments[n]))
                        Object.prototype.hasOwnProperty.call(t, o) &&
                            (e[o] = t[o]);
                return e;
            }),
        dr.apply(this, arguments)
    );
};
function mr(e, t) {
    for (var n in e) if (e[n] !== t[n]) return !1;
    for (var n in t) if (!(n in e)) return !1;
    return !0;
}
function hr(e, t, n) {
    return "object" == typeof e
        ? null
        : new Error("Invalid prop " + t + " supplied to " + n);
}
function vr(e, t) {
    if (null != t) {
        if (t.then) return t.then(e.setState);
        e.setState(t);
    }
}
function yr(e, t) {
    return function () {
        for (var n = [], r = 0; r < arguments.length; r++) n[r] = arguments[r];
        return "function" == typeof t.middleware
            ? t.middleware(t, e, n)
            : vr(t, e.apply(void 0, [t.getState()].concat(n)));
    };
}
var gr = (function (e) {
    function t(t, n) {
        var r = e.call(this, t, n) || this;
        return (
            (r.update = function () {
                var e = r.getProps(r.props, r.context);
                mr(e, r.state) || r.setState(e);
            }),
            (r.state = r.getProps(t, n)),
            (r.actions = r.getActions()),
            r
        );
    }
    return (
        pr(t, e),
        (t.prototype.UNSAFE_componentWillMount = function () {
            this.unsubscribe = this.context.store.subscribe(this.update);
        }),
        (t.prototype.componentWillUnmount = function () {
            this.unsubscribe(this.update);
        }),
        (t.prototype.UNSAFE_componentWillReceiveProps = function (e, t) {
            var n = this.getProps(e, t);
            mr(n, this.state) || this.setState(n);
        }),
        (t.prototype.getProps = function (e, t) {
            var n = e.mapToProps,
                r = (t.store && t.store.getState()) || {};
            return n ? n(r, e) : r;
        }),
        (t.prototype.getActions = function () {
            return (function (e, t, n) {
                e = "function" == typeof e ? e(t, n) : e;
                var r = {};
                for (var o in e) {
                    var i = e[o];
                    r[o] = yr(i, t);
                }
                return r;
            })(this.props.actions, this.context.store, this.props);
        }),
        (t.prototype.render = function () {
            return this.props.children(
                dr({ store: this.context.store }, this.state, this.actions),
            );
        }),
        (t.contextTypes = { store: hr }),
        t
    );
})(lr.Component);
var wr =
        "createContext" in lr
            ? lr.createContext(void 0)
            : {
                  Provider: function (e) {
                      var t = e.children;
                      return lr.Children.only(t);
                  },
              },
    br = (function (e) {
        function t() {
            return (null !== e && e.apply(this, arguments)) || this;
        }
        return (
            pr(t, e),
            (t.prototype.getChildContext = function () {
                return { store: this.props.store };
            }),
            (t.prototype.render = function () {
                var e = this.props,
                    t = e.store,
                    n = e.children;
                return lr.createElement(wr.Provider, { value: t }, n);
            }),
            (t.childContextTypes = { store: hr }),
            t
        );
    })(lr.Component);
function _r() {
    return lr.useContext(wr);
}
var Er = "undefined" != typeof window ? lr.useLayoutEffect : lr.useEffect;
ur.connect = function (e, t) {
    return (
        void 0 === t && (t = {}),
        function (n) {
            return (function (r) {
                function o() {
                    return (null !== r && r.apply(this, arguments)) || this;
                }
                return (
                    pr(o, r),
                    (o.prototype.render = function () {
                        var r = this.props;
                        return lr.createElement(
                            gr,
                            dr({}, r, { mapToProps: e, actions: t }),
                            function (e) {
                                return lr.createElement(n, dr({}, e, r));
                            },
                        );
                    }),
                    o
                );
            })(lr.Component);
        }
    );
};
var Or = (ur.Provider = br);
((ur.Connect = gr), (ur.useStore = _r));
var Sr = (ur.useSelector = function (e) {
    var t,
        n = _r(),
        r = lr.useReducer(function (e) {
            return e + 1;
        }, 0)[1],
        o = lr.useRef(void 0),
        i = lr.useRef(void 0),
        a = lr.useRef(void 0);
    try {
        t = o.current !== e || a.current ? e(n.getState()) : i.current;
    } catch (s) {
        var c =
            "An error occurred while selecting the store state: " +
            s.message +
            ".";
        throw (
            a.current &&
                (c +=
                    "\nThe error may be related with this previous error:\n" +
                    a.current.stack +
                    "\n\nOriginal stack trace:"),
            new Error(c)
        );
    }
    return (
        Er(function () {
            ((o.current = e), (i.current = t), (a.current = void 0));
        }),
        Er(
            function () {
                var e = function () {
                        try {
                            var e = o.current(n.getState());
                            if (e === i.current) return;
                            i.current = e;
                        } catch (s) {
                            a.current = s;
                        }
                        r({});
                    },
                    t = n.subscribe(e);
                return (
                    e(),
                    function () {
                        return t();
                    }
                );
            },
            [n],
        ),
        t
    );
});
ur.useAction = function (e) {
    var t = _r();
    return lr.useMemo(
        function () {
            return yr(e, t);
        },
        [t, e],
    );
};
var Ar =
        (window && window.__extends) ||
        (function () {
            var e = function (t, n) {
                return (e =
                    Object.setPrototypeOf ||
                    ({ __proto__: [] } instanceof Array &&
                        function (e, t) {
                            e.__proto__ = t;
                        }) ||
                    function (e, t) {
                        for (var n in t)
                            Object.prototype.hasOwnProperty.call(t, n) &&
                                (e[n] = t[n]);
                    })(t, n);
            };
            return function (t, n) {
                if ("function" != typeof n && null !== n)
                    throw new TypeError(
                        "Class extends value " +
                            String(n) +
                            " is not a constructor or null",
                    );
                function r() {
                    this.constructor = t;
                }
                (e(t, n),
                    (t.prototype =
                        null === n
                            ? Object.create(n)
                            : ((r.prototype = n.prototype), new r())));
            };
        })(),
    Pr =
        (window && window.__assign) ||
        function () {
            return (
                (Pr =
                    Object.assign ||
                    function (e) {
                        for (var t, n = 1, r = arguments.length; n < r; n++)
                            for (var o in (t = arguments[n]))
                                Object.prototype.hasOwnProperty.call(t, o) &&
                                    (e[o] = t[o]);
                        return e;
                    }),
                Pr.apply(this, arguments)
            );
        },
    Cr =
        (window && window.__read) ||
        function (e, t) {
            var n = "function" == typeof Symbol && e[Symbol.iterator];
            if (!n) return e;
            var r,
                o,
                i = n.call(e),
                a = [];
            try {
                for (; (void 0 === t || t-- > 0) && !(r = i.next()).done; )
                    a.push(r.value);
            } catch (c) {
                o = { error: c };
            } finally {
                try {
                    r && !r.done && (n = i.return) && n.call(i);
                } finally {
                    if (o) throw o.error;
                }
            }
            return a;
        },
    xr =
        (window && window.__spreadArray) ||
        function (e, t) {
            for (var n = 0, r = t.length, o = e.length; n < r; n++, o++)
                e[o] = t[n];
            return e;
        };
const Ir = window.React,
    Tr = window.React.useContext,
    jr = window.React.useMemo,
    kr = window.React.useRef;
var Rr = new Tn(sr({})),
    Nr = Ir.createContext(Rr),
    Mr = function () {
        return Tr(Nr);
    },
    Lr = (function (e) {
        function t(t) {
            var n,
                r = e.call(this, t) || this;
            return (
                (r.state = {
                    renderStore:
                        null !== (n = t.renderStore) && void 0 !== n
                            ? n
                            : new Tn(sr({})),
                }),
                r
            );
        }
        return (
            Ar(t, e),
            (t.getDerivedStateFromProps = function (e, t) {
                return e.renderStore && e.renderStore !== t.renderStore
                    ? { renderStore: e.renderStore }
                    : null;
            }),
            (t.prototype.render = function () {
                var e = this.props.children,
                    t = this.state.renderStore;
                return Ir.createElement(
                    Nr.Provider,
                    { value: t },
                    Ir.createElement(Or, { store: t.rootStore }, e),
                );
            }),
            t
        );
    })(Ir.Component);
var $r = (0, window.React.createContext)({});
$r.displayName = "IteratorContext";
const Hr = window.React;
function Dr(e) {
    var t = e.instance,
        n = e.global,
        r = e.meta,
        o = t.data.hotAreas;
    return o && o.length
        ? o.map(function (e, o) {
              var i = e.size,
                  a = e.position;
              return Hr.createElement(rr, {
                  key: o,
                  instance: t,
                  hotArea: e,
                  meta: r,
                  global: n,
                  style: {
                      width: D(i.width),
                      height: D(i.height),
                      left: D(a.x),
                      top: D(a.y),
                      cursor: "pointer",
                      position: "absolute",
                      zIndex: 20,
                  },
              });
          })
        : null;
}
var Ur = (0, window.React.createContext)({
        materials: {},
        meta: {},
        global: {},
        autoParseStyle: !0,
        schema: { components: [], plugins: [] },
    }),
    Vr =
        (window && window.__assign) ||
        function () {
            return (
                (Vr =
                    Object.assign ||
                    function (e) {
                        for (var t, n = 1, r = arguments.length; n < r; n++)
                            for (var o in (t = arguments[n]))
                                Object.prototype.hasOwnProperty.call(t, o) &&
                                    (e[o] = t[o]);
                        return e;
                    }),
                Vr.apply(this, arguments)
            );
        },
    Gr =
        (window && window.__rest) ||
        function (e, t) {
            var n = {};
            for (var r in e)
                Object.prototype.hasOwnProperty.call(e, r) &&
                    t.indexOf(r) < 0 &&
                    (n[r] = e[r]);
            if (
                null != e &&
                "function" == typeof Object.getOwnPropertySymbols
            ) {
                var o = 0;
                for (r = Object.getOwnPropertySymbols(e); o < r.length; o++)
                    t.indexOf(r[o]) < 0 &&
                        Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
                        (n[r[o]] = e[r[o]]);
            }
            return n;
        };
const Wr = window.React,
    zr = window.React.memo,
    Br = window.React.useCallback,
    Fr = window.React.useContext,
    Kr = window.React.useMemo;
var Jr = zr(
        function (e) {
            var t,
                n = e.meta,
                r = e.global,
                o = e.instance,
                i = e.path,
                a = e.injectProps,
                c = e.hotAreas,
                s = e.children,
                u = e.withComponentAdaptor,
                l = e.store,
                f = e.eventHandlers,
                p = Gr(e, [
                    "meta",
                    "global",
                    "instance",
                    "path",
                    "injectProps",
                    "hotAreas",
                    "children",
                    "withComponentAdaptor",
                    "store",
                    "eventHandlers",
                ]),
                d = o.key,
                m = o.name,
                h = o.component,
                v = h.component,
                y = h.__implementHotArea,
                g = o.position,
                w = o.commonStyle,
                b = o.data,
                _ = o.slot,
                E = o.style,
                O = Br(
                    function (e, t) {
                        return (function (e, t, n, r, o, i) {
                            var a = e.key,
                                c = e.name,
                                s = e.component.emitEvents;
                            if (
                                !s ||
                                s.find(function (e) {
                                    return e.eventName === t;
                                })
                            ) {
                                i &&
                                    i.forEach(function (e) {
                                        var n = e.eventName,
                                            r = e.key,
                                            i = e.name,
                                            s = e.handler;
                                        n !== t ||
                                            (r !== a && i !== c) ||
                                            s(a, c, o);
                                    });
                                var u = e.actions.filter(function (e) {
                                    return e.trigger === t;
                                });
                                if (u.length)
                                    return $e(
                                        u,
                                        e,
                                        void 0,
                                        o,
                                    )(void 0, { global: n, meta: r });
                            }
                        })(o, e, r, n, t, f);
                    },
                    [o, r, n, f],
                ),
                S = Br(
                    function (e, t) {
                        return (function (e, t, n) {
                            var r = e.key,
                                o = e.component,
                                i = o.onEvents,
                                a = (o.name, "__impage__component-event-" + t);
                            if (
                                !i ||
                                i.find(function (e) {
                                    return e.eventName === a;
                                })
                            ) {
                                var c = Ge(r);
                                if (!c) return Ve.set(r, new Map([[a, [n]]]));
                                var s = c.get(a);
                                if (!s) return c.set(a, [n]);
                                s.push(n);
                            }
                        })(o, e, t);
                    },
                    [o],
                ),
                A = Br(
                    function (e, t) {
                        return (function (e, t, n) {
                            var r = "__impage__component-event-" + t,
                                o = Ge(e.key);
                            if (o) {
                                var i = o.get(r);
                                if (!i) return o.delete(r);
                                var a = i.findIndex(function (e) {
                                    return e === n;
                                });
                                a > -1 && i.splice(a, 1);
                            }
                        })(o, e, t);
                    },
                    [o],
                ),
                P = i + "/" + m,
                C = y
                    ? null != c
                        ? c
                        : Wr.createElement(Dr, {
                              global: r,
                              meta: n,
                              instance: o,
                          })
                    : null,
                x = Mr(),
                I = Br(
                    function (e, t) {
                        return x.getStoreActionsByKey(e, t);
                    },
                    [x],
                ),
                T = Br(
                    function (e) {
                        return x.getParentSchemaStores(o, e);
                    },
                    [x, o],
                ),
                j = Vr(Vr(Vr({}, p), a), {
                    injectProps: a,
                    meta: n,
                    global: r,
                    hotAreas: C,
                    store: l,
                    name: m,
                    key: d,
                    data: b,
                    slot: _,
                    style: E,
                    commonStyle: w,
                    componentKey: d,
                    emit: O,
                    on: S,
                    off: A,
                    path: P,
                    getStoreActionsByKey: I,
                    getParentSchemaStores: T,
                    componentsMap: K,
                    getComponentByKey: J,
                }),
                k = null !== (t = o.id) && void 0 !== t ? t : o.name,
                R = u ? Je("WrappedComponent_" + k, v, u) : v,
                N = Wr.createElement(R, Vr({}, j, { instance: o }), s),
                M = g
                    ? Wr.createElement(ar, { positionStyle: g, instance: o }, N)
                    : N;
            return Wr.createElement(
                Jn,
                { instance: o, scope: V(o.key) },
                Wr.createElement(er, { instance: o, meta: n, global: r }, M),
            );
        },
        function (e, t) {
            return Vn.compare(e, t, [
                /^instance$/,
                /^instance\.data(?:\..*)?$/,
                /^instance\.commonStyle(?:\..*)?$/,
                /^instance\.wrapperStyle(?:\..*)?$/,
                /^instance\.actions(?:\..*)?$/,
                /^store(?:\..*)?$/,
            ]);
        },
    ),
    qr = function (e, t, n) {
        var r = Mr().rootStore,
            o = Fr($r),
            i = e.key,
            a = e.data,
            c = e.actions,
            s = {
                rootStore: r,
                global: t,
                storeId: i,
                parseExpression: n,
                iterator: o,
            },
            u = Hn(a, s),
            l = u.data,
            f = u.storeIds,
            p = c.map(function (e) {
                var t = Hn(e.data, s),
                    n = t.data,
                    r = t.storeIds;
                return ((f = f.concat(r)), Vr(Vr({}, e), { data: n }));
            }),
            d = (function (e, t, n) {
                var r = Mr(),
                    o = kr({}),
                    i = t.key,
                    a = t.component,
                    c = (void 0 === a ? {} : a).store,
                    s = void 0 === c ? {} : c,
                    u = t.action;
                (u && (s = null == u ? void 0 : u.store),
                    In(n) && r.registerCircleSchemaStore(s, t, n));
                var l = (0, r.getIndexList)(n),
                    f = Sr(function (t) {
                        var n = e.reduce(
                                function (e, n) {
                                    var r;
                                    return {
                                        hadChange:
                                            e.hadChange ||
                                            !R(o.current[n], t[n]),
                                        relativeState: Pr(
                                            Pr({}, e.relativeState),
                                            ((r = {}), (r[n] = t[n]), r),
                                        ),
                                    };
                                },
                                { hadChange: !1, relativeState: {} },
                            ),
                            r = n.hadChange,
                            i = n.relativeState;
                        return (r && (o.current = i), o.current);
                    }),
                    p = jr(
                        function () {
                            return r.actions[i]
                                ? Object.entries(r.actions[i]).reduce(function (
                                      e,
                                      t,
                                  ) {
                                      var o = Cr(t, 2),
                                          a = o[0],
                                          c = o[1];
                                      return (
                                          (e[a] = r.bindAction(i, c, n)),
                                          e
                                      );
                                  }, {})
                                : {};
                        },
                        [i, r.actions[i], JSON.stringify(n)],
                    );
                In(n)
                    ? An(r.bindedActions, xr([i], Cr(l)), p)
                    : (r.bindedActions[i] = p);
                var d = In(n) ? Sn(f, xr([i], Cr(l))) : f[i];
                return Pr(Pr(Pr({}, d), p), { key: i });
            })(f, e, o);
        return {
            instance: Vr(Vr({}, e), { iterator: o, data: l, actions: p }),
            schemaStore: d,
        };
    },
    Xr = [],
    Yr = function (e) {
        var t = e.instance,
            n = e.renderHoc,
            r = e.meta,
            o = e.path,
            i = e.global,
            a = e.parseExpression,
            c = e.withComponentAdaptor,
            s = e.disableStore,
            u = e.eventHandlers,
            l = t,
            f = null,
            p = qr(t, i, a);
        s || ((l = p.instance), (f = p.schemaStore));
        var d = n ? Je("WrappedComponentItem", Jr, n) : Jr,
            m = Vr(Vr({}, e), { instance: l, store: f }),
            h = Kr(
                function () {
                    var e = t.children,
                        l = t.name,
                        f = o + "/" + l;
                    return (null == e ? void 0 : e.length)
                        ? null == e
                            ? void 0
                            : e.map(function (e, t) {
                                  return Wr.createElement(Yr, {
                                      path: f,
                                      meta: r,
                                      global: i,
                                      index: t,
                                      renderHoc: n,
                                      key: e.key,
                                      instance: Vr(Vr({}, e), {
                                          parent: p.instance,
                                      }),
                                      slot: e.slot,
                                      parseExpression: a,
                                      withComponentAdaptor: c,
                                      disableStore: s,
                                      eventHandlers: u,
                                  });
                              })
                        : Xr;
                },
                [s, i, t, r, a, o, n, c, u],
            );
        return Wr.createElement(d, Vr({}, m), h);
    };
function Qr(e) {
    var t = e.componentInstances,
        n = e.pluginInstances,
        r = Fr(Ur),
        o = r.meta,
        i = r.global,
        a = Wr.useCallback(function () {
            n.forEach(function (e) {
                var t = e.plugin.plugin,
                    n = (function (e, t, n) {
                        return {
                            key: e.key,
                            data: e.data,
                            meta: n,
                            global: t,
                            on: Be,
                            componentsMap: K,
                            getComponentByKey: J,
                        };
                    })(e, i, o);
                t(n);
            });
        }, []);
    return (
        Wr.useEffect(function () {
            (a(),
                Ae(le.INIT, { global: i, meta: o }),
                (function (e) {
                    var t = e.global,
                        n = e.meta,
                        r = new Date().getTime();
                    window.addEventListener("beforeunload", function () {
                        var e = new Date().getTime();
                        Ae(le.CLOSE, {
                            global: t,
                            meta: n,
                            addition: { visitDuration: e - r },
                        });
                    });
                })({ global: i, meta: o }));
        }, []),
        Wr.createElement(
            Wr.Fragment,
            null,
            t.map(function (e, t) {
                return Wr.createElement(
                    Yr,
                    Vr({ path: "", index: t, key: e.key, instance: e }, r),
                );
            }),
        )
    );
}
var Zr =
        (window && window.__assign) ||
        function () {
            return (
                (Zr =
                    Object.assign ||
                    function (e) {
                        for (var t, n = 1, r = arguments.length; n < r; n++)
                            for (var o in (t = arguments[n]))
                                Object.prototype.hasOwnProperty.call(t, o) &&
                                    (e[o] = t[o]);
                        return e;
                    }),
                Zr.apply(this, arguments)
            );
        },
    eo =
        (window && window.__rest) ||
        function (e, t) {
            var n = {};
            for (var r in e)
                Object.prototype.hasOwnProperty.call(e, r) &&
                    t.indexOf(r) < 0 &&
                    (n[r] = e[r]);
            if (
                null != e &&
                "function" == typeof Object.getOwnPropertySymbols
            ) {
                var o = 0;
                for (r = Object.getOwnPropertySymbols(e); o < r.length; o++)
                    t.indexOf(r[o]) < 0 &&
                        Object.prototype.propertyIsEnumerable.call(e, r[o]) &&
                        (n[r[o]] = e[r[o]]);
            }
            return n;
        };
const to = window.React,
    no = window.React.useContext,
    ro = window.React.useEffect,
    oo = window.React.useMemo,
    io = window.React.useState;
!{}.SSR &&
    "undefined" != typeof window &&
    window.document &&
    window.document.createElement &&
    (window.stores = []);
var ao = function () {
    var e = no(Ur),
        t = e.schema,
        n = e.renderInstance,
        r = e.materials,
        o = e.autoParseStyle,
        i = Mr();
    ro(
        function () {
            return (
                window.stores.push(i),
                function () {
                    window.stores =
                        window.stores.filter(function (e) {
                            return e !== i;
                        }) || [];
                }
            );
        },
        [i],
    );
    var a = oo(
        function () {
            return t
                ? ht(t, r, { autoParseStyle: o, renderStore: i })
                : { componentInstances: [], pluginInstances: [] };
        },
        [t, r, o, i],
    );
    ro(function () {
        return function () {
            Ke = {};
        };
    }, []);
    var c = null != n ? n : a,
        s = c.componentInstances,
        u = c.pluginInstances;
    return (
        ee(s),
        to.createElement(Qr, { pluginInstances: u, componentInstances: s })
    );
};
const co = function (e) {
        var t = e.rendererHooks,
            n = void 0 === t ? {} : t,
            r = e.externalStore,
            o = e.meta,
            i = void 0 === o ? {} : o,
            a = e.global,
            c = void 0 === a ? {} : a,
            s = e.autoParseStyle,
            u = void 0 === s || s,
            l = e.parseExpression,
            f = void 0 === l || l,
            p = eo(e, [
                "rendererHooks",
                "externalStore",
                "meta",
                "global",
                "autoParseStyle",
                "parseExpression",
            ]),
            d = n.construct,
            m = n.didMount;
        return (
            io(function () {
                null == d || d();
            }),
            ro(function () {
                null == m || m();
            }, []),
            to.createElement(
                Lr,
                { renderStore: r },
                to.createElement(
                    Ur.Provider,
                    {
                        value: Zr(
                            {
                                meta: i,
                                global: c,
                                autoParseStyle: u,
                                parseExpression: f,
                            },
                            p,
                        ),
                    },
                    to.createElement(ao, null),
                ),
            )
        );
    },
    so = Object.freeze(
        Object.defineProperty(
            {
                __proto__: null,
                IteratorContext: $r,
                RenderStore: Tn,
                createActionInstance: ft,
                createActionSchema: et,
                createComponentInstance: dt,
                createComponentSchema: nt,
                createHotAreaInstance: pt,
                createHotAreaSchema: tt,
                createPluginInstance: mt,
                createPluginSchema: rt,
                default: co,
                evalExpression: Ln,
                formatActionInstance: vt,
                formatComponentInstance: yt,
                formatInstance: function (e, t, n) {
                    (void 0 === n && (n = {}),
                        e.componentInstances.forEach(function (e) {
                            return yt(e, t, n);
                        }),
                        e.pluginInstances.forEach(function (e) {
                            return gt(e, t);
                        }));
                },
                formatPluginInstance: gt,
                getSchema: function (e) {
                    return {
                        components: e.componentInstances.map(function (e) {
                            return nt(e);
                        }),
                        plugins: e.pluginInstances.map(function (e) {
                            return rt(e);
                        }),
                        version: C(e.version),
                    };
                },
                getStoreKeyByExpression: $n,
                handleSchema: Hn,
                isCircleComp: In,
                memoCompare: Vn,
                mergeMaterials: function () {
                    for (var e = [], t = 0; t < arguments.length; t++)
                        e[t] = arguments[t];
                    if (1 === e.length) return e[0];
                    var n = e.reduce(
                        function (e, t) {
                            return (
                                Object.assign(e.components, t.components),
                                Object.assign(e.plugins, t.plugins),
                                Object.assign(e.actions, t.actions),
                                e
                            );
                        },
                        { components: {}, plugins: {}, actions: {} },
                    );
                    return n;
                },
                parseDollarRowIterator: Nn,
                parseSchema: ht,
                parseStyles: lt,
            },
            Symbol.toStringTag,
            { value: "Module" },
        ),
    ),
    uo = window.React,
    lo = window.ReactDom,
    fo = () => {
        (!window.React && uo && (window.React = uo),
            !window.ReactDom && lo && (window.ReactDom = lo),
            !window.GemsRendererReact && so && (window.GemsRendererReact = so),
            (window.__gems_preview = Fo));
    },
    po = (e, t = 3) =>
        new Promise((n, r) => {
            const o = (t) => {
                e()
                    .then(n)
                    .catch((e) => {
                        t > 0 ? o(t - 1) : r(e);
                    })
                    .then();
            };
            o(t);
        }),
    mo = (e, t, n, r) => {
        const o = `@impage-materials-main${n && "*" !== n ? `.${n}` : ""}-${e}`;
        return o in r
            ? r[o]
            : new Promise((n, i) => {
                  const a = r.document,
                      c = a.createElement("script");
                  (c.setAttribute("src", t),
                      c.setAttribute(
                          "class",
                          "@impage-materials-inject-script",
                      ),
                      c.addEventListener("load", () => {
                          if (o in r) {
                              const e = r[o];
                              return n(e);
                          }
                          return i(
                              `main bundle [${e}] must build with UMD except:${o}`,
                          );
                      }),
                      c.addEventListener("error", i),
                      a.body.appendChild(c));
              });
    };
async function ho(e, t, n = document) {
    if (!document.querySelector(`link[href=${JSON.stringify(t)}]`))
        return new Promise((e, r) => {
            const o = n.createElement("link");
            ((o.href = t),
                (o.rel = "stylesheet"),
                (o.type = "text/css"),
                o.setAttribute("class", "@impage-materials-inject-style"),
                o.addEventListener("load", () => {
                    e(void 0);
                }),
                o.addEventListener("error", () => {
                    r();
                }),
                n.head.appendChild(o));
        });
}
class vo {
    constructor() {
        this.eventMap = new Map();
    }
    newInstance() {
        return new vo();
    }
    extend() {
        return this;
    }
    on(e, t) {
        var n;
        return (
            this.eventMap.has(e) || this.eventMap.set(e, []),
            null === (n = this.eventMap.get(e)) || void 0 === n || n.push(t),
            () => {
                const n = this.eventMap.get(e);
                if (!n) return;
                const r = n.indexOf(t);
                -1 !== r && n.splice(r, 1);
            }
        );
    }
    emit(e, ...t) {
        const n = [];
        if (this.eventMap.has(e)) {
            const r = this.eventMap.get(e);
            if (!r) return n;
            for (const e of r.slice(0)) n.push(e(...t));
        }
        return n;
    }
    off(e, t) {
        e
            ? t
                ? this.eventMap.forEach((n, r) => {
                      if (r === e) {
                          const e = n.indexOf(t);
                          -1 !== e && n.splice(e, 1);
                      }
                  })
                : this.eventMap.delete(e)
            : this.eventMap.clear();
    }
    keys() {
        return Array.from(this.eventMap.keys());
    }
}
(window.React.useEffect, window.React.useState);
const yo = window.React.useLayoutEffect,
    go = window.React.useMemo,
    wo = window.React.useRef,
    bo = function ({ schema: e, materials: t, global: n, meta: r }) {
        const o = wo();
        (null == n ? void 0 : n.eventBus) ||
            o.current ||
            (o.current = new vo());
        const i = go(
            () => (o.current ? { eventBus: o.current, ...n } : n),
            [n],
        );
        return t && e
            ? f.jsx(Fo.GemsRendererReact, {
                  schema: e,
                  materials: t,
                  global: i,
                  meta: r,
              })
            : null;
    },
    _o = function ({ materials: e, schema: t, global: n, meta: r, loader: o }) {
        return (
            yo(() => {
                if (o) {
                    if (Array.isArray(o)) {
                        const e = o.map((e) => jo(e, -1));
                        return () => {
                            for (const t of e) t();
                        };
                    }
                    return jo(o);
                }
            }, [o]),
            ko(e),
            go(fo, []),
            f.jsx(Ro, { schema: t, global: n, meta: r })
        );
    },
    Eo = window.React.useEffect,
    Oo = window.React.useLayoutEffect,
    So = window.React.useMemo,
    Ao = window.React.useRef,
    Po = window.React.useState,
    Co = [],
    xo = {},
    Io = {},
    To = {},
    jo = (e, t = 0) =>
        "function" != typeof e
            ? () => {}
            : (-1 === t
                  ? Co.push(e)
                  : 0 === t
                    ? Co.unshift(e)
                    : Co.splice(t, 0, e),
              () => {
                  const t = Co.indexOf(e);
                  -1 !== t && Co.splice(t, 1);
              }),
    ko = (e) => {
        (Oo(() => {
            if (!(null == document ? void 0 : document.querySelectorAll))
                return;
            const e = document.querySelectorAll("script[data-gems]");
            if (!e.length) return;
            const t = {};
            for (const n of e) {
                const e = n.getAttribute("data-gems") || "",
                    r = n.getAttribute("data-name") || e,
                    o = n.getAttribute("data-type") || "*",
                    i = n.getAttribute("src") || "";
                e && (t[e] = { meta: i, name: r, alias: e, type: o });
            }
            return jo((e) => {
                if (e in t) return t[e];
            });
        }, []),
            Oo(() => {
                if (e)
                    return Array.isArray(e)
                        ? jo(async (t, n) => {
                              const r = e.find(
                                  (e) => (e.alias || e.name) === t,
                              );
                              if (r)
                                  return {
                                      meta: r.meta,
                                      name: r.name,
                                      type: r.type,
                                      alias: r.alias,
                                  };
                          })
                        : jo((t, n) => {
                              if (!(t in e)) return;
                              const r = e[t],
                                  o = Wo(r);
                              return {
                                  meta: r,
                                  name: o.gems || t,
                                  alias: t,
                                  type: o.type || "*",
                              };
                          });
            }, [e]));
    },
    Ro = function ({ schema: e, global: t, meta: n }) {
        const r = So(() => {
                var n, r;
                const o =
                    e ||
                    (null ==
                    (r =
                        null == (n = null == t ? void 0 : t.pages)
                            ? void 0
                            : n[0])
                        ? void 0
                        : r.data);
                return "string" == typeof o ? JSON.parse(o) : o;
            }, [null == t ? void 0 : t.pages, e]),
            [o, i] = Po(() => Mo(r));
        return (
            Eo(() => {
                r &&
                    (Mo(r)
                        ? i(!0)
                        : $o(r).then(() => {
                              i(!0);
                          }));
            }, [r]),
            Eo(() => {
                if (!o || !(null == t ? void 0 : t.pages)) return;
                const e = t.pages;
                if (!e || !Array.isArray(e)) return;
                const n = setTimeout(() => {
                    for (const t of e) {
                        if (!t) continue;
                        const e =
                            "string" == typeof t.data
                                ? JSON.parse(t.data)
                                : t.data;
                        e &&
                            $o(e, { silent: !0 })
                                .then()
                                .catch((e) => {});
                    }
                }, 2e3);
                return () => {
                    clearTimeout(n);
                };
            }, [t, o]),
            o
                ? f.jsx(bo, {
                      materials: Fo.materialsMap,
                      schema: r,
                      global: t,
                      meta: n,
                  })
                : null
        );
    },
    No = async (e) => {
        if ("materialsName" in xo) return xo[e];
        for (const t of Co) {
            const n = await t(e, {});
            if (n) {
                const t = n.alias || n.name;
                if (t !== e)
                    throw new Error(
                        `loader: 返回的name与传入的name不一致,[name]:${e},loader返回：${t}`,
                    );
                return ((xo[e] = n), n);
            }
        }
        throw new Error(`素材库加载失败！无法解析素材库：${e}`);
    },
    Mo = (e) => {
        if (!e) return !1;
        const { components: t } = e,
            n = (e) => {
                if (!Array.isArray(e)) return !1;
                for (const t of e) {
                    if (!t) continue;
                    const { id: e } = t;
                    if (!(e in To)) return !1;
                    if (t.children && !n(t.children)) return !1;
                }
                return !0;
            };
        return n(t);
    };
let Lo = !1;
const $o = async (e, t) => {
    Lo = (null == t ? void 0 : t.silent) || !1;
    const { components: n } = e,
        r = [],
        o = (e) => {
            if (Array.isArray(e))
                for (const t of e) {
                    if (!t) continue;
                    const { id: e } = t;
                    (r.push(Uo(e)), r.push(Vo(e)), o(t.children));
                }
        };
    (o(n), await Promise.all(r));
};
let Ho = new Date().getTime();
const Do = () => {
        let e = new Date().getTime();
        const t = Object.keys(Io)
            .map((e) => [e, Io[e]])
            .filter(([, e]) => e.status >= 0 && e.startTime >= Ho)
            .map(
                ([t, n]) => (
                    (e = Math.min(e, n.startTime)),
                    { name: t, progress: n.progress }
                ),
            );
        if (0 === t.length) return;
        const n = t.reduce((e, t) => e + t.progress, 0) / t.length;
        (100 === n && (Ho = Date.now()),
            Fo.event.emit("onLoadProgress", {
                task: t,
                progress: n,
                startTime: e,
            }));
    },
    Uo = async (e) => {
        var t;
        if (e in To) return;
        if (e in Io) {
            if (5 === Io[e].status) return;
            return void (await Io[e].task);
        }
        const n = `${e}`.split("/")[1];
        await Go(n);
        const r = Fo.materialsMap.components.get(e);
        if (!r) throw new Error(`素材库下没有这个组件【${e}】`);
        if (
            "function" == typeof r.component ||
            ("object" == typeof r.component && "$$typeof" in r.component)
        )
            return void (To[e] = Date.now());
        const o = r.loader || (null == (t = r.component) ? void 0 : t.loader);
        if ("function" == typeof o) {
            let t = !1;
            const i = {
                startTime: Date.now(),
                status: 0,
                progress: 0,
                task: new Promise((e, n) => {
                    const r = setInterval(() => {
                        t && (!0 === t ? e() : n(t), clearInterval(r));
                    }, 20);
                }),
            };
            ((Io[e] = i), (i.status = 1), Do());
            const a = await No(n),
                c = a.meta.substring(0, a.meta.lastIndexOf("/") + 1);
            if (
                ((r.component = (
                    await po(o.bind(null, c), 3).catch((n) => {
                        throw (
                            (i.status = -1),
                            (t =
                                n instanceof Error
                                    ? n
                                    : new Error(
                                          `加载组件[${e}]发生异常：${n}`,
                                      )),
                            t
                        );
                    })
                ).default),
                !r.component)
            )
                throw (
                    (i.status = -1),
                    (t = new Error(
                        `组件loader结果格式不正确，组件[${e}]加载失败！`,
                    )),
                    t
                );
            return (
                delete r.loader,
                (i.endTime = Date.now()),
                (i.progress = 100),
                (i.status = 5),
                (To[e] = Date.now()),
                Do(),
                void (t = !0)
            );
        }
        throw new Error(`无法加载这个组件！${e}`);
    },
    Vo = async (e) => {
        const t = `config:${e}`;
        if (t in To) return;
        if (t in Io) {
            if (5 === Io[t].status) return;
            return void (await Io[t].task);
        }
        const n = `${e}`.split("/")[1],
            r = `${e}`.split("/")[2];
        await Go(n);
        const o = Fo.materialsMap.components.get(e);
        if ("dataForm" in o) To[t] = Date.now();
        else {
            if ("configLoader" in o) {
                if ("function" == typeof o.configLoader) {
                    let i = !1;
                    const a = {
                        startTime: Date.now(),
                        status: 0,
                        progress: 0,
                        task: new Promise((e, t) => {
                            const n = setInterval(() => {
                                i && (!0 === i ? e() : t(i), clearInterval(n));
                            }, 20);
                        }),
                    };
                    ((Io[t] = a), (a.status = 1), Do());
                    const c = await No(n),
                        s = c.meta.substring(0, c.meta.lastIndexOf("/") + 1),
                        u = (
                            await po(o.configLoader.bind(null, s), 3).catch(
                                (t) => {
                                    throw (
                                        (a.status = -1),
                                        (i =
                                            t instanceof Error
                                                ? t
                                                : new Error(
                                                      `加载组件[${e}]表单发生异常：${t}`,
                                                  )),
                                        i
                                    );
                                },
                            )
                        ).default;
                    Object.assign(o, u);
                    const l = window.__gems_editor;
                    if (null == l ? void 0 : l.store) {
                        const t = l.store.getState();
                        t.editorOptions.materialsBundles
                            .filter((e) => e.meta.js.project.libName === n)
                            .forEach((e) => {
                                e.meta.js.components
                                    .filter((e) => e.name === r)
                                    .forEach((e) => {
                                        Object.assign(e, u);
                                    });
                            });
                        for (let n = 0; n < t.materials.components.length; n++)
                            t.materials.components[n].id === e &&
                                Object.assign(t.materials.components[n], u);
                        l.store.setState(t);
                    }
                    if (!o.dataForm)
                        throw (
                            (a.status = -1),
                            (i = new Error(
                                `组件表单loader结果格式不正确，组件[${t}]表单加载失败！`,
                            )),
                            i
                        );
                    return (
                        delete o.configLoader,
                        (a.endTime = Date.now()),
                        (a.progress = 100),
                        (a.status = 5),
                        (To[t] = Date.now()),
                        Do(),
                        void (i = !0)
                    );
                }
                throw new Error(`无法加载这个组件表单！${t}`);
            }
            To[t] = Date.now();
        }
    },
    Go = async (e) => {
        if (e in To) return;
        if (e in Io) {
            if (5 === Io[e].status) return;
            return void (await Io[e].task);
        }
        const t = [];
        if (
            (Fo.materialsMap.components.forEach((e, n) => {
                "string" == typeof n && t.push(n);
            }),
            t.find((t) => t.startsWith(`component/${e}/`)))
        )
            return void (To[e] = Date.now());
        let n = !1;
        const r = {
            startTime: Date.now(),
            status: 0,
            progress: 0,
            task: new Promise((e, t) => {
                const r = setInterval(() => {
                    n && (!0 === n ? e() : t(n), clearInterval(r));
                }, 20);
            }),
        };
        ((Io[e] = r), Do());
        const o = await No(e).catch((e) => {
            throw (
                (r.status = -1),
                (n =
                    e instanceof Error
                        ? e
                        : new Error(`调用loader发生异常：${e}`)),
                n
            );
        });
        ((r.status = 1),
            (r.progress = 50),
            Do(),
            await Fo.mountMaterials(o).catch((e) => {
                throw (
                    (r.status = -1),
                    (n =
                        e instanceof Error
                            ? e
                            : new Error(`挂载素材库发生异常：${e}`)),
                    n
                );
            }),
            (r.endTime = Date.now()),
            (r.progress = 100),
            (r.status = 5),
            Do(),
            (To[e] = Date.now()),
            (n = !0));
    },
    Wo = (e) => {
        const t = e.split("?")[1];
        if (!t) return {};
        const n = t.split("#")[0].split("&"),
            r = {};
        return (
            n.forEach((e) => {
                const t = e.split("=");
                r[t[0] ? decodeURIComponent(t[0]) : t[0]] = t[1]
                    ? decodeURIComponent(t[1])
                    : t[1];
            }),
            r
        );
    },
    zo = async (e) => {
        const { meta: t, type: n, name: r, alias: o } = e,
            i = `@impage-materials-main${n && "*" !== n ? `.${n}` : ""}-${r}`;
        if (i in window) return window[i];
        const a = document.querySelector(
            `script[data-gems=${JSON.stringify(o || r)}]`,
        );
        if (a) {
            let e;
            if (
                (await Promise.race([
                    new Promise((e) => {
                        a.addEventListener("load", () => {
                            e(void 0);
                        });
                    }),
                    new Promise((t) => {
                        window[i]
                            ? t(void 0)
                            : (e = setInterval(() => {
                                  window[i] && t(void 0);
                              }, 10));
                    }),
                    new Promise((e) => {
                        setTimeout(() => {
                            e(void 0);
                        }, 1e4);
                    }),
                ]),
                e && clearInterval(e),
                !(i in window))
            )
                throw new Error(`FastMaterials: 素材库【${o || r}】加载失败!`);
            return window[i];
        }
        let c = await (async () => {
            const e = document.querySelector(
                `script[data-meta=${JSON.stringify(t)}]`,
            );
            if (e) {
                const t = e.getAttribute("data-content");
                if (t)
                    try {
                        const e = JSON.parse(t);
                        if (e) return e;
                    } catch (i) {}
            }
            const o = Wo(t);
            if ("gems" in o) {
                const e = {},
                    { hash: t, vision: i, meta: a } = o,
                    c = qe(n);
                if ("string" == typeof a) {
                    const t = a.split(",");
                    (([e[c.mainJS]] = t),
                        "main.css" in o && ([, e[c.mainCSS]] = t));
                } else {
                    const a = "string" == typeof i ? `${r}.` : "",
                        s = n && "*" !== n ? `.${n}` : "",
                        u = t ? `${t}.` : "";
                    ((e[c.mainJS] = `${a}main${s}.${u}js`),
                        "main.css" in o &&
                            (e[c.mainCSS] = `${a}main${s}.${u}css`));
                }
                return e;
            }
            return JSON.parse(
                await (async function (e) {
                    return "fetch" in window
                        ? (await fetch(e)).text()
                        : new Promise((t, n) => {
                              const r = new XMLHttpRequest();
                              (r.open("GET", e),
                                  r.send(),
                                  (r.onreadystatechange = function () {
                                      4 === r.readyState &&
                                          (r.status >= 200 && r.status < 300
                                              ? t(r.responseText)
                                              : n(new Error(r.statusText)));
                                  }));
                          });
                })(t),
            );
        })();
        c.manifest && (c = c.manifest);
        const s =
                n ||
                ((e) =>
                    e["meta.js"]
                        ? "*"
                        : e["meta.web.js"]
                          ? "web"
                          : e["meta.h5.js"]
                            ? "h5"
                            : e["meta.pc.js"]
                              ? "pc"
                              : e["meta.mp.js"]
                                ? "mp"
                                : e["meta.hybrid.js"]
                                  ? "hybrid"
                                  : "*")(c),
            u = `@impage-materials-main${s && "*" !== s ? `.${s}` : ""}-${r}`;
        if (u in window) return window[u];
        const { mainJS: l, mainCSS: f } = (function (e, t) {
                const n = qe(t);
                return {
                    metaJS: e[n.metaJS],
                    metaCSS: e[n.metaCSS],
                    mainJS: e[n.mainJS],
                    mainCSS: e[n.mainCSS],
                };
            })(c, s),
            p = t.substring(0, t.lastIndexOf("/") + 1),
            [, d] = await Promise.all([
                f ? ho(0, p + f) : Promise.resolve(),
                mo(r, p + l, s, window),
            ]);
        return d;
    },
    Bo = function () {
        var e, t;
        const [n, r] = Po("none"),
            [o, i] = Po(0),
            [a, c] = Po(0),
            { loadingAnimation: s } = Fo,
            u = Ao(),
            l = Ao();
        return (
            Eo(() => {
                if (s.enable)
                    return Fo.event.on("onLoadProgress", (e) => {
                        if (s.enable && !Lo) {
                            if (e.progress >= 100)
                                (u.current &&
                                    (clearTimeout(u.current),
                                    (u.current = void 0)),
                                    l.current ||
                                        (l.current = setTimeout(() => {
                                            ((l.current = void 0),
                                                i(0),
                                                setTimeout(() => {
                                                    (r("none"), c(0));
                                                }, 400));
                                        }, s.delay)));
                            else if (
                                (l.current &&
                                    (clearTimeout(l.current),
                                    (l.current = void 0)),
                                !u.current)
                            ) {
                                let t = e.startTime + s.delay - Date.now();
                                (t < 0 && (t = 0),
                                    (u.current = setTimeout(() => {
                                        ((u.current = void 0),
                                            r("block"),
                                            i(1));
                                    }, t)));
                            }
                            setTimeout(() => {
                                c(Math.round(10 * e.progress) / 10);
                            });
                        } else r("none");
                    });
            }, [s.delay, s.enable]),
            f.jsx(
                "div",
                {
                    style: {
                        position: "fixed",
                        top: null != (e = s.offsetY) ? e : 0,
                        left: null != (t = s.offsetX) ? t : 0,
                        right: 0,
                        bottom: 0,
                        margin: "auto",
                        width: "156px",
                        height: "134px",
                        lineHeight: "134px",
                        backgroundColor: "rgba(0, 0, 0, 0.6)",
                        borderRadius: "8px",
                        zIndex: 1e9,
                        pointerEvents: "none",
                        userSelect: "none",
                        textAlign: "center",
                        color: "#fff",
                        display: n,
                        opacity: o,
                        transition: "opacity 0.2s",
                        transitionDelay: "0.2s",
                        fontSize: "14px",
                    },
                    children: f.jsxs("svg", {
                        width: "108px",
                        height: "108px",
                        style: { verticalAlign: "middle" },
                        children: [
                            f.jsx("circle", {
                                cx: "52",
                                cy: "52",
                                r: "25",
                                fill: "none",
                                strokeWidth: "4",
                                stroke: "#808080",
                            }),
                            f.jsx("circle", {
                                cx: "52",
                                cy: "52",
                                r: "25",
                                fill: "none",
                                strokeWidth: "4",
                                style: {
                                    strokeDashoffset: 314 - (a / 100) * 157,
                                    fill: "none",
                                    stroke: "#fff",
                                    strokeWidth: "4",
                                    strokeDasharray: "314",
                                    strokeLinecap: "round",
                                    transform: "rotate(-90deg)",
                                    transformOrigin: "center",
                                    transformBox: "fill-box",
                                    transition:
                                        "stroke-dashoffset 0.2s ease 0s",
                                },
                            }),
                            f.jsx("text", {
                                x: "52",
                                y: "57",
                                fill: "#fff",
                                textAnchor: "middle",
                                children: f.jsxs("tspan", {
                                    style: {
                                        fontWeight: "400",
                                        color: "#fff",
                                        width: "0.8rem",
                                        height: "0.8rem",
                                        border: "0.1rem solid #ccc",
                                        borderRadius: "50%",
                                        textAlign: "center",
                                        lineHeight: ".8rem",
                                    },
                                    children: [a, "%"],
                                }),
                            }),
                        ],
                    }),
                },
                "loading",
            )
        );
    },
    Fo = {
        materialsMap: {
            components: new Map(),
            actions: new Map(),
            plugins: new Map(),
        },
        addLoader: jo,
        GemsRendererReact: co,
        mountMaterials: async (e) => {
            const t = await po(() => zo(e), 3).catch((e) => {
                    throw e;
                }),
                n = e.alias || e.name;
            (Object.keys(t.components).forEach((e) => {
                const r = `component/${n}/${e}`,
                    o = t.components[e];
                Fo.materialsMap.components.set(
                    r,
                    "function" == typeof o ? { component: o } : o,
                );
            }),
                Object.keys(t.actions).forEach((e) => {
                    const r = `action/${n}/${e}`;
                    Fo.materialsMap.actions.set(r, t.actions[e]);
                }),
                Object.keys(t.plugins).forEach((e) => {
                    const r = `plugin/${n}/${e}`;
                    Fo.materialsMap.plugins.set(r, t.plugins[e]);
                }));
        },
        event: new vo(),
        GemsRender: Ro,
        getComponentNodeMap: () => K,
        getHotAreaNodeMap: () => X,
        loadingAnimation: { enable: !0, delay: 300 },
        loaderMaterials: No,
        ensurePageContent: $o,
        ensureComponent: Uo,
        ensureComponentConfig: Vo,
    },
    Ko = function () {
        const [e, t, n, r] = Array.isArray(window.__initPage)
            ? window.__initPage
            : [
                  window.__initPage.schema,
                  window.__initPage.materials,
                  window.__initPage.global,
                  window.__initPage.loader,
              ];
        return f.jsxs(f.Fragment, {
            children: [
                f.jsx(_o, {
                    materials: t,
                    schema: e,
                    global: n,
                    meta: void 0,
                    loader: r,
                }),
                f.jsx(Bo, {}),
            ],
        });
    };
window.ReactDom.render(f.jsx(Ko, {}), document.getElementById("app"));
export { e as __vite_legacy_guard };
