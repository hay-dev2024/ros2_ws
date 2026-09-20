import os
from glob import glob

from setuptools import find_packages, setup

package_name = "robot_nodes"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (os.path.join("share", package_name, "launch"), glob("launch/*.launch.py")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="hay",
    maintainer_email="hay@todo.todo",
    description="TODO: Package description",
    license="Apache-2.0",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        "console_scripts": [
            "heartbeat = robot_nodes.heartbeat:main",
            "listener = robot_nodes.listener:main",
            "hello_pub = robot_nodes.hello_pub:main",
            "hello_sub = robot_nodes.hello_sub:main",
            "laserscan_pub = robot_nodes.laserscan_pub:main",
            "image_pub = robot_nodes.image_pub:main",
            "imu_pub = robot_nodes.imu_pub:main",
        ],
    },
)
