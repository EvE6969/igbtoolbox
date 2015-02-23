## IGB Toolbox - a platform for creating EVE online web applications

### Motivation

The IGB toolbox has been created as a platform for creating web based tools for EVE Online. It provides basic functionality for interacting with the IGB, access restriction and working with the EVE APIs. The key idea is that multiple individual tools can be added into a single application instead of having them to run standalone with their own setup requirements.

The server side stack is very simple. Applications are served by Tornado using Python 3. MongoDB is used as default database. Python has been chosen as language as it's very versatile and easy to learn. Developers should be able to get started quickly without having to learn complex frameworks.

Client side JavaScript code has also been designed with simplicity in mind. [React](http://reactjs.com/) and [FlightJS](http://flightjs.github.io/) is used to create JavaScript components which are decoupled and interact with each other based on events. You are however not stuck using these framworks and can in fact use any JavaScript framework you like, as generated events are just custom DOM events.

[Bower](http://bower.io/) is used as package manager to include JavaScript dependencies. However, it's also used to include individual tools when setting up you own toolbox instance. To make this possible, each tool must adhere a certain convention on where certain JavaScript and Python files can be found. Read more on how to create custom modules [here](http://TODO).

### Available applications

The following applications are available to be used in a IGB toolbox setup:

* [Signatures](https://github.com/igbtoolbox/evesignatures) -  collaborative signature scanning tool

### Available modules

The following list of modules can be used to create new applications for the IGB toolbox:

* [Portal](https://github.com/igbtoolbox/eveportal) - basic portal components
* [IGB](https://github.com/igbtoolbox/eveigb) - basic IGB related functionalities
* [Simple Authentication](https://github.com/igbtoolbox/eveauthnsimple) - basic access control
* [Simple Authorization](https://github.com/igbtoolbox/eveauthzsimple) - basic permission management
* [EVE XML API](https://github.com/igbtoolbox/evexmlapi) - support for using the official XML API
* [Spatial](https://github.com/igbtoolbox/evespatial) -
EVE universe graph algorithms
* [Messagebus](https://github.com/igbtoolbox/evemessagebus) - WebSockets emulation for the IGB
* [Auto Complete](https://github.com/igbtoolbox/eveautocomplete) - input auto-completion
* [Static Data Export](https://github.com/igbtoolbox/evesde) - JavaScript SDE access using [EVEoj](http://eve-oj.xyjax.com/)
* [FlightJS](https://github.com/igbtoolbox/eveflightjs) - FlightJS integration


### Setting up a development environment

There're two ways to create a development environment to get started with the IGB toolbox. First you need to clone the project to a local directory. The easiest way is to use Vagrant from there.

#### Using Vagrant

Vagrant can be used to bootstrap a fully working development environment in a custom virtual machine. Please install Vagrant according to the [installation instructions](http://docs.vagrantup.com/v2/installation/index.html). Then simply run `vagrant up` in the projects root directory.

Please be patient during the first time the VM is started. It will take some time to provision it with all required packages. In case the setup is getting aborted with an error try to run `vagrant provision` to try again. Afterwards you should be able to login using `vagrant ssh`. You'll find the project files in the `/vagrant` directory.

#### Manual Installation

If you don't want to use Vagrant for some reason you can also install a custom dev environment with the following steps. Fortunately you can use most of the scripts creating for Vagrant which can be found at `scripts/bootstrap-*.sh`.

* [Install MongoDB](https://www.mongodb.org/)
* Install Python 3 and virtualenv (see `scripts/bootstrap-python.sh` for Ubuntu)
* Install Python requirements in a new virtualenv space (see `scripts/bootstrap-venv.sh`)
* Install NodeJS and node developer tools incl. git (see `scripts/bootstrap-node.sh`)

#### Creating a JavaScript build

All individual JavaScript files will be bundled using [webpack](https://webpack.github.io/). To create a build you need to setup and login into the dev environment as described above. For vagrant, change to the project dir:
* `vagrant ssh`
* `cd /vagrant`

Create a build:
* `npm run build` or for production `npm run minimize`

#### Starting the Server

Change to the project directory (e.g. `/vagrant`) and run `scripts/start.sh --debug` to start the server. You should see the server output on your console. Afterwards you should be able to access the server from `http://localhost:8080/`. At this point the toolbox will be empty except from the about page. You'll have to install [applications](#available-applications) for more content. Hit CTRL+C in the console to stop the server.

#### Server Configuration

A local config file will be created after starting the server for the first time. You'll have to edit the file at `/home/vagrant/.igbtoolbox.yml` and add your alliance in `host_alliance_id`. Restart the server afterwards.

#### Setting up a Browser Instance to Emulate the IGB

Although you should be able to access the toolbox at `http://localhost:8080` from any browser, you'll most likely not see any modules except the about page. You should therefor install some useful add-ons for your browser to make it behave like the IGB and send additional informations such as your corp or alliance.

First you need to enable your browser to identify as the IGB. Recommended add-ons:

 * Chrome: [Ultimate User Agent Switcher](https://chrome.google.com/webstore/detail/ultimate-user-agent-switc/ljfpjnehmoiabkefmnjegmpdddgcdnpo?hl=en-US)
 * Firefox: [User Agent Switcher](http://chrispederick.com/work/user-agent-switcher/)

Use the following user agent string: `Mozilla/5.0 (X11; Linux x86_64; rv:6.0.1) Gecko/20100101 Firefox/6.0.1 EVE-IGB`

Next you need a way to add the IGB header to your browsers requests. Recommended add-ons:

 * Chrome: [Header Hacker](https://chrome.google.com/webstore/detail/header-hacker/phnffahgegfkcobeaapbenpmdnkifigc?hl=en-US)
 * Firefox: [Modify Headers](http://www.garethhunt.com/modifyheaders/)

You need to add the following headers (provided values are examples):
 * EVE_SOLARSYSTEMID - 30003620
 * EVE_SOLARSYSTEMNAME - ZXA-V6
 * EVE_ALLIANCEID - 123123123 (use dotlan! should match alliance id in server config)
 * EVE_ALLIANCENAME - My Alliance
 * EVE_CORPID - 123123123
 * EVE_CORPNAME - My Corp
 * EVE_CHARID - 123123123
 * EVE_CHARNAME	- Its me
 * EVE_SHIPTYPEID	- 11978
 * EVE_TRUSTED - Yes


### Deploying to Production

Please follow the steps described in Manual Installation except for the NodeJS tools. Afterwards you can use a tool like `rsync` to deploy the project to the server, see `scripts/sync-*` for examples.
