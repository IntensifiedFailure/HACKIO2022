
from PIL import Image

# Import an image from directory:
input_image = Image.open("advanced_test_1.png")
  
# Extracting pixel map:
pixel_map = input_image.load()
  
# Extracting the width and height 
# of the image:
width, height = input_image.size

# expected rgb values
er, eg, eb = 190, 57, 214
# allowed error
e = 20

top_pixel = height
bottom_pixel = 0
left_pixel = width
right_pixel = 0

corners = [[], [], [], []]

print(er, eg, eb, e)
print(width, "x", height)
# taking half of the width:
for i in range(width):
    for j in range(height):
        
        # getting the RGB pixel value.
        r, g, b = input_image.getpixel((i, j))
          
        if (abs(r-er)+abs(b-eb)+abs(g-eg)<3*e):
            r, g, b = 255, 255, 255
            s, t, u = 0, 255, 0
            if j > bottom_pixel:
                bottom_pixel = j
            elif j < top_pixel:
                top_pixel = j
            if i > right_pixel:
                right_pixel = i
            elif i < left_pixel:
                left_pixel = i
        else:
             s, t, u = 0, 0, 0
             r, g, b = r-1, g, b
        
            # setting the pixel value.
        pixel_map[i, j] = (r, g, b)
print("Extreme Pixels located")

extreme_pixels = [[top_pixel, bottom_pixel],[left_pixel, right_pixel]]
for i in range(width):
    for j in range(len(extreme_pixels[0])):
        r, g, b = input_image.getpixel((i, extreme_pixels[0][j]))
        if(r == 255):
            corners[2*j+1].append([i, extreme_pixels[0][j]])
        else:
            pixel_map[i, extreme_pixels[0][j]] = (128,128,128)
for j in range(height):
    for i in range(len(extreme_pixels[1])):
        r, g, b = input_image.getpixel((extreme_pixels[1][i], j))
        if(r == 255):
            corners[2*i].append([extreme_pixels[1][i], j])
        else:
            pixel_map[extreme_pixels[1][i], j] = (128,128,128)
print("corner data:")
print(corners[0])
print(corners[1])
print(corners[2])
print(corners[3])

r,g,b = 0, 0, 255
lines = []
for i in range(len(corners)):
    xone = corners[i][(len(corners[i])-1)*(round(i/2+0.01)%2)][0]
    xtwo = corners[(i+1)%4][(len(corners[(i+1)%4])-1)*(round((i-1)/2+0.01)%2)][0]
    yone = corners[i][(len(corners[i])-1)*(round((i-1)/2+0.01)%2)][1]
    ytwo = corners[(i+1)%4][(len(corners[(i+1)%4])-1)*(round(i/2+0.01)%2)][1]
    lines.append((ytwo-yone)/(xtwo-xone))
    print("iteration", i, "index = ",round((i-1)/2+0.01)%2)
    print("slope", i, ": ", lines[i])

adjusted_corners = []
# d is the adjustment for edge pixels not caught in the initial imaging
d = 3
for i in range(width):
    for j in range(height):
        s, t, u = input_image.getpixel((i, j))
        # getting the RGB pixel value.
        r, g, b = 128, 128, 128
        if (s != 255):  
            if(j-corners[0][0][1] == round(lines[0]*(i-corners[0][0][0]))-d):
                pixel_map[i, j] = (r,g,b)
            elif(j-corners[1][len(corners[1])-1][1] == round(lines[1]*(i-corners[1][len(corners[1])-1][0]))-d):
                pixel_map[i, j] = (r,g,b)
            elif(j-corners[2][len(corners[2])-1][1] == round(lines[2]*(i-corners[2][len(corners[2])-1][0]))+d):
                pixel_map[i, j] = (r,g,b)
            elif(j-corners[3][0][1] == round(lines[3]*(i-corners[3][0][0]))+d):
                pixel_map[i, j] = (r,g,b)
print("slanted guidelines drawn")
adjusted_corners = []
coefficient = [-1, -1, 1, 1]
for i in range(len(corners)):
    index1 = (len(corners[i])-1)*(round(i/2+0.01)%2)
    index2 = (len(corners[(i+1)%4])-1)*(round((i+1)/2+0.01)%2)
    print("Indices: ", index1, index2)
    m1 = lines[i]
    m2 = lines[(i+1)%4]
    x1 = corners[i][index1][0]
    x2 = corners[(i+1)%4][index2][0]
    y1 = corners[i][index1][1]+coefficient[i]*d
    y2 = corners[(i+1)%4][index2][1]+coefficient[(i+1)%4]*d
    x = round((m1*x1 - m2*x2 + y2 - y1)/(m1 - m2))
    y = round(m1*(x-x1))+y1
    adjusted_corners.append([x,y])
    print(adjusted_corners[i])
print("image 1f saving")
# Saving the final output
input_image.save("advanced_test_1f", format="png")
print("image 1f saved")

# Calculate object height and width
o_height = bottom_pixel-top_pixel
o_width = right_pixel-left_pixel

print("top:", top_pixel, "bottom:", bottom_pixel, "left:", left_pixel, "right:", right_pixel)
print("height:", o_height, "width:", o_width)
print("corner 1:", corners[0])
print("corner 2:", corners[1])
print("corner 3:", corners[2])
print("corner 4:", corners[3])
# use input_image.show() to see the image on the
# output screen.
input_image.show()
print("image 1ff processing:")
for i in range(width):
    for j in range(height):
        # getting the RGB pixel value.
        r, g, b = input_image.getpixel((i, j))
        if (r == 255):
            r, g, b = 0, 255, 0
        elif (r == 128 and g == 128 and b == 128):
            r, g, b = r, g, b
        else:
            r, g, b = 0, 0, 0
        pixel_map[i, j] = (r,g,b)
for k in adjusted_corners:
    pixel_map[k[0],k[1]] = (255, 255, 255)

print("corners drawn")
subbox = []

for j in range(o_height):
    switch = 0
    line = []
    for i in range(o_width):
        x = i + left_pixel
        y = j + top_pixel
        r, g, b = input_image.getpixel((x, y))
        if (g == 255 and switch == 0):
            switch = 1
        elif (g != 255 and (switch == 1 or switch == 2)):
            switch = 2
            line.append([x,y])
        elif (g == 255 and switch == 2):
            subbox.append(line)
            line = []
print("subbox pixels collated")

count = 0
x_sum = 0
y_sum = 0
for i in range(len(subbox)):
    for j in range(len(subbox[i])):
        count += 1
        x_sum += subbox[i][j][0]
        y_sum += subbox[i][j][1]
        pixel_map[subbox[i][j][0], subbox[i][j][1]] = (0,0,255)

subbox_center_x = round(x_sum/count)
subbox_center_y = round(y_sum/count)
print(subbox_center_x, subbox_center_y)

for i in range(width):
    pixel_map[i, subbox_center_y] = (255,0,0)
for j in range(height):
    pixel_map[subbox_center_x, j] = (255,0,0)

subbox_rc_x = (subbox_center_x-left_pixel)/o_width
subbox_rc_y = (subbox_center_y-top_pixel)/o_height
relative_corners = []
d_to_key_corner = 2
key_corner = []
for i in adjusted_corners:
    relative_corners.append([(i[0]-left_pixel)/o_width,(i[1]-top_pixel)/o_height])
    distance = (subbox_rc_x-(i[0]-left_pixel)/o_width)**2 + (subbox_rc_y-(i[1]-top_pixel)/o_height)**2
    if (distance < d_to_key_corner):
        d_to_key_corner = distance
        key_corner = i
print("key corner located")
for i in range(width):
    pixel_map[i, key_corner[1]] = (0,0,255)
for j in range(height):
    pixel_map[key_corner[0], j] = (0,0,255)

print("subbox guidelines drawn")
print("saving image 1ff")

input_image.save("advanced_test_1ff", format="png")
input_image.show()
