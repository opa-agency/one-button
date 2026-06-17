(function(){
  if (!navigator.serviceWorker) {
    return;
  }
  navigator.serviceWorker.getRegistrations().then(function(regs) {
    regs.filter(function(reg) {
      return reg && reg.active && reg.active.scriptURL && reg.active.scriptURL.includes('django-browser-reload/');
    }).forEach(function(reg) {
      reg.unregister();
    });
  });
})();
