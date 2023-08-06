from setuptools import setup, find_packages
from setuptools_rust import Binding, RustExtension

packages = find_packages()
extended_packages = {package: ["py.typed", ".pyi", "**/.pyi"] for package in packages}


setup(
    name="llm-rs-cuda",
    version="1.0.0",
    rust_extensions=[RustExtension("llm_rs.llm_rs", binding=Binding.PyO3, features=["metal"])],
    packages=extended_packages,
    package_data={"llm_rs": ["*.pyi", "*.typed"]},
    # rust extensions are not zip safe, just like C-extensions.
    zip_safe=False,
)