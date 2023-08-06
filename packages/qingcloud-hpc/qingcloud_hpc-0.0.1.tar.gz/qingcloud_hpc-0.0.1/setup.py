import setuptools

with open("qingcloud_hpc/README.md", "r") as fh:
  long_description = fh.read()
# python3 setup.py sdist bdist_wheel --universal

setuptools.setup(
    name="qingcloud_hpc",
    version="0.0.1",
    author="Qingcloud.HPC",
    author_email="siriusliang@yunify.com",
    description="Qingcloud hpc sdk",
    long_description=long_description,
    packages=setuptools.find_packages(),
    python_requires='>=2.7',
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License"
],

)