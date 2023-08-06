from setuptools import setup

setup(
    name='reliableGPT',
    version='0.2.901',
    description='Error handling and auto-retry library for GPT',
    author='Ishaan Jaffer',
    packages=['reliablegpt'],
    install_requires=[
        'openai',
        'termcolor',
        'klotty',
        'numpy',
        'posthog'
    ],
)
