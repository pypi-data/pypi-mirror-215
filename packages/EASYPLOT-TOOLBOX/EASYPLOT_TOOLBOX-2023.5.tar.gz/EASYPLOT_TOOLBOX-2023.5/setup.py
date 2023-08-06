from setuptools import setup

setup(
    	name = 'EASYPLOT_TOOLBOX',
    	version = '2023.5',
		url = 'https://wmpjrufg.github.io/EASYPLOT_TOOLBOX/',
    	description= 'Ferramenta para plotagem rápida de gráficos',
        keywords = ["Plot", "Data Science", "Optimezation"],
		license = 'Apache License 2.0',
        readme = 'readme.md',
		authors = ['Wanderlei Malaquias Pereira Junior', 'Sergio Francisco da Silva', 'Nilson Jorge Leão Junior', 'Mateus Pereira da Silva'],
		author_email = 'wanderlei_junior@ufcat.edu.br',
    	maintainers = ['Wanderlei Malaquias Pereira Junior', 'Mateus Pereira da Silva'],
		packages = ['EASYPLOT_TOOLBOX'],
    	install_requires = ["matplotlib", "seaborn"],
		classifiers = [
    		'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
			'Topic :: Software Development :: Build Tools',
  		]
    )

