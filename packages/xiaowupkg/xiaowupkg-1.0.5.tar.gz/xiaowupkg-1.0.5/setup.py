from setuptools import setup, find_packages

setup(
    name='xiaowupkg',
    version='1.0.5',
    author='wzh',
    author_email='wzh@example.com',
    description="it's wzh's packages include many useful menthod",
    packages=['xiaowupkg'],
    install_requires=[
        'pyautogui>=0.9.54',
        'pyperclip>=1.8.2',
        'openpyxl>=3.1.2',
        'PyQt5>=5.15.9',
    ],
)
