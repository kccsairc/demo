import sys
import os
import dlib
import cv2

def detect(img):
    detector = dlib.get_frontal_face_detector()
    #win = dlib.image_window()
    dets = detector(img, 0)
    print("Number of faces detected: {}".format(len(dets)))
    #win.clear_overlay()
    #win.set_image(img)
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
#    # Ask the detector to find the bounding boxes of each face. The 1 in the
#    # second argument indicates that we should upsample the image 1 time. This
#    # will make everything bigger and allow us to detect more faces.
  
    print("Number of faces detected: {}".format(len(dets)))
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
        # Get the landmarks/parts for the face in box d.
        shape = predictor(img, d)
        print("Part 0: {}, Part 1: {} ...".format(shape.part(0),
                                                  shape.part(1)))
        # Draw the face landmarks on the screen.
        #win.add_overlay(shape)

    #win.add_overlay(dets)

if __name__ == "__main__":
    fname ="C:\\Users\\120350181\\Desktop\\one_image\\Keishi_Ueda\\img\\e139.jpg"       
    #img = cv2.imread(fname)
    #dets = detect(img)
    