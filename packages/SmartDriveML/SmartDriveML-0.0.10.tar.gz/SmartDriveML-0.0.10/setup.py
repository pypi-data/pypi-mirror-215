from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.10'
DESCRIPTION = 'SmartDriveML: Driving Industrial Projects with Affordable ML Solutions, Frameworks and Cloud Choices'
LONG_DESCRIPTION = 'SmartDriveML is a state-of-the-art Python library created to revolutionize the way industries drive projects using machine learning. This advanced application serves as a comprehensive tool, assisting users in making informed decisions regarding cloud service providers, framework selection, and project feasibility, all while maintaining a cost-effective approach. One of the core functionalities of SmartDriveML is its ability to compare costs among various cloud service providers. By leveraging its integrated algorithms and extensive data on cloud service pricing, this tool enables users to evaluate the financial implications of different providers such as AWS or Azure. With this crucial information at their disposal, industries can optimize their budget allocation, ensuring that their machine learning projects remain economically viable. Another essential feature of SmartDriveML is its framework analysis capability. The library provides comprehensive insights into popular frameworks like Pandas and PySpark, aiding users in choosing the most suitable option for their specific project requirements. By considering factors such as data volume, computational needs, and ease of implementation, SmartDriveML helps industries make informed decisions that align with their objectives and resource constraints. Moreover, SmartDriveML goes beyond cost and framework analysis by providing essential functions for exploratory data analysis and executing fundamental machine learning algorithms on sample datasets. These functions enable users to assess the potential of their projects, allowing them to evaluate whether machine learning can effectively drive their initiatives. By providing this accessible yet powerful toolset, SmartDriveML empowers industries to make data-driven decisions and confidently embark on machine learning-driven projects.'

# Setting up
setup(
    name="SmartDriveML",
    version=VERSION,
    author="Hrishikesh Thakurdesai",
    author_email="hrishikesh.thakurdesai.92@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas'],
    keywords=['python', 'machine learning', 'pyspark', 'cloud'],
    classifiers=[
        "Development Status :: 1 - Planning ",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)