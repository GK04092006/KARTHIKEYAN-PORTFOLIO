// Composition geometry.
//
// Every constant here was measured off the supplied hero artwork rather than
// eyeballed, so the live page keeps the reference's proportions exactly:
//   VIGNESH ink box   x 3.31% .. 96.75%,  cap top 27.00%, baseline 80.22%
//   WELCOME strip     centred, y 20.44%
//   LEGEND chip       x 88.12%, y 26.78%, 10.38% x 4.22%
//   ARTIST chip       x  1.50%, y 68.78%, 15.00% x 3.67%
// The word is then fitted to whatever viewport it lands in without ever
// changing its own width : cap-height ratio.

import { TARGET_RATIO } from './type.js';

export const REF = {
  wordWidth: 0.90,       // fraction of viewport width
  capHeight: 0.36,       // fraction of viewport height (leaves clean room for Hero HUD below)
  vCentre: 0.41,         // vertical centre of the cap box
  legend: { x: 0.95, y: 0.21, h: 0.036 },
  artist: { x: 0.05, y: 0.21, h: 0.036 },
  dotsBR: { x: 0.9844, y: 0.9500 },
  arrows: { left: 0.0181, right: 0.9750, top: 0.30, bottom: 0.56, count: 5 },
};

export function computeLayout(w, h) {
  const portrait = h / w > 1.05;
  const narrow = w < 760;

  // fit the word by whichever axis binds first, preserving its proportions
  const byWidth = (REF.wordWidth * w) / TARGET_RATIO;
  const byHeight = REF.capHeight * h;
  let capH = Math.min(byWidth, byHeight);

  if (portrait) capH = Math.min(byWidth * 1.0, h * 0.22);

  const wordW = capH * TARGET_RATIO;
  const cx = w * 0.5;
  const vCentre = portrait ? h * 0.36 : h * REF.vCentre;
  const capTop = vCentre - capH * 0.5;
  const baseline = vCentre + capH * 0.5;

  const word = {
    x: cx - wordW * 0.5,
    y: capTop,
    w: wordW,
    h: capH,
    capH,
    baseline,
  };

  let heroH = capH * 1.45;
  let feet = baseline + capH * 0.22;

  if (portrait) {
    heroH = h * 0.44;
    feet = h * 0.84;
  }

  const chipY = Math.max(82, capTop - (portrait ? 28 : 34));

  return {
    w,
    h,
    dpr: Math.min(window.devicePixelRatio || 1, 2),
    portrait,
    narrow,
    word,
    hero: { h: heroH, cx, feet },
    welcomeY: Math.max(76, capTop - (portrait ? 54 : 46)),
    legend: {
      x: word.x + word.w,
      y: chipY,
      h: Math.max(18, h * REF.legend.h),
      alignRight: true,
    },
    artist: {
      x: word.x,
      y: chipY,
      h: Math.max(18, h * REF.artist.h),
    },
    ember: { x: 0.5, y: vCentre / h },
  };
}

/**
 * Place a clip so the SUBJECT (not the video rectangle) lands where we want.
 * The tracks baked into the manifest give the subject's box per frame, so a
 * figure can be anchored by his feet and held at a chosen height even though he
 * walks toward the camera and grows through the shot.
 */
export function fitSubject(track, frameAspect, opts) {
  const [x0, y0, x1, y1] = track;
  const subH = Math.max(y1 - y0, 1e-3);
  const subCX = (x0 + x1) * 0.5;

  const quadH = opts.height / subH;          // video height needed
  const quadW = quadH * frameAspect;

  const footY = opts.feet !== undefined ? opts.feet : opts.top + opts.height;
  return {
    x: opts.cx - quadW * subCX,
    y: footY - quadH * y1,
    w: quadW,
    h: quadH,
  };
}
