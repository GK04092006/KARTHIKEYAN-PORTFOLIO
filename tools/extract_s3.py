"""Lift the section-3 artwork out of the supplied reference.

Two things come out of the poster:

  * the six card photographs, one per year. They are small in the source
    (~90-140px wide) and are graded warm; they are lifted at native detail and
    given a light clean-up rather than an upscale that invents nothing.

  * the central figure's silhouette, found with grabCut for the same reason as
    in scene two: he is nearly black against a nearly black floor, so no
    luminance threshold can separate them. Only his SHAPE is kept - the scene
    lights him at runtime.

Nothing here is redrawn or replaced.
"""

import json
import os

import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "section 3 image.jpg")
OUT = os.path.join(ROOT, "public", "years")

# photo box per year, measured off the VIGNESH reference (1672x941)
PHOTOS = {
    2021: (283, 227, 396, 313),
    2022: (460, 298, 577, 386),
    2023: (638, 342, 755, 430),
    2024: (838, 396, 960, 488),
    2025: (1098, 439, 1217, 529),
    2026: (1277, 448, 1462, 587),
}

FIGURE_REGION = (740, 480, 930, 920)
FIGURE_SEED = (0.12, 0.02, 0.88, 0.98)

# every photo is emitted at this width in 4:3 ratio
OUT_W = 264


def photo(year, box):
    img = cv2.imread(SRC)
    x0, y0, x1, y1 = box
    c = img[y0:y1, x0:x1].astype(np.float32)

    # The poster grades these warm and dark. Held at source levels they read as
    # muddy brown smears once they are card-sized, so the range is opened up
    # while the warm cast that ties them to the scene is kept.
    lo, hi = np.percentile(c, [2, 99])
    c = np.clip((c - lo) / max(hi - lo, 1e-6), 0, 1)
    c = np.power(c, 0.86) * 255.0

    h = int(round(OUT_W * (y1 - y0) / (x1 - x0)))
    c = cv2.resize(c, (OUT_W, h), interpolation=cv2.INTER_LANCZOS4)
    c = cv2.bilateralFilter(np.clip(c, 0, 255).astype(np.uint8), 5, 30, 6)
    # a touch of local contrast back, since the resize softens it
    blur = cv2.GaussianBlur(c, (0, 0), 1.6)
    c = np.clip(c.astype(np.float32) * 1.35 - blur.astype(np.float32) * 0.35, 0, 255)

    path = os.path.join(OUT, "%d.jpg" % year)
    cv2.imwrite(path, c.astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 88])
    return OUT_W, h


def figure():
    img = cv2.imread(SRC)
    x0, y0, x1, y1 = FIGURE_REGION
    crop = img[y0:y1, x0:x1]
    h, w = crop.shape[:2]

    mask = np.zeros((h, w), np.uint8)
    rect = (int(0.15 * w), int(0.04 * h), int(0.70 * w), int(0.92 * h))
    bgd = np.zeros((1, 65), np.float64)
    fgd = np.zeros((1, 65), np.float64)

    cv2.grabCut(crop, mask, rect, bgd, fgd, 6, cv2.GC_INIT_WITH_RECT)
    cv2.line(mask, (int(0.50 * w), int(0.08 * h)), (int(0.50 * w), int(0.85 * h)), cv2.GC_FGD, 9)
    cv2.circle(mask, (int(0.50 * w), int(0.15 * h)), 12, cv2.GC_FGD, -1)
    cv2.rectangle(mask, (0, 0), (int(0.10 * w), h), cv2.GC_BGD, -1)
    cv2.rectangle(mask, (int(0.90 * w), 0), (w, h), cv2.GC_BGD, -1)
    cv2.rectangle(mask, (0, 0), (w, int(0.04 * h)), cv2.GC_BGD, -1)

    cv2.grabCut(crop, mask, rect, bgd, fgd, 6, cv2.GC_INIT_WITH_MASK)

    m = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 1, 0).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(m, 8)
    best, score = 0, -1e18
    for i in range(1, n):
        area = st[i, cv2.CC_STAT_AREA]
        if area < 0.05 * w * h:
            continue
        s = area * (1.0 - abs(cen[i][0] / w - 0.5))
        if s > score:
            best, score = i, s
    if best:
        m = (lab == best).astype(np.uint8)

    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    a = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.2)
    a = np.clip((a - 0.35) / 0.42, 0, 1)

    fade = np.clip(np.linspace(0, 1, a.shape[0]) * 12.0 - 10.4, 0, 1)[:, None]
    a *= (1.0 - fade)

    ys, xs = np.nonzero(a > 0.15)
    pad = 5
    cy0, cy1 = max(0, ys.min() - pad), min(h, ys.max() + pad)
    cx0, cx1 = max(0, xs.min() - pad), min(w, xs.max() + pad)
    a = a[cy0:cy1, cx0:cx1]
    body = crop[cy0:cy1, cx0:cx1]

    rgba = np.dstack([np.clip(body.astype(np.float32) * 1.3, 0, 255), a * 255]).astype(np.uint8)
    cv2.imwrite(os.path.join(OUT, "figure.png"), rgba)
    return rgba.shape[1], rgba.shape[0], float((a > 0.5).mean())


def main():
    os.makedirs(OUT, exist_ok=True)
    meta = {}
    for year, box in PHOTOS.items():
        w, h = photo(year, box)
        meta[str(year)] = {"w": w, "h": h}
        print("  photo %d  %dx%d" % (year, w, h))
    fw, fh, cov = figure()
    meta["figure"] = {"w": fw, "h": fh}
    print("  figure   %dx%d  coverage %.1f%%" % (fw, fh, cov * 100))
    with open(os.path.join(OUT, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=1)
    print("wrote ->", OUT)


if __name__ == "__main__":
    main()
