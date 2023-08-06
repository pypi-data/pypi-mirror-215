from setuptools import setup


setup(
    name="TestAPackageH",
    version="0.2",
    description="A publishing test",
    author = "Test",
    install_requires=["google-auth", "google"],
    packages=["hanalytics/profile"]
)