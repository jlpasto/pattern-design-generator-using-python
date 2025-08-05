import os
from split_pattern import split_colors, split_colors_no_resize
from motifs_color import generate_motif_colors, get_color_tab, generate_motif_colors_9x4_grid, generate_motif_colors_9x4_grid_no_assembly, generate_motif_layer_no_assembly
from script_content import generateFriseContent
from script_border import generateFriseBorder
from prompt import assemble_pattern_program_numbered
from generate_hexapattern import generate_hexapattern
from gui import get_pattern_assembly_params
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



    # Generate sample assembly image first for user to check
    sample_dir = f"output/{nom_motif}/Sample Assembly"
    mkdir(sample_dir)
    base_img_path = f"patterns/{nom_motif}.png"
    if os.path.exists(base_img_path):
        base_img = cv2.imread(base_img_path, cv2.IMREAD_UNCHANGED)
        tile = cv2.resize(base_img, (122, 122))

        top_left = tile
        top_right = tile
        bottom_right = tile
        bottom_left = tile
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
            top_right = cv2.flip(top_left, 1)  # 1 = horizontal flip
            bottom_right = cv2.flip(top_left, 1)  # 1 = horizontal flip
            bottom_left = tile
        elif assembly_subtype_choice == 5:
            top_left = tile
            top_right = cv2.flip(cv2.rotate(top_left, cv2.ROTATE_180), 0)  # rotate 180, then flip vertically
            bottom_right = tile
            bottom_left = cv2.flip(cv2.rotate(top_left, cv2.ROTATE_180), 0) # rotate 180, then flip vertically

        output_image = None
        if assembly_subtype_choice in (1, 2, 3, 4, 5):
            # Assemble 2x2 grid
            joint_size = 2
            marge = int(joint_size / 4)
            size = tile.shape[0]
            # Get the number of channels from the tile
            num_channels = tile.shape[2] if len(tile.shape) > 2 else 1
            output_image = np.zeros((size*2 + joint_size, size*2 + joint_size, num_channels), dtype=np.uint8)
            output_image[0:size, 0:size] = top_left
            output_image[size+joint_size:size*2+joint_size, 0:size] = bottom_left
            output_image[0:size, size+joint_size:size*2+joint_size] = top_right
            output_image[size+joint_size:size*2+joint_size, size+joint_size:size*2+joint_size] = bottom_right
            # Joints
            output_image[size-marge:size+joint_size+marge, :] = 0
            output_image[:, size-marge:size+joint_size+marge] = 0
        elif assembly_subtype_choice == 6:
            print("Handle pattern 6")
            output_image = generate_hexapattern(nom_motif, base_img_path, image=None, num_rows=num_rows, num_cols=num_cols)
            
        sample_path = os.path.join(sample_dir, f"sample_assembly_image.png")
        cv2.imwrite(sample_path, output_image)
        print(f"Sample assembly image generated: {sample_path}")
            

        # Sépare les couleurs du pattern pour récupérer les différents motifs
        pattern_path = f"patterns/{nom_motif}.png"    
        pattern_output_dir =  f"output/{nom_motif}/motifs"
        mkdir(pattern_output_dir)
        if assembly_subtype_choice == 6:
            split_colors_no_resize(pattern_path, pattern_output_dir, nom_motif)
        else:
            split_colors(pattern_path, pattern_output_dir)
        print("Motifs séparés")

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
                generate_motif_colors(nom_motif, num_motif, motif_path, motifs_output_dir1, colors, assembly_subtype_choice, num_rows, num_cols, width, height) # generate layer 1
                generate_motif_colors_9x4_grid(nom_motif, num_motif, motif_path, motifs_output_dir2, colors, assembly_subtype_choice, num_rows, num_cols, width, height) # generate layer 2
            if assembly_type_choice == "product assembly":
                mkdir(motifs_output_dir1)
                generate_motif_colors(nom_motif, num_motif, motif_path, motifs_output_dir1, colors, assembly_subtype_choice, num_rows, num_cols, width, height) # generate layer 1
            if assembly_type_choice == "border assembly":
                mkdir(motifs_output_dir2)
                generate_motif_colors_9x4_grid(nom_motif, num_motif, motif_path, motifs_output_dir2, colors, assembly_subtype_choice, num_rows, num_cols, width, height) # generate layer 2
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
    #prompt_result = assemble_pattern_program_numbered()
    prompt_result = get_pattern_assembly_params()
    print(f"prompt result {prompt_result}")
    if isinstance(prompt_result, dict) and prompt_result.get("assemble_choice") == "no":
        nom_motif = prompt_result["assemble_pattern"]
        width_produit = prompt_result["width_produit"]
        height_produit = prompt_result["height_produit"]
        width_frise = prompt_result["width_frise"]
        height_frise = prompt_result["height_frise"] 
        is_border_answer = prompt_result["is_border_answer"] 


        # generate motifs
        pattern_path = f"patterns/{nom_motif}.png"    
        pattern_output_dir =  f"output/{nom_motif}/motifs"
        mkdir(pattern_output_dir)
        split_colors(pattern_path, pattern_output_dir)
        
        # generate product and Frise layers
        Produit = "Produit"
        Frise = "Frise"
        Frise_Content = "Frise Content"
        Frise_Border = "Frise Border"
        colors = get_color_tab("correspondance.csv")
        pattern_output_dir =  f"output/{nom_motif}/motifs"
        motifs = os.listdir(pattern_output_dir)
        motifs_output_dir1 = ""
        motifs_output_dir2 = ""
        motifs_output_dir2_frise = f"output/{nom_motif}/{Frise}"
        motifs_output_dir2_frise_content = f"output/{nom_motif}/{Frise_Content}"
        motifs_output_dir2_frise_border = f"output/{nom_motif}/{Frise_Border}"
        for motif in motifs:
            num_motif = motif.split(".")[0]
            motif_path = f"{pattern_output_dir}/{motif}"
            motifs_output_dir1 = f"output/{nom_motif}/{Produit}/{num_motif}"
            motifs_output_dir2 = f"output/{nom_motif}/{Frise}/{num_motif}"
            mkdir(motifs_output_dir1)
            mkdir(motifs_output_dir2)
            generate_motif_layer_no_assembly(nom_motif, num_motif, motif_path, motifs_output_dir1, colors, width_produit, height_produit)
            generate_motif_colors_9x4_grid_no_assembly(nom_motif, num_motif, motif_path, motifs_output_dir2, colors, width_frise, height_frise)
            print(f"{num_motif} : OK")


        # Border frise content
        base_dir = motifs_output_dir2_frise
        folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
        for folder in folders:
            output_dir = os.path.join(motifs_output_dir2_frise_content, folder)
            output_dir_frise_border = os.path.join(motifs_output_dir2_frise_border, folder)
            input_dir = os.path.join(motifs_output_dir2_frise, folder)
            print(input_dir)
            if is_border_answer == "yes":
                generateFriseBorder(input_dir, output_dir_frise_border)
            else:
                generateFriseContent(input_dir, output_dir)

        print("Layer generated with no assembly.")
        import sys
        sys.exit(0)

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

            pattern_output_dir = ""

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
                    top_right = cv2.flip(top_left, 1)  # 1 = horizontal flip
                    bottom_right = cv2.flip(top_left, 1)  # 1 = horizontal flip
                    bottom_left = tile
                elif assembly_subtype_choice == 5:
                    top_left = tile
                    top_right = cv2.flip(cv2.rotate(top_left, cv2.ROTATE_180), 0)  # rotate 180, then flip vertically
                    bottom_right = tile
                    bottom_left = cv2.flip(cv2.rotate(top_left, cv2.ROTATE_180), 0) # rotate 180, then flip vertically

                output_image = None
                if assembly_subtype_choice in (1,2,3,4,5):

                    joint_size = 2
                    marge = int(joint_size / 4)
                    size = tile.shape[0]
                    # Get the number of channels from the tile
                    num_channels = tile.shape[2] if len(tile.shape) > 2 else 1
                    output_image = np.zeros((size*2 + joint_size, size*2 + joint_size, num_channels), dtype=np.uint8)
                    output_image[0:size, 0:size] = top_left
                    output_image[size+joint_size:size*2+joint_size, 0:size] = bottom_left
                    output_image[0:size, size+joint_size:size*2+joint_size] = top_right
                    output_image[size+joint_size:size*2+joint_size, size+joint_size:size*2+joint_size] = bottom_right
                    output_image[size-marge:size+joint_size+marge, :] = 0
                    output_image[:, size-marge:size+joint_size+marge] = 0
                elif assembly_subtype_choice == 6:
                    print("Handle pattern 6")
                    output_image = generate_hexapattern(nom_motif, base_img_path, image=None, num_rows=num_rows_product, num_cols=num_cols_product)



                # Sample image for product
                sample_dir = f"output/{nom_motif}/Sample Assembly"
                mkdir(sample_dir)

                sample_path = os.path.join(sample_dir, f"sample_assembly_image.png")
                cv2.imwrite(sample_path, output_image)
                print(f"Sample assembly image generated: {sample_path}")


                # Sépare les couleurs du pattern pour récupérer les différents motifs
                pattern_path = f"patterns/{nom_motif}.png"    
                pattern_output_dir =  f"output/{nom_motif}/motifs"
                mkdir(pattern_output_dir)
                if assembly_subtype_choice == 6:
                    split_colors_no_resize(pattern_path, pattern_output_dir, nom_motif)
                else:
                    split_colors(pattern_path, pattern_output_dir)
                print("Motifs séparés")


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
                generate_motif_colors(nom_motif, num_motif, motif_path, motifs_output_dir1, colors, assembly_subtype_choice, num_rows_product, num_cols_product, width_product, height_product)
                generate_motif_colors_9x4_grid(nom_motif, num_motif, motif_path, motifs_output_dir2, colors, assembly_subtype_choice, num_rows_border, num_cols_border, width_border, height_border)
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

