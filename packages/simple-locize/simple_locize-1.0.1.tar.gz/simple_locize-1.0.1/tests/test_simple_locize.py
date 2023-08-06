import os
import unittest
from dotenv import load_dotenv
from simple_locize.simple_locize import SimpleLocize

load_dotenv()

class TestSimpleLocize(unittest.TestCase):
	namespace = os.getenv('LOCIZE_NAMESPACE')
	locize_public = SimpleLocize(os.getenv('LOCIZE_PROJECT_ID'), os.getenv('LOCIZE_ENVIRONMENT'))
	locize_private = SimpleLocize(os.getenv('LOCIZE_PROJECT_ID'), os.getenv('LOCIZE_PRIVATE_ENVIRONMENT'), os.getenv('LOCIZE_PRIVATE_KEY'))

	def test_get_all_translations_from_namespace_public(self):
		test_en = self.locize_public.get_all_translations_from_namespace(self.namespace, 'en')
		test_es = self.locize_public.get_all_translations_from_namespace(self.namespace, 'es')

		self.assertEqual(test_en['one'], 'One')
		self.assertEqual(test_es['one'], 'Uno')
		self.assertEqual(test_en['two']['three'], 'Two Three')
		self.assertEqual(test_es['two']['three'], 'Dos Tres')
		self.assertEqual(test_en['four']['five']['six'], 'Four Five Six')
		self.assertEqual(test_es['four']['five']['six'], 'Quattro Cinco Seis')

	def test_translate_public(self):
		test1 = self.locize_public.translate(self.namespace, 'en', 'one')
		test2 = self.locize_public.translate(self.namespace, 'es', 'one')
		test3 = self.locize_public.translate(self.namespace, 'en', 'two.three')
		test4 = self.locize_public.translate(self.namespace, 'es', 'two.three')
		test5 = self.locize_public.translate(self.namespace, 'en', 'four.five.six')
		test6 = self.locize_public.translate(self.namespace, 'es', 'four.five.six')

		self.assertEqual(test1, 'One')
		self.assertEqual(test2, 'Uno')
		self.assertEqual(test3, 'Two Three')
		self.assertEqual(test4, 'Dos Tres')
		self.assertEqual(test5, 'Four Five Six')
		self.assertEqual(test6, 'Quattro Cinco Seis')

	def test_get_all_translations_from_namespace_private(self):
		test_en = self.locize_private.get_all_translations_from_namespace(self.namespace, 'en')
		test_es = self.locize_private.get_all_translations_from_namespace(self.namespace, 'es')

		self.assertEqual(test_en['one'], 'One')
		self.assertEqual(test_es['one'], 'Uno')
		self.assertEqual(test_en['two']['three'], 'Two Three')
		self.assertEqual(test_es['two']['three'], 'Dos Tres')
		self.assertEqual(test_en['four']['five']['six'], 'Four Five Six')
		self.assertEqual(test_es['four']['five']['six'], 'Quattro Cinco Seis')

	def test_translate_private(self):
		test1 = self.locize_private.translate(self.namespace, 'en', 'one')
		test2 = self.locize_private.translate(self.namespace, 'es', 'one')
		test3 = self.locize_private.translate(self.namespace, 'en', 'two.three')
		test4 = self.locize_private.translate(self.namespace, 'es', 'two.three')
		test5 = self.locize_private.translate(self.namespace, 'en', 'four.five.six')
		test6 = self.locize_private.translate(self.namespace, 'es', 'four.five.six')

		self.assertEqual(test1, 'One')
		self.assertEqual(test2, 'Uno')
		self.assertEqual(test3, 'Two Three')
		self.assertEqual(test4, 'Dos Tres')
		self.assertEqual(test5, 'Four Five Six')
		self.assertEqual(test6, 'Quattro Cinco Seis')
