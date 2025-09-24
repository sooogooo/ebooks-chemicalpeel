const CACHE_NAME = 'chemical-peel-v1';
const urlsToCache = [
  '/',
  '/stylesheets/extra.css',
  '/javascripts/reading-progress.js',
  '/javascripts/mathjax.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});
