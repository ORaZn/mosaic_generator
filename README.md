# mosaic_generator
Run “python mosaic_generator.py --help” for input parameters information.
Example: python Mosaic_Creator.py --input kitty.jpg --images <images base folder> --patchsize 100 100 --shape rectangle

The program apart from the input image and images folder takes asparameters a grid size to which the original image is divided (numberof patches across the horizontal dimension and number of patchesacross the vertical dimension) and the shape with which candidateimages will fill the original image. According to the size of the gridthe dimensions of patches is automatically calculated given thedimensions of an original image.

The implementation:

The main approach was to divide the main image into the patches withthe size computed from the input value of the grid size and store thatpatches in one array.
The division into patches was conductedrow-by-row like in the following way, where the number correspond tothe patch:

|1 | 2 | 3 | 4 |

|5 | 6 | 7 | 8 |

|9 |10|11|12|

|13|14|15|16|

“SplitImage” function implements the above operation splitting theoriginal image into patches and storing them into an array. Let’s callthis array “patches_array”.

The function “processCandidateImages” reads the image files, resizesthem and stores them into an array. The size for each candidate imageis the same as for the original image patch.

Then, after all the inputs are read and processed the function“GenerateMosaic” is called.

GenerateMosaic function for each original image patch finds the bestmatching candidate image using one of the techniques discussed belowand stores it into the array.
Basically the function maps eachoriginal image patch from the “pathes_arras” into the correspondingbest matching candidate image from the “candidates_array”.
“candidates_array” is then fed into “CreateMosaicImage” function which embeds each image from the array into the final image row by row (i.e.conducts the process opposite to the one that was used for splittingthe original image)
