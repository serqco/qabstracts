import qabs.annotations

annots = qabs.annotations.Annotations()  # global, for reuse to read codebook only once


def test_codings_of():
    assert annots.codings_of("background") == {'background'}
    assert annots.codings_of("objective method") == {'objective', 'method'}
    assert annots.codings_of("claim,-hype") == {'claim', '-hype'}
    assert annots.codings_of("h-method, a-method") == {'h-method', 'a-method'}
    assert annots.codings_of("method:i0, result:u33") == {'method:i0', 'result:u33'}
    assert annots.codings_of("method:i0, result:u33", strip_suffixes=True) == {'method', 'result'}


def test_find_all_sentence_and_annotation_pairs():
    input = "title\n\nL1\nL2\n{{ann}}\nL11\nL21\n{{ann1}}\nL3\n{{ann2}}\n---"
    output = annots.find_all_sentence_and_annotation_pairs(input)
    print(output)
    assert output[2].annotation == "{{ann2}}"


def test_is_empty_annotation():
    assert annots.is_empty_annotation("{{}}")
    assert annots.is_empty_annotation("{{ }}")
    assert annots.is_empty_annotation("{{  }}")
    assert not annots.is_empty_annotation("{{ a}}")