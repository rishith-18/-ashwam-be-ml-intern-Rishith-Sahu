from pii_scrubber import process

def test_phone_not_steps():
    e = {"entry_id":"x","text":"Steps today 6234 not phone"}
    assert process(e)["types_found"] == []

def test_email():
    e = {"entry_id":"x","text":"Mail me at a@b.com"}
    assert "EMAIL" in process(e)["types_found"]

def test_overlap():
    e = {"entry_id":"x","text":"Ref APPT-12345 confirmed"}
    assert process(e)["scrubbed_text"].count("[APPT_ID]") == 1
