"""
Setup.py per Pythonita IA
Permette installazione come package Python.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Leggi README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

# Leggi requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text().strip().split('\n')

setup(
    name="pythonita-ia",
    version="3.1.0",
    author="Pythonita Team",
    author_email="support@pythonita.com",
    description="Software professionale traduzione NLP italiano → Python con visualizzatore 3D robot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ballales1984-wq/pythonita-ia",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Natural Language :: Italian",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pythonita=pythonita.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

