import cv2
import numpy as np
import math


def generate_pattern_6(nom_motif, base_img_path):
    print("Generating sample pattern 6")
    # Load the hexagon tile with alpha channel (RGBA)
    tile = cv2.imread(f"{base_img_path}", cv2.IMREAD_UNCHANGED)
    if tile is None:
        raise FileNotFoundError(f"{nom_motif}.png not found or failed to load.")

    tile_h, tile_w = tile.shape[:2]

    # Honeycomb layout spacing
    dx = int(tile_w * 0.75)       # horizontal step 0.75
    dy = int(tile_h * 0.990)      # vertical step (sin 60°) original = 0.866

    # Define the number of rows and columns
    rows = 3
    cols = 3

    # Compute canvas size large enough to hold all tiles
    canvas_width = dx * cols + tile_w
    canvas_height = dy * rows + tile_h

    # Create a blank canvas with 4 channels (RGBA)
    canvas = np.zeros((canvas_height, canvas_width, 4), dtype=np.uint8)

    # Paste tiles in honeycomb pattern
    for row in range(rows):
        for col in range(cols):
            # Compute top-left corner for each tile
            x = col * dx
            y = row * dy
            if col % 2 == 1:
                y += dy // 2  # offset every other column

            # Coordinates to paste tile
            x1, y1 = x, y
            x2, y2 = x + tile_w, y + tile_h

            # Clip if tile goes outside canvas
            if x2 > canvas.shape[1]:
                tile_w_clip = canvas.shape[1] - x1
            else:
                tile_w_clip = tile_w

            if y2 > canvas.shape[0]:
                tile_h_clip = canvas.shape[0] - y1
            else:
                tile_h_clip = tile_h

            if tile_w_clip <= 0 or tile_h_clip <= 0:
                continue  # skip if outside bounds

            # Extract region of interest
            roi = canvas[y1:y1 + tile_h_clip, x1:x1 + tile_w_clip]

            # Prepare alpha masks
            tile_crop = tile[:tile_h_clip, :tile_w_clip]
            alpha_tile = tile_crop[:, :, 3] / 255.0
            alpha_bg = 1.0 - alpha_tile

            for c in range(3):
                roi[:, :, c] = (alpha_tile * tile_crop[:, :, c] + alpha_bg * roi[:, :, c])

            # Update alpha channel
            canvas[y1:y1 + tile_h_clip, x1:x1 + tile_w_clip, 3] = np.maximum(
                tile_crop[:, :, 3], roi[:, :, 3])
    return canvas
    # # Save result
    # cv2.imwrite("honeycomb_output.png", canvas)
    # print("Honeycomb pattern saved as 'honeycomb_output.png'")
