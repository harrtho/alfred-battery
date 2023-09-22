# Battery Alfred Workflow

[![GitHub Version][version-shield]][gh-releases]
[![GitHub All Releases][downloads-shield]][gh-releases]
[![GitHub][license-shield]][mit-license]

Display battery information of your Apple laptop in [Alfred][alfred]

![][preview]

## Download & Installation

Download the [latest workflow release][gh-latest-release] from GitHub. Open the workflow file to
install in Alfred.

## Usage

- `battery` — Show battery charging state and additional information
  - Charging state `Draining`, `Charging` or `Fully Charged`
  - Remaining time until `full`, `empty` or `On AC power`
  - Temperature in `°C`
  - Charging cycle count
  - Health in `%`
  - Serial number

## Bug reports and feature requests

Please use [GitHub issues][gh-issues] to report bugs or request features.

## Contributors

The original idea for this Alfred Workflow comes from the [Battery workflow][benzi-alfred-battery]
of [Benzi][benzi-ahamed]

## License

Battery Alfred Workflow is licensed under the [MIT License][mit-license]

The workflow uses the following libraries:

- [Alfred-PyWorkflow][alfred-pyworkflow] ([MIT License][mit-license])

[alfred-pyworkflow]: https://github.com/harrtho/alfred-pyworkflow
[alfred]: https://www.alfredapp.com
[benzi-ahamed]: https://github.com/BenziAhamed
[benzi-alfred-battery]: https://github.com/BenziAhamed/alfred-battery
[downloads-shield]: https://img.shields.io/github/downloads/harrtho/alfred-battery/total.svg
[gh-issues]: https://github.com/harrtho/alfred-battery/issues
[gh-latest-release]: https://github.com/harrtho/alfred-battery/releases/latest
[gh-releases]: https://github.com/harrtho/alfred-battery/releases
[license-shield]: https://img.shields.io/github/license/harrtho/alfred-battery.svg
[mit-license]: http://opensource.org/licenses/MIT
[preview]: img/preview.png
[version-shield]: https://img.shields.io/github/release/harrtho/alfred-battery.svg
