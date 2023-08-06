from setuptools import setup, find_packages

setup(name='gen-validate',
      version='0.0.1',
      description='validate客户端',
      author='吴建华',
      author_email='wujianhua@lanqiao.cn',
      url="https://www.lanqiao.cn/",
      packages=find_packages(),  # 系统自动从当前目录开始找包
      include_package_data=False,  # 是否包含非py文件
      install_requires=['grpcio-tools>=1.38.0'],  # 依赖的第三方包
      license="MIT",
      python_requires='>=3.8',
      )
