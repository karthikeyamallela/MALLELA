"""
Setup script for QUANTUMIDS
"""
from setuptools import setup, find_packages

setup(
    name="quantumids",
    version="2.0.0",
    description="Quantum-Inspired Intrusion Detection System",
    author="QUANTUMIDS Team",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.4.0",
        "qiskit>=0.39.0",
        "streamlit>=1.28.0",
        "openpyxl>=3.0.0",
    ],
    python_requires=">=3.8",
)

