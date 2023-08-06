import setuptools
import subprocess

setuptools.setup(
	name="scriptpak",
	version="0.2",
	author="RixTheTyrunt",
	author_email="rixthetyrunt@gmail.com",
	description="The scriptpak programming language",
	packages=["scriptpak"],
	classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
	install_requires=["flask"],
	long_description=subprocess.Popen(["python", "-m", "scriptpak"], stdout=subprocess.PIPE).communicate()[0].decode(),
	long_description_content_type="text/plain"
)