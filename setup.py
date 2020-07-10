from setuptools import setup
# NOT 
setup(
    name='alias', # Needed to silence warnings (and to be a worthwhile package)
    url='https://github.com/psytron/alias',
    author='Mico Malecki',
    author_email='m@psytron.com',
    packages=['alias'], # Needed to actually package
    install_requires=[
        'keycache',
        'pandas',
        'alpaca_trade_api',
        'v20',
        'ccxt'],# DEPENDENCIES 
    version='0.3.9',
    license='PSYTRON', # Can be anything
    description='Alias is the container.',
    long_description=open('PYPI.md').read(),
    long_description_content_type='text/markdown'
)