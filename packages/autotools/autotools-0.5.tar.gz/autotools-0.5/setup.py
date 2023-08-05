from setuptools import setup

description = 'Just save your time'
long_description = 'Simple module for realisate simple tasks'

setup(
    name='autotools',
    version='0.5',
    description=description,
    long_description=long_description,
    author='automatic, ebu sobak',
    author_email='',
    license='OpenSource',
    packages=['autotools'],
    install_requires=[
        'openai',
        'SpeechRecognition',
        'playsound',
        'gtts',
        'requests',
        'Pillow',
        'numpy',
    ]
)
