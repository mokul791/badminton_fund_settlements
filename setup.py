from setuptools import setup

APP = ['badminton_splitter_modern.py']  # main script
DATA_FILES = ['badminton_logo.png']     # image to bundle into Resources

OPTIONS = {
    'iconfile': 'app_icon.icns',        # .icns icon in the same folder
    'argv_emulation': True,             # drag-and-drop & Finder-friendly args
    'includes': ['tkinter'],            # ensure Tkinter is bundled
    # 'plist': {
    #     'CFBundleName': 'Badminton Expense Splitter',
    #     'CFBundleDisplayName': 'Badminton Expense Splitter',
    #     'CFBundleIdentifier': 'com.ismail.badminton-expense-splitter',
    #     'CFBundleVersion': '1.0.0',
    #     'CFBundleShortVersionString': '1.0.0',
    # },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)