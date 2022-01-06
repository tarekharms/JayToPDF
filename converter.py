import os
from PIL import Image
from PyPDF2 import PdfFileMerger
from pathlib import Path
import shutil

albumDirs = os.scandir("./album")

for albumDir in albumDirs:
    print("Starting " + albumDir.name)
    
    album = os.scandir(albumDir)
    volumePath = Path("./pdf/" + albumDir.name)
    volumePath.mkdir(parents=True, exist_ok=True)

    print('Converting to PDF:', end='')

    for page in album:
        if(page.name.endswith(".jpg")):
            print('.', end='', flush=True)
            name = page.name[:-3]
            jpeg = Image.open(page.path)
            image = jpeg.convert("RGB")
            image.save("./pdf/" + albumDir.name + "/" + name + "pdf")
        elif(os.path.isdir(page)):
            subfolder = os.scandir(page)
            for subfolderPage in subfolder:
                if(subfolderPage.name.endswith(".jpg")):
                    print('.', end='', flush=True)
                    name = subfolderPage.name[:-3]
                    jpeg = Image.open(subfolderPage.path)
                    image = jpeg.convert("RGB")
                    image.save("./pdf/" + albumDir.name + "/" + name + "pdf")

    
    print()

    volumeMerger = PdfFileMerger()

    volumeDir = os.scandir(volumePath)
    
    print('Merging PDF:', end='')

    for pdfFile in volumeDir:
        print('.', end='', flush=True)
        volumeMerger.append(pdfFile.path)
    
    print()
    
    volumeMerger.write("./pdf/" + albumDir.name + ".pdf")
    volumeMerger.close()
    print("Finished " + albumDir.name)

    shutil.rmtree(volumePath)