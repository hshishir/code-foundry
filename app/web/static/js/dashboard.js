(function () {
  window.addEventListener("DOMContentLoaded", function () {
    const search = document.querySelector("[data-dashboard-search]");
    const rows = Array.from(document.querySelectorAll("[data-feature-row]"));
    if (!search || rows.length === 0) return;

    search.addEventListener("input", function () {
      const query = search.value.trim().toLowerCase();
      rows.forEach(function (row) {
        row.hidden = query.length > 0 && !row.textContent.toLowerCase().includes(query);
      });
    });
  });
})();

