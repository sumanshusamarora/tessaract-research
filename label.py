import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from os import listdir
from os.path import isfile, join
import pandas as pd
import sys
# Create a function based on a CV2 Event (Left button click)
class image_annotation:
    def __init__(self, folder_path:str = ""):
        if folder_path == '':
            self.folder_path = sys.path[len(sys.path)-1] + "\\Data"
        else:
            self.folder_path = folder_path
        self.image_name = ""
        self.pt1 = (0,0)
        self.pt2 = (0,0)
        self.topLeft_clicked = False
        self.botRight_clicked = False
        self.pts_list = []
        self.pts_list_final = []
        self.pts_dict = dict()
        self.annotated_df = pd.DataFrame()
        
    # mouse callback function
    def draw_rectangle(self, event,x,y,flags,param):
        # get mouse click
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.topLeft_clicked == True and self.botRight_clicked == True:
                self.topLeft_clicked = False
                self.botRight_clicked = False
                self.pt1 = (0,0)
                self.pt2 = (0,0)
    
            if self.topLeft_clicked == False:
                self.pt1 = (x,y)
                self.pts_list.append(self.pt1)
                self.topLeft_clicked = True
                
            elif self.botRight_clicked == False:
                self.pt2 = (x,y)
                self.pts_list.append(self.pt2)
                self.botRight_clicked = True
    
    def annotate_by_image(self, image_name:str = ""):
        self.pt1 = (0,0)
        self.pt2 = (0,0)
        self.topLeft_clicked = False
        self.botRight_clicked = False
        self.pts_list = []
        self.pts_list_final = []
        self.pts_dict = dict()
        self.image_name = image_name
        # Haven't drawn anything yet!        
    
        img = cv2.imread(os.path.join(self.folder_path, self.image_name))
        # Create a named window for connections
        cv2.namedWindow(winname=self.image_name)
        # Connects the mouse button to our callback function
        cv2.setMouseCallback(self.image_name,self.draw_rectangle)
        while True: #Runs forever until we break with Esc key on keyboard
            # Shows the image window
            cv2.imshow(self.image_name,img)
            if self.topLeft_clicked:
                cv2.circle(img, center=self.pt1, radius=5, color=(0,0,255), thickness=-1)
            #drawing rectangle
            if self.topLeft_clicked and self.botRight_clicked:
                cv2.rectangle(img, self.pt1, self.pt2, (0, 0, 255), 2)
            # EXPLANATION FOR THIS LINE OF CODE:
            # https://stackoverflow.com/questions/35372700/whats-0xff-for-in-cv2-waitkey1/39201163
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Once script is done, its usually good practice to call this line
        # It closes all windows (just in case you have multiple windows called)
        cv2.destroyAllWindows()
        for i in range(0,len(self.pts_list),2):
            self.pts_list_final.append([self.pts_list[i], self.pts_list[i+1]])
            
        return self.pts_list_final
    
    def annotate_by_folder(self):
        print("Exttacting images from folder - "+self.folder_path)
        self.pts_dict = dict()
        onlyimagefiles = [f for f in listdir(self.folder_path) if isfile(join(self.folder_path, f)) and os.path.splitext(f)[len(os.path.splitext(f))-1] in ['.png','.jpg','.jpeg','.gif']]                
        for image_name in onlyimagefiles:
            self.pt1 = (0,0)
            self.pt2 = (0,0)
            self.topLeft_clicked = False
            self.botRight_clicked = False
            self.pts_list = []
            self.pts_list_final = []
            self.image_name = image_name
            # Haven't drawn anything yet!
            self.pt1 = (0,0)
            self.pt2 = (0,0)
            self.topLeft_clicked = False
            self.botRight_clicked = False
            
        
            img = cv2.imread(os.path.join(self.folder_path, self.image_name))
            # Create a named window for connections
            cv2.namedWindow(winname=self.image_name)
            # Connects the mouse button to our callback function
            cv2.setMouseCallback(self.image_name,self.draw_rectangle)
            while True: #Runs forever until we break with Esc key on keyboard
                # Shows the image window
                cv2.imshow(self.image_name,img)
                if self.topLeft_clicked:
                    cv2.circle(img, center=self.pt1, radius=5, color=(0,0,255), thickness=-1)
                #drawing rectangle
                if self.topLeft_clicked and self.botRight_clicked:
                    cv2.rectangle(img, self.pt1, self.pt2, (0, 0, 255), 2)
                # EXPLANATION FOR THIS LINE OF CODE:
                # https://stackoverflow.com/questions/35372700/whats-0xff-for-in-cv2-waitkey1/39201163
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            # Once script is done, its usually good practice to call this line
            # It closes all windows (just in case you have multiple windows called)
            cv2.destroyAllWindows()
            for i in range(0,len(self.pts_list),2):
                self.pts_list_final.append([self.pts_list[i], self.pts_list[i+1]])
            self.pts_dict[image_name] = self.pts_list_final
                
        return self.pts_dict
    
    def save_to_excel(self, file_location:str="", file_name:str="ImageAnnotation.xlsx"):
        if len(self.pts_dict) == 0:
            raise TypeError("Annotation dictionary empty, please run annotate_by_folder function first")
            
        elif os.path.splitext(file_name)[len(os.path.splitext(file_name))-1] not in ['.xlsx','.xls']:
                raise TypeError("Provided file name is not valid, please provide valid excel extension")
        else:
            if file_location == "":
                file_location = "\\".join(self.folder_path.split("\\")[:len(self.folder_path.split("\\"))-1]) + "\\Annotated Files"
                
            pts_dict_keys = list(self.pts_dict.keys())
            pts_dict_values = list(self.pts_dict.values())
            self.annotated_df = pd.DataFrame(columns=["Image Name", "Co-ordinates"])
            self.annotated_df["Image Name"] = pts_dict_keys
            self.annotated_df["Co-ordinates"] = pts_dict_values
            self.annotated_df.to_excel(os.path.join(file_location, file_name))
            print("Excel with annotated data saved at location - " + os.path.join(file_location, file_name))
