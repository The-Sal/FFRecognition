"""Fast Face Recognition Library for Python built with face.dylib"""
try:
    from ffrecognition import _bindings
except ImportError:
    raise ImportError('Bindings not found. Did you forget to run generate_bindings.py?')

import face_recognition as fr
from ffrecognition.exceptions import *
from ffrecognition.classes import Swift_Image, Swift_FaceImage, BATCH_METHODS

def euclidian_distance(face1: Swift_FaceImage, face2: Swift_FaceImage) -> float:
     """Returns the euclidian distance between two face images"""
     face1_encodings = face1.fr_encodings
     face2_encodings = face2.fr_encodings
     encs = [face1, face2]
     for enc in encs:
            if enc.fr_encodings is None:
                raise UnableToCompareFacesError('Face not detected in image: {}'.format(enc))

     return fr.face_distance([face1_encodings], face2_encodings)[0]

