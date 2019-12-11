from PIL import Image


# ===== FONCTION

def convert_to_tab(im):
    """
    Entrée : Fichier image
    Sortie : Tableau à deux dimensions
    Chaque pixels blancs devient un 1 dans le tableau, sinon un 0.
    La deuxième dimension du tableau correspond aux lignes de pixels.
    """

    im_RGB = im.convert('RGB')
    size = ( im_RGB.size[0], im_RGB.size[1] )
    tab = []

    for j in range(0, size[1], 1):

        line = []

        for i in range(0, size[0], 1):

            pix = im_RGB.getpixel((i, j))

            if pix[0]>=245 and pix[1]>=245 and pix[2]>=245:
                line.append(1)
            else:
                line.append(0)

        tab.append(line)

    return(tab)


# ===== EXECUTION

"""
tab = Image.open('tab3.jpg') # entrer le fichier à convertir
res = convert_to_tab(tab)

print("[\n")
for i in range(0, len(res)):
    print(str(res[i]) + ",\n")
print("]\n")
"""