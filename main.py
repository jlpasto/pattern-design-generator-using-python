import os
from split_pattern import split_colors
from motifs_color import generate_motif_colors, get_color_tab, generate_motif_colors_9x4_grid
import argparse


def mkdir(name):
    if not os.path.exists(name):
        os.makedirs(name)


def main(nom_motif):
    layer1 = "Layer 1"
    layer2 = "Layer 2"
    mkdir("output")
    mkdir("output/" + nom_motif)
    mkdir("output/" + nom_motif + "/" + layer1)
    mkdir("output/" + nom_motif + "/" + layer2)

    # Sépare les couleurs du pattern pour récupérer les différents motifs
    pattern_path = f"patterns/{nom_motif}.png"    
    pattern_output_dir =  f"output/{nom_motif}/motifs"
    mkdir(pattern_output_dir)

    split_colors(pattern_path, pattern_output_dir)
    print("Motifs séparés")

    # Récupère les motifs générés
    colors = get_color_tab("correspondance.csv")
    motifs = os.listdir(pattern_output_dir)

    for motif in motifs:
        num_motif = motif.split(".")[0]
        motif_path = f"{pattern_output_dir}/{motif}"
        motifs_output_dir1 = f"output/{nom_motif}/{layer1}/{num_motif}"
        motifs_output_dir2 = f"output/{nom_motif}/{layer2}/{num_motif}"
        mkdir(motifs_output_dir1)        
        mkdir(motifs_output_dir2)        

        generate_motif_colors(motif_path, motifs_output_dir1, colors) # generate layer 1
        generate_motif_colors_9x4_grid(motif_path, motifs_output_dir2, colors) # generate layer 2
        print(f"{num_motif} : OK")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--motif", type=str, help="Nom du motif")

    args = parser.parse_args()
    print(args)
    if args.motif:
        nom_motif = args.motif
        main(nom_motif)
    else:
        print("Aucun nom de motif spécifié. Veuillez spécifier -m NOM_MOTIF.")
