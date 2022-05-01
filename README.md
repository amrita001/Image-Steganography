# Image-Steganography
Hides some data into an Image, and can successfully decode the same data from that image.

### Encryption Algorithm used : Least Significant Bit Technique (LSB)
In LSB Technique, we hide the data in the image by modifying the rightmost bit which is the least significant bit of the pixels in the image. This helps us dealing with the resolution of the image. The resolution does not vary on a larger scale, hence the difference between the original image and encoded image is very minimal. The program creates a copy of the image, hides the data in that copy by manipulating the righmost bits and saves the encoded image in user's choice of path with user's choice of name.

#### User just needs to provide :
  - cover image to hide data
  - data 
  - name of the final encoded image
  - path where final image will be stored


#### Aim of this project -

  :black_medium_small_square:  To provide secure communication

  :black_medium_small_square:  Hiding confidential or sensitive information in an Image


#### The User-Interface is -

  :heavy_check_mark: interactive 

  :heavy_check_mark: user-friendly

  :heavy_check_mark: deals with all test cases

  :heavy_check_mark: shows pop-up dialogue boxes in case of any error
