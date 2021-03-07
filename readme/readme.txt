Plugin for CudaText.
Adds Python auto-completion to the built-in Console.

Default hotkey:
	Ctrl+Space - Completes current identifier in console

Function can be accessed via the main menu: "Plugins > Console Auto-Completion". 

Also works in document tabs; this goes nicely with "Execute selected text in console" command from "CudaExt" plugin.
Other auto-completion plugins will interfere with this plugin's functionality in document tabs if command in "Command Palette" is assigned "Ctrl+Space" hotkey.


-----------------------------

Several options are available to modify the behavior of the plugin. Can be accessed via main menu:
"Options / Settings-pligins / Console Auto-Completion".

- Show function parameters in auto-completion list
- Replace right part - if caret is in the middle of the identifier on auto-completion - part to the right will also be replaced
- Prefix for the auto-completion list
    
-----------------------------
    
Author: Shovel (CudaText forum user)
License: MIT
