"""Q14: Reassemble 5x5 jigsaw.webp using mapping, convert to grayscale (0.2126 R, 0.7152 G, 0.0722 B), save PNG."""
from PIL import Image
import os

# Table: Scrambled Row, Scrambled Col = position in scrambled image; Original Row, Original Col = position in output.
# So: tile at (scr_r, scr_c) in scrambled -> place at (orig_r, orig_c) in reconstructed.
MAPPING = [
    (0,0,2,1), (0,1,1,1), (0,2,4,1), (0,3,0,3), (0,4,0,1),
    (1,0,1,4), (1,1,2,0), (1,2,2,4), (1,3,4,2), (1,4,2,2),
    (2,0,0,0), (2,1,3,2), (2,2,4,3), (2,3,3,0), (2,4,3,4),
    (3,0,1,0), (3,1,2,3), (3,2,3,3), (3,3,4,4), (3,4,0,2),
    (4,0,3,1), (4,1,1,2), (4,2,1,3), (4,3,0,4), (4,4,4,0),
]

img_path = r"C:\Users\HP\Documents\jigsaw.webp" #change path
out_path = r"C:\Users\HP\Downloads\jigsaw_gray_2.png"

img = Image.open(img_path).convert("RGB")
w, h = img.size
tile_w, tile_h = w // 5, h // 5

# Reconstruct: tile at (scr_r, scr_c) in scrambled image -> place at (orig_r, orig_c) in output
reconstructed = Image.new("RGB", (w, h))
for (scr_r, scr_c, orig_r, orig_c) in MAPPING:
    sx0, sy0 = scr_c * tile_w, scr_r * tile_h
    box = (sx0, sy0, sx0 + tile_w, sy0 + tile_h)
    tile = img.crop(box)
    dx0, dy0 = orig_c * tile_w, orig_r * tile_h
    reconstructed.paste(tile, (dx0, dy0))

# Grayscale: 0.2126 R + 0.7152 G + 0.0722 B, integer per pixel (no rounding to avoid float differences)
gray_img = Image.new("L", (w, h))
gray_pix = gray_img.load()
pix = reconstructed.load()
for y in range(h):
    for x in range(w):
        r, g, b = pix[x, y][:3]
        g_val = 0.2126 * r + 0.7152 * g + 0.0722 * b
        gray = int(g_val + 0.5)  # round
        gray = max(0, min(255, gray))
        gray_pix[x, y] = gray

# Lossless PNG
gray_img.save(out_path, format="PNG", compress_level=0)
print("Saved:", os.path.abspath(out_path))
print("Upload this file in the exam for Q19.")
