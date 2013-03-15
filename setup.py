import setuptools


def parse_requirements():
    fap = open('requirements.txt', 'r')
    raw_req = fap.read()
    fap.close()
    return raw_req.split('\n')


setuptools.setup(
    name='warmongo',
    version='0.2.0',
    description='JSON-Schema-based ORM for MongoDB',
    author='Rob Britton',
    author_email='rob@robbritton.com',
    url='http://github.com/robbrit/warmongo',
    packages=['warmongo'],
    install_requires=parse_requirements(),
)
