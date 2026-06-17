/*
 * Production stub for django-browser-reload's service worker.
 * Ensures any previously registered worker unregisters itself
 * so it stops polling the /__reload__/events/ endpoint.
 */
self.addEventListener("install", (event) => {
  event.waitUntil(self.skipWaiting());
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.registration.unregister());
});

self.addEventListener("fetch", () => {
  // no-op
});
