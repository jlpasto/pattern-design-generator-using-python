import cv2
import numpy as np
import math

import numpy as np

def crop_to_content(image: np.ndarray) -> np.ndarray:
    """
    Crops a 4-channel (BGRA) image to the smallest possible bounding box
    that contains all non-transparent pixels.

    Args:
        image (np.ndarray): The input image with an alpha channel.

    Returns:
        np.ndarray: The cropped image. Returns the original image if
                    it's fully transparent.
    """
    # Get the alpha channel (the 4th channel, index 3)
    alpha_channel = image[:, :, 3]

    # Find the coordinates of all pixels where the alpha value is greater than 0
    y_coords, x_coords = np.where(alpha_channel > 0)

    # If there are no non-transparent pixels, the image is empty.
    # Return the original image or an empty array.
    if y_coords.size == 0:
        print("Warning: Image is fully transparent. No cropping performed.")
        return image

    # Find the minimum and maximum coordinates to define the bounding box
    y_min, y_max = np.min(y_coords), np.max(y_coords)
    x_min, x_max = np.min(x_coords), np.max(x_coords)

    # Slice the original image using the bounding box coordinates
    # We add 1 to the max coordinates because Python slicing is exclusive of the end index
    cropped_image = image[y_min:y_max + 1, x_min:x_max + 1]

    return cropped_image

def generate_hexapattern(nom_motif, base_img_path, image = None, num_rows = 3, num_cols = 3, num_motif = ""):
    #print("Generating sample pattern 6")

    if num_motif == "Background":
        return image
    
    # Load the hexagon tile with alpha channel (RGBA)
    if image is None:
        tile = cv2.imread(f"{base_img_path}", cv2.IMREAD_UNCHANGED)
    else:
        tile = image

    if tile is None:
        raise FileNotFoundError(f"{nom_motif}.png not found or failed to load.")
    
    # Check if the image has an alpha channel; if not, add one for consistency
    if tile.shape[2] == 3:
        tile = cv2.cvtColor(tile, cv2.COLOR_BGR2BGRA)

    tile_h, tile_w = tile.shape[:2]

    # Honeycomb layout spacing
    dx = int(tile_w * 0.75)       # horizontal step 0.75
    dy = int(tile_h * 0.990)       # vertical step (sin 60°) original = 0.866

    # Define the number of rows and columns
    rows = num_rows
    cols = num_cols

    # Compute canvas size large enough to hold all tiles
    canvas_width = dx * cols + tile_w - (tile_w - (tile_w /4))
    canvas_height = dy * rows + tile_h - (tile_h /2)

    # Ensure canvas dimensions are integers before creating the array
    canvas_width = int(canvas_width)
    canvas_height = int(canvas_height)

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

            # --- OPTIMIZED ALPHA BLENDING ---
            # Reshape the alpha masks for broadcasting across the BGR channels
            alpha_tile_3d = alpha_tile[:, :, np.newaxis]
            alpha_bg_3d = alpha_bg[:, :, np.newaxis]

            # Perform the blending for all 3 BGR channels at once
            roi[:, :, :3] = (alpha_tile_3d * tile_crop[:, :, :3] + alpha_bg_3d * roi[:, :, :3])
            
            # Update alpha channel
            canvas[y1:y1 + tile_h_clip, x1:x1 + tile_w_clip, 3] = np.maximum(
                tile_crop[:, :, 3], roi[:, :, 3])
            # --- END OF OPTIMIZED BLOCK ---

    return canvas

# def generate_hexapattern(nom_motif, base_img_path, image = None, num_rows = 3, num_cols = 3, num_motif = ""):
#     #print("Generating sample pattern 6")

#     if num_motif == "Background":
#         return image
    
#     # Load the hexagon tile with alpha channel (RGBA)
#     if image is None:
#         tile = cv2.imread(f"{base_img_path}", cv2.IMREAD_UNCHANGED)
#     else:
#         tile = image

#     if tile is None:
#         raise FileNotFoundError(f"{nom_motif}.png not found or failed to load.")

#     tile_h, tile_w = tile.shape[:2]

#     # Honeycomb layout spacing
#     dx = int(tile_w * 0.75)       # horizontal step 0.75
#     dy = int(tile_h * 0.990)      # vertical step (sin 60°) original = 0.866

#     # Define the number of rows and columns
#     rows = num_rows
#     cols = num_cols

#     # Compute canvas size large enough to hold all tiles
#     canvas_width = dx * cols + tile_w - (tile_w - (tile_w /4))
#     canvas_height = dy * rows + tile_h - (tile_h /2)

#     # Ensure canvas dimensions are integers before creating the array
#     canvas_width = int(canvas_width)
#     canvas_height = int(canvas_height)

#     # Create a blank canvas with 4 channels (RGBA)
#     canvas = np.zeros((canvas_height, canvas_width, 4), dtype=np.uint8)

#     # Paste tiles in honeycomb pattern
#     for row in range(rows):
#         for col in range(cols):
#             # Compute top-left corner for each tile
#             x = col * dx
#             y = row * dy
#             if col % 2 == 1:
#                 y += dy // 2  # offset every other column

#             # Coordinates to paste tile
#             x1, y1 = x, y
#             x2, y2 = x + tile_w, y + tile_h

#             # Clip if tile goes outside canvas
#             if x2 > canvas.shape[1]:
#                 tile_w_clip = canvas.shape[1] - x1
#             else:
#                 tile_w_clip = tile_w

#             if y2 > canvas.shape[0]:
#                 tile_h_clip = canvas.shape[0] - y1
#             else:
#                 tile_h_clip = tile_h

#             if tile_w_clip <= 0 or tile_h_clip <= 0:
#                 continue  # skip if outside bounds

#             # Extract region of interest
#             roi = canvas[y1:y1 + tile_h_clip, x1:x1 + tile_w_clip]

#             # Prepare alpha masks
#             tile_crop = tile[:tile_h_clip, :tile_w_clip]
#             alpha_tile = tile_crop[:, :, 3] / 255.0
#             alpha_bg = 1.0 - alpha_tile

#             for c in range(3):
#                 roi[:, :, c] = (alpha_tile * tile_crop[:, :, c] + alpha_bg * roi[:, :, c])

#             # Update alpha channel
#             canvas[y1:y1 + tile_h_clip, x1:x1 + tile_w_clip, 3] = np.maximum(
#                 tile_crop[:, :, 3], roi[:, :, 3])
#     return canvas
#     # # Save result
#     # cv2.imwrite("honeycomb_output.png", canvas)
#     # print("Honeycomb pattern saved as 'honeycomb_output.png'")
