(function () {
  var root = document.querySelector("[data-project-filter]");
  if (!root) return;

  var buttons = root.querySelectorAll("[data-filter]");
  var status = root.querySelector("[data-filter-status]");
  var lang = document.documentElement.lang || "ja";
  var regions = [
    { id: "projects", items: document.querySelectorAll("#projects .soujo-feature, #projects .project-card") },
    { id: "engineering", items: document.querySelectorAll("#engineering .engineering-list article") },
    { id: "exploring", items: document.querySelectorAll("#exploring .exploring-list article") }
  ];

  function tagsOf(item) {
    var raw = item.getAttribute("data-tags");
    if (!raw) return [];
    return raw.trim().split(/\s+/).filter(Boolean);
  }

  function matches(item, filter) {
    if (filter === "all") return true;
    return tagsOf(item).indexOf(filter) !== -1;
  }

  function labelFor(filter) {
    var i;
    for (i = 0; i < buttons.length; i += 1) {
      if (buttons[i].getAttribute("data-filter") === filter) {
        return buttons[i].textContent.replace(/\s+/g, " ").trim();
      }
    }
    return filter;
  }

  function apply(filter) {
    var total = 0;
    Array.prototype.forEach.call(buttons, function (button) {
      button.setAttribute("aria-pressed", button.getAttribute("data-filter") === filter ? "true" : "false");
    });
    regions.forEach(function (region) {
      var count = 0;
      Array.prototype.forEach.call(region.items, function (item) {
        var show = matches(item, filter);
        item.classList.toggle("is-filtered-out", !show);
        if (show) count += 1;
      });
      total += count;
      var empty = document.querySelector('[data-filter-empty="' + region.id + '"]');
      if (empty) empty.hidden = filter === "all" || count > 0;
    });
    if (!status) return;
    if (filter === "all") {
      status.textContent = "";
      return;
    }
    var label = labelFor(filter);
    status.textContent = lang === "en"
      ? label + ": " + total + (total === 1 ? " item" : " items")
      : label + "：" + total + "件";
  }

  Array.prototype.forEach.call(buttons, function (button) {
    button.addEventListener("click", function () {
      apply(button.getAttribute("data-filter"));
    });
  });

  document.addEventListener("click", function (event) {
    var link = event.target.closest && event.target.closest("a[href^='#']");
    if (!link) return;
    var id = decodeURIComponent(link.getAttribute("href").slice(1));
    var target = document.getElementById(id);
    if (target && target.closest(".is-filtered-out")) apply("all");
  });

  apply("all");
  root.hidden = false;
}());
