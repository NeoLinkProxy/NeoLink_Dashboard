import PyInstaller.__main__ as pyi


pyi.run([
    '--onefile',
    '--noconsole',
    '--add-data',
    'config.yaml;.',
    'NeoLink_kingda.py'
])
