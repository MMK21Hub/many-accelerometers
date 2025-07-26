# Many accelerometers

## Development instructions

### Option A: Setup with `esphome` installed globally

This option is recommended if your operating system provides a package for the `esphome` command-line utility, e.g. [extra/esphome](https://archlinux.org/packages/extra/any/esphome/) on Arch Linux.

1. Install ESPHome globally, e.g. `sudo pacman -S esphome`
2. Clone the repository and open it in VSCode
3. Install the [ESPHome VSCode extension](https://marketplace.visualstudio.com/items?itemName=ESPHome.esphome-vscode) if you haven't already

### Option B: Setup with `esphome` provided by a venv

1. Clone the repository and `cd` into it
2. Create and activate a virtual environment, e.g. `python -m venv venv && source venv/bin/activate`
3. Install ESPHome to the venv: `pip install -r requirements.txt`
4. Open VSCode within the virtual environment: `code .`
5. Install the [ESPHome VSCode extension](https://marketplace.visualstudio.com/items?itemName=ESPHome.esphome-vscode) if you haven't already
