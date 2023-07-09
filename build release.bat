pyinstaller gmtk2023.py --onefile --name FurryQuest -w --add-data ".\assets;.\assets"
xcopy "assets\*" "dist\assets\" /E