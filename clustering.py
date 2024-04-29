import cv2
import numpy as np
import os
import shutil
import csv
from sklearn import cluster



def files(cwd = os.getcwd()):
	
	if (os.path.exists('./Slices')==True):
		shutil.rmtree('./Slices')
	
	if (os.path.exists('./Clusters')==True):
		shutil.rmtree('./Clusters')
	for i in os.listdir(os.path.join(cwd,"testPatient")):
		if("thresh" in i ):
			slices_clusters(os.path.join(cwd,"testPatient"),i)


def draw_box(contour,img_file,img_path):
       index = 1
       extra=0
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
       image = cv2.imread(os.path.join(img_path,img_file))
       contour_len=len(contour)
       for i in range(0,contour_len):
              array = contour[contour_len - i-1]
              x_coord1, y_coord1, z_coord1, z_coord2 = cv2.boundingRect(array)
		
		
              x_coord2 = x_coord1+w-z_coord1
              y_coord2 = y_coord1-h+extra
              x_coord1 = x_coord1 + z_coord1+z_coord1
              y_coord1 = y_coord1 + z_coord2+extra
              
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
                       cv2.imwrite(os.path.join(os.path.join(os.getcwd(),"Slices"),img_file.split('.')[0])+'/'+str(index) +'.png', img)
                       img_path = os.path.join(os.path.join(os.getcwd(),"Slices"),img_file.split('.')[0])
                       indx = index
                       csvfile =os.path.join(os.path.join(os.path.join(os.getcwd(),"Clusters"),img_file.split('.')[0]),img_file.split('.')[0]+str(".csv"))
                       dbscan(img_file, img_path, indx,csvfile)

              else:
                       continue
              index = index + 1

	

def dbscan(img_file, img_path,indx,csvfile):

	read_img = cv2.imread(os.path.join(img_path,str(indx)+".png"))
	hsv_img = cv2.cvtColor(read_img, cv2.COLOR_BGR2HSV)
	rem_disturb = cv2.inRange(hsv_img, (0, 0, 0), (0, 0, 255))
	img = cv2.imread(os.path.join(img_path,str(indx)+".png")) 
	img[np.where(rem_disturb)] = 0
	gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	(_,thresh)=cv2.threshold(gray_img, 1, 255,cv2.THRESH_BINARY)
	height , width = gray_img.shape
	values = []
	for i in range(height):
		for j in range(width):
			if(gray_img[i,j]):
				values.append([i,j])
	img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
	img[np.where(thresh)] = [0,191,0]
	if(len(values)>0):	
		dbscan = cluster.DBSCAN(eps = 1.5, n_jobs=100).fit(values)
		_, count = np.unique(dbscan.labels_[dbscan.labels_>=0], return_counts=True)
		counts= 0
		for i in count:
			if(i>135):
				counts = counts+1
	else:
		counts = 0
	cv2.imwrite(os.path.join(os.path.join(os.getcwd(),"Clusters"),img_file.split('.')[0])+'/'+str(indx) +'.png', img)
	f = open(csvfile,'a')
	writer = csv.writer(f)
	writer.writerow([indx,counts])
	f.close()


def split(img_path,img_file):
     if(os.path.exists('./Slices')==False):
          os.mkdir('./Slices')
     if(os.path.exists(os.path.join('./Slices',img_file.split('.')[0]))==False):
          os.mkdir(os.path.join('./Slices',img_file.split('.')[0]))
		
	
     if(os.path.exists('./Clusters')==False):
          os.mkdir('./Clusters')
	
     if(os.path.exists(os.path.join('./Clusters',img_file.split('.')[0]))==False):
          os.mkdir(os.path.join('./Clusters',img_file.split('.')[0]))
          header = ["SliceNumber","ClusterCount"]
          f = open(os.path.join(os.path.join(os.path.join(os.getcwd(),"Clusters"),img_file.split('.')[0]),img_file.split('.')[0]+str(".csv")),'w')
          writer = csv.writer(f)
          writer.writerow(header)
          f.close()
          

def slices_clusters(img_path,img_file):
	
	
     split(img_path,img_file)
     read_img = cv2.imread(os.path.join(img_path,img_file))
     gray_img=cv2.cvtColor(read_img,cv2.COLOR_BGR2GRAY)
     thresh_img=cv2.inRange(gray_img,255,255)
     edge_img = cv2.Canny(thresh_img, 255, 255)
     (contours, _) = cv2.findContours(edge_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	
     draw_box(contours, img_file,img_path)
     
     



