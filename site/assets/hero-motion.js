(() => {
  const artwork = document.querySelector('.hero-paths');
  const button = document.querySelector('.hero-replay');
  if (!artwork || !button) return;

  const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
  let playing = false;

  function stop() {
    artwork.classList.remove('is-playing');
    playing = false;
    button.textContent = button.dataset.playLabel;
  }

  function play() {
    stop();
    // Commit the completed state so another click restarts the CSS sequence.
    artwork.getBoundingClientRect();
    artwork.classList.add('is-playing');
    playing = true;
    button.textContent = button.dataset.stopLabel;
  }

  button.addEventListener('click', () => playing ? stop() : play());
  artwork.addEventListener('animationend', event => {
    if (event.target.matches('.hero-arrival')) stop();
  });
  preference.addEventListener('change', stop);
  window.addEventListener('pagehide', stop);
  button.hidden = false;
  if (!preference.matches) play();
})();
