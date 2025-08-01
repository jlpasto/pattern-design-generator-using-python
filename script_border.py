import os
import numpy as np
import PIL
from PIL import Image
import cv2


def generateFriseBorder(input_dir, output_dir):
        
    # ✅ Dimensions de l’image finale
    W, H = 1215, 1537

    # ✅ Points de destination (dans l’image finale)
    # top-left, top-right, bottom-right, bottom-left
    pts_dst = np.array([
        [361, 1159],       # top-left
        [965, 1161],       # top-right
        [1188, 1537],    # bottom-right
        [85,    1537]     # bottom-left
    ], dtype='float32')

    print(f"📐 Image finale: {W}x{H} / Points:\n{pts_dst}")

    # 🛠 Parcourir tous les PNG et appliquer la projection
    for root, _, files in os.walk(input_dir):
        for file in files:
            if not file.lower().endswith('.png'):
                continue

            input_path = os.path.join(root, file)
            rel_path = os.path.relpath(input_path, input_dir)
            base_name, ext = os.path.splitext(os.path.basename(file))
            Frise_Border = "Border"
            new_name = f"{base_name}-{Frise_Border}{ext}"
            output_path = os.path.join(output_dir, new_name)
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

                # ✂ Si tu veux, couper 100px à gauche
                final_pil = Image.fromarray(warped)
                cropped = final_pil.crop((200, 0, final_pil.width, final_pil.height))

                # 💾 Sauvegarder
                cropped.save(output_path)
                print(f"✅ Généré: {output_path}")

            except Exception as e:
                print(f"⚠️ Erreur pour {input_path}: {e}")

    print("🎉 Terminé !")
