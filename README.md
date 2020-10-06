# Trello cli
Add cards to your trello boards straight from the commandline!

# Pre-requisites
* python 3 (preferably python 3.3 and above)
* pip

# Setup
* Create a virtual env for the project
```
python -m venv cli && cd cli
```

* Extract the tarball inside the virtual env
```
tar xzf trello-cli.tar.gz
```

Now your working directory should look like this
```
$ tree -L 1
.
├── bin
├── include
├── lib
├── lib64 -> lib
├── pyvenv.cfg
└── trello-cli
```
* Create a .env file and add your trello key and token
```
cp .env.example .env
```
If you don't have a key and token they can be generated [here](https://trello.com/app-key)

* Activate the env
```
source bin/activate
```

* Install the cli
```
cd trello-cli && pip install --editable .
```

* Usage
```
$ trello
Usage: trello [OPTIONS] COMMAND [ARGS]...

  Trello command line tool

Options:
  --help  Show this message and exit.

Commands:
  add-card  Work with trello cards
```

* Examples
```
# Add card
$ trello add-card --board "test" --list "list one" --text "buffalo"

# Add card with a comment
$ trello add-card --board "test" --list "list one" --text "buffalo" --comment "tag"

# Add card with a label
$ trello add-card --board "test" --list "list one" --text "buffalo" --label "Important"

# Add card with a label and comment
$ trello add-card --board "cloud test" --list "list one" --text "buffalo" --label "Important" --comment "super"
```