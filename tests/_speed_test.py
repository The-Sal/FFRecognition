import os

from utils3 import Timer
from ffrecognition import BATCH_METHODS
from generate_bindings import main as compile_swift_code

def test_speed(images_paths: list):
    compile_swift_code()

    timeTaken = 0
    def _timeTaken(x):
        nonlocal timeTaken
        timeTaken = x


    with Timer(_timeTaken):
        BATCH_METHODS.init_images(images_paths)


    print('{} in {} seconds. Speed {}/s'.format(len(images_paths), timeTaken, len(images_paths)/timeTaken))



if __name__ == '__main__':
    from utils3.system import paths
    location_files = paths.Path('/Users/Salman/Desktop/sal/').files(absolute=True)
    for location_file in location_files:
        if location_file.endswith('.DS_Store'):
            location_files.remove(location_file)


    test_speed(location_files)
