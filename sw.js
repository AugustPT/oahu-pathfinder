/* Oʻahu Pathfinder service worker — app shell cache, offline-first. */
const CACHE = 'oahu-pathfinder-v1.2.0';
const ASSETS = [
  './',
  './index.html',
  './qrcode.js',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './apple-touch-icon.png',
  './images/bg.jpg',
  './images/diamondhead.jpg',
  './images/lanikai.jpg',
  './images/hanauma.jpg',
  './images/food.jpg',
  './images/shaveice.jpg',
  './images/hike.jpg',
  './images/skyline.jpg',
  './images/pearlharbor.jpg',
  './images/hibiscus.jpg',
  './images/sunset.jpg',
  './images/kailua.jpg',
  './images/northshore.jpg',
  './images/thebus.jpg'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then((cached) => {
      if (cached) return cached;
      return fetch(e.request)
        .then((resp) => {
          // cache same-origin responses for offline use
          if (resp.ok && new URL(e.request.url).origin === self.location.origin) {
            const copy = resp.clone();
            caches.open(CACHE).then((c) => c.put(e.request, copy));
          }
          return resp;
        })
        .catch(() => caches.match('./index.html'));
    })
  );
});
