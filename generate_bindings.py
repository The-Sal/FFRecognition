# Compile Swift Code and Generate Bindings for Python
import os
import ctypes
import shutil
import platform
import subprocess


# Where the source Swift file are
_filesDir = __file__.replace('generate_bindings.py', 'Xcode/Face/Face')
assert platform.system() == 'Darwin', 'This script is only for macOS'

def compile_swift_code():
    print('Compiling Swift Code...')

    files = os.listdir(_filesDir)
    absFiles = []
    for file in files:
        if file.endswith('.swift'):
            absFiles.append(os.path.join(_filesDir, file))

    cmd = [
        'swiftc',
        '-emit-library',
        '-o', 'face.dylib',
    ]

    cmd.extend(absFiles)

    subprocess.check_call(cmd)
    return os.getcwd() + '/face.dylib'


def generate_bindings(dylib_path: str):
    print('Generating Bindings...')
    try:
        subprocess.check_output(['PySiGen', '-h'])
    except FileNotFoundError:
        raise FileNotFoundError('PySiGen not installed')

    subprocess.check_call([
        'PySiGen',
        _filesDir,
        __file__.replace('generate_bindings.py', 'FFRecognition/_bindings.py'),
        '-d', dylib_path
    ])

    print('Bindings Generated')


def main():
    dylib_path = compile_swift_code()

    cdll = ctypes.CDLL(dylib_path)
    _application_support_func = cdll._install_application_support
    _application_support_func.restype = ctypes.c_char_p

    application_support = os.path.join(_application_support_func().decode(), 'FFRecognition')

    try:
        os.mkdir(application_support)
    except FileExistsError:
        pass

    persis_dylib_path = os.path.join(application_support, 'face.dylib')

    try:
        os.remove(persis_dylib_path)
    except FileNotFoundError:
        pass

    shutil.copy(dylib_path, persis_dylib_path)
    generate_bindings(persis_dylib_path)

    del cdll
    os.remove(dylib_path)


if __name__ == '__main__':
    main()




