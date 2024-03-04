
# FFRecognition

FFRecognition is a lightweight Python library that provides hardware-accelerated facial recognition capabilities by leveraging an optimized Swift library (`face.dylib`).

## Installation

To install FFRecognition, you'll need to have Python 3.6 or later installed on your system. You can install the library using pip:

```bash
pip install git+https://github.com/The-Sal/FFRecognition
```

Note: During installation the package has to compile the swift code into the face.dylib file, the library also has to generate the python bindings for the library once the file is compiled.
This process requires swiftc and PySiGen to be installed on your system.
If you do not have access to PySiGen you might have to manually create the bindings and add the file to the ffrecognition library under the name `_bindings.py`

Here is a sample of what bindings should look like:
```python
import ctypes
# File: ffrecognition/_bindings.py
# Global Variables (private):
_lib = ctypes.CDLL("~/Application Support/ffrecognition/face.dylib")

# Auto-generated Functions by PySiGen v2:

def ipd_batch_init_image(arg0: str):
    x = _lib.ipd_batch_init_image
    x.argtypes = [ctypes.c_char_p]
    x.restype = ctypes.c_char_p
    arg0 = arg0.encode()
    return x(arg0).decode()

def ipd_batch_faces(arg0: str):
    x = _lib.ipd_batch_faces
    x.argtypes = [ctypes.c_char_p]
    x.restype = ctypes.c_char_p
    arg0 = arg0.encode()
    return x(arg0).decode()
```
You only have to generate the bindings once, the library will use the generated file for future use. Only bindings for swift functions with the _cdecl calling convention are required.


## Getting Started

Here's a simple example of how to use FFRecognition:

```python
from ffrecognition import Swift_Image, euclidean_distance

# Initialize an image
image = Swift_Image("/path/to/your/image.jpg")

# Get the extracted face images
face_images = image.faces

# Calculate the Euclidean distance between two face images
distance = euclidian_distance(face_images[0], face_images[1])
print(f"Euclidean distance: {distance}")
```

## API Reference

### `Swift_Image`

`Swift_Image` represents an original image and provides access to the extracted face images.

#### Constructor

```python
__init__(self, imagePath: str, noLoad=False)
```

- `imagePath` (str): The path to the image file.
- `noLoad` (bool, optional): If `True`, the face images will not be loaded during initialization. Default is `False`.

#### Properties

```python
Swift_Image.faces
```

A list of `Swift_FaceImage` objects representing the extracted face images.

### `Swift_FaceImage`

`Swift_FaceImage` represents a single face image extracted from the original image.

#### Constructor

```python
__init__(self, binary_data_encoded: str)
```

- `binary_data_encoded` (str): A base64-encoded string representing the binary data of the face image.

#### Methods

```python
save(self, path: str)
```

Saves the face image to the specified file path.

- `path` (str): The file path where the face image should be saved.

#### Properties

```python
frImage
```

A property that returns the face image in a format compatible with the `face_recognition` library. If the image hasn't been converted yet, it performs the conversion and caching.

```python
fr_encodings
```

A property that returns the face encodings for the face image, computed using the `face_recognition` library. The encodings are generated using the `face_recognition.face_encodings` function with the `"large"` model. If the encodings haven't been computed yet, it computes and caches them. This property may return `None` if no face was detected in the image.

### Batch Processing

FFRecognition provides efficient batch processing capabilities through the `BATCH_METHODS` class.

```python
from ffrecognition import BATCH_METHODS

# List of image paths
image_paths = [
    "/path/to/image1.jpg",
    "/path/to/image2.png",
    "/path/to/image3.jpeg",
    # ...
]

# Initialize a batch of images
batch_images = BATCH_METHODS.init_images(image_paths)

# Access the extracted face images for each image
for image in batch_images:
    face_images = image.faces
    # Process face images...
```

#### `BATCH_METHODS.init_images(image_paths)`

- `image_paths` (list): A list of image paths.
- Returns: A list of `Swift_Image` objects. Each `Swift_Image` object in the list will have its `faces` attribute populated with the corresponding `Swift_FaceImage` instances, representing the extracted face images.

This batch processing approach leverages optimizations in the underlying Swift library (`face.dylib`) to parallelize the face detection and extraction tasks, resulting in significant performance improvements compared to initializing and processing images individually.

### Utility Functions

#### `euclidean_distance(face1, face2)`

Calculates the Euclidean distance between the face encodings of two `Swift_FaceImage` objects.

- `face1` (`Swift_FaceImage`): The first face image.
- `face2` (`Swift_FaceImage`): The second face image.
- Returns: A float representing the Euclidean distance between the face encodings.

**Note:** If no face was detected in either of the input images, this function will raise an `UnableToCompareFacesError` exception.

## Performance

FFRecognition is designed to provide significant performance improvements over traditional facial recognition approaches, especially when processing large batches of images. The following benchmarks illustrate the speed-up achieved by FFRecognition compared to the `face_recognition` library:

```
Acclerated by face.dylib version 1.8 🚀
[ffrecognition] 29 in 0.6211409568786621 seconds. Speed 46.68827530828088/s
[face_recognition] 29 in 9.638936758041382 seconds. Speed 3.0086305915231213/s
```

**FFRecognition is 1451.81% faster than the `face_recognition` library for this benchmark.**

The benchmark was performed on a set of 29 images, measuring the time taken to load the images, detect faces, and extract the face regions. FFRecognition's hardware acceleration and optimized batch processing capabilities allow it to achieve a remarkable speed-up over the traditional `face_recognition` library.
The test file can found in the `tests` directory. under the name `_speed_test.py`

## Contributing

Contributions to FFRecognition are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/The-Sal/FFRecognition/pulls).

## Acknowledgments

FFRecognition wouldn't be possible without the following open-source projects:

- [face_recognition](https://github.com/ageitgey/face_recognition): A Python library for facial recognition built on top of dlib.
- [dlib](https://github.com/davisking/dlib): A C++ library for machine learning and computer vision.

Special thanks to the developers of these projects for their incredible work.

