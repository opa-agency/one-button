// noop worker for production to avoid polling reload events
self.addEventListener('install', event => event.waitUntil(self.skipWaiting()));
self.addEventListener('activate', event => event.waitUntil(self.registration.unregister()));
self.addEventListener('fetch', () => {});
