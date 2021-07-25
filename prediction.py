# -*- coding: utf-8 -*-
"""facenet_svm_test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16BKx4PJaS3YJ2NQzXRv7rcifgFpswcWU
"""

import json
from mtcnn.mtcnn import MTCNN
import numpy as np
from PIL import Image
import pickle
from keras.models import load_model

def get_embedding(model, face_pixels):
	# scale pixel values
	face_pixels = face_pixels.astype('float32')
	# standardize pixel values across channels (global)
	mean, std = face_pixels.mean(), face_pixels.std()
	face_pixels = (face_pixels - mean) / std
	# transform face into one sample
	samples = np.expand_dims(face_pixels, axis=0)
	# make prediction to get embedding
	yhat = model.predict(samples)
	return yhat[0]



def predict(fname):

        # Commented out IPython magic to ensure Python compatibility.
        # Test với 1 ảnh
        #test_img = "data/test/Tran Canh Xuan B1706970.jpg"

        # %cd /content/drive/My\ Drive/Colab\ Notebooks/who

        facenet_model = load_model('facenet_keras.h5')
        detector = MTCNN()
        dest_size = (160, 160)

        # Load SVM model từ file
        pkl_filename = 'faces_svm.pkl'
        with open(pkl_filename, 'rb') as file:
            pickle_model = pickle.load(file)

        # Load ouput_enc từ file để hiển thị nhãn
        pkl_filename = 'output_enc.pkl'
        with open(pkl_filename, 'rb') as file:
            output_enc = pickle.load(file)

        try:

            # Detect khuôn mặt
            image = Image.open(fname)
            image = image.convert('RGB')
            pixels = np.asarray(image)
            results = MTCNN().detect_faces(pixels)    

            if len(results) > 0:
                x1, y1, width, height = results[0]['box']
                x1, y1 = abs(x1), abs(y1)
                x2, y2 = x1 + width, y1 + height
                face = pixels[y1:y2, x1:x2]
                image = Image.fromarray(face)
                image = image.resize(dest_size)

                # Lây face embeding
                face_emb =  get_embedding(facenet_model, np.array(image))
                # Chuyển thành tensor
                face_emb = np.expand_dims(face_emb, axis=0)
                
                
                # Predict qua SVM
                y_pred = pickle_model.predict_proba(face_emb)
                #print(y_pred)

                # Lấy nhãn và viết lên ảnh
                #predict_names = output_enc.inverse_transform(y_pred)

                max = 0
                pos = 0
                for i in range(len(y_pred[0])):
                    if(y_pred[0][i] >= max):
                        pos =i
                        max = y_pred[0][i]
                #print(pos)
                #print(max)
                X_pos = []
                X_pos.append(pos) 
                #print(output_enc.inverse_transform(X_pos))
                predict_names = output_enc.inverse_transform(X_pos)

                #print(predict_names[0])
                
                #import IPython
                #IPython.display.Image(test_img)
                #from google.colab.patches import cv2_imshow
                #img = cv2.imread(test_img, cv2.IMREAD_UNCHANGED)
                #cv2.putText(img,predict_names[0],(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                #cv2_imshow(img)
                
                # Create Dictionary
                #persons = {
                #    "person": predict_names[0],
                #    "accuracy": max
                #}
  
                # Dictionary to JSON Object using dumps() method
                # Return JSON Object
                #return json.dumps(persons)
                
                output = {'persons': []}
                #for _, person, score in results:
                output['persons'] += (([predict_names[0] + str(': ') + str(float(max))]))

                return [output]
                
                
            
        except IOError:
            print("Không thể nhận dạng file: ")

if __name__ == '__main__':
       # print(predict("data/test/Tran Canh Xuan B1706970.jpg"))
       print(predict("data/test/Dao Minh Khoa.png"))