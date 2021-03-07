Plugin for CudaText.
Adds Python auto-completion to the built-in Console, which can be triggered in several ways:
	- in Console - "Ctrl+Space" hotkey
	- in Console and document tabs - menu item "Plugins > Console Auto-Complete > Complete", can be assigned to a hotkey via "Command Palette",
			but should not be "Ctrl+Space" in presence of other "Python" auto-completion.

Auto-completion in documents is nicely complemented by "Execute selected text in console" command from "CudaExt" plugin.

-----------------------------

A few options are available to modify the behavior of the plugin. Can be accessed via main menu:
"Options / Settings-pligins / Console Auto-Completion".

- Show function parameters in auto-completion list
- Replace right part - if caret is in the middle of the identifier on auto-completion - part to the right will also be replaced
- Prefix for the auto-completion list
    
-----------------------------
    
Author: Shovel (CudaText forum user)
License: MIT
