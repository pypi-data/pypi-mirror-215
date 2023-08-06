from setuptools import setup, Extension, find_packages

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="SpLFastlyWrite",
    version="1.0.0",
    description="Easier access and Less Waits library for pyrogram",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/ShutupKeshav/SpLFastlyWrite",
    download_url="https://github.com/ShutupKeshav/SpLFastlyWrite/releases/latest",
    author="ShutupKeshav",
    author_email="keshavatripathi@yahoo.com",
    license="MIT",
    keywords="SpLFastlyWrite",
    project_urls={
        "Tracker": "https://github.com/ShutupKeshav/SpLFastlyWrite/issues",
        "Community": "https://t.me/SpLBots",
        "Source": "https://github.com/ShutupKeshav/SpLFastlyWrite",
        "Documentation": "https://t.me/SpLBots",
    },
    python_requires="~=3.7",
    packages=find_packages(),
    test_suite="tests",
    zip_safe=False
)

print("SpLFastlyWrite BY SpL Network !")
