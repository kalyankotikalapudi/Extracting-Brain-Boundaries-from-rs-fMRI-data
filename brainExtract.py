import numpy as np
import cv2
import shutil
import os


def files(cwd = os.getcwd()):
	
	if (os.path.exists('./Slices')==True):
		shutil.rmtree('./Slices')
	
	if (os.path.exists('./Boundaries')==True):
		shutil.rmtree('./Boundaries')
	for i in os.listdir(os.path.join(cwd,"testPatient")):
		if("thresh" in i ):
			slices_boundaries(os.path.join(cwd,"testPatient"),i)


def draw_box(contour,img_file,img_path):
       index = 1
       read_img = cv2.imread(os.path.join(img_path,img_file))
       x_coord1, y_coord1, z_coord1, z_coord2 = cv2.boundingRect(contour[len(contour)-1])
       for i in range(1,len(contour)):
         x_coord2,y_coord2,z_coord1,z_coord2 = cv2.boundingRect(contour[len(contour)-i-1])
         if(y_coord2 != y_coord1 and abs(y_coord2-y_coord1) > z_coord1):
			                  break
       for i in range(1,len(contour)):
         x_coord3, y_coord3, z_coord1, z_coord2 = cv2.boundingRect(contour[len(contour)-i-1])
         if(x_coord3 != x_coord1 and abs(x_coord3-x_coord1) > z_coord2):
               break
	
       x_coord4, y_coord4, z_coord1, z_coord2 = cv2.boundingRect(contour[-1])
       w = x_coord3 - x_coord1
       h = y_coord2 - y_coord1
	
       contour_len=len(contour)
       for i in range(0,contour_len):
              array = contour[contour_len - i-1]
              x_coord1, y_coord1, z_coord1, z_coord2 = cv2.boundingRect(array)
		
		
              x_coord2 = x_coord1+w-z_coord1
              y_coord2 = y_coord1-h
              x_coord1 = x_coord1 + z_coord1+z_coord1
              y_coord1 = y_coord1 + z_coord2
              
              img = read_img[y_coord2:y_coord1, x_coord1:x_coord2]	
              
              if(x_coord1 <x_coord4 or y_coord2 < y_coord4):
                        continue
              
              img = read_img[y_coord2:y_coord1, x_coord1:x_coord2]	
              gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
              thresh_img=cv2.inRange(gray_img,0,25)
              edge_img = cv2.Canny(thresh_img, 50, 100)
              (contours, _) = cv2.findContours(edge_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
              contours_len=len(contours)
              if(contours_len):
                       img = read_img[y_coord2:y_coord1, x_coord1:x_coord2]
                       cv2.imwrite(os.path.join(os.path.join(os.getcwd(),"Slices"),
                       img_file.split('.')[0])+'/'+"slice"+str(index) +'.png'
                       , img)
                       cv2.drawContours(img, contours, -1, (0,0,255), 1)
                       cv2.imwrite(os.path.join(os.path.join(os.getcwd(),"Boundaries"),
                       img_file.split('.')[0])+'/'+"bound"+str(index) +'.png', 
                       img)

              else:
                       continue
              index = index + 1

def split(img_path,img_file):
     if(os.path.exists('./Slices')==False):
          os.mkdir('./Slices')
     if(os.path.exists(os.path.join('./Slices',img_file.split('.')[0]))==False):
          os.mkdir(os.path.join('./Slices',img_file.split('.')[0]))
		
	
     if(os.path.exists('./Boundaries')==False):
          os.mkdir('./Boundaries')
	
     if(os.path.exists(os.path.join('./Boundaries',img_file.split('.')[0]))==False):
          os.mkdir(os.path.join('./Boundaries',img_file.split('.')[0]))
          
          

def slices_boundaries(img_path,img_file):
	
	
	split(img_path,img_file)
	read_img = cv2.imread(os.path.join(img_path,img_file))
	gray_img=cv2.cvtColor(read_img,cv2.COLOR_BGR2GRAY)
	thresh_img=cv2.inRange(gray_img,255,255)
	edge_img = cv2.Canny(thresh_img, 255, 255)
	(contours, _) = cv2.findContours(edge_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	
	draw_box(contours, img_file,img_path)




