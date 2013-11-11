#!/usr/bin/env python
"""

A little helper for manual annotion confirmation/rejection

Test e.g. with

http://127.0.0.1:5000/annotate/a_test_gene

"""
__description__ = ""
__author__ = "Konrad Foerstner <konrad@foerstner.org>"
__copyright__ = "2013 by Konrad Foerstner <konrad@foerstner.org>"
__license__ = "ISC license"
__email__ = "konrad@foerstner.org"
__version__ = ""

from flask import Flask, url_for, render_template, redirect
from flask.ext.bootstrap import Bootstrap
import json
import datetime

# Make the test app also accessible from other machines
externally_accessible = True

app = Flask(__name__)
data_file = "list_annotation.json"

@app.route("/")
def hello():
    return "Welcome!\n"

@app.route("/annotate/<entity_id>")
def annotate(entity_id):
    features = _get_features(entity_id)
    return render_template(
        "annotate.html", 
        entity_id=entity_id,
        status=features["status"],
        offset=features.get("offset", 0),
        mod_time=features["mod_time"],
        fuzziness=features.get("fuzziness", 0),
        confirm_url=url_for("confirm", entity_id=entity_id),
        reject_url=url_for("reject", entity_id=entity_id),
        offset_min_3_url=_offset_url(entity_id, -3),
        offset_min_2_url=_offset_url(entity_id, -2),
        offset_min_1_url=_offset_url(entity_id, -1),
        offset_0_url=_offset_url(entity_id, 0),
        offset_plus_1_url=_offset_url(entity_id, 1),
        offset_plus_2_url=_offset_url(entity_id, 2),
        offset_plus_3_url=_offset_url(entity_id, 3),
        fuzzynes_min_5_url=_fuzziness_url(entity_id, -5),
        fuzzynes_min_4_url=_fuzziness_url(entity_id, -4),
        fuzzynes_min_3_url=_fuzziness_url(entity_id, -3),
        fuzzynes_min_2_url=_fuzziness_url(entity_id, -2),
        fuzzynes_min_1_url=_fuzziness_url(entity_id, -1),
        fuzzynes_0_url=_fuzziness_url(entity_id, 0),
        fuzzynes_plus_1_url=_fuzziness_url(entity_id, 1),
        fuzzynes_plus_2_url=_fuzziness_url(entity_id, 2),
        fuzzynes_plus_3_url=_fuzziness_url(entity_id, 3),
        fuzzynes_plus_4_url=_fuzziness_url(entity_id, 4),
        fuzzynes_plus_5_url=_fuzziness_url(entity_id, 5),
        list_all_url=url_for("list_all"))

def _offset_url(entity_id, offset):
    return url_for("add_offset", entity_id=entity_id, offset=offset)

def _fuzziness_url(entity_id, fuzziness):
    return url_for("set_fuzziness", entity_id=entity_id, fuzziness=fuzziness)

@app.route("/confirm/<entity_id>")
def confirm(entity_id):
    _save_annotation(entity_id, status="confirmed")
    return redirect(url_for("annotate", entity_id = entity_id))

@app.route("/reject/<entity_id>")
def reject(entity_id):
    _save_annotation(entity_id, status="rejected")
    return redirect(url_for("annotate", entity_id = entity_id))

@app.route("/listall")
def list_all():
    mod_time_sorted_entity_ids = [entidy_id for mod_time, entidy_id in sorted(
            [(features["mod_time"], entidy_id) 
             for entidy_id, features in _entities().items()], reverse=True)]
    return render_template(
        "list_all.html", entities=_entities(), 
        mod_time_sorted_entity_ids=mod_time_sorted_entity_ids)

@app.route("/add_offset/<entity_id>/<offset>")
def add_offset(entity_id, offset):
    _save_annotation(entity_id, offset=int(offset))
    return redirect(url_for("annotate", entity_id = entity_id))

@app.route("/set_fuzziness/<entity_id>/<fuzziness>")
def set_fuzziness(entity_id, fuzziness):
    _save_annotation(entity_id, fuzziness=int(fuzziness))
    return redirect(url_for("annotate", entity_id = entity_id))

def _get_features(entity_id):
    entities = _entities()
    return entities.get(entity_id, {"status" : "Undefined", "offset" : 0, 
                                    "fuzziness" : 0, "mod_time" : ""})

def _entities():
    try:
        with open(data_file) as fh:
            return json.load(fh)
    except IOError:
        with open(data_file, "w") as fh:
            fh.write("{}")
            return {}

def _save_annotation(entity_id, status=None, offset=None, fuzziness=None):
    entities = _entities()
    if entity_id in entities:
        if status is None:
            status = entities[entity_id].get("status", "Undefined")
        if offset is None:
            offset = entities[entity_id].get("offset", 0)
        if fuzziness is None:
            fuzziness = entities[entity_id].get("fuzziness", 0)
    else:
        if status is None:
            status = "Undefined"
        if offset is None:
            offset = 0
        if fuzziness is None:
            fuzziness = 0
    entities[entity_id] = {"status" : status, "mod_time" : _now_str(), 
                           "offset" : offset, "fuzziness" : fuzziness}
    with open(data_file, "w") as fh:
        json.dump(entities, fh)

def _now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    Bootstrap(app)
    app.debug = True
    host = "127.0.0.1"
    if externally_accessible is True:
        host = "0.0.0.0"
    app.run(host=host, port=5000)
