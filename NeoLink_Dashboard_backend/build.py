import PyInstaller.__main__ as pyi


pyi.run([
    '--onefile',
    '--noconsole',
    '--add-data',
    'files/;files',
    '--add-data',
    'Edition_logs.txt;.',
    '--add-data',
    'VersionSystem/;VersionSystem',
    'NeoLink_Dashboard.py'
])
