"""
–* FAST FACIAL RECOGNITION *–
"""
import json
import base64
import os.path
import tempfile
import face_recognition
from ffrecognition import _bindings as swift_bindings
from ffrecognition import _private_classes as _private_cls

class Swift_FaceImage:
    """An Image containing a single face extracted from the original image. All image data is PNG format."""
    def __init__(self, binary_data_encoded: str):
        self._data = base64.b64decode(binary_data_encoded)
        self._frImage = None

    def save(self, path: str):
        with open(path, "wb") as file:
            file.write(self._data)

    def _convertToFr(self):
        named_temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        self.save(named_temp_file.name)
        loaded_image = face_recognition.load_image_file(named_temp_file.name)
        self._frImage = loaded_image
        os.unlink(named_temp_file.name)
        return

    @property
    def frImage(self):
        if self._frImage is None:
            self._convertToFr()

        return self._frImage

    @property
    def fr_encodings(self):
        """Returns the face_recognition encodings for the face image."""
        image_dimensions = self.frImage.shape
        known_face_locations = [(0, image_dimensions[1], image_dimensions[0], 0)]

        try:
            return face_recognition.face_encodings(self.frImage, known_face_locations)[0]
        except IndexError:
            return None



class Swift_Image:
    """An image class that registers the image with the swift library and allows for hardware accelerated manipulation of the image."""
    def __init__(self, imagePath: str, noLoad=False):
        self.imagePath = imagePath
        self._faces = []

        if not noLoad:
            self._swift_ref = swift_bindings.ipd_init_image(os.path.abspath(imagePath))
            self._load_images_of_faces()

    @classmethod
    def from_ref(cls, ref: int):
        """This function should only be used by BATCH_METHODS"""
        self = cls.__new__(cls)
        self._swift_ref = ref
        self._faces = []
        return self


    def _load_images_of_faces(self):
        """Takes the original image and crops out all the faces from the image and stores them in _faces as Swift_FaceImage objects."""
        faces = json.loads(swift_bindings.ipd_faces(self._swift_ref))['faces']
        for face in faces:
            self._faces.append(Swift_FaceImage(face))

    @property
    def faces(self):
        """Returns a list of Swift_FaceImage objects that contain the faces from the original image."""
        return self._faces

    def __repr__(self):
        return f"Swift_Image(path={self.imagePath}, faces={len(self._faces)})"



class BATCH_METHODS:
    @staticmethod
    def init_images(paths: list) -> [Swift_Image]:
        # This function is used to initialize a batch of images. It is faster than initializing each image individually.
        # This function will not load the cropped face image data on the init of Swift_Image objects.
        # rather, it will load the cropped face image data using the batch method in the library.

        data = _private_cls.Batch_ImagePaths(paths) # All the swift paths converted to a swift object

        # Init all the images and get the swift references
        swift_data = swift_bindings.ipd_batch_init_image(data.transferable())
        ids = _private_cls.Batch_ImageIds.from_transferable(swift_data)

        finalObjects = []

        # Ask the dylib to batch create all the swift cropped face images
        # the dylib will return the images array inside an array in the order of the ids

        # make the call
        array_of_cropped_faces_raw = swift_bindings.ipd_batch_faces(ids.transferable())
        array_of_cropped_faces = _private_cls.Batch_FaceImagesRAW64.from_transferable(array_of_cropped_faces_raw)

        # Apply the swift references to the swift objects and assign the cropped face data to the swift objects
        index = 0
        for i, swift_ref in zip(ids.ids, array_of_cropped_faces.faces_for_image):
            swiftObject = Swift_Image.from_ref(i)
            face_data = array_of_cropped_faces.faces_for_image[index]
            swiftObject._faces = face_data
            swiftObject.imagePath = paths[index]
            index += 1
            finalObjects.append(swiftObject)

        return finalObjects




if __name__ == '__main__':
    print(BATCH_METHODS.init_images(
        [
            "/Users/Salman/Desktop/Screenshot.png",
            "/Users/Salman/Desktop/test2.jpeg"
        ]
    )[0].faces[0].fr_encodings
          )
