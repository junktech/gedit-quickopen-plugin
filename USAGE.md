# How to use this plugin

## 1. Remove the original plugin
This plugin is meant to replace the original QuickOpen plugin. First, you have to locate where the original plugin is installed on your system. The location differs from distribution to distribution. You have to remove the original plugin by deleting the "quickopen" directory and the "quickopen.plugin" file.

## 2. Install this plugin
Execute the following commands:
```
git clone git://github.com/junktech/gedit-quickopen-plugin
mkdir -p ~/.local/share/gedit/plugins
mv gedit-quickopen-plugin/* ~/.local/share/gedit/plugins/

```

## 3. Activate plugin
1. Start gedit
2. Open Preferences > Plugins 
3. Check to box next to "Quick open" on the list
