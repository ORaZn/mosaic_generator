import numpy as np
import os
from PIL import Image, ImageDraw
import argparse,math

parser = argparse.ArgumentParser()
parser.add_argument('--input', dest='input', required=True)
parser.add_argument('--images', dest='images', required=True)
parser.add_argument('--patchsize', dest='patchsize',nargs=2, required=True, help="#ofRows #ofColumns")
parser.add_argument('--shape', dest='shape', required=True, help = "shape of candidate images: rectangle,circle")
args = parser.parse_args()

def GenerateMosaic(main_image, candidate_images, patches,patch_size, candidates_shape):
    main_image_patches = splitImage(main_image, patches)

    output_images = []
    avgs = []
    for img in candidate_images:
        avgs.append(meanRGB(img))
        #avgs.append(AverageIntensity(img))

    counter = 0
    for img in main_image_patches:
        #patch_avg = AverageIntensity(img)
        patch_avg = meanRGB(img)
        img_index = bestMatchingImage(patch_avg, avgs)
        output_images.append(candidate_images[img_index])
        counter += 1

    mosaic_final = CreateMosaicImage(output_images, patches,patch_size,candidates_shape)
    return mosaic_final


def splitImage(image, patches):
    width, height = image.size[0], image.size[1]
    rows, cols = patches
    patch_width, patch_height = int(width / cols), int(height / rows)
    images = []
    for r in range(rows):
        for c in range(cols):
            images.append(image.crop((c * patch_width, r * patch_height, (c + 1) * patch_width, (r + 1) * patch_height)))
    return images


def AverageIntensity(image):
    im_arr = np.array(image)
    return im_arr.mean()

#calculate the average red channel value, green value and blue value across all pixels of an image
def meanRGB(image):
    img_array = np.array(image)
    width, height, channels = img_array.shape
    return img_array.reshape(width * height, channels).mean(axis=0)


def processCandidateImages(candidates_dir,patch_size):
    candidate_images = os.listdir(candidates_dir)
    images = []
    for image in candidate_images:
        if image.split('.')[-1] != 'jpg':
            continue
        imgPath = os.path.join(candidates_dir, image)
        img = Image.open(imgPath)
        images.append(img.resize(patch_size))
    return images


def bestMatchingImage(input_avg, avgs):
    index = 0
    min_index = 0
    isfirst = True
    minimal_distance = 0
    for avg in avgs:
        #distance = math.sqrt((input_avg - avg)**2)
        distance = ((input_avg - avg)**2).sum()
        if isfirst:
            minimal_distance = distance
            isfirst=False
        if distance < minimal_distance:
            minimal_distance = distance
            min_index = index
        index += 1
    return min_index


def CreateMosaicImage(images, patches,patch_size, candidates_shape):
    im_size = images[0].size
    circle = Image.new("L", im_size, 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0,0,patch_size[0],patch_size[1]),fill=255)
    
    m, n = patches
    width = patch_size[0]
    height = patch_size[1]
    grid_img = Image.new('RGB', (n * width, m * height))
    for index in range(len(images)):
        row = int(index / n)
        col = index - n * row
        if candidates_shape == 'circle':
            grid_img.paste(images[index], (col * width, row * height),circle)
        else:
            grid_img.paste(images[index], (col * width, row * height))
    return grid_img





#----------------------------------------------

print('starting...')
main_image = Image.open(args.input)

# number of patches of the original image (prows,pcols): prows - number of patches along the vertical axis(x)
#                                                pcols - number of patches along the horizontal axis(y)
patches = (int(args.patchsize[0]),int(args.patchsize[1]))

candidates_shape = args.shape

# given the patches amount, we need to determine the maximum size (width x height) candidate images can have
# i.e. divide the image width by the number of patches in horizontal axis
# and the height by the number in vertical
patch_size = (int(main_image.size[0] / patches[1]) , int(main_image.size[1] / patches[0]))

candidate_images = processCandidateImages(args.images,patch_size)

mosaic_final = GenerateMosaic(main_image, candidate_images, patches,patch_size, candidates_shape)

mosaic_final.save('mosaic.jpg', 'jpeg')
print('done! Check the mosaic.jpg image in the folder from which you run the command')
