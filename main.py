import os
from split_pattern import split_colors
from motifs_color import generate_motif_colors, get_color_tab, generate_motif_colors_9x4_grid
from script_content import generateFriseContent
from prompt import assemble_pattern_program_numbered
import argparse
import cv2
import numpy as np


def mkdir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def main(nom_motif, assemble_choice, assembly_type_choice, assembly_subtype_choice, num_rows=2, num_cols=2, width=1990, height=1771):
    Produit = "Produit"
    Frise = "Frise"
    Frise_Content = "Frise Content"
    mkdir("output")
    mkdir("output/" + nom_motif)
    mkdir("output/" + nom_motif + "/" + Produit)
    mkdir("output/" + nom_motif + "/" + Frise)
    mkdir("output/" + nom_motif + "/" + Frise_Content)

    # Sépare les couleurs du pattern pour récupérer les différents motifs
    pattern_path = f"patterns/{nom_motif}.png"    
    pattern_output_dir =  f"output/{nom_motif}/motifs"
    mkdir(pattern_output_dir)
    split_colors(pattern_path, pattern_output_dir)
    print("Motifs séparés")

    # Generate sample assembly image first for user to check
    sample_dir = f"output/{nom_motif}/Sample Assembly"
    mkdir(sample_dir)
    base_img_path = f"patterns/{nom_motif}.png"
    if os.path.exists(base_img_path):
        base_img = cv2.imread(base_img_path, cv2.IMREAD_UNCHANGED)
        tile = cv2.resize(base_img, (122, 122))
        # Rotation logic as in motifs_color.py lines 60-79
        if assembly_subtype_choice == 1:
            top_left = tile
            top_right = tile
            bottom_right = tile
            bottom_left = tile
        elif assembly_subtype_choice == 2:
            bottom_left = tile
            top_right = cv2.rotate(bottom_left, cv2.ROTATE_180)
            top_left = cv2.rotate(bottom_left, cv2.ROTATE_90_CLOCKWISE)
            bottom_right = cv2.rotate(bottom_left, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif assembly_subtype_choice == 3:
            top_right = tile
            top_left = cv2.rotate(top_right, cv2.ROTATE_90_COUNTERCLOCKWISE)
            bottom_right = cv2.rotate(top_right, cv2.ROTATE_90_CLOCKWISE)
            bottom_left = cv2.rotate(top_right, cv2.ROTATE_180)
        elif assembly_subtype_choice == 4:
            top_left = tile
            top_right = cv2.rotate(top_left, cv2.ROTATE_180)
            bottom_right = cv2.rotate(top_left, cv2.ROTATE_180)
            bottom_left = tile
        # Assemble 2x2 grid
        joint_size = 2
        marge = int(joint_size / 4)
        size = tile.shape[0]
        output_image = np.zeros((size*2 + joint_size, size*2 + joint_size, 4), dtype=np.uint8)
        output_image[0:size, 0:size] = top_left
        output_image[size+joint_size:size*2+joint_size, 0:size] = bottom_left
        output_image[0:size, size+joint_size:size*2+joint_size] = top_right
        output_image[size+joint_size:size*2+joint_size, size+joint_size:size*2+joint_size] = bottom_right
        # Joints
        output_image[size-marge:size+joint_size+marge, :] = 0
        output_image[:, size-marge:size+joint_size+marge] = 0
        sample_path = os.path.join(sample_dir, f"sample_assembly_image.png")
        cv2.imwrite(sample_path, output_image)
        print(f"Sample assembly image generated: {sample_path}")
        print("Please check the sample image and type '1' to continue with layer generation:")
        user_input = input()
        if user_input != '1':
            print("Layer generation cancelled.")
            return

    # Récupère les motifs générés
    colors = get_color_tab("correspondance.csv")
    motifs = os.listdir(pattern_output_dir)

    motifs_output_dir1 = ""
    motifs_output_dir2 = ""
    motifs_output_dir2_frise = f"output/{nom_motif}/{Frise}"
    motifs_output_dir2_frise_content = f"output/{nom_motif}/{Frise_Content}"
    
    for motif in motifs:
        num_motif = motif.split(".")[0]
        motif_path = f"{pattern_output_dir}/{motif}"
        motifs_output_dir1 = f"output/{nom_motif}/{Produit}/{num_motif}"
        motifs_output_dir2 = f"output/{nom_motif}/{Frise}/{num_motif}"
        
        if assembly_type_choice == "both":
            mkdir(motifs_output_dir1)
            mkdir(motifs_output_dir2)   
            generate_motif_colors(motif_path, motifs_output_dir1, colors, assembly_subtype_choice, num_rows, num_cols, width, height) # generate layer 1
            generate_motif_colors_9x4_grid(motif_path, motifs_output_dir2, colors, assembly_subtype_choice, num_rows, num_cols, width, height) # generate layer 2
        if assembly_type_choice == "product assembly":
            mkdir(motifs_output_dir1)
            generate_motif_colors(motif_path, motifs_output_dir1, colors, assembly_subtype_choice, num_rows, num_cols, width, height) # generate layer 1
        if assembly_type_choice == "border assembly":
            mkdir(motifs_output_dir2)
            generate_motif_colors_9x4_grid(motif_path, motifs_output_dir2, colors, assembly_subtype_choice, num_rows, num_cols, width, height) # generate layer 2
        print(f"{num_motif} : OK")

    # generate frise content
    if assembly_type_choice == "border assembly":
        base_dir = motifs_output_dir2_frise
        folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
        for folder in folders:
            output_dir = os.path.join(motifs_output_dir2_frise_content, folder)
            input_dir = os.path.join(motifs_output_dir2_frise, folder)
            print(input_dir)
            generateFriseContent(input_dir, output_dir)


if __name__ == '__main__':
    prompt_result = assemble_pattern_program_numbered()
    if len(prompt_result) == 12:
        # both: nom_motif, assemble_choice, assembly_type_choice, assembly_subtype_choice, num_rows_product, num_cols_product, width_product, height_product, num_rows_border, num_cols_border, width_border, height_border
        nom_motif, assemble_choice, assembly_type_choice, assembly_subtype_choice, num_rows_product, num_cols_product, width_product, height_product, num_rows_border, num_cols_border, width_border, height_border = prompt_result
        def main_both(nom_motif, assemble_choice, assembly_type_choice, assembly_subtype_choice, num_rows_product, num_cols_product, width_product, height_product, num_rows_border, num_cols_border, width_border, height_border):
            Produit = "Produit"
            Frise = "Frise"
            Frise_Content = "Frise Content"
            mkdir("output")
            mkdir("output/" + nom_motif)
            mkdir("output/" + nom_motif + "/" + Produit)
            mkdir("output/" + nom_motif + "/" + Frise)
            mkdir("output/" + nom_motif + "/" + Frise_Content)

            pattern_path = f"patterns/{nom_motif}.png"    
            pattern_output_dir =  f"output/{nom_motif}/motifs"
            mkdir(pattern_output_dir)
            split_colors(pattern_path, pattern_output_dir)
            print("Motifs séparés")

            # Sample image for product
            sample_dir = f"output/{nom_motif}/Sample Assembly"
            mkdir(sample_dir)
            base_img_path = f"patterns/{nom_motif}.png"
            if os.path.exists(base_img_path):
                base_img = cv2.imread(base_img_path, cv2.IMREAD_UNCHANGED)
                tile = cv2.resize(base_img, (122, 122))
                # Rotation logic as before
                if assembly_subtype_choice == 1:
                    top_left = tile
                    top_right = tile
                    bottom_right = tile
                    bottom_left = tile
                elif assembly_subtype_choice == 2:
                    bottom_left = tile
                    top_right = cv2.rotate(bottom_left, cv2.ROTATE_180)
                    top_left = cv2.rotate(bottom_left, cv2.ROTATE_90_CLOCKWISE)
                    bottom_right = cv2.rotate(bottom_left, cv2.ROTATE_90_COUNTERCLOCKWISE)
                elif assembly_subtype_choice == 3:
                    top_right = tile
                    top_left = cv2.rotate(top_right, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    bottom_right = cv2.rotate(top_right, cv2.ROTATE_90_CLOCKWISE)
                    bottom_left = cv2.rotate(top_right, cv2.ROTATE_180)
                elif assembly_subtype_choice == 4:
                    top_left = tile
                    top_right = cv2.rotate(top_left, cv2.ROTATE_180)
                    bottom_right = cv2.rotate(top_left, cv2.ROTATE_180)
                    bottom_left = tile
                joint_size = 2
                marge = int(joint_size / 4)
                size = tile.shape[0]
                output_image = np.zeros((size*2 + joint_size, size*2 + joint_size, 4), dtype=np.uint8)
                output_image[0:size, 0:size] = top_left
                output_image[size+joint_size:size*2+joint_size, 0:size] = bottom_left
                output_image[0:size, size+joint_size:size*2+joint_size] = top_right
                output_image[size+joint_size:size*2+joint_size, size+joint_size:size*2+joint_size] = bottom_right
                output_image[size-marge:size+joint_size+marge, :] = 0
                output_image[:, size-marge:size+joint_size+marge] = 0
                sample_path = os.path.join(sample_dir, f"sample_assembly_image.png")
                cv2.imwrite(sample_path, output_image)
                print(f"Sample assembly image generated: {sample_path}")
                print("Please check the sample image and type '1' to continue with layer generation:")
                user_input = input()
                if user_input != '1':
                    print("Layer generation cancelled.")
                    return

            colors = get_color_tab("correspondance.csv")
            motifs = os.listdir(pattern_output_dir)
            motifs_output_dir1 = ""
            motifs_output_dir2 = ""
            motifs_output_dir2_frise = f"output/{nom_motif}/{Frise}"
            motifs_output_dir2_frise_content = f"output/{nom_motif}/{Frise_Content}"
            for motif in motifs:
                num_motif = motif.split(".")[0]
                motif_path = f"{pattern_output_dir}/{motif}"
                motifs_output_dir1 = f"output/{nom_motif}/{Produit}/{num_motif}"
                motifs_output_dir2 = f"output/{nom_motif}/{Frise}/{num_motif}"
                mkdir(motifs_output_dir1)
                mkdir(motifs_output_dir2)
                generate_motif_colors(motif_path, motifs_output_dir1, colors, assembly_subtype_choice, num_rows_product, num_cols_product, width_product, height_product)
                generate_motif_colors_9x4_grid(motif_path, motifs_output_dir2, colors, assembly_subtype_choice, num_rows_border, num_cols_border, width_border, height_border)
                print(f"{num_motif} : OK")
            # Border frise content
            base_dir = motifs_output_dir2_frise
            folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
            for folder in folders:
                output_dir = os.path.join(motifs_output_dir2_frise_content, folder)
                input_dir = os.path.join(motifs_output_dir2_frise, folder)
                print(input_dir)
                generateFriseContent(input_dir, output_dir)
        main_both(nom_motif, assemble_choice, assembly_type_choice, assembly_subtype_choice, num_rows_product, num_cols_product, width_product, height_product, num_rows_border, num_cols_border, width_border, height_border)
    else:
        # single assembly
        if 'product assembly' in prompt_result:
            nom_motif, assemble_choice, assembly_type_choice, assembly_subtype_choice, num_rows, num_cols, width_product, height_product = prompt_result
            main(nom_motif, assemble_choice, assembly_type_choice, assembly_subtype_choice, num_rows, num_cols, width_product, height_product)
        else:
            nom_motif, assemble_choice, assembly_type_choice, assembly_subtype_choice, num_rows, num_cols, width_border, height_border = prompt_result
            main(nom_motif, assemble_choice, assembly_type_choice, assembly_subtype_choice, num_rows, num_cols, width_border, height_border)
    print("DONE")

