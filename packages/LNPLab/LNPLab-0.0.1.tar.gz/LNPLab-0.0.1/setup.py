from setuptools import setup, find_packages

setup(
    name='LNPLab',
    version='0.0.1',
    description='Utils for LNP Solution and Clients',
    author='william',
    author_email='william@lnpsolution.com',
    url='https://github.com/wosaKim/LNPLab',
    install_requires=['tqdm', 'pandas', 'scikit-learn', 'rdkit'],
    packages=find_packages(exclude=[]),
    keywords=['Deep Learning Model Evaluation', 'Smart Banch'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
