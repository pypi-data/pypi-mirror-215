from setuptools import setup

setup(name='autotools',
      version='0.4',
      description='many autools by automatic',
      author='automatic',
      author_email='automatick07@gmail.com',
      requires=["openai", "gtts", "playsound", "SpeechRecognition"],
      license='OpenSource',
      packages=['autotools'],
      long_description="""
      Autotools module for automatising many simple tasks.
      """, 
      install_requires=[],
      zip_safe=False)
