# gedit-quickopen-plugin
Customized version of Gedit's QuickOpen plugin.

## Added features
- begin search on first letter entry (disabled auto search when dialog is shown)
- search in all subdirectories of File browser's root directory

## Removed features 
- display results from Bookmarks
- display results from Home directory
- display results from Recent documents list
- display results from Open documents list

## Usage
Same as the original plugin: press CTRL + ALT + O and start typing.

## Warning
Due to full depth directory scanning, the plugin can be slow on extremely large directory hierarchies. Please select an appropriately narrow scope by navigating to a specific folder in the File browser pane.

