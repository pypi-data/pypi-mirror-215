import setuptools

with open("README.md","r", encoding="utf-8") as fh:
	long_description = fh.read()
	
setuptools.setup(
  name = "blipnlptest",
  version = "0.0.6",
  author = "Caio Souza",
  author_email = "caios@take.net",
  description = "Teste dos provedores integrados na plataforma em conjunto com o Assistente de Conteudo.",
  long_description = long_description,
  long_description_content_type="text/markdown",
  keywords = [],
  install_requires=[
  'pandas',
  'ujson',
  'requests'
  ],
  classifiers=[  
    "Development Status :: 4 - Beta",
    "License :: OSI Approved :: MIT License",
	 "Operating System :: OS Independent",
    "Programming Language :: Python :: 3"
  ],
    package_dir={"": "blipnlptest"},
    python_requires=">=3.6",
)