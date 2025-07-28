import os
from split_pattern import split_colors
from motifs_color import generate_motif_colors, get_color_tab, generate_motif_colors_9x4_grid
from script_content import generateFriseContent
from prompt import assemble_pattern_program_numbered
import argparse


def mkdir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def main(nom_motif, assemble_choice, assembly_type_choice, assembly_subtype_choice):
    Produit = "Produit"
    Frise = "Frise"
    Frise_Content = "Frise Content"
    mkdir("output")
    mkdir("output/" + nom_motif)
    mkdir("output/" + nom_motif + "/" + Produit)
    mkdir("output/" + nom_motif + "/" + Frise)
    mkdir("output/" + nom_motif + "/" + Frise_Content)

    # for now 1, value should come from user input as paramater
    assembly_type = 1

    # Sépare les couleurs du pattern pour récupérer les différents motifs
    pattern_path = f"patterns/{nom_motif}.png"    
    pattern_output_dir =  f"output/{nom_motif}/motifs"
    mkdir(pattern_output_dir)

    split_colors(pattern_path, pattern_output_dir)
    print("Motifs séparés")

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
        mkdir(motifs_output_dir1)        
               
        generate_motif_colors(motif_path, motifs_output_dir1, colors, assembly_type) # generate layer 1
        generate_motif_colors_9x4_grid(motif_path, motifs_output_dir2, colors, assembly_type) # generate layer 2

        print(f"{num_motif} : OK") 


    # generate frise content

    base_dir = motifs_output_dir2_frise
    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    # list all folders inside Frise/

    for folder in folders:
        output_dir = os.path.join(motifs_output_dir2_frise_content, folder)
        input_dir = os.path.join(motifs_output_dir2_frise, folder)
        print(input_dir)
        generateFriseContent(input_dir, output_dir)

if __name__ == '__main__':
    nom_motif, assemble_choice, assembly_type_choice, assembly_subtype_choice = assemble_pattern_program_numbered()
    main(nom_motif, assemble_choice, assembly_type_choice, assembly_subtype_choice)
    print("DONE")

