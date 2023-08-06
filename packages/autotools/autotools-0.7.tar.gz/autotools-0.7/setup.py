from setuptools import setup

description = 'Just save your time'
long_description = 'Simple module for realize simple tasks'

setup(
    name='autotools',
    version='0.7',
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
