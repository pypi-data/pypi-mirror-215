import setuptools

setuptools.setup(
	name="scriptpak",
	version="0.1",
	author="RixTheTyrunt",
	author_email="rixthetyrunt@gmail.com",
	description="The scriptpak programming language",
	packages=["scriptpak"],
	classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
	install_requires=["flask"]
)