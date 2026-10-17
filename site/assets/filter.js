(function () {
  var root = document.querySelector("[data-project-filter]");
  if (!root) return;

  var buttons = root.querySelectorAll("[data-filter]");
  var status = root.querySelector("[data-filter-status]");
  var lang = document.documentElement.lang || "ja";
  var regions = [
    { id: "projects", items: document.querySelectorAll("#projects .project-card") },
    { id: "engineering", items: document.querySelectorAll("#engineering .engineering-list article") },
    { id: "exploring", items: document.querySelectorAll("#exploring .exploring-list article") }
  ];

  function tagsOf(item) {
    var raw = item.getAttribute("data-tags");
    if (!raw) return [];
    return raw.trim().split(/\s+/).filter(Boolean);
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

  // 該当した理由が見えるよう、選んだ分野と同じ名前の表示タグを塗りつぶす。
  function markTags(item, label, highlighted) {
    Array.prototype.forEach.call(item.querySelectorAll(".tag-list li"), function (tag) {
      tag.classList.toggle("is-current-tag", highlighted && tag.textContent.trim() === label);
    });
  }

  // 該当しない項目も隠さず、該当する項目だけを強調する。
  function apply(filter) {
    var total = 0;
    var active = filter !== "all";
    var label = labelFor(filter);
    Array.prototype.forEach.call(buttons, function (button) {
      button.setAttribute("aria-pressed", button.getAttribute("data-filter") === filter ? "true" : "false");
    });
    regions.forEach(function (region) {
      var count = 0;
      Array.prototype.forEach.call(region.items, function (item) {
        var highlighted = active && tagsOf(item).indexOf(filter) !== -1;
        item.classList.toggle("is-highlighted", highlighted);
        markTags(item, label, highlighted);
        if (highlighted) count += 1;
      });
      total += count;
      var empty = document.querySelector('[data-filter-empty="' + region.id + '"]');
      if (empty) empty.hidden = !active || count > 0;
    });
    if (!status) return;
    if (!active) {
      status.textContent = "";
      return;
    }
    status.textContent = lang === "en"
      ? "Highlighting " + total + (total === 1 ? " item" : " items") + " tagged " + label + "."
      : label + "に該当する" + total + "件を強調しています。";
  }

  Array.prototype.forEach.call(buttons, function (button) {
    button.addEventListener("click", function () {
      apply(button.getAttribute("data-filter"));
    });
  });

  apply("all");
  root.hidden = false;
}());
