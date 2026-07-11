// tracker/tracker.js
(function () {
  const script = document.currentScript;
  const API_KEY = script.dataset.key;
  const ENDPOINT = "http://127.0.0.1:8000/events";

  function send(eventType, extra) {
    fetch(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        api_key: API_KEY,
        event_type: eventType,
        page: window.location.pathname,
        properties: extra || {},
      }),
      keepalive: true,
    }).catch(() => {});
  }

  // auto-capture: page view on load
  send("page_view");

  // auto-capture: clicks
  document.addEventListener("click", (e) => {
    const t = e.target.closest("button, a");
    if (t)
      send("click", {
        element: t.tagName,
        text: (t.innerText || "").slice(0, 40),
      });
  });

  // custom events for site owners
  window.analytics = { track: send };
})();
