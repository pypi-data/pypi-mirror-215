import setuptools
import subprocess

setuptools.setup(
	name="scriptpak",
	version="0.3",
	author="RixTheTyrunt",
	author_email="rixthetyrunt@gmail.com",
	description="The scriptpak programming language",
	packages=["scriptpak"],
	classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
	install_requires=["flask"],
	long_description="\n".join(subprocess.Popen(["python", "-m", "scriptpak"], stdout=subprocess.PIPE).communicate()[0].decode().split("\n")[2:]),
	long_description_content_type="text/plain"
)