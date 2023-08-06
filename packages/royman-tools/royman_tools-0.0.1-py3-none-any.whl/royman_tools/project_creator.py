import click
import os


class ProjectCreator():


    def __init__(self, project_name: str):
        self.project_name = project_name
        self.package_name=project_name.replace('-', '_').replace(' ', '_')


    def create_readme(self) -> None:
        with open(f'{self.project_name}/README.md', 'w') as f:
            f.write(
f'''# {self.project_name}
> description

## Installation
```
pip install {self.package_name}
```
or from Github:
```
git clone https://github.com/roymanigley/{self.package_name}.git
cd {self.package_name}
python setup.py install
'''
            )


    def create_license(self) -> None:
        with open(f'{self.project_name}/LICENSE', 'w') as f:
            f.write(
'''MIT License

Copyright (c) 2022 roymanigley

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
            )
        

    def create_gitignore(self) -> None:
        with open(f'{self.project_name}/.gitignore', 'w') as f:
            f.write(
f'''{self.package_name}.egg-info
build
dist
__pycache__
.env
.venv
env
venv
'''
            )


    def create_setup_file(self) -> None:
        with open(f'{self.project_name}/setup.py', 'w') as f:
            f.write(
f'''from setuptools import setup, find_packages

long_description = open('README.md', "rt").read()

setup(
    name='{self.package_name}',
    version='0.0.1',    
    description='generated project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/roymanigley/{self.package_name}',
    author='Roy Manigley',
    author_email='roy.manigley@gmail.com',
    license='MIT',
    packages=['{self.package_name}'],
    install_requires=[
        'requests>=2.28.1',
        'click>=8.1.3',
    ],
    # entry_points = {{
    #     'console_scripts': [
    #         'your-command = {self.package_name}.your_module:main',
    #     ],
    # }},

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.10',
    ],
)
'''
            )


    def create_publish_script(self) -> None:
        with open(f'{self.project_name}/publish.sh', 'w') as f:
            f.write(
''' #!/bin/bash
rm ./dist/*.whl
python setup.py sdist bdist_wheel
twine upload dist/*.whl
'''         )


    def create_requirements(self) -> None:
        with open(f'{self.project_name}/requirements.txt', 'w') as f:
            f.write(
'''
wheel
twine==4.0.2
'''
            )


    def create_sources(self) -> None:
        source_dir = f'{self.project_name}/{self.package_name}'
        os.mkdir(source_dir)
        with open(f'{source_dir}/__init__.py', 'w') as f:
            f.write('# __init__.py')


    def generate(self) -> None:
        try:
            print(f'[+] create project:\n\t{self.project_name}')
            os.mkdir(self.project_name)
            print(f'[+] create readme:\n\t{self.project_name}/README.md')
            self.create_readme()
            print(f'[+] create locense:\n\t{self.project_name}/LICENSE')
            self.create_license()
            print(f'[+] create gitignore:\n\t{self.project_name}/.gitignore')
            self.create_gitignore()
            print(f'[+] create requirements:\n\t{self.project_name}/requirements.txt')
            self.create_requirements()
            print(f'[+] create setup.py:\n\t{self.project_name}/setup.py')
            self.create_setup_file()
            print(f'[+] create sources:\n\t{self.project_name}/{self.package_name}')
            self.create_sources()
            print(f'[+] completed')
        except Exception as e:
            print(f'[!] an error occurred:\n\t{e}')


@click.command()
@click.option(
        '--project-name', 
        prompt='Enter the project name', 
        help='the project you want to create', 
        type=str
)
def main(project_name: str) -> None:
    ProjectCreator(project_name).generate()


if __name__ == '__main__':
    main()
