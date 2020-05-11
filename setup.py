from setuptools import setup, find_packages
import os


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".py") or filename.endswith(".pyc"):
                continue
            else:
                paths.append(os.path.join(path, filename).replace("src/creatediscordbot/", ""))
    return paths


extra_files = package_files('src/creatediscordbot/bot_template')
extra_files += package_files('src/creatediscordbot/docker_templates')
extra_files += package_files('src/creatediscordbot/cog_template')
print(extra_files)

setup(name='create-discord-bot',
      version='0.8',
      url='https://github.com/StartupTechTutorial/DiscordBot',
      license='GNU 3.0',
      author='StartupTechTutorials',
      author_email='hello@startuptechtutorials.com',
      description='Simple ',
      package_data={
          'creatediscordbot': extra_files
      },
      package_dir={'': 'src'},
      packages=find_packages(where='src'),
      long_description=open('README.md').read(),
      entry_points={
          'console_scripts': ['create-discord-bot=creatediscordbot:main']
      },
      python_requires='>=3.5, <4',
      install_requires=[
          'colorama>=0.4.3'
      ],
      zip_safe=False)
