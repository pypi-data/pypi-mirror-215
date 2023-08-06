import setuptools

setuptools.setup(
    name="biblioteca2080",
    version="1.0.1",
    author="Saullo",
    author_email="saullo.guilherme7@unifesspa.edu.br",
    description="Biblioteca para entender sobre o funcionamento de bibliotecas",
    packages=setuptools.find_packages(),
    package_dir={"": "src"},
    package_data={"biblioteca2080.data": ["*.csv", "*.zip"]},
    py_modules=["funcionalidades"]
)