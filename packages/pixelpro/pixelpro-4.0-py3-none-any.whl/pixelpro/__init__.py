def index():
    print("""

1)  WAP to demonstrate the following aspects of signal processing on suitable data.
1a) Upsampling and downsampling on Image/speech signal
1b) Fast Fourier Transform to compute DFT

2) WAP to perform Convolution and correlation of gray scale image.

3) WAP to perform the DFT of 4x4 Gray Scale Image

4)  Write program to implement point/pixel intensity transformations such as:
4a) Log and Power-law transformations
4b) Contrast adjustments
4c) Histogram equalization
4d) Thresholding, and halftoning operations

5) WAP to apply various enhancements on images using image derivatives 
   by implementing Gradient and Laplacian operations.

6) WAP to apply various image enhancement using image derivatives by 
   implementing smoothing, sharpening, and unsharp masking filters.

7) WAP to Apply edge detection techniques such as Sobel and Canny 
   to extract meaningful information

8) WAP to implement various morphological image processing techniques.

9) Image Segmentation.   

          """)
          



def prog(num):
    if(num=="1a"):
        print(""" 

import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

img1 = cv2.imread("my native place.jpg", 0)
[m, n] = img1.shape

print('Image Shape:', m, n)
print('Original Image:')
plt.imshow(img1, cmap="gray")
plt.show()

f = 4

# Down sample
img2 = np.zeros((m // f, n // f), dtype=int)

for i in range(0, m, f):
    for j in range(0, n, f):
        try:
            img2[i // f][j // f] = img1[i][j]
        except IndexError:
            pass

print('Down Sampled Image:')
plt.imshow(img2, cmap="gray")
plt.show()

# Up sample
img3 = np.zeros((m - 1, n - 1), dtype=int)

for i in range(0, m - 1, f):
    for j in range(0, n - 1, f):
        try:
            img3[i, j] = img2[i // f][j // f]
        except IndexError:
            pass

for i in range(1, m - (f - 1), f):
    for j in range(0, n - (f - 1)):
        img3[i:i + (f - 1), j] = img3[i - 1, j]

for i in range(0, m - 1):
    for j in range(1, n - 1, f):
        img3[i, j:j + (f - 1)] = img3[i, j - 1]

print('Up Sampled Image:')
plt.imshow(img3, cmap="gray")
plt.show()

              """) 

        
    elif(num=="1b"):
        print("""

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from skimage.metrics import normalized_root_mse

im = Image.open('elephant.PNG').convert('L')
im = np.array(im)
freq = np.fft.fft2(im)
im1 = np.fft.ifft2(freq).real
snr = normalized_root_mse(im, im1)
print('SNR for the image obtained after reconstruction =', snr)
assert np.allclose(im, im1)

plt.figure(figsize=(20, 10))
plt.subplot(121), plt.imshow(im, cmap='gray'), plt.axis('off')
plt.title('Original Image', size=20)
plt.subplot(122), plt.imshow(im1, cmap='gray'), plt.axis('off')
plt.title('Image Obtained After Reconstruction', size=20)
plt.show()

                """)
        

    elif(num=="2"):
        print("""

import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("my native place.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

fig, ax = plt.subplots(1, figsize=(12, 8))
plt.imshow(image)
plt.show()

abc = np.ones((3, 3))
kernel = np.ones((3, 3), np.float32) / 9
img = cv2.filter2D(image, -1, kernel)

fig, ax = plt.subplots(1, 2, figsize=(10, 6))
ax[0].imshow(image)
ax[1].imshow(img)
plt.show()

kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])

img = cv2.filter2D(image, -1, kernel)

fig, ax = plt.subplots(1, 2, figsize=(10, 6))
ax[0].imshow(image)
ax[1].imshow(img)
plt.show()

                """)


    elif(num=="3"):
        print("""

import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread("puppy.jpg", 0)
rows, cols = img.shape
optimalRows = cv2.getOptimalDFTSize(rows)
optimalCols = cv2.getOptimalDFTSize(cols)
optimalImg = np.zeros((optimalRows, optimalCols))
optimalImg[:rows, :cols] = img
dft = cv2.dft(np.float32(optimalImg), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)
f_complex = dft_shift[:, :, 0] + 1j * dft_shift[:, :, 1]
f_abs = np.abs(f_complex) + 1  # lie between 1 and 1e6
f_bounded = 20 * np.log(f_abs)
f_img = 255 * f_bounded / np.max(f_bounded)
f_img = f_img.astype(np.uint8)
i_shift = np.fft.ifftshift(dft_shift)
result = cv2.idft(i_shift)
result = cv2.magnitude(result[:, :, 0], result[:, :, 1])
images = [optimalImg, f_img, result]
imageTitles = ['Input image', 'DFT', 'Reconstructed image']

for i in range(len(images)):
    plt.subplot(1, 3, i + 1)
    plt.imshow(images[i], cmap='gray')
    plt.title(imageTitles[i])
    plt.xticks([])
    plt.yticks([])

plt.show()
cv2.waitKey()
cv2.destroyAllWindows()
        
                """)


    elif(num=="4a"):
        print("""

# Log and Power-law transformations
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("camera_sample.jpg")

# Apply log transform.
c = 255 / (np.log(1 + np.max(img)))
log_transformed = c * np.log(1 + img)

# Specify the data type.
log_transformed = np.array(log_transformed, dtype=np.uint8)

# Save the output.
cv2.imwrite('log_transformed.jpg', log_transformed)

plt.imshow(img)
plt.show()

plt.imshow(log_transformed)
plt.show()

# Open the image.
img2 = cv2.imread("camera_sample.jpg")
plt.imshow(img2)
plt.show()

# Trying 4 gamma values.
for gamma in [0.1, 0.5, 1.2, 2.2, 5]:
    # Apply gamma correction.
    gamma_corrected = np.array(255 * (img2 / 255) ** gamma, dtype='uint8')
    cv2.imwrite('gamma_transformed' + str(gamma) + '.jpg', gamma_corrected)

    plt.imshow(gamma_corrected)
    plt.show()

                """)



    elif(num=="4b"):
        print(""" 

# Contrast adjustments
import numpy as np
from skimage.io import imread
from skimage.color import rgb2gray
from skimage import data, img_as_float, img_as_ubyte, exposure, io, color
from PIL import Image, ImageEnhance, ImageFilter
from scipy import ndimage, misc
import matplotlib.pyplot as pylab
import cv2

def plot_image(image, title=""):
    pylab.title(title, size=10)
    pylab.imshow(image)
    pylab.axis('off')

def plot_hist(r, g, b, title=""):
    r, g, b = img_as_ubyte(r), img_as_ubyte(g), img_as_ubyte(b)
    pylab.hist(np.array(r).ravel(), bins=256, range=(0, 256), color='r', alpha=0.3)
    pylab.hist(np.array(g).ravel(), bins=256, range=(0, 256), color='g', alpha=0.3)
    pylab.hist(np.array(b).ravel(), bins=256, range=(0, 256), color='b', alpha=0.3)
    pylab.xlabel('Pixel Values', size=20)
    pylab.ylabel('Frequency', size=20)
    pylab.title(title, size=10)

im = Image.open("marigold.jpg")
im_r, im_g, im_b = im.split()

pylab.style.use('ggplot')
pylab.figure(figsize=(15, 5))
pylab.subplot(121)
plot_image(im)
pylab.subplot(122)
plot_hist(im_r, im_g, im_b)
pylab.show()

def contrast(c):
    return 0 if c < 50 else (255 if c > 150 else int((255 * c - 22950) / 48))

imc = im.point(contrast)
im_rc, im_gc, im_bc = imc.split()

pylab.style.use('ggplot')
pylab.figure(figsize=(15, 5))
pylab.subplot(121)
plot_image(imc)
pylab.subplot(122)
plot_hist(im_rc, im_gc, im_bc)
pylab.yscale('log')
pylab.show()

        """)

    
    elif(num=="4c"):
        print("""

# Histogram equalization
import cv2
from matplotlib import pyplot as plt

img = cv2.imread("puppy.jpg", 0)
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
eq = cv2.equalizeHist(img)
cdf = hist.cumsum()
cdfnmhist = cdf * hist.max() / cdf.max()
histeq = cv2.calcHist([eq], [0], None, [256], [0, 256])
cdfeq = histeq.cumsum()
cdfnmhisteq = cdfeq * histeq.max() / cdf.max()

plt.subplot(221), plt.imshow(img, 'gray')
plt.subplot(222), plt.plot(hist), plt.plot(cdfnmhist)
plt.subplot(223), plt.imshow(eq, 'gray')
plt.subplot(224), plt.plot(histeq), plt.plot(cdfnmhisteq)
plt.xlim([0, 256])
plt.show()

                """)



    elif(num=="4d"):
        print("""

# Thresholding, and halftoning operations 
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread("sunflower.jpg", 0)
ret, thresh1 = cv.threshold(img, 127, 255, cv.THRESH_BINARY)
ret, thresh2 = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
ret, thresh3 = cv.threshold(img, 127, 255, cv.THRESH_TRUNC)
ret, thresh4 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO)
ret, thresh5 = cv.threshold(img, 127, 255, cv.THRESH_TOZERO_INV)

titles = ['Original Image', 'BINARY', 'BINARY_INV', 'TRUNC', 'TOZERO', 'TOZERO_INV']
images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

for i in range(6):
    plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray', vmin=0, vmax=255)
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])

plt.show()

                """)



    elif(num=="5"):
        print(""" 
import numpy as np
from scipy import signal, misc, ndimage
from skimage import filters, feature, img_as_float
from skimage.io import imread
from skimage.color import rgb2gray
from PIL import Image, ImageFilter
import matplotlib.pylab as pylab
from skimage.transform import rescale


def plot_image(image, title=""):
    pylab.title(title, size=20)
    pylab.imshow(image)
    pylab.axis('off')


def plot_hist(r, g, b, title=""):
    r, g, b = img_as_ubyte(r), img_as_ubyte(g), img_as_ubyte(b)
    pylab.hist(np.array(r).ravel(), bins=256, range=(0, 256), color='r', alpha=0.3)
    pylab.hist(np.array(g).ravel(), bins=256, range=(0, 256), color='g', alpha=0.3)
    pylab.hist(np.array(b).ravel(), bins=256, range=(0, 256), color='b', alpha=0.3)
    pylab.xlabel('Pixel Values', size=20)
    pylab.ylabel('Frequency', size=20)
    pylab.title(title, size=10)


ker_x = [[-1, 1]]
ker_y = [[-1], [1]]

im = rgb2gray(imread("sunflower.jpg"))
im_x = signal.convolve2d(im, ker_x, mode='same')
im_y = signal.convolve2d(im, ker_y, mode='same')
im_mag = np.sqrt(im_x**2 + im_y**2)
im_dir = np.arctan(im_y / im_x)

pylab.gray()
pylab.figure(figsize=(30, 20))
pylab.subplot(231)
plot_image(im, 'Original')
pylab.subplot(232)
plot_image(im_x, 'Gradient_x')
pylab.subplot(233)
plot_image(im_y, 'Gradient_y')
pylab.subplot(234)
plot_image(im_mag, '||Gradient||')
pylab.subplot(235)
plot_image(im_dir, r'$\theta$')
pylab.subplot(236)
pylab.plot(range(im.shape[1]), im[0, :], 'b-', label=r'$f(x,y)|_{x=0}$', linewidth=5)
pylab.plot(range(im.shape[1]), im_x[0, :], 'r-', label=r'$grad_x (f(x,y))|_{x=0}$')
pylab.title(r'$grad_x (f(x,y))|_{x=0}$', size=30)
pylab.legend(prop={'size': 20})
pylab.show()

# LAPLACIAN

ker_laplacian = [[0, -1, 0],
                 [-1, 4, -1],
                 [0, -1, 0]]

im = rgb2gray(imread("sunflower.jpg"))
im1 = np.clip(signal.convolve2d(im, ker_laplacian, mode='same'), 0, 1)

pylab.gray()
pylab.figure(figsize=(20, 10))
pylab.subplot(121)
plot_image(im, 'Original')
pylab.subplot(122)
plot_image(im1, 'Laplacian Convolved')
pylab.show()

        """)
    
    
    elif(num=="6"):
        print("""

import numpy as np
from scipy import ndimage
from skimage import img_as_float
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.filters import laplace
import matplotlib.pylab as pylab



def plot_image(image, title=""):
    pylab.title(title, size=10)
    pylab.imshow(image)
    pylab.axis('off')


# sharpening of images
im = rgb2gray(imread('windows.jpg'))
im1 = np.clip(laplace(im) + im, 0, 1)

pylab.figure(figsize=(10, 15))
pylab.subplot(121)
plot_image(im, 'Original Image')
pylab.subplot(122)
plot_image(im1, 'Sharpened Image')
pylab.tight_layout()
pylab.show()


# UNSHARP MASKING
def rgb2gray(im):
    return np.clip(0.2989 * im[..., 0] + 0.5870 * im[..., 1] + 0.1140 * im[..., 2], 0, 1)


im = rgb2gray(img_as_float(imread('windows.jpg')))
im_blurred = ndimage.gaussian_filter(im, 3)
im_detail = np.clip(im - im_blurred, 0, 1)

pylab.gray()
fig, axes = pylab.subplots(nrows=2, ncols=3, sharex=True, sharey=True, figsize=(15, 15))
axes = axes.ravel()

axes[0].set_title('Original Image', size=15)
axes[0].imshow(im)

axes[1].set_title('Blurred Image, sigma=5', size=15)
axes[1].imshow(im_blurred)

axes[2].set_title('Detail Image', size=15)
axes[2].imshow(im_detail)

alpha = [1, 5, 10]

for i in range(3):
    im_sharp = np.clip(im + alpha[i] * im_detail, 0, 1)
    axes[3 + i].imshow(im_sharp)
    axes[3 + i].set_title('Sharpened Image, alpha=' + str(alpha[i]), size=15)

for ax in axes:
    im_sharp = np.clip(im + alpha[i] * im_detail, 0, 1)
    axes[2].imshow(im_sharp)
    axes[2].set_title('Sharpened Image', size=15)
    ax.axis('off')

fig.tight_layout()
pylab.show()
        
                """)



    elif(num=="7"):
        print("""

                """)



    elif(num=="8"):
        print("""
 
                """)




    elif(num=="9"):
        print("""


                """)




    else:
        print("invalid input")



