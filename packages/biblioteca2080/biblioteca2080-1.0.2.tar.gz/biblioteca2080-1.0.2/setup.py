import setuptools

setuptools.setup(
    name="biblioteca2080",
    version="1.0.2",
    author="Saullo",
    author_email="saullo.guilherme7@unifesspa.edu.br",
    description="Biblioteca para entender sobre o funcionamento de bibliotecas",
    packages=setuptools.find_packages(),
    package_dir={"": "src"},
    py_modules=["funcoes"],
    package_data={'biblioteca2080': ['src/biblioteca2080/data/receita_2023.csv', 'src/biblioteca2080/data/receita_2023.zip']},
    include_package_data=True
)