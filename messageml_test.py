import unittest
from messageml import serialize


class TestMessageML(unittest.TestCase):

    def test_serialize_text(self):
        obj = {
            'type': 'text',
            'value': 'Hello World'
        }
        serialized = serialize(obj)
        self.assertEqual(serialized, 'Hello World')

    def test_serialize_text_linebreak(self):
        obj = {
            'type': 'text',
            'value': 'Hello World\nMore Stuff'
        }
        serialized = serialize(obj)
        self.assertEqual(serialized, 'Hello World<br/>More Stuff')

    def test_serialize_table(self):
        obj = {
            'type': 'table',
            'value': {
              'columns': ['Name', 'Price'],
              'data': [
                {'type': 'text', 'value': 'Some name'},
                {'type': 'text', 'value': '$10'},
                {'type': 'text', 'value': 'Some More name'},
                {'type': 'text', 'value': '$15'},
              ]
            }
        }
        serialized = serialize(obj)
        self.assertEqual(serialized, 
        """
				<table>
					<tr>
						<td>Name</td>
						<td>Price</td>
					</tr>
					<tr>
						<td>Some name</td>
						<td>$10</td>
					</tr>
					<tr>
						<td>Some More name</td>
						<td>$15</td>
					</tr>
				</table>
				""".replace("\t", "").replace("\n", ""))


if __name__ == '__main__':
    unittest.main()
