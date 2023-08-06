from setuptools import setup, find_packages

setup(
    name='SegmentTec-Everything',
    version='0.1.0',
    description='A package for everything related to segmentation',
    author='Vishnu',
    author_email='mubin@codewave.com',
    url='https://github.com/Mubin-Hardy/segmentTc-Everything-package',
    packages=find_packages(),
    extras_require={
        "all": ["matplotlib", "pycocotools", "opencv-python", "onnx", "onnxruntime"],
        "dev": ["flake8", "isort", "black", "mypy"],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    python_requires='>=3.7',
)