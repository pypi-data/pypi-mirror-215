import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-metaflow-aws",
    "version": "0.0.0",
    "description": "cdktf-metaflow-aws",
    "license": "Apache-2.0",
    "url": "https://github.com/bcgalvin/cdktf-metaflow-aws.git",
    "long_description_content_type": "text/markdown",
    "author": "Bryan Galvin<bcgalvin@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/bcgalvin/cdktf-metaflow-aws.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_metaflow_aws",
        "cdktf_metaflow_aws._jsii"
    ],
    "package_data": {
        "cdktf_metaflow_aws._jsii": [
            "cdktf-metaflow-aws@0.0.0.jsii.tgz"
        ],
        "cdktf_metaflow_aws": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "cdktf>=0.17.0",
        "constructs>=10.0.107",
        "jsii>=1.84.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
