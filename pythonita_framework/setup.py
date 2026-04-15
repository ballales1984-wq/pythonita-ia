"""
Pythonita AI Agent Framework
Setup configuration
"""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [
        line.strip() for line in f if line.strip() and not line.startswith("#")
    ]

setup(
    name="pythonita-framework",
    version="1.0.0",
    description="Framework multi-agent offline per AI agent con vector memory",
    long_description=open("README.md").read() if __name__ == "__main__" else "",
    long_description_content_type="text/markdown",
    author="Pythonita IA Team",
    author_email="info@pythonita.com",
    url="https://github.com/ballales1984-wq/pythonita-ia",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Artificial Intelligence :: Robotics",
        "Artificial Intelligence :: Natural Language Processing",
    ],
    entry_points={
        "console_scripts": [
            "pythonita-agent=ai_agent:main",
        ],
    },
)
