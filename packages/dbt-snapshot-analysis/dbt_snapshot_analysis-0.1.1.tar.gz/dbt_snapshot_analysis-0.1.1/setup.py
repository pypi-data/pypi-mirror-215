from setuptools import setup, find_packages

setup(
    name="dbt_snapshot_analysis",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["pandas", "matplotlib", "streamlit"],
    entry_points={
        "console_scripts": ["dbt_snapshot_analysis=dbt_snapshot_analysis:main"]
    },
    author="Sammy Teillet",
    author_email="sammy.teillet@gmail.com",
    description="A package for analyzing snapshots",
    url="https://github.com/data-drift/dbt-snapshot-analytics",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
