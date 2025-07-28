import os
import numpy as np
from PIL import Image
import cv2


def generateFriseContent(input_dir, output_dir):
    # 📂 Chemins
    #input_dir = './calques-type-1'
    #output_dir = './calques-type-2'

    # ✅ Dimensions de l’image finale
    W, H = 1015, 1537

    # ✅ Points de destination (dans l’image finale)
    # top-left, top-right, bottom-right, bottom-left
    pts_dst = np.array([
        [243, 1182],       # top-left
        [686, 1182],       # top-right
        [822, 1536],      # bottom-right
        [55, 1535]        # bottom-left
    ], dtype='float32')

    print(f"📐 Image finale: {W}x{H} / Points:\n{pts_dst}")

    # 🛠 Parcourir tous les PNG et appliquer la projection
    for root, _, files in os.walk(input_dir):
        for file in files:
            if not file.lower().endswith('.png'):
                continue

            input_path = os.path.join(root, file)
            rel_path = os.path.relpath(input_path, input_dir)
            output_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            try:
                # 📦 Charger le motif
                pil_img = Image.open(input_path).convert('RGBA')
                img = np.array(pil_img)
                h, w = img.shape[:2]

                # Points source = rectangle complet
                pts_src = np.array([[0,0],[w,0],[w,h],[0,h]], dtype='float32')

                # 🪞 Calculer la transformation
                matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)

                # ⚡ Appliquer warpPerspective
                warped = cv2.warpPerspective(img, matrix, (W, H), borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))

                # 💾 Sauvegarder directement sans découper
                Image.fromarray(warped).save(output_path)
                print(f"✅ Généré: {output_path}")

            except Exception as e:
                print(f"⚠️ Erreur pour {input_path}: {e}")

    print("🎉 Terminé !")
