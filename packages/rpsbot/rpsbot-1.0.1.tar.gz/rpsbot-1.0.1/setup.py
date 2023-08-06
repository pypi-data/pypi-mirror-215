import setuptools

setuptools.setup(name="rpsbot",
                 author="Elia Toselli",
                 author_email="elia.toselli@outlook.it",
                 packages=["rpsbot"],
                 entry_points={'console_scripts': ['rpsbot = rpsbot.rpsbot:main']})