from distutils.core import setup

setup(
    name='fake_data_producer_for_apache_kafka',  # How you named your package folder (MyLib)
    packages=['fake_data_producer_for_apache_kafka'],  # Chose the same as "name"
    version='0.1',  # Start with a small number and increase it with every change you make
    license='apache-2.0',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='The Python fake data producer for Apache Kafka® is a complete demo app allowing you to quickly '
                'produce JSON fake streaming datasets and push it to an Apache Kafka topic. ',  # Give a short
    # description about your library
    author='Open Source @ Aiven',  # Type in your name
    author_email='',  # Type in your E-Mail
    url='https://github.com/aiven/python-fake-data-producer-for-apache-kafka',
    # Provide either the link to your github or to your website
    download_url='TBD',  # I explain this later on
    keywords=['kafka', 'faker', 'producer'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'yahoo_fin',
        'faker',
        'kafka-python',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'License :: OSI Approved :: Apache license 2.0',  # Again, pick a license
        'Programming Language :: Python :: 3.5',  # Specify which python versions that you want to support
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
