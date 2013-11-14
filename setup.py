import setuptools


def parse_requirements():
    fap = open('requirements.txt', 'r')
    raw_req = fap.read()
    fap.close()
    return raw_req.split('\n')


setuptools.setup(
    name='warmongo',
    version='0.4.5',
    description='JSON-Schema-based ORM for MongoDB',
    author='Rob Britton',
    author_email='rob@robbritton.com',
    url='http://github.com/robbrit/warmongo',
    keywords=["mongodb", "jsonschema"],
    packages=['warmongo'],
    package_data={"warmongo": ["requirements.txt"]},
    include_package_data=True,
    install_requires=parse_requirements(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Database :: Front-Ends"
    ],
    long_description="""\
  JSON-Schema-based ORM for MongoDB
  ---------------------------------

  Allows you to build models validated against a JSON-schema file, and save
  them to MongoDB.
""",
)
