from setuptools import setup

setup(name='cellworld',description='Maciver Lab computational biology research package',author='german espinosa',author_email='germanespinosa@gmail.com',packages=['cellworld'],install_requires=['numpy', 'matplotlib', 'json-cpp', 'tcp-messages', 'networkx', 'cv'],data_files=[('files',['files/mouse.png','files/robot.png'])],license='MIT',version='0.0.209',zip_safe=False)
