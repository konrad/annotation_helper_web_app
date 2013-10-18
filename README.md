## Purpose ##

This little web app can assist in the manual confirmation/rejection of
features when screening with the [Integrated Genome Browser
(IGB)](http://bioviz.org/) (tested with version 7.0.1). It was
developed to help during the visual inspection of transcription start
sites (TSS) predicted computationally using dRNA-Seq data but can be
used for any other annotation set. Currently it is just a quick hack
which hijacks IGBs web links feature. The data persistency relies only
on a plain text file in JSON format.

## Requirements ##

The packages [Flask](http://flask.pocoo.org/) and
[Flask-Bootstrap](https://pypi.python.org/pypi/Flask-Bootstrap/) need
to be installed.

## Usage ##

### The GFF file ###

You need a GFF file that will be loaded into the IGB. It is very
important that each entry has an **unique** "ID" and "Name" attribute.

### Running the app ###

To start the app just call it:

    $ python annotate.py
     * Running on http://0.0.0.0:5000/
     * Restarting with reloader

If you run it on your local machine you can access the web site at
http://127.0.0.1:5000/listall. If you run it on a different machine
you have to replace 127.0.0.1 by the IP address of that machine. The
page presents a list of all features and should be empty when you run
this for the first time. The app does requires any annotation list but
will generate new entries if a certain URL is accessed. E.g. if you go
to the address

http://127.0.0.1:5000/annotate/my_little_test

The entry for the annotation entry "my_little_test" will be created
and can by modified. On the presented page you can confirm or reject
the entry. You can also set an off-set of -3 to +3 (e.g. if a TSS is
predicted some nucleotides up- or downstream of its actual
position). You can also direct confirm or recect entris by calling the URL

http://127.0.0.1:5000/confirm/my_little_test

or

http://127.0.0.1:5000/reject/my_little_test

respectively.

### Configuring IGB ###

To make use of the web app we need the IGB to call the URL above with
the specific feature IDs. To do so start the IGB, click the "Tool"
button in the menu and select "Configure Web Links". Add the bottom of
the new menu click "Create New". Select the new entry and fill the
following values into the fields:

* Name: Reject
* Regular Expression: .*
* URL Pattern: http://127.0.0.1:5000/reject/$$
* Regular Expression Matches: Annotation ID

If you load your GFF file into the IGB and click with the right mouse
on a feature the pop-up menu should contain an option named "Reject"
(or whatever you wrote in the "Name" field). Clicking this button
should tell IGB to open the link for this specific feature an web
browser. This set-up could be used for a workflow in which you assume
that any feature that you do not reject is accepted. If you want to
use a different workflow you can use a different URL pattern
(e.g. replace "reject" with "confirm"). You have to use a different IP
in the URL pattern if you are not running the app on your local
machine.
