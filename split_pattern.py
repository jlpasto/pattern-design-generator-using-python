import cv2
import numpy as np

NOM_MOTIF = "agathe"


def hex_to_rgb(hex_code:str) -> tuple[int]:
    """ Convertit une couleur hexa en RGB
    In:
        - hex_code (str) : couleur en hexa
    Out:
        - (tuple[int]) : couleur en RGB (R:int, G:int, B:int)
    """
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_bgr(r, g, b):
    return (b, g, r)


def get_colors(txt_file_path:str) -> list[str]:
    """ Récupère la liste des couleurs depuis le fichier colors.txt
    In:
        - txt_file_path (str) : fichier lsitant les couleurs présentes dans le pattern
    Out:
        - colors (list[str]) : liste des couleurs en hexa
    """
    colors = []
    with open(txt_file_path, "r") as f:
        for color in f.readlines():
            color = color.strip("\n")
            if len(color) == 7:
                colors.append(color)
    return colors


def split_colors(pattern_path:str, output_dir:str) -> None:
    """ Sépare l'image couleur par couleur
    In :
        - pattern_path (str) : chemin vers l'image du pattern
    Out:
        - output_dir (str) : dossier de destination où va se générer les motifs
    """
    image = cv2.imread(pattern_path, cv2.IMREAD_UNCHANGED)
    height, width, channels = image.shape
    size = min(height, width)
    if channels == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    image = image[:size, :size, :]

    colors_txt_path = pattern_path.split(".")[0] + "_colors.txt"
    colors = get_colors(colors_txt_path)

    root_pixels = image.reshape(-1, 4)
    size = int(np.sqrt(root_pixels.shape[0]))

    # Motifs
    for i, color in enumerate(colors):
        pixels = np.copy(root_pixels)
        bgr = rgb_to_bgr(*hex_to_rgb(color))
        mask = np.all(np.abs(pixels[:, :3] - bgr) == 0, axis=1)
        pixels[~mask] = [0, 0, 0, 0]
        root_pixels[mask] = [1, 2, 3, 4]

        out_img = pixels.reshape(size, size, 4)
        
        cv2.imwrite(f"{output_dir}/Motif {i+1}.png", out_img)

    # Background
    root_pixels[~np.all(root_pixels == [1, 2, 3, 4], axis=1)] = [255, 255, 255, 255]
    out_img = root_pixels.reshape(size, size, 4)
    cv2.imwrite(f"{output_dir}/Background.png", out_img)

def split_colors_no_resize(pattern_path: str, output_dir: str, nom_motif:str = "hexagon") -> None:
    """
    Sépare l'image couleur par couleur sans la redimensionner en carré.
    Génère un motif pour chaque couleur détectée et un fond.

    In :
        - pattern_path (str) : chemin vers l'image du pattern (peut être rectangulaire)
        - output_dir (str) : dossier de destination où va se générer les motifs
    """
    print(f"Processing image: {pattern_path}")
    image = cv2.imread(pattern_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        raise FileNotFoundError(f"Image not found or failed to load: {pattern_path}")

    height, width, channels = image.shape

    # --- START MODIFICATION ---
    # Removed: size = min(height, width)
    # Removed: image = image[:size, :size, :]
    # The image will retain its original height and width.
    # --- END MODIFICATION ---

    # Ensure the image has an alpha channel (BGRA) for consistent processing
    if channels == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        print("Converted 3-channel image to 4-channel (BGRA).")

    # Construct the path to the colors text file
    colors_txt_path = pattern_path.split(".")[0] + "_colors.txt"
    try:
        colors = get_colors(colors_txt_path)
        if not colors:
            print(f"No colors found in {colors_txt_path}. Please ensure the file exists and contains hex color codes.")
            return # Exit if no colors to process
    except NameError:
        print("Error: `get_colors` function not defined. Please ensure helper functions are available.")
        return
    except Exception as e:
        print(f"An error occurred while getting colors: {e}")
        return

    # Flatten the image into a 2D array where each row is a pixel (BGRA)
    # The -1 lets numpy infer the number of rows based on the total elements and 4 columns.
    root_pixels = image.reshape(-1, 4)

    # --- START MODIFICATION ---
    # We will use the original height and width for reshaping back,
    # so no need to recalculate 'size' from root_pixels.shape[0]
    # --- END MODIFICATION ---

    # Create a copy of the original pixels to be modified for each motif
    # This ensures that the original 'root_pixels' (which will become the background)
    # retains its state for marking processed pixels.

    # Motifs: Iterate through each specified color to create a separate pattern image
    for i, color_hex in enumerate(colors):
        # Create a fresh copy of the flattened image for each motif
        pixels_for_motif = np.copy(root_pixels)

        try:
            # Convert the hexadecimal color to BGR format
            bgr_color = rgb_to_bgr(*hex_to_rgb(color_hex))
        except NameError:
            print("Error: `hex_to_rgb` or `rgb_to_bgr` functions not defined. Skipping color.")
            continue
        except Exception as e:
            print(f"Error converting color '{color_hex}': {e}. Skipping.")
            continue

        # Create a boolean mask: True for pixels matching the current color, False otherwise.
        # np.abs(pixels_for_motif[:, :3] - bgr_color) calculates the absolute difference
        # between each pixel's BGR values and the target color.
        # == 0 checks if the difference is zero (i.e., exact match).
        # np.all(..., axis=1) ensures that ALL B, G, and R components match for a pixel.
        mask = np.all(np.abs(pixels_for_motif[:, :3] - bgr_color) == 0, axis=1)

        # Set pixels that DO NOT match the current color to transparent black (0,0,0,0)
        pixels_for_motif[~mask] = [0, 0, 0, 0]

        # Mark the pixels that DO match the current color in the original `root_pixels` array.
        # This is done to keep track of which pixels have been "extracted" into a motif.
        # The values [1, 2, 3, 4] are arbitrary markers, indicating "this pixel was part of a motif".
        root_pixels[mask] = [1, 2, 3, 4]

        # Reshape the motif's pixels back into the original image dimensions (height, width, 4 channels)
        out_img = pixels_for_motif.reshape(height, width, 4)

        # Save the individual motif image
        output_filename = f"{output_dir}/Motif {i+1}.png"
        cv2.imwrite(output_filename, out_img)
        print(f"Saved motif {i+1} to {output_filename}")

    # # Background: Process the remaining pixels to form the background image
    # # Select pixels in `root_pixels` that were NOT marked as part of any motif.
    # # These are the pixels whose values are NOT [1, 2, 3, 4].
    # background_mask = ~np.all(root_pixels == [1, 2, 3, 4], axis=1)

    # # Set these background pixels to solid white (255,255,255,255)
    # root_pixels[background_mask] = [255, 255, 255, 255]

    # # Set any remaining marked pixels (which should not exist if all colors were processed)
    # # to transparent black, just in case. This makes the background truly just the background.
    # root_pixels[~background_mask] = [0, 0, 0, 0] # This ensures only background pixels are white

    # # Reshape the `root_pixels` (now representing the background) back to image dimensions
    # out_img = root_pixels.reshape(height, width, 4)

    # Save the background image
    sample_assembly_img_path = f"output/{nom_motif}/Sample Assembly/sample_assembly_image.png"
    out_img = transform_colors_and_alpha(sample_assembly_img_path)
    background_filename = f"{output_dir}/Background.png"
    cv2.imwrite(background_filename, out_img)
    print(f"Saved background to {background_filename}")

def transform_colors_and_alpha(image_path: str) -> np.ndarray:
    """
    Reads an image, transforms its transparent areas to solid white,
    and its colored (non-transparent) areas to fully transparent.

    Args:
        image_path (str): The path to the input image file.

    Returns:
        np.ndarray: The transformed image in BGRA format.
                    Returns an empty array if the image cannot be loaded.
    """
    # 1. Read the image with unchanged flag to preserve alpha channel if it exists
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if image is None:
        print(f"Error: Image not found or failed to load from {image_path}")
        return np.array([])  # Return an empty array to indicate failure

    # 2. Ensure the image has an alpha channel (BGRA format)
    # If it's a 3-channel image (BGR), convert it to 4-channel (BGRA)
    if image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        print("Converted 3-channel image to 4-channel (BGRA).")
    elif image.shape[2] != 4:
        print(f"Warning: Image has {image.shape[2]} channels, not 3 or 4. "
              "Proceeding but results might be unexpected.")

    # Create a copy of the image to modify
    transformed_image = np.copy(image)

    # Get the alpha channel from the original image
    alpha_channel = image[:, :, 3]

    # 3. Create masks to identify transparent and non-transparent pixels
    transparent_mask = (alpha_channel == 0)
    non_transparent_mask = (alpha_channel > 0)

    # 4. Apply transformation for transparent areas:
    # Set the pixels where the original alpha was 0 to solid white (255, 255, 255)
    # and make them fully opaque (alpha = 255).
    transformed_image[transparent_mask] = [255, 255, 255, 255]

    # 5. Apply transformation for non-transparent areas:
    # Set the pixels where the original alpha was > 0 to fully transparent (alpha = 0).
    # The BGR values are not important as the pixel will be invisible, but setting
    # them to black [0, 0, 0] is good practice.
    transformed_image[non_transparent_mask] = [0, 0, 0, 0]

    return transformed_image

def main():
    img_path = f"patterns/{NOM_MOTIF}.png"
    image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    split_colors(image)


if __name__ == '__main__':
    main()
