from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="utilities",
    version="0.0.1",
    description="A Frappe App for SaaS",
    author="umar",
    author_email="umartarekbusiness@gmail.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)

