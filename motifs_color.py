import os 
import cv2
import numpy as np

NOM_MOTIF = "monceau"


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


def get_color_tab(csv_path:str) -> dict:
    """ Récupère le tableau de correspondance nom_couleur:hexa
    In: 
        - csv_path (str) : chemin vers le csv
    Out:
        - (dict) : dictionnaire associant un code hexa au nom de la couleur
    """
    colors = {}
    with open(csv_path, 'r', encoding="utf-8") as f:
        f.readline()
        for row in f.readlines():
            color, hexa = row.split(";")
            colors[hexa.strip("\n")] = color
    return colors


def group_by_4(image:object, assembly_type:int, joint_size:int=None) -> object:
    """ Regroupe l'image par 4 avant de l'enregistrer
    In:
        - image (cv2.Image) : image a regrouper
        - joint_size (int) : épaisseur du joint
    Out:
        - grouped (cv2.Image) : l'image en quadruple
    """
    size = image.shape[0]
    # Get the number of channels from the input image
    num_channels = image.shape[2] if len(image.shape) > 2 else 1

    if joint_size is None:
        joint_size = int(size/100)
    marge = int(joint_size/4)

    output_image = np.zeros((size*2 + joint_size, size*2 + joint_size, num_channels), dtype=np.uint8)

    top_left = image
    top_right = image
    bottom_right = image
    bottom_left = image


    if assembly_type == 1:
        top_left = image
        top_right = image
        bottom_right = image
        bottom_left = image
    elif assembly_type == 2:
        bottom_left = image
        top_right = cv2.rotate(bottom_left, cv2.ROTATE_180) 
        top_left = cv2.rotate(bottom_left, cv2.ROTATE_90_CLOCKWISE)    
        bottom_right = cv2.rotate(bottom_left, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif assembly_type == 3:
        top_right = image 
        top_left = cv2.rotate(top_right, cv2.ROTATE_90_COUNTERCLOCKWISE)
        bottom_right = cv2.rotate(top_right, cv2.ROTATE_90_CLOCKWISE)
        bottom_left = cv2.rotate(top_right, cv2.ROTATE_180)
    elif assembly_type == 4:
        top_left = image
        top_right = cv2.rotate(top_left, cv2.ROTATE_180)
        bottom_right = cv2.rotate(top_left, cv2.ROTATE_180)
        bottom_left = image

    horizontal_joint = np.zeros((joint_size+marge*2, size*2+joint_size, num_channels), dtype=np.uint8)
    vertical_joint = np.zeros((size*2+joint_size, joint_size+marge*2, num_channels), dtype=np.uint8)

    output_image[0:size, 0:size] = top_left
    output_image[size+joint_size:size*2+joint_size, 0:size] = bottom_left
    output_image[0:size, size+joint_size:size*2+joint_size] = top_right
    output_image[size+joint_size:size*2+joint_size, size+joint_size:size*2+joint_size] = bottom_right

    # Joints
    output_image[size-marge:size+joint_size+marge, :] = horizontal_joint
    output_image[:, size-marge:size+joint_size+marge] = vertical_joint

    return output_image


def generate_motif_colors(img_path:str, output_dir:str, colors:dict, assembly_type:int, num_rows:int=2, num_cols:int=2, width:int=1990, height:int=1771) -> None:
    image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    for hexa in colors:
        image[image[:, :, 3] > 50] = list(rgb_to_bgr(*hex_to_rgb(hexa))) + [255]
        resized = cv2.resize(image, (122, 122))
        joint_size = 2
        out_img = generate_custom_grid(resized, assembly_type, num_rows, num_cols, joint_size)
        out_img = cv2.resize(out_img, (width, height))
        output_path = f"{output_dir}/{colors[hexa]}.png"    
        print(output_path)
        cv2.imwrite(output_path, out_img)


def stack_horizontal(images: list, joint_size: int, marge: int) -> object:
    """Stacks a list of images horizontally, inserting a joint between each."""
    if not images:
        return None
    actual_joint_thickness = joint_size + marge * 2
    result = images[0]
    # Get the number of channels from the first image
    num_channels = result.shape[2] if len(result.shape) > 2 else 1
    for i in range(1, len(images)):
        vertical_joint = np.zeros((images[0].shape[0], actual_joint_thickness, num_channels), dtype=np.uint8)
        result = np.concatenate((result, vertical_joint, images[i]), axis=1)
    return result

def stack_vertical(images: list, joint_size: int, marge: int) -> object:
    """Stacks a list of images vertically, inserting a joint between each."""
    if not images:
        return None
    actual_joint_thickness = joint_size + marge * 2
    result = images[0]
    # Get the number of channels from the first image
    num_channels = result.shape[2] if len(result.shape) > 2 else 1
    for i in range(1, len(images)):
        horizontal_joint = np.zeros((actual_joint_thickness, images[0].shape[1], num_channels), dtype=np.uint8)
        result = np.concatenate((result, horizontal_joint, images[i]), axis=0)
    return result

# --- Main grid generation function ---
def generate_9x4_grid(image: object, assembly_type:int, joint_size: int = None) -> object:
    """
    Generates a 9x4 grid pattern based on the input image following the revised instructions.

    In:
        - image (np.ndarray) : Image (tile) to be grouped.
        - joint_size (int) : Thickness of the joint.    
        - assembly_type (int) : type d'assemblage (1, 2, 3, 4, 5)

    Out:
        - grid (np.ndarray) : The 9x4 patterned image.
    """
    size = image.shape[0] # Assuming square input images (height == width)

    if joint_size is None:
        joint_size = int(size / 100)
    marge = int(joint_size / 4)

    image1 = image
    image2 = image
    image3 = image
    image4 = image

    if assembly_type == 1:
        image1 = image
        image2 = image
        image3 = image
        image4 = image
    if assembly_type == 2:
        image1 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        image2 = cv2.rotate(image, cv2.ROTATE_180)
        image3 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        image4 = cv2.rotate(image, cv2.ROTATE_180)
    if assembly_type == 3:
        image1 = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        image2 = image
        image3 = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        image4 = image
    if assembly_type == 4:
        image1 = image
        image2 = cv2.rotate(image, cv2.ROTATE_180)
        image3 = image
        image4 = cv2.rotate(image, cv2.ROTATE_180)


    # second row

    rotated_image1 = image
    rotated_image2 = image
    rotated_image3 = image
    rotated_image4 = image

    if assembly_type == 1:
        image1 = image
        image2 = image
        image3 = image
        image4 = image
    elif assembly_type == 2:
        rotated_image1 = image
        rotated_image2 = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        rotated_image3 = image
        rotated_image4 = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif assembly_type == 3:
        rotated_image1 = cv2.rotate(image, cv2.ROTATE_180) 
        rotated_image2 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        rotated_image3 = cv2.rotate(image, cv2.ROTATE_180)
        rotated_image4 = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif assembly_type == 4:
        rotated_image1 = image
        rotated_image2 =  cv2.rotate(image, cv2.ROTATE_180)
        rotated_image3 = image
        rotated_image4 =  cv2.rotate(image, cv2.ROTATE_180)
    else:
        print("No assembly")



    # 1. Create row_original_1x4: Stack 4 copies of the image horizontally, with joints.
    row_original_1x4 = stack_horizontal([image1, image2, image3, image4], joint_size, marge)

    # 2. Create row_rotated_1x4: Stack 4 copies of the image rotated 180 degrees horizontally, with joints.
    
    row_rotated_1x4 = stack_horizontal([rotated_image1, rotated_image2, rotated_image3, rotated_image4], joint_size, marge)

    # 3. Combine into block_2x4: Stack row_original_1x4 vertically on top of row_rotated_1x4, with a joint.
    block_2x4 = stack_vertical([row_original_1x4, row_rotated_1x4], joint_size, marge)

    # 4. Combine into block_4x4: Stack block_2x4 vertically on top of another block_2x4.
    #    (This interprets "row_original_2x4" as "block_2x4")
    block_4x4 = stack_vertical([block_2x4, block_2x4], joint_size, marge)

    # 5. Combine into block_6x4: Stack block_4x4 vertically on top of block_2x4.
    block_6x4 = stack_vertical([block_4x4, block_2x4], joint_size, marge)

    # 6. Combine into block_8x4: Stack block_6x4 vertically on top of block_2x4.
    block_8x4 = stack_vertical([block_6x4, block_2x4], joint_size, marge)

    # Final 9x4 grid: Stack grid_8x4 vertically on top of row_original_1x4, with a joint.
    # (Assuming "Final 9x5 grid" was a typo and you meant 9x4)
    final_9x4_grid = stack_vertical([block_8x4, row_original_1x4], joint_size, marge)

    return final_9x4_grid


def generate_motif_colors_9x4_grid(img_path:str, output_dir:str, colors:dict, assembly_type:int, num_rows:int=9, num_cols:int=4, width:int=501, height:int=780) -> None:
    image = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    for hexa in colors:
        image[image[:, :, 3] > 50] = list(rgb_to_bgr(*hex_to_rgb(hexa))) + [255]
        resized_tile = cv2.resize(image, (122, 122))
        joint_size = 2
        final_grid = generate_custom_grid(resized_tile, assembly_type, num_rows, num_cols, joint_size)
        out_img = cv2.resize(final_grid, (width, height))
        output_path = f"{output_dir}/{colors[hexa]}.png"    
        print(output_path)
        cv2.imwrite(output_path, out_img)


def generate_custom_grid(image: object, assembly_type: int, num_rows: int, num_cols: int, joint_size: int = 2) -> object:
    """
    Generates a custom grid pattern based on the input image, number of rows and columns, and assembly type.
    The logic for rotation is preserved as in the original quadrant logic.
    """
    marge = int(joint_size / 4)
    tile_h, tile_w = image.shape[:2]
    # Get the number of channels from the input image
    num_channels = image.shape[2] if len(image.shape) > 2 else 1
    
    def get_rotated_tile(row, col):
        # Logic for rotation based on position and assembly_type
        if assembly_type == 1:
            return image
        elif assembly_type == 2:
            if (row + col) % 2 == 0:
                return image
            else:
                return cv2.rotate(image, cv2.ROTATE_180)
        elif assembly_type == 3:
            if (row % 2 == 0 and col % 2 == 0) or (row % 2 == 1 and col % 2 == 1):
                return image
            elif row % 2 == 0:
                return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            else:
                return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif assembly_type == 4:
            if (row % 2 == 0):
                return image
            else:
                return cv2.rotate(image, cv2.ROTATE_180)
        elif assembly_type == 5:
            # For assembly_type 5, alternate flip/rotate for odd columns, but flip logic for even/odd rows
            if row % 2 == 0:
                # Even row: normal/rotated pattern
                if col % 2 == 0:
                    return image
                else:
                    return cv2.flip(cv2.rotate(image, cv2.ROTATE_180), 0)
            else:
                # Odd row: invert the pattern
                if col % 2 == 0:
                    return cv2.flip(cv2.rotate(image, cv2.ROTATE_180), 0)
                else:
                    return image
        else:
            return image

    # Build grid row by row
    grid_rows = []
    for row in range(num_rows):
        row_tiles = []
        for col in range(num_cols):
            tile = get_rotated_tile(row, col)
            row_tiles.append(tile)
        # Stack horizontally with joints
        if len(row_tiles) > 1:
            actual_joint_thickness = joint_size + marge * 2
            row_img = row_tiles[0]
            for t in row_tiles[1:]:
                vertical_joint = np.zeros((tile_h, actual_joint_thickness, num_channels), dtype=np.uint8)
                row_img = np.concatenate((row_img, vertical_joint, t), axis=1)
        else:
            row_img = row_tiles[0]
        grid_rows.append(row_img)
    # Stack rows vertically with joints
    if len(grid_rows) > 1:
        actual_joint_thickness = joint_size + marge * 2
        grid_img = grid_rows[0]
        for r in grid_rows[1:]:
            horizontal_joint = np.zeros((actual_joint_thickness, grid_img.shape[1], num_channels), dtype=np.uint8)
            grid_img = np.concatenate((grid_img, horizontal_joint, r), axis=0)
    else:
        grid_img = grid_rows[0]
    return grid_img


def main():
    motifs = os.listdir("patterns/" + NOM_MOTIF)
    motifs.remove("pattern.png")
    
    colors = get_color_tab("correspondance.csv")

    for motif in motifs:
        img_path = f"patterns/{NOM_MOTIF}/{motif}"
        output_dir = f"motifs/output/{NOM_MOTIF}"
        #generate_motif_colors(img_path, output_dir, colors)


if __name__ == '__main__':
    main()