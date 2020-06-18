import setuptools

install_requires = ["h5py", "numpy"]

setuptools.setup(
    name="istra2py",
    version="0.0.1",
    author="Julian Bauer, Jonas Hund",
    author_email="julian.bauer@kit.edu, jonas.hund@kit.edu",
    description="Read hdf5 files exported from Istra4D digital image correlation with python",
    url="https://git.scc.kit.edu/ifm/werkstatt/istra2py",
    py_modules=["istra2py"],
    # packages=["istra2py"],
    # package_dir={"istra2py": "istra2py"},
    # module_data={"istra2py": ["data.bib"]},
    # scripts=["scripts/create_excel_view.py"],
    # include_package_data=True,
    install_requires=install_requires,
    tests_require=install_requires + ["pytest", "matplotlib"],
    # extras_require={
    #     ":python_version>'3.5'": ["pandas", "pybtex", "openpyxl", "matplotlib"]
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
