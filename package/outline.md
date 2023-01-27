## Introduction

- Python packaging is the most common way to share code/libraries/applications. It allows packaging of the modules, so that they can later be published and deployed by other users, either by sharing binary files, source code or by using a package manager to fetch them from online (public or private) repositories.
- The recommended way to package your code is by using the built-in python library _setuptools_ which has a lot and powerful functionalities.
- In this video, I ll show you how to harness some the power of _setuptools_ so that you can package and publish your code on the official python repository _PyPI._
- Stay with me until the end of the video, where I will present a cool and practical alternative to a common practice most developers do, but is not needed anymore when packaging your code.

## Example use cases (where packaging is a must)

- Easier management of release versioning
- Shipping and deployment becomes pretty simple
- Automatic dependency management
- Increase your code’s accessibility
- Cloud computing
- Containerizing your application

## Code example

- Brief presentation of the library itself
  - A library that contains various ID generators ( password, guid, valid credit card number, object id and numerical pin)
  - Unit tests are also included
- Explain how the project is structured, folders, sub-folders because it plays important role when you install the package on the installed structure.

## Present setuptools

- _setuptools_ is a (now standard) python library that facilitates packaging python projects by enhancing the _distutils_ library.
- Important keywords/parameters of _setuptools_ to be aware of:
  - wheel (.whl): A pre-built (zip) binary file, which is ready to be installed, that contains all the necessary information (code itself and metadata) for python package manager to install the package. To create one you should run `python setup.py bdist_wheel` within the shell. bdist stands for binary distribution.
  - sdist (.tar.gz) : The source code distribution equivalent to wheel. A tar file (zip) that contains the source code together with the [setup.py](http://setup.py) file, so the user can re-built it. To create a source distribution run `python setup.py sdist`
- The above two commands can be combined into one, if both distributions are desired. The output will be stored within the _dist_ folder that setuptools will create in the same level with [setup.py](http://setup.py) resides.
- The build folder: Contains all the source code / modules that will be distributed.
- egg-info: A directory placed adjacent to the project's code and resources, that directly contains the project's metadata. Replaced by wheels. (directly from Wikipedia)
  - Python eggs are a way of bundling additional information with a Python project, that allows the project's dependencies to be checked and
    satisfied at runtime, as well as allowing projects to provide [plugins](<https://en.wikipedia.org/wiki/Plug-in_(computing)>) for other projects. (quoting wikipedia)

## Present [setup.py](http://setup.py)

- Talk about the basic parameters (the ones already in our example [setup.py](http://setup.py) file), brief explanation on what each one is responsible for.
- Explain in a nutshell how to customize the parameters it needs for [setup.py](http://setup.py) to work, mostly package dir and packages that allows setuptools to automatically find all the packages in our project structure (which is explained before in code example).
- Mention that _\*\*init_\*\*.py needs to be present in every directory/folder in order for it to be seen as a package directory.
- Mention that an alternative to adding the parameters in [setup.py](http://setup.py) (python file) you can screate a setup.cfg (configuration file) as well. But that’s outside the scope of this video.

## Building and installing a package (sdist, wheel)

- Run [setup.py](http://setup.py) using ‘_python [setup.py](http://setup.py/) bdist_wheel sdist’_ command. Explain that this creates both source code files and binary (.whl) file.
- Then install package locally by running ‘_pip install idgenerator-0.0.x-py3-none-any.whl’._ Alternatively, you can also run _pip install ._ under the directory where [setup.py](http://setup.py) lives and will install your package directly, but that doesn’t the _dist_ folder which contains all the files needed for publishing in the PyPI repository. (up to you).
- Optionally, explain how to update _.gitignore_ to ignore _build, dist and .egg-info_ files.
- NOTE: The current [setup.py](http://setup.py) file is configured to also install the tests within the python environment. That is not the way it should normally happen, it happens only for the purposes of this demo. We can always change that for the video if you think it should happen otherwise.

## Introducing PyPI

- Explain what PyPI is in a nutshell, how to browse/search packages and see the metadata about it (set up the ground for when you publish your package later).
- Maybe a catchy point is to mention that when you _pip install anything_ you are basically fetching from PyPI (surprisingly enough some people might not know this!).
- Make an account so that you can publish a package. I would recommend to make a testPyPI account [https://test.pypi.org/](https://test.pypi.org/) so that you don’t actually publish under the official repository.
- Optional but good practice, explain how to configure / create _.pypirc_ file, so authentication happens automatically when uploading your package to the repository. Also good for privacy issues when making the video that your token doesn’t get compromised.

## Publishing the package on PyPI

- Make sure you have _twine_ installed. That’s a good point to run ‘_pip install .[dev]’._ Twine is declared as a development dependency, so that will install it automatically together with the package itself.
- Run _twine check dist/_ ,\* you should see tests passed for both source code and wheel file.
- Run ‘_twine upload — repository testpypi dist/_’ ._ Assuming you have a _.pypirc\* file configured, that should work and publish your package to the testPyPI repo.
- Small detail to be aware of: If you try to publish same version name as already published, testPyPI won’t allow it and you ll get an error. (see point 7 in retrospective)
- Visit your package’s webpage so that viewers can see how the package looks published.
- You can also create a new environment and install the newly published package via pip. You can do the same within the existing environment but always more neat to do on a fresh environment.

## Further capabilities of packaging

- This part is totally up to you, as in how much further you want to go. Take a look at retro to see what you think is worth mentioning more extensively here. Number 4, 11 for example might be such cases.
- Some interesting capabilities worth discussed for sure imo within the context of this video is _‘pip install -e .’_

## Hook sharing

- Talk about the no need of _requirements.txt_ due to the [setup.py](http://setup.py) dev option. If you did the first bullet point of Publishing the package, you can call back to it.

## Retrospective

Things to keep in mind before diving into code packaging:

1. How much does it make sense when you package your code? (Is your code easily re-usable/abstracted enough and ‘plug and play’ after deployment?)
2. Are you packaging your code for own use (for example in different environment), or to share it easier with other developers? (Documenting it, creating a helper web-page might be a good idea, or even necessary in some cases)
3. If you re planning to share your package with others, consider using a software license before. Have a look at [https://tldrlegal.com/](https://tldrlegal.com/) or [https://choosealicense.com/](https://choosealicense.com/) for understanding the most popular software licenses available.
4. If the application requires extra data, should those data be incorporated in the module or linked externally (depending on size)?
5. Are the code modules decoupled enough for the end user to utilize parts of the package if needed?
6. Is the architecture good enough for further development and do the modules/submodules semantically make sense to be named/placed the way they are?
7. To avoid the overhead of updating the package version manually every time versioning management modules might come handy (ex. bumpversion\***\*).\*\*** Plus you are avoiding publishing clashes (PyPI) that occur under a version number already published previously.
8. Good practice to use as many classifiers applicable, so that it helps developers find your package easier by filtering and it provides some metadata as well. Check the available classifiers here [https://pypi.org/classifiers/](https://pypi.org/classifiers/)
9. Instead of using [setup.py](http://setup.py) file (code) you can atlernatively use setup.cfg which is a configuration file instead.
10. Avoid using distutils package, use always setuptools, which is an enhancement of the former.
11. Always publish your code under a license. By not using any license when packaging your code you are not allowing anyone to use your code?
