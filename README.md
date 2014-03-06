[![Build Status](https://travis-ci.org/aronwoost/sublime-expand-region.png?branch=master)](https://travis-ci.org/aronwoost/sublime-expand-region)

# ExpandRegion for Sublime Text

### Like "Expand Selection to Scope". But better!

ExpandRegion works a bit like the build in "Expand Selection to Scope", however it does not depend on Scopes (Scopes are used by ST to "understand" code, i.e. for syntax highlighting). Therefore selection expansion can be more granular and customizable.

It works simlar to ExpandRegion for Emacs and "Structural Selection" (Control-W) in the JetBrain IDE's (i.e. IntelliJ IDEA).

Currently the plugin works best with C'ish language syntaxes (including Java and JavaScript). For other language and textfiles or markdown is does little or nothing. [Feature requests or bug reports welcome](https://github.com/aronwoost/sublime-expand-region/issues).

Video comming soon.

## Installing

**With the Package Control plugin:** The easiest way to install ExpandRegion is through Package Control, which can be found at this site: [http://wbond.net/sublime_packages/package_control](http://wbond.net/sublime_packages/package_control)

Once you install Package Control, restart ST and bring up the Command Palette (`Command+Shift+P` on OS X, `Control+Shift+P` on Linux/Windows). Select "Package Control: Install Package", wait while Package Control fetches the latest package list, then select ExpandRegion when the list appears. The advantage of using this method is that Package Control will automatically keep ExpandRegion up to date with the latest version.

**Without Git:** Download the latest source from [GitHub](https://github.com/aronwoost/sublime-expand-region) and copy the ExpandRegion folder to your Sublime Text "Packages" directory.

**With Git:** Clone the repository in your Sublime Text "Packages" directory:

    git clone https://github.com/aronwoost/sublime-expand-region.git


The "Packages" directory is located at:

* OS X:

        ~/Library/Application Support/Sublime Text 2/Packages/

* Linux:

        ~/.config/sublime-text-2/Packages/

* Windows:

        %APPDATA%/Sublime Text 2/Packages/

## Using

By default **no shortcut is set**. I recommend using the shortcut for the build in "Expand Selection to Scope". Open "Key Bindings - User" and add to following line:
```
{ "keys": ["super+shift+space"], "command": "expand_region" }
```

## Develop

## Background

This plugin is inspired by the amazing [expand-region for Emacs](https://github.com/magnars/expand-region.el).

Here a video showing this feature (in Emacs):  

[![](http://img.youtube.com/vi/_RvHz3vJ3kA/0.jpg)](http://www.youtube.com/watch?v=_RvHz3vJ3kA?feature=player_embedded&v=M)

Read more:  
[Extend Selection by Semantic Unit](http://ergoemacs.org/emacs/syntax_tree_walk.html)

## License

MIT
