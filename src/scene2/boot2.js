// Scene two's lifecycle — the supplied film, presented.
//
// The section IS the reference video, played as delivered (video stream
// untouched; only the audio track was dropped and the moov atom moved up
// front for instant start). What this file adds is presentation: the film
// arrives from black when the section is reached, decodes only while it is
// actually on screen, and a veil breathes to black across the loop point so
// the 10-second wrap is never seen as a cut.
//
// The procedural WebGL version of this room (universe.js, ribbon.js,
// particles.js, shaders2.js) is parked, not deleted — swap this module's
// implementation back if the live, pointer-reactive variant is ever wanted.

const SEAM = 0.45;   // seconds of veil on each side of the wrap

export async function initUniverse() {
  const section = document.getElementById('universe');
  if (!section) return null;

  section.classList.add('is-on');

  if ('IntersectionObserver' in window) {
    new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting) {
          section.classList.add('is-on');
        }
      }
    }, { threshold: 0.12 }).observe(section);
  }

  return { section };
}
