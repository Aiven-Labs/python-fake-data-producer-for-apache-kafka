from distutils.core import setup

setup(
    name='aiven_fake_data_producer_for_apache_kafka',
    packages=['aiven_fake_data_producer_for_apache_kafka'],
    version='1.0.0',
    license='apache-2.0',
    description='The Python fake data producer for Apache Kafka® is a complete demo app allowing you to quickly '
                'produce JSON fake streaming datasets and push it to an Apache Kafka topic. ',
    author='Open Source @ Aiven',
    url='https://github.com/aiven/python-fake-data-producer-for-apache-kafka',

    download_url='TBD',
    keywords=['kafka', 'faker', 'producer'],
    install_requires=[
        'yahoo_fin',
        'faker',
        'kafka-python',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache license 2.0',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
