# Alfred Battery

Display battery information of your Apple laptop in Alfred

![][demo]

Alfred Battery shows:

- the current charging state
- the remaining time until full or empty
- the tempertature
- the charging cycles
- the health
- as well as the serial number

Alfred Battery uses a a [built-in Swift][built-in-swift] programm to retive the battery information from the system.

## Dependencies

The Alfred Battery workflow dependes on a [python3.7+][python] installation. Install `python3` e.g. via. [Homebrew][homebrew] `brew install python`.

Additionaly during the first execution and after an update of the workflow, the workflow compiles the `BatteryInfo` programm. This programm dependes on swift and the macOS `command line tools`. [freeCodeCamp tutorial][command-line-tutorial]

## Licence, thanks

The workflow code, the bundeled [Alfred-PyWorkflow][alfred-pyworkflow] library as well as the graphics are all under the [MIT Licence][mit-licence].

The original idea is from [BenziAhamed][benzi-ahamed] and his [Battery workflow][benzi-ahamed-alfred-battery]

[alfred-pyworkflow]: https://github.com/harrtho/alfred-pyworkflow
[benzi-ahamed-alfred-battery]: https://github.com/BenziAhamed/alfred-battery
[benzi-ahamed]: https://github.com/BenziAhamed
[built-in-swift]: src/BatteryInfo.swift
[command-line-tutorial]: https://www.freecodecamp.org/news/install-xcode-command-line-tools/
[demo]: demo.gif
[homebrew]: https://brew.sh
[mit-licence]: http://opensource.org/licenses/MIT
[python]: https://www.python.org
