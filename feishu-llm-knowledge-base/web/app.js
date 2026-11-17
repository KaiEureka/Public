// Web edition behaviour: sidebar drawer, section highlighting, full-text search, search-term highlighting,
// figure zoom, code copy buttons and the PDF download. The colour theme follows the viewer's setting (style.css).
(function () {
  "use strict";
  var body = document.body;

  // ---------- sidebar drawer (narrow screens) ----------
  var menuBtn = document.getElementById("menu-btn");
  menuBtn.addEventListener("click", function () { body.classList.toggle("nav-open"); });
  document.getElementById("scrim").addEventListener("click", function () { body.classList.remove("nav-open"); });
  document.querySelectorAll(".sidebar a").forEach(function (a) {
    a.addEventListener("click", function () { body.classList.remove("nav-open"); });
  });
  // centre the current chapter inside the sidebar only (scrollIntoView would also scroll the page and its host)
  var sidebar = document.getElementById("sidebar"), cur = sidebar.querySelector("a.current");
  if (cur) sidebar.scrollTop = cur.offsetTop - sidebar.clientHeight / 2;

  // ---------- a page opened from a link starts at its top (or at its #target) ----------
  // The viewer may keep the previous page's scroll position, or scroll a frame that grows with its content,
  // so put the reader in place explicitly; back/forward and reload keep the browser's own restoration.
  var hold = false;  // set when something else (a search hit) decides where the page should be
  var nav = performance.getEntriesByType && performance.getEntriesByType("navigation")[0];
  if (!nav || nav.type === "navigate") {
    var touched = false;
    ["wheel", "touchstart", "keydown", "mousedown"].forEach(function (t) {
      window.addEventListener(t, function () { touched = true; }, { once: true, passive: true });
    });
    var place = function () {
      if (touched || hold) return;
      var target = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (target) target.scrollIntoView({ block: "start" });
      else { window.scrollTo(0, 0); document.documentElement.scrollIntoView({ block: "start" }); }
    };
    place();
    window.addEventListener("load", place);
    setTimeout(place, 300);
  }

  // ---------- highlight the section being read ----------
  var secLinks = {};
  document.querySelectorAll(".side-secs a").forEach(function (a) { secLinks[a.dataset.sec] = a; });
  var heads = Array.prototype.filter.call(document.querySelectorAll(".content h3[id]"), function (h) { return secLinks[h.id]; });
  if (heads.length) {
    var active = null;
    var update = function () {
      var y = 90, hit = heads[0];
      for (var i = 0; i < heads.length; i++) { if (heads[i].getBoundingClientRect().top < y) hit = heads[i]; else break; }
      if (hit !== active) {
        if (active) secLinks[active.id].classList.remove("active");
        secLinks[hit.id].classList.add("active");
        active = hit;
      }
    };
    window.addEventListener("scroll", update, { passive: true });
    update();
  }

  // ---------- search ----------
  var input = document.getElementById("search"), panel = document.getElementById("search-results");
  var index = null, loading = null, sel = -1;
  if (matchMedia("(max-width: 640px)").matches) input.placeholder = "搜索";
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function load() {
    if (!loading) {
      loading = fetch("assets/search.json").then(function (r) { return r.json(); }).then(function (d) {
        index = d.map(function (e) { return { p: e[0], a: e[1], t: e[2], x: e[3], lx: e[3].toLowerCase(), lt: e[2].toLowerCase() }; });
      });
    }
    return loading;
  }
  function snippet(e, terms) {
    var i = e.lx.indexOf(terms[0]);
    if (i < 0) i = 0;
    var a = Math.max(0, i - 40), s = (a ? "…" : "") + e.x.slice(a, a + 140) + (a + 140 < e.x.length ? "…" : "");
    var out = esc(s);
    terms.forEach(function (t) {
      if (!t) return;
      var re = new RegExp(esc(t).replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "gi");
      out = out.replace(re, function (m) { return "<mark>" + m + "</mark>"; });
    });
    return out;
  }
  function run() {
    var q = input.value.trim().toLowerCase();
    sel = -1;
    if (!q) { panel.hidden = true; return; }
    if (!index) { panel.hidden = false; panel.innerHTML = '<div class="hint">正在载入索引…</div>'; load().then(run); return; }
    var terms = q.split(/\s+/), hits = [];
    for (var i = 0; i < index.length && hits.length < 400; i++) {
      var e = index[i], ok = true, score = 0;
      for (var k = 0; k < terms.length; k++) {
        var inT = e.lt.indexOf(terms[k]) >= 0, inX = e.lx.indexOf(terms[k]) >= 0;
        if (!inT && !inX) { ok = false; break; }
        score += inT ? 10 : 0;
      }
      if (ok) hits.push({ e: e, s: score, n: i });
    }
    hits.sort(function (a, b) { return b.s - a.s || a.n - b.n; });
    var total = hits.length;
    hits = hits.slice(0, 60);
    panel.hidden = false;
    if (!hits.length) { panel.innerHTML = '<div class="hint">没有找到“' + esc(input.value.trim()) + '”</div>'; return; }
    panel.innerHTML = '<div class="hint">共 ' + (total >= 400 ? "400+" : total) + " 处" + (total > 60 ? "，显示前 60 处" : "") + "</div>" +
      hits.map(function (h) {
        var url = h.e.p + ".html" + (h.e.a ? "#" + encodeURIComponent(h.e.a) : "");
        return '<a href="' + url + '"><b>' + esc(h.e.t) + "</b><span>" + snippet(h.e, terms) + "</span></a>";
      }).join("");
  }
  function remember() { try { sessionStorage.setItem("hl", input.value.trim()); } catch (e) {} }
  panel.addEventListener("click", function (ev) { if (ev.target.closest("a")) remember(); });
  var timer = null;
  input.addEventListener("focus", load);
  input.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(run, 120); });
  input.addEventListener("keydown", function (ev) {
    var items = panel.querySelectorAll("a");
    if (ev.key === "ArrowDown" || ev.key === "ArrowUp") {
      if (!items.length) return;
      ev.preventDefault();
      if (sel >= 0) items[sel].classList.remove("sel");
      sel = (sel + (ev.key === "ArrowDown" ? 1 : items.length - 1)) % items.length;
      items[sel].classList.add("sel");
      items[sel].scrollIntoView({ block: "nearest" });
    } else if (ev.key === "Enter" && items.length) {
      remember();
      location.href = items[Math.max(sel, 0)].href;
    } else if (ev.key === "Escape") {
      panel.hidden = true; input.blur();
    }
  });
  document.addEventListener("click", function (ev) { if (!ev.target.closest(".search")) panel.hidden = true; });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "/" && document.activeElement !== input && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) {
      ev.preventDefault(); input.focus();
    }
  });

  // ---------- highlight the searched words on the target page ----------
  var hl = null;
  try { hl = sessionStorage.getItem("hl"); sessionStorage.removeItem("hl"); } catch (e) {}
  if (hl) {
    var terms = hl.toLowerCase().split(/\s+/).filter(Boolean), first = null;
    var start = location.hash ? document.getElementById(decodeURIComponent(location.hash.slice(1))) : null;
    var walker = document.createTreeWalker(document.querySelector(".content"), NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) { return n.parentNode.closest("svg, math, script") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT; }
    });
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (n) {
      var low = n.nodeValue.toLowerCase(), best = -1, len = 0;
      terms.forEach(function (t) { var i = low.indexOf(t); if (i >= 0 && (best < 0 || i < best)) { best = i; len = t.length; } });
      while (best >= 0) {
        var m = document.createElement("mark"), rest = n.splitText(best);
        n = rest.splitText(len);
        m.appendChild(rest.cloneNode());
        rest.parentNode.replaceChild(m, rest);
        if (!first && (!start || (start.compareDocumentPosition(m) & Node.DOCUMENT_POSITION_FOLLOWING))) first = m;
        low = n.nodeValue.toLowerCase(); best = -1;
        terms.forEach(function (t) { var i = low.indexOf(t); if (i >= 0 && (best < 0 || i < best)) { best = i; len = t.length; } });
      }
    });
    input.value = hl;
    if (first) { hold = true; setTimeout(function () { first.scrollIntoView({ block: "center" }); }, 60); }
  }

  // ---------- figures: click to enlarge; flash the target of a figure reference ----------
  document.querySelectorAll("figure > svg").forEach(function (svg) {
    svg.addEventListener("click", function () {
      var box = document.createElement("div"), card = document.createElement("div"), big = svg.cloneNode(true);
      var vb = svg.viewBox.baseVal, w = Math.max(Math.min(window.innerWidth * 0.94 - 32, 1500), 900 * vb.width / 660);
      if (window.innerWidth >= 900) w = Math.min(w, (window.innerHeight * 0.92 - 32) * vb.width / vb.height);
      big.style.width = Math.round(Math.max(w, svg.getBoundingClientRect().width)) + "px";
      big.style.maxWidth = "none";
      box.className = "lightbox";
      card.appendChild(big); box.appendChild(card); document.body.appendChild(box);
      var close = function () { box.remove(); document.removeEventListener("keydown", onKey); };
      var onKey = function (ev) { if (ev.key === "Escape") close(); };
      box.addEventListener("click", close);
      document.addEventListener("keydown", onKey);
    });
  });
  function flash() {
    var t = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (t && t.tagName === "FIGURE") { t.classList.add("flash"); setTimeout(function () { t.classList.remove("flash"); }, 1600); }
  }
  window.addEventListener("hashchange", flash);
  flash();

  // ---------- display formulas wider than the column: shrink a little, else scroll with an edge hint ----------
  function fitMath() {
    document.querySelectorAll('.content math[display="block"]').forEach(function (m) {
      m.style.fontSize = ""; m.classList.remove("wide");
      var s = m.clientWidth / m.scrollWidth;
      if (s >= 1) return;
      if (s >= 0.7) m.style.fontSize = (1.08 * s * 0.98).toFixed(3) + "em";
      if (m.scrollWidth > m.clientWidth + 1) { m.style.fontSize = ""; m.classList.add("wide"); }
    });
  }
  (document.fonts ? document.fonts.ready : Promise.resolve()).then(fitMath);
  var fitTimer = null;
  window.addEventListener("resize", function () { clearTimeout(fitTimer); fitTimer = setTimeout(fitMath, 150); });

  // ---------- copy buttons on code blocks ----------
  document.querySelectorAll(".content pre").forEach(function (pre) {
    var b = document.createElement("button");
    b.className = "copy-btn"; b.type = "button"; b.textContent = "复制";
    b.addEventListener("click", function () {
      var text = (pre.querySelector("code") || pre).innerText.replace(/\n?复制$/, "");
      var done = function () { b.textContent = "已复制"; setTimeout(function () { b.textContent = "复制"; }, 1200); };
      var select = function () {
        var r = document.createRange(); r.selectNodeContents(pre.querySelector("code") || pre);
        var sel = getSelection(); sel.removeAllRanges(); sel.addRange(r);
        b.textContent = "已选中，按 Ctrl+C";
      };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, select); else select();
    });
    (pre.parentNode.classList.contains("sourceCode") ? pre.parentNode : pre).appendChild(b);
  });

  // ---------- PDF download ----------
  function toast(msg, ms) {
    var t = document.querySelector(".toast");
    if (!t) { t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.textContent = msg; t.hidden = false;
    clearTimeout(t._h); if (ms) t._h = setTimeout(function () { t.hidden = true; }, ms);
  }
  var NAME = "从零造一个前沿大模型.pdf", busy = false;
  function plainDownload() {
    var a = document.createElement("a"); a.href = "book.pdf"; a.download = NAME;
    document.body.appendChild(a); a.click(); a.remove();
  }
  function downloadPdf() {
    if (busy) return;
    var use = window.claude && window.claude.use;
    if (!use) { plainDownload(); return; }
    busy = true; toast("正在准备 PDF（约 12 MB）…");
    Promise.all([window.claude.use("downloads"), fetch("book.pdf").then(function (r) {
      if (!r.ok) throw new Error("http " + r.status);
      return r.blob();
    })]).then(function (res) {
      if (!res[0]) { toast("这里不能直接下载，请在本书首页点“下载 PDF”。", 5000); return; }
      toast("请在弹出的确认框里确认保存。");
      return res[0].save({ filename: NAME, data: res[1] }).then(function () { toast("已交给浏览器保存。", 3000); }, function (e) {
        toast(e && e.code === "declined" ? "已取消下载。" : "下载没有成功，请稍后再试。", 4000);
      });
    }).catch(function () { toast("PDF 读取失败，请检查网络后再试。", 4000); })
      .then(function () { busy = false; });
  }
  document.querySelectorAll(".pdf-dl").forEach(function (b) { b.addEventListener("click", downloadPdf); });
})();
