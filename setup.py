import setuptools

def generate_binding():
    from generate_bindings import main
    main()

# Generate the bindings before the package is installed so that the bindings are included in the package
generate_binding()

# Set up the package
setuptools.setup(
    name="ffrecognition",
    version="0.0.6",
    author="Salman",
    packages=setuptools.find_packages(),
    install_requires=[
            'face_recognition',
            'utils3 @ git+https://github.com/the-sal/utils3'
    ]
)

