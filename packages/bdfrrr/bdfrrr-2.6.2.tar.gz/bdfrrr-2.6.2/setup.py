import setuptools

with open("README.md", "r") as fh:
	description = fh.read()

setuptools.setup(
	name="bdfrrr",
	version="0.0.1",
	author="Matt",
	author_email="contact@gfg.com",
	packages=["bdfrrr"],
	description="A sample test package",
	long_description=description,
	long_description_content_type="text/markdown",
	url="https://github.com/mattray0295/bdfrr",
	license='MIT',
	python_requires='>=3.8',
	install_requires=[]
)

