# 🎨 Pattern Design Generator

## 📌 Overview

This Python-based application automates the creation of visually compelling pattern designs by layering motifs with customizable colors.

Simply provide a base motif image, and the script will generate design layers by applying color transformations—making it an excellent tool for textile, wallpaper, and surface design prototyping.

---

## ⚙️ Technologies Used

- **Python 3**
- **opencv-python**
- **NumPy**
- **Color Manipulation**
- **Image Layering**
- **OS & File Handling**

---

## 🚀 Features

- 🖼 **Accepts any motif image** (`.png`, `.jpg`, etc.) as input.
- 🎨 **Generates multiple layers** with different colors derived from a base palette.
- 🧩 **Supports grouping and sub-grouping** for structured layer organization.
- 📁 **Saves images** in designated folders for easy access and reference.
- 🔄 **Easily customizable** for batch generation and pattern variations.

---

## 📂 Folder Structure

```
pattern-design-generator-using-python/
│
├── main.py                 # Main script to run the generator
├── motifs_color.py         # Helper functions (e.g., generating grid and applying colors)
├── split_pattern.py        # Helper functions (e.g., splitting pattern by colors)
├── patterns/               # Motif images and Motif_color.txt (user-provided)
├── outputs/                # Generated design layers
├── correspondance.csv      # Reference color palettes
├── README.md               # Project documentation
└── requirements.txt        # Project dependencies
```

---

## 🔐 Environment Variables

No environment variables are required. All configurations are handled via parameters or file inputs.

---

## ✅ Prerequisites

- Python 3.7+
- `opencv-python`, `numpy`

Install the required packages with:

```bash
pip install -r requirements.txt
```

---

## 🏁 Getting Started

1. Clone the repository:

```bash
git clone https://github.com/jlpasto/pattern-design-generator-using-python
cd pattern-design-generator-using-python
```

2. Place your motif image inside the `patterns/` folder.
3. Run the main script:
   - where Motif_Name is the name of the image without extension.
```bash
python main.py -m Motif_Name
```

4. Check the `output/` folder for generated layers.

---

## 📌 Notes

- Ensure motif images have transparent or white backgrounds for best results.
- You can define your own color palette in the code or modify the default palette.
- The script is ideal for automating repetitive design experimentation.

---

## 📧 Contact

For feedback, suggestions, or feature requests, please contact [Jhon Loyd Pastorin](mailto:jhonloydpastorin.03@gmail.com).
