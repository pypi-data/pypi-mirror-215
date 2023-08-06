from setuptools import setup, find_packages

setup(
	name="cnapps",
	version="0.0.1",
	author="zhaoweiren",
	author_email="1013036362@qq.com",
	description="Predict CN cross-coupling reaction yield",
	url="https://github.com/ZWR0/Apps.git",
	packages=find_packages(),
	install_requires=['lazypredict==0.2.12', "matplotlib==3.4.3", "numpy==1.24.3", "pandas==1.5.3", "Pillow==9.5.0", "rdkit==2023.3.1", "scikit_learn==1.2.2", "streamlit==1.5.1", "lightgbm==2.3.1"],
	python_requires=">=3.9"
	)
