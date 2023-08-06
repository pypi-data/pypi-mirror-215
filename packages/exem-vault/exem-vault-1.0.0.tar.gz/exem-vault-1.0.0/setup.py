from setuptools import setup, find_packages

setup(
    name='exem-vault',
    version='1.0.0',
    description='All secrets now at reach.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/exem2/libraries/api/vault',
    author='Félix BOULE--REIFF',
    author_email='boulereiff@exem.fr',
    license='BSD 2-clause',
    install_requires=[
      "hvac",
    ],
    py_modules=[  # Ajoute des scripts de la racine
        'vault',
        'policy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License'
    ],
)
