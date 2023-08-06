from setuptools import setup, find_packages

setup(
    name = 'tweeter-basic',
    description = 'Send tweets (with optional images) through the Twitter v2 API (OAuth 2.0) - authentication included',
    version = '0.1.1',
    license = 'MIT',
    url = 'https://mike.busuttil.ca/',
    install_requires =['flask', 'requests', 'requests-oauthlib'],
    packages = find_packages(),
    long_description = open('readme.md', encoding='utf-8').read(),
    long_description_content_type = 'text/markdown',
    author = 'Mike Busuttil',
    author_email = 'mike@busuttil.ca',

    keywords = ['tweet', 'twitter', 'v2', 'OAuth', 'OAuth2.0', 'API', 'images'],
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3',
                   'Topic :: Education',
                   'Topic :: Software Development',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)