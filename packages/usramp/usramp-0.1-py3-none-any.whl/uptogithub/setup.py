import setuptools
from pkg_resources import parse_requirements
with open("README.md", "r") as fh:
     long_description = fh.read()
def reqs(fl):
    rqs=set()
    with open(fl, "r") as f:
        for r in parse_requirements(f):
            rqs.add(r.name)
    return sorted(rqs)
setuptools.setup(
     name='usramp',
     version='0.1',
     scripts=['x.usramp.py'] ,
     author="Filiberto Ortiz-Chi, Jose Aminadat Morato Marquez, Srinivas Godavarthi, Claudia Guadalupe Espinosa Gonzalez, and Jose Gilberto Torres-Torres",
     author_email="fortiz666@gmail.com",
     description=" Ultrafast shape-recognition algorithm with mass ponderation",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url = 'https://github.com/fortizchi/usramp',
     packages=setuptools.find_packages(),
     install_requires=reqs("requirements.txt"),
     license='None',
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
     python_requires='>=3.5'
)
