(function () {
  function show(message) {
    const region = document.querySelector("[data-toast-region]");
    if (!region || !message) return;
    const toast = document.createElement("div");
    toast.className = "af-toast";
    toast.textContent = message;
    region.appendChild(toast);
    window.setTimeout(function () {
      toast.remove();
    }, 3200);
  }

  window.afToast = { show };

  window.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const toast = params.get("toast");
    const messages = {
      "feature-created": "Feature created",
      "status-updated": "Status updated",
    };
    if (toast && messages[toast]) {
      show(messages[toast]);
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  });
})();

