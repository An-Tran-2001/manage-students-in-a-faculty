from setuptools import setup # bo thu vien de khi chay tren trang flask 

setup(
    name='student_management',
    packages=['student_management'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)
