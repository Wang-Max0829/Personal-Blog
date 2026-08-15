(function () {
  "use strict";

  // 年份
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  // 主题切换
  function applyTheme(t) {
    document.documentElement.setAttribute("data-theme", t);
    try { localStorage.setItem("theme", t); } catch (e) {}
    var light = document.getElementById("hljs-light");
    var dark = document.getElementById("hljs-dark");
    if (light) light.disabled = t === "dark";
    if (dark) dark.disabled = t !== "dark";
  }
  var btn = document.getElementById("theme-toggle");
  if (btn) {
    btn.addEventListener("click", function () {
      var cur = document.documentElement.getAttribute("data-theme");
      applyTheme(cur === "dark" ? "light" : "dark");
    });
  }
  applyTheme(document.documentElement.getAttribute("data-theme") || "light");

  // 页面加载后：代码高亮 + 数学公式渲染
  function renderAll() {
    if (window.hljs) {
      document.querySelectorAll("pre code").forEach(function (b) {
        try { window.hljs.highlightElement(b); } catch (e) {}
      });
    }
    if (window.renderMathInElement) {
      document.querySelectorAll(".post-content, .article").forEach(function (el) {
        try {
          window.renderMathInElement(el, {
            delimiters: [
              { left: "$$", right: "$$", display: true },
              { left: "$", right: "$", display: false }
            ],
            throwOnError: false
          });
        } catch (e) {}
      });
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderAll);
  } else {
    renderAll();
  }

  // 首页搜索 + 分类过滤
  var searchInput = document.getElementById("search");
  if (searchInput && window.POSTS) {
    var listEl = document.getElementById("post-list");

    function cardHTML(p) {
      var tags = (p.tags || []).map(function (t) {
        return '<span class="tag">' + t + "</span>";
      }).join("");
      return (
        '<article class="post-card">' +
        '<h2 class="post-title"><a href="' + p.url + '">' + p.title + "</a></h2>" +
        '<div class="post-meta"><span>' + p.date + '</span><span class="dot">·</span>' +
        '<span class="cat">' + p.category_cn + '</span><span class="dot">·</span>' +
        "<span>" + p.reading_min + " 分钟</span></div>" +
        '<p class="post-summary">' + (p.summary || "") + "</p>" +
        '<div class="tags">' + tags + "</div>" +
        "</article>"
      );
    }

    function render(list) {
      if (!list.length) {
        listEl.innerHTML = '<p class="empty">没有找到匹配的文章。</p>';
        return;
      }
      listEl.innerHTML = list.map(cardHTML).join("");
    }

    function filter() {
      var q = searchInput.value.trim().toLowerCase();
      var active = document.querySelector(".chip.active");
      var cat = active ? active.getAttribute("data-cat") : "all";
      var res = window.POSTS.filter(function (p) {
        var okCat = cat === "all" || p.category === cat;
        var hay = (p.title + " " + (p.tags || []).join(" ") + " " + (p.summary || "")).toLowerCase();
        var okQ = !q || hay.indexOf(q) >= 0;
        return okCat && okQ;
      });
      render(res);
    }

    searchInput.addEventListener("input", filter);
    document.querySelectorAll(".chip").forEach(function (c) {
      c.addEventListener("click", function () {
        document.querySelectorAll(".chip").forEach(function (x) { x.classList.remove("active"); });
        c.classList.add("active");
        filter();
      });
    });

    render(window.POSTS);
  }
})();
