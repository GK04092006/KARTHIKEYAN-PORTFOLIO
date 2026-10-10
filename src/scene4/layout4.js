// Scene four's measured geometry — every number read off the supplied
// reference (section 4 image.jpg, 1600x900), which is the source of truth.
// The card sprites and the environment plate are cut from that image by
// tools/extract_s4.py; this module records where each piece goes back.
//
// Coordinates are reference-frame pixels. fitCover() maps the frame onto the
// viewport the way the plate shader does (cover: fill, centre-anchored), so
// the DOM cards and the canvas can never drift apart.

export const FRAME = [1600, 900];

export const CARDS = [
  { id: 'p01_careloop', title: 'CareLoop', box: [72, 105, 390, 250], depth: 0.45, tint: [0.40, 0.12, 0.12] },
  { id: 'p02_weather', title: 'Weather App', box: [560, 70, 420, 260], depth: 0.60, tint: [0.16, 0.30, 0.45] },
  { id: 'p03_fitness', title: 'Fitness', box: [1110, 105, 390, 250], depth: 0.45, tint: [0.20, 0.36, 0.24] },
  { id: 'p04_course', title: 'Course Outcome Analyzer', box: [90, 475, 390, 240], depth: 0.25, tint: [0.34, 0.20, 0.40] },
  { id: 'p05_zoo', title: 'Zoo Management', box: [590, 485, 360, 230], depth: 0.90, tint: [0.34, 0.27, 0.12] },
  { id: 'p06_crop', title: 'Smart Crop Advisory', box: [1080, 470, 410, 250], depth: 0.25, tint: [0.15, 0.36, 0.20] },
];

// the central figure: crop box in frame px (his lighting is baked in)
export const PERSON = { x: 690, y: 300, w: 220, h: 390 };

// the floor's lit ellipses (centre x, centre y, rx, ry) and the overhead ring,
// used by the live glints the canvas draws over the baked plate
export const FLOOR_OUT = [798, 735, 372, 80];
export const FLOOR_IN = [798, 741, 240, 57];
export const RING = [802, 34, 392, 148];

/** Cover-fit the reference frame onto a viewport. */
export function fitCover(w, h) {
  const s = Math.max(w / FRAME[0], h / FRAME[1]);
  return { s, ox: (w - FRAME[0] * s) / 2, oy: (h - FRAME[1] * s) / 2 };
}

// --------------------------------------------------------------------------
// Portrait is a recomposition, not a crop: cover-fitting a 16:9 amphitheatre
// to a phone leaves only the centre quarter on screen. The plate still cover-
// fits (floor, circle and haze survive centred), and a curated set of cards
// restacks into a column that keeps the reference hierarchy: hero screen up
// top, the small row over the figure, the two green closers at his feet.
// Entries: card index -> centre x/y (viewport fractions), width (vw fraction).
// --------------------------------------------------------------------------
export const PORTRAIT = new Map([
  [1, { cx: 0.50, cy: 0.19, w: 0.74 }],
  [0, { cx: 0.25, cy: 0.36, w: 0.45 }],
  [2, { cx: 0.75, cy: 0.36, w: 0.45 }],
  [3, { cx: 0.22, cy: 0.70, w: 0.43 }],
  [4, { cx: 0.50, cy: 0.70, w: 0.40 }],
  [5, { cx: 0.78, cy: 0.70, w: 0.43 }],
]);;
