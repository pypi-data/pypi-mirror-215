import setuptools


setuptools.setup(
    name="isTrue",
    version="0.0.6",
    description="IDK???",
    keywords="IDK???",
    packages=setuptools.find_packages(),
    python_requires='>=3.4',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "License :: Free To Use But Restricted",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",

    ],
    entry_points={
        'gui_scripts': [
            'psgissue=PySimpleGUI.PySimpleGUI:main_open_github_issue',
            'psgmain=PySimpleGUI.PySimpleGUI:_main_entry_point',
            'psgupgrade=PySimpleGUI.PySimpleGUI:_upgrade_entry_point',
            'psghelp=PySimpleGUI.PySimpleGUI:main_sdk_help',
            'psgver=PySimpleGUI.PySimpleGUI:main_get_debug_data',
            'psgsettings=PySimpleGUI.PySimpleGUI:main_global_pysimplegui_settings',
        ], },
)
