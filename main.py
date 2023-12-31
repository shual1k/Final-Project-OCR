from PIL import Image
import pytesseract
import json
import math
import sys
import os

def OCR(ioPath):
    image = Image.open(ioPath+"/input.png")
    greyscale = image.convert('L')
    text = pytesseract.image_to_string(greyscale)
    image.close
    return text

def getDimentions(ioPath):
    image = Image.open(ioPath+"/input.png")
    [width, height] = image.size
    image.close
    return [width, height]

def createOutput(text, imageWidth, imageHeight):
    output = {"data": []}
    paragraphs = text.split("\n\n")
    heightAcc = 10
    for paragraph in paragraphs:
        width, height = annotationSize(paragraph, imageWidth, imageHeight)
        if width != 0:
            annotation = {}
            annotation["content"] = paragraph
            annotation["startX"] = (imageWidth - width) / 2
            annotation["startY"] = heightAcc
            heightAcc += height
            annotation["endX"] = annotation["startX"] + width
            annotation["endY"] = heightAcc
            output["data"].append(annotation)
            heightAcc += 10
    return output

    """textHeight = X, textWidth = 2X, annotationSquare = 2X^2
    characterSize = 25x25, characterCount = len, textLineSize = 625len
    both areas must equal so 2X^2=625len -> X=
    """
def annotationSize(content : str, imageWidth, imageHeight):
    charSquareSize = 25 * 20
    charCount = len(content)
    textLineSize = charSquareSize * charCount
    
    if charCount == 0:
        return 0, 0
    
    annotationHeight = round(math.sqrt(textLineSize / 2))
    annotationWidth = annotationHeight * 2
    
    annotationWidth = min(annotationWidth, imageWidth)
    annotationHeight = min(annotationHeight, imageHeight)
    return annotationWidth, annotationHeight
    

def writeOutput(output, ioPath):
    outputfile = os.path.join(ioPath, "output.txt")
    with open(outputfile, 'w') as file:
        json.dump(output, file, indent=4)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the path string as an argument.")
        sys.exit(1)
        
    ioPath = sys.argv[1]
    text = OCR(ioPath)
    [imageWidth, imageHeight] = getDimentions(ioPath)
    output = createOutput(text, imageWidth, imageHeight)
    writeOutput(output, ioPath)