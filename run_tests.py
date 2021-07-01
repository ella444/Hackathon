import json
from midi import *
from qdg import QDG


def test_midi_plays():
    csvdata = pd.read_csv('test_data/session_1.csv')
    try:
        main_playmidi(csvdata)
    except:
        raise Exception('midi.py faild palying midi sample ')

def test_qdg_stats():
    stats_orig = json.loads('{"session_duration": 0, "note duration": {"mean": 1.0183333333333335, "std": 0.9256783367573005, "CV": 0.9090130966520134}, "press velocity": {"mean": 25.802197802197803, "std": 7.530479867697501, "CV": 0.2918542027088895}, "press frequency": {"mean": 3.5, "std": 1.0295630140987, "CV": 0.29416086117105716}}')
    df = pd.read_csv("test_data/session_1.csv")
    stats = QDG(df).get_stats()
    assert stats_orig == stats


