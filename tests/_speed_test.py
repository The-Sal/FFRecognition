import os

from utils3 import Timer
from ffrecognition import BATCH_METHODS
from generate_bindings import main as compile_swift_code

def test_speed(images_paths: list):
    # Load an images
    # find all faces
    # crop out the faces
    timeTaken = 0
    def _timeTaken(x):
        nonlocal timeTaken
        timeTaken = x


    with Timer(_timeTaken):
        BATCH_METHODS.init_images(images_paths)


    print('[ffrecognition] {} in {} seconds. Speed {}/s'.format(len(images_paths), timeTaken, len(images_paths)/timeTaken))
    return timeTaken


def test_speed_of_face_recognition(image_paths):
    # Load an images
    # find all faces
    # crop out the faces
    import face_recognition as fr
    import numpy

    timeTaken = 0

    def _timeTaken(x):
        nonlocal timeTaken
        timeTaken = x

    with Timer(_timeTaken):
        images = []
        for image_path in image_paths:
            images.append(fr.load_image_file(image_path))

        for image in images:
            locations = fr.face_locations(image)
            for location in locations:
                top, right, bottom, left = location
                face_image = image[top:bottom, left:right]
                face_image = numpy.array(face_image)
                face_encodings = fr.face_encodings(face_image)



    print('[face_recognition] {} in {} seconds. Speed {}/s'.format(len(image_paths), timeTaken, len(image_paths)/timeTaken))
    return timeTaken




if __name__ == '__main__':
    from utils3.system import paths
    location_files = paths.Path('/Users/Salman/Desktop/aa/').files(absolute=True)
    for location_file in location_files:
        if location_file.endswith('.DS_Store'):
            location_files.remove(location_file)

    compile_swift_code()

    t1 = test_speed(location_files)
    t2 = test_speed_of_face_recognition(location_files)
    # Calculate the difference between a and b
    difference = t2 - t1

    # Calculate the percentage difference
    percentage_difference = (difference / t1) * 100

    # Print the percentage difference with two decimal places
    print(f"{percentage_difference:.2f}% faster")

