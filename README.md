# HOL4-dash-hack

A simple hack to build a HOL4 docset for [Dash](https://kapeli.com/dash).

Make sure that you are in the `help` directory in your HOL4 directory:

    python3 -m venv venv
    source ./venv/bin/activate
    pip install BeautifulSoup4 html5lib
    # If you cloned this repository directly to the help directory:
    ./HOL4-dash-hack/dashgen.py

In case you need to re-generate the docset just do `rm -r HOL4.docset` and run `dashgen.py` again.

To import the docset into Dash: The big "Manage Docsets" button -> the "Docsets" tab -> the small plus button in the lower-left corner -> "Add Local Docset" -> pick the `HOL4.docset` folder in your `help` folder.
