# This is a special test because we corrupt the generated data.
# That is why it does not reuse the standard fixures.

from suitcase.jsonl import Serializer
from bluesky.plans import count
from ophyd.sim import det
from tiled.client import from_tree

from ... import from_files


def test_no_stop_document(RE, tmpdir):
    """
    When a Run has no RunStop document, whether because it does not exist yet
    or because the Run was interrupted in a critical way and never completed,
    we expect the field for 'stop' to contain None.
    """
    directory = str(tmpdir)

    serializer = Serializer(directory)

    def insert_all_except_stop(name, doc):
        if name != 'stop':
            serializer(name, doc)

    RE(count([det]), insert_all_except_stop)
    serializer.close()
    service = from_files.Tree.from_directory(directory)
    client = from_tree(service)
    assert client[-1].metadata['start'] is not None
    assert client[-1].metadata['stop'] is None
