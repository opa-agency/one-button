// Production stub that prevents django-browser-reload from registering
// its service worker and cleans up any previously registered instance.
(function () {
  if (navigator.serviceWorker) {
    navigator.serviceWorker.getRegistrations().then(function (regs) {
      regs
        .filter(function (reg) {
          return (
            reg &&
            reg.active &&
            reg.active.scriptURL &&
            reg.active.scriptURL.indexOf("django-browser-reload/") !== -1
          );
        })
        .forEach(function (reg) {
          reg.unregister();
        });
    });
  }
})();
