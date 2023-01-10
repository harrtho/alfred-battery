# Alfred Battery

[![GitHub Version][version-shield]][releases]
[![GitHub All Releases][downloads-shield]][releases]
[![GitHub][licence-shield]][mit-licence]

Display battery information of your Apple laptop in Alfred

![][demo]

Alfred Battery shows:

- the current charging state
- the remaining time until full or empty
- the temperature
- the charging cycles
- the health
- as well as the serial number

Alfred Battery uses a [built-in Swift][built-in-swift] program to retrieve the battery information from the system.

## Requirements

- [Alfred][alfred] (version 4.0+)
- The [Alfred Powerpack][alfred-powerpack].
- Python 3.7+ ([Command Line Tools][command-line-tools]: `xcode-select --install` or [Homebrew][homebrew]: `brew install python`)
- The Swift Compiler `swiftc` ([Command Line Tools][command-line-tools]: `xcode-select --install`)

During the first execution and after an update of the workflow, the workflow compiles the [`BatteryInfo`][built-in-swift] program.

## Licence, thanks

The workflow code, the bundled [Alfred-PyWorkflow][alfred-pyworkflow] library as well as the graphics are all under the [MIT Licence][mit-licence].

The original idea is from [BenziAhamed][benzi-ahamed] and his [Battery workflow][benzi-ahamed-alfred-battery]

[alfred-powerpack]: https://www.alfredapp.com/powerpack/
[alfred-pyworkflow]: https://github.com/harrtho/alfred-pyworkflow
[alfred]: https://www.alfredapp.com
[benzi-ahamed-alfred-battery]: https://github.com/BenziAhamed/alfred-battery
[benzi-ahamed]: https://github.com/BenziAhamed
[built-in-swift]: src/BatteryInfo.swift
[command-line-tools]: https://www.freecodecamp.org/news/install-xcode-command-line-tools/
[demo]: demo.gif
[downloads-shield]: https://img.shields.io/github/downloads/harrtho/alfred-battery/total.svg
[homebrew]: https://brew.sh
[licence-shield]: https://img.shields.io/github/license/harrtho/alfred-battery.svg
[mit-licence]: http://opensource.org/licenses/MIT
[python]: https://www.python.org
[releases]: https://github.com/harrtho/alfred-battery/releases
[version-shield]: https://img.shields.io/github/release/harrtho/alfred-battery.svg
