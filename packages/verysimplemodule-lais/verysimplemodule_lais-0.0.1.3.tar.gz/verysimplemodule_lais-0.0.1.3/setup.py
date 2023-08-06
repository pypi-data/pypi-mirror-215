from setuptools import setup, find_packages

VERSION = '0.0.1.3' 
DESCRIPTION = 'Pacote para baixar arquivo'
LONG_DESCRIPTION = 'Pacote em Python para baixar um PDF'

# Setting up
setup(
       # 'name' deve corresponder ao nome da pasta 'verysimplemodule'
        name="verysimplemodule_lais", 
        version=VERSION,
        author="Lais Sousa",
        author_email="<laissouroch@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['requests'], # adicione outros pacotes que 
        # precisem ser instalados com o seu pacote. Ex: 'caer'
        py_modules=['baixar_arquivo'],
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)