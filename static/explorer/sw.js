/* Service worker — Centre de Ressources Danfoss (design Explorer)
   Stratégie fiable :
   - Navigation (HTML) : RÉSEAU d'abord -> toujours la dernière version en ligne,
     repli sur le cache uniquement hors-ligne (pas de "version figée").
   - Autres ressources même domaine : stale-while-revalidate.
   Les PDF Danfoss (autre domaine) ne sont jamais mis en cache. */
const CACHE = 'kk-explorer-v2';

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.add('./')).catch(() => {}));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // laisser passer danfoss.com etc.

  // Navigation / page HTML : réseau d'abord.
  if (req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html')) {
    e.respondWith(
      fetch(req)
        .then(res => { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return res; })
        .catch(() => caches.match(req).then(r => r || caches.match('./')))
    );
    return;
  }

  // Ressources statiques : cache d'abord, mise à jour en arrière-plan.
  e.respondWith(
    caches.open(CACHE).then(cache =>
      cache.match(req).then(cached => {
        const network = fetch(req).then(res => {
          if (res && res.status === 200 && res.type === 'basic') cache.put(req, res.clone());
          return res;
        }).catch(() => cached);
        return cached || network;
      })
    )
  );
});
