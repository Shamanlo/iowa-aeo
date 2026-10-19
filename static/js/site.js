/* Iowa AEO: navigation, AI simulator, video and forms. */
(function () {
  "use strict";

  /* ---------- Nav ---------- */
  var path = location.pathname;
  document.querySelectorAll("[data-nav]").forEach(function (a) {
    var key = a.getAttribute("data-nav");
    if (key === "/" ? path === "/" : path.indexOf(key) === 0) a.classList.add("is-active");
  });

  document.querySelectorAll(".dd").forEach(function (dd) {
    var b = dd.querySelector(".dd-btn");
    var t;
    function set(open) {
      dd.classList.toggle("open", open);
      b.setAttribute("aria-expanded", open ? "true" : "false");
    }
    b.addEventListener("click", function (ev) {
      ev.stopPropagation();
      var open = !dd.classList.contains("open");
      document.querySelectorAll(".dd.open").forEach(function (o) { if (o !== dd) o.classList.remove("open"); });
      set(open);
    });
    dd.addEventListener("mouseenter", function () { clearTimeout(t); if (matchMedia("(hover: hover)").matches) set(true); });
    dd.addEventListener("mouseleave", function () { t = setTimeout(function () { set(false); }, 120); });
  });
  document.addEventListener("click", function () {
    document.querySelectorAll(".dd.open").forEach(function (o) { o.classList.remove("open"); });
  });
  document.addEventListener("keydown", function (ev) {
    if (ev.key === "Escape") document.querySelectorAll(".dd.open").forEach(function (o) { o.classList.remove("open"); });
  });

  var menuBtn = document.querySelector("[data-menu]");
  var mobile = document.querySelector("[data-mobile-nav]");
  if (menuBtn && mobile) {
    menuBtn.addEventListener("click", function () {
      var open = mobile.hasAttribute("hidden");
      if (open) mobile.removeAttribute("hidden"); else mobile.setAttribute("hidden", "");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* ---------- Hero video ---------- */
  document.querySelectorAll(".vf-play").forEach(function (b) {
    b.addEventListener("click", function () {
      var frame = b.closest("[data-vframe]");
      var src = b.getAttribute("data-video");
      var el;
      if (/youtube\.com|youtu\.be|vimeo\.com/.test(src)) {
        el = document.createElement("iframe");
        el.src = src + (src.indexOf("?") > -1 ? "&" : "?") + "autoplay=1";
        el.allow = "autoplay; encrypted-media; picture-in-picture";
        el.allowFullscreen = true;
        el.title = "Iowa AEO video";
      } else {
        el = document.createElement("video");
        el.src = src;
        el.controls = true;
        el.autoplay = true;
        el.playsInline = true;
        var poster = b.getAttribute("data-poster");
        if (poster) el.poster = poster;
      }
      frame.classList.add("playing");
      frame.appendChild(el);
    });
  });

  /* ---------- Forms ---------- */
  var params = new URLSearchParams(location.search);
  if (params.get("topic") === "call") {
    document.querySelectorAll('input[name="topic"][value="Book a call"]').forEach(function (r) { r.checked = true; });
  }

  document.querySelectorAll("[data-form]").forEach(function (form) {
    var msg = form.querySelector("[data-msg]");
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var btn = form.querySelector("button[type=submit]");
      var data = Object.fromEntries(new FormData(form));
      var topic = data.topic || "Inquiry";
      data.subject = topic + " - " + (data.business || "Iowa AEO website") + (data.city ? " (" + data.city + ")" : "");
      data.page = (data.page || "") + " " + location.pathname;
      btn.disabled = true;
      msg.className = "form-msg";
      msg.textContent = "Sending…";
      fetch(form.action, {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (r) { return r.json(); })
        .then(function (res) {
          if (!res.success) throw new Error(res.message || "Something went wrong.");
          var done = document.createElement("div");
          done.className = "form-done";
          done.innerHTML = '<span class="b-ico"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg></span>' +
            "<h3>Thanks! We got it.</h3><p>We'll be in touch within one business day. Keep an eye on your inbox.</p>";
          form.appendChild(done);
          form.classList.add("sent");
        })
        .catch(function (err) {
          msg.className = "form-msg err";
          msg.textContent = (err && err.message ? err.message : "Couldn't send.") + " You can also email info@iowaaeo.com.";
          btn.disabled = false;
        });
    });
  });

  /* ---------- AI simulator ---------- */
  var WEIGHTS = { listings: 18, reviews: 20, website: 20, schema: 16, mentions: 20 };
  var BASE = 6;
  var LEVELS = [
    { min: 0, label: "INVISIBLE", status: "Not mentioned", why: "AI couldn't find enough consistent information about you." },
    { min: 30, label: "EMERGING", status: "Mentioned", why: "AI found you, but isn't confident enough to rank you high." },
    { min: 55, label: "VISIBLE", status: "Recommended", why: "AI trusts your facts and recommends you alongside competitors." },
    { min: 80, label: "TOP PICK", status: "Top pick", why: "Clear, consistent, trusted facts. AI recommends you first." }
  ];
  var COMPETITORS = [
    ["Competitor A", "Lots of reviews, but few details about what they do best."],
    ["Competitor B", "Consistent listings and a clear, easy-to-read website."],
    ["Competitor C", "Mentioned in a local “best of” guide."]
  ];
  var INTRO = {
    chatgpt: "Here are a few great options:",
    gemini: "Here are some well-regarded options to consider:",
    perplexity: "Based on local listings, reviews and guides, here are the strongest options:",
    claude: "Here are a few options that stand out:",
    google: "Several local businesses are frequently recommended:"
  };
  var OUTRO = {
    chatgpt: "Want me to check availability or narrow these down by price?",
    gemini: "Would you like directions or more details on any of these?",
    perplexity: "",
    claude: "I'd suggest calling ahead to confirm availability. Want help comparing them?",
    google: ""
  };

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }

  function svg(body, size) {
    return '<svg class="i" width="' + (size || 18) + '" height="' + (size || 18) + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + "</svg>";
  }
  var IC = {
    chev: svg('<path d="m6 9 6 6 6-6"/>', 18),
    copy: svg('<rect x="8" y="8" width="13" height="13" rx="2.5"/><path d="M16 8V5.5A2.5 2.5 0 0 0 13.5 3h-8A2.5 2.5 0 0 0 3 5.5v8A2.5 2.5 0 0 0 5.5 16H8"/>'),
    thumb: svg('<path d="M7 10v11M15 5.9 14 10h5.8a2 2 0 0 1 1.9 2.6l-2.3 7A2 2 0 0 1 17.5 21H4a1 1 0 0 1-1-1v-9a1 1 0 0 1 1-1h2.8a2 2 0 0 0 1.8-1.1L12 2a3 3 0 0 1 3 3.9z"/>'),
    refresh: svg('<path d="M21 12a9 9 0 1 1-2.6-6.4L21 8"/><path d="M21 3v5h-5"/>'),
    plus: svg('<path d="M12 5v14M5 12h14"/>', 22),
    mic: svg('<rect x="9" y="2.5" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3.5"/>', 20),
    wave: svg('<path d="M4 10v4M8 7v10M12 4v16M16 7v10M20 10v4"/>', 20),
    up: svg('<path d="M12 19V5M5 12l7-7 7 7"/>', 20),
    search: svg('<circle cx="11" cy="11" r="7.5"/><path d="m21 21-4.6-4.6"/>', 20),
    layers: svg('<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5M2 12l10 5 10-5"/>', 18),
    spark: svg('<path d="M12 3l1.8 4.7L18.5 9.5l-4.7 1.8L12 16l-1.8-4.7L5.5 9.5l4.7-1.8z"/>', 18)
  };

  function level(score) {
    var n = 0;
    LEVELS.forEach(function (l, i) { if (score >= l.min) n = i; });
    return n;
  }

  function youDescription(q, on) {
    var bits = [];
    if (on.reviews) bits.push(q.review.charAt(0).toUpperCase() + q.review.slice(1));
    if (on.website) bits.push((bits.length ? "the" : "The") + " website shows " + q.site);
    if (on.listings && bits.length < 2) bits.push((bits.length ? "listings" : "Listings") + " match across Google, Apple Maps and Yelp");
    if (on.mentions && bits.length < 2) bits.push((bits.length ? "featured" : "Featured") + " in local guides and press");
    if (on.schema && bits.length < 2) bits.push((bits.length ? "hours" : "Hours") + " and service area are clearly listed");
    if (!bits.length) return "Some information available.";
    return bits.slice(0, 2).join("; ") + ".";
  }

  function answerList(q, on, lvl) {
    var items = COMPETITORS.map(function (c) { return { name: c[0], desc: c[1], you: false }; });
    if (lvl === 0) return items;
    var you = { name: q.you, desc: youDescription(q, on), you: true };
    if (lvl === 1) { items.push(you); return items; }
    if (lvl === 2) return [items[0], you, items[1]];
    return [you, items[1], items[0]];
  }

  function listHTML(items) {
    return "<ol>" + items.map(function (it) {
      return "<li" + (it.you ? ' class="you"' : "") + "><strong>" + esc(it.name) + "</strong> – " + esc(it.desc) + "</li>";
    }).join("") + "</ol>";
  }

  function chatHTML(ai, aiName, mark, q, items) {
    var intro = INTRO[ai], outro = OUTRO[ai];
    var list = listHTML(items);
    var qq = esc(q.q);
    var input = function (ph, right) {
      return '<div class="c-foot"><div class="c-input">' + IC.plus + '<span class="grow">' + ph + "</span>" + right + "</div>";
    };
    if (ai === "chatgpt") {
      return '<div class="c-head">ChatGPT ' + IC.chev + '</div><div class="c-body"><div class="c-user">' + qq + '</div><div class="c-ans" data-ans><p>' + intro + "</p>" + list + "<p>" + outro + '</p></div><div class="c-acts">' + IC.copy + IC.thumb + IC.refresh + "</div></div>" +
        input("Ask anything", IC.mic + '<span class="c-send">' + IC.wave + "</span>") + '<p class="c-disc">ChatGPT can make mistakes. Check important info.</p></div>';
    }
    if (ai === "gemini") {
      return '<div class="c-head">Gemini ' + IC.chev + '</div><div class="c-body"><div class="c-user">' + qq + '</div><div class="c-ans"><span>' + mark + '</span><div data-ans><p>' + intro + "</p>" + list + "<p>" + outro + "</p></div></div></div>" +
        input("Ask Gemini", IC.mic) + '<p class="c-disc">Gemini can make mistakes, so double-check it.</p></div>';
    }
    if (ai === "perplexity") {
      var src = [["yelp.com", "Reviews"], ["maps.apple.com", "Listing"], ["local guide", "Best of " + esc(q.city)], ["+4 sources", ""]];
      return '<div class="c-head">' + mark + ' perplexity</div><div class="c-body"><div class="c-user">' + qq + '</div><div class="c-label">' + IC.layers + 'Sources</div><div class="c-sources">' +
        src.map(function (s) { return '<span class="c-src"><b>' + s[0] + "</b>" + s[1] + "</span>"; }).join("") +
        '</div><div class="c-label">' + mark + 'Answer</div><div class="c-ans" data-ans><p>' + intro + "</p>" + list + '</div><div class="c-acts">' + IC.copy + IC.refresh + "</div></div>" +
        input("Ask a follow-up", '<span class="c-send">' + IC.up + "</span>") + "</div>";
    }
    if (ai === "claude") {
      return '<div class="c-head">' + mark + ' Claude</div><div class="c-body"><div class="c-user"><span class="c-av">Y</span><span>' + qq + '</span></div><div class="c-ans" data-ans><p>' + intro + "</p>" + list + "<p>" + outro + '</p></div><div class="c-acts">' + IC.copy + IC.thumb + IC.refresh + "</div></div>" +
        input("Reply to Claude…", '<span class="c-send">' + IC.up + "</span>") + '<p class="c-disc">Claude can make mistakes. Please double-check responses.</p></div>';
    }
    return '<div class="c-head">' + mark + '</div><div class="c-search">' + IC.search + "<span>" + qq + "</span>" + IC.mic + '</div><div class="c-tabs"><b>All</b><span>AI Mode</span><span>Maps</span><span>Images</span><span>News</span></div>' +
      '<div class="c-body"><div class="c-ov"><div class="c-label">' + IC.spark + 'AI Overview</div><div class="c-ans" data-ans><p>' + intro + "</p>" + list + '</div></div><div class="c-acts">' + IC.thumb + IC.copy + '</div></div><div class="c-foot"><p class="c-disc">AI responses may include mistakes.</p></div>';
  }

  document.querySelectorAll("[data-sim]").forEach(function (sim) {
    var data = JSON.parse(sim.querySelector(".sim-data").textContent);
    var chat = sim.querySelector("[data-chat]");
    var state = { q: 0, ai: "chatgpt", on: {} };
    var lastLevel = 0;
    var timer;

    function score() {
      var s = BASE;
      Object.keys(state.on).forEach(function (k) { if (state.on[k]) s += WEIGHTS[k]; });
      return Math.min(100, s);
    }

    function render(animate) {
      var sc = score(), lvl = level(sc), L = LEVELS[lvl];
      var q = data.questions[state.q];
      var aiBtn = sim.querySelector('.sim-ai[data-ai="' + state.ai + '"]');
      var mark = aiBtn.querySelector("svg").outerHTML;
      var aiName = aiBtn.textContent.trim();

      sim.querySelector("[data-pct]").textContent = sc + "%";
      sim.querySelector("[data-bar]").style.width = sc + "%";
      sim.querySelector("[data-lvl]").textContent = L.label;
      sim.querySelector(".meter").setAttribute("data-level", lvl);
      var pill = sim.querySelector("[data-pill]");
      pill.innerHTML = "Your business: <strong>" + L.status + "</strong>";
      pill.setAttribute("data-level", lvl);
      sim.querySelector("[data-why]").textContent = L.why;

      chat.setAttribute("data-ai", state.ai);
      var items = answerList(q, state.on, lvl);
      clearTimeout(timer);
      if (animate) {
        chat.innerHTML = chatHTML(state.ai, aiName, mark, q, []);
        var ans = chat.querySelector("[data-ans]");
        ans.innerHTML = '<span class="typing"><i></i><i></i><i></i></span>';
        timer = setTimeout(function () {
          chat.innerHTML = chatHTML(state.ai, aiName, mark, q, items);
        }, 650);
      } else {
        chat.innerHTML = chatHTML(state.ai, aiName, mark, q, items);
      }
      lastLevel = lvl;
    }

    sim.querySelectorAll(".sim-q").forEach(function (b) {
      b.addEventListener("click", function () {
        sim.querySelectorAll(".sim-q").forEach(function (x) { x.classList.remove("is-on"); x.setAttribute("aria-pressed", "false"); });
        b.classList.add("is-on"); b.setAttribute("aria-pressed", "true");
        state.q = +b.getAttribute("data-q");
        render(true);
      });
    });
    sim.querySelectorAll(".sim-ai").forEach(function (b) {
      b.addEventListener("click", function () {
        sim.querySelectorAll(".sim-ai").forEach(function (x) { x.classList.remove("is-on"); x.setAttribute("aria-pressed", "false"); });
        b.classList.add("is-on"); b.setAttribute("aria-pressed", "true");
        state.ai = b.getAttribute("data-ai");
        render(true);
      });
    });
    var boxes = sim.querySelectorAll("input[data-sig]");
    boxes.forEach(function (c) {
      c.addEventListener("change", function () {
        var before = lastLevel;
        state.on[c.getAttribute("data-sig")] = c.checked;
        render(level(score()) !== before);
      });
    });
    sim.querySelector("[data-all]").addEventListener("click", function () {
      boxes.forEach(function (c) { c.checked = true; state.on[c.getAttribute("data-sig")] = true; });
      render(true);
    });
    sim.querySelector("[data-reset]").addEventListener("click", function () {
      boxes.forEach(function (c) { c.checked = false; });
      state.on = {};
      render(true);
    });
    render(false);
  });
})();
