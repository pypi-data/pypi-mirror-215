import json
import urllib.request
from functools import reduce

class SimpleLocize:
	project_id = None
	environment = None
	private_key = None
	translations = {}

	def __init__(self, project_id, environment, private_key = None):
		self.project_id = project_id
		self.environment = environment
		self.private_key = private_key

	def fetch_from_locize(self, namespace, language):
		try:
			# API URL
			url = f'https://api.locize.io/{ "private/" if self.private_key else ""}{self.project_id}/{self.environment}/{language}/{namespace}'

			# build request
			request = urllib.request.Request(url)

			if self.private_key:
				request.add_header('Authorization', self.private_key)

			# execute request
			response = urllib.request.urlopen(request)

			# decode JSON
			result = json.loads(response.read())

			# update translations
			if namespace not in self.translations.keys():
				self.translations[namespace] = {}

			if language not in self.translations[namespace].keys():
				self.translations[namespace] = {}

			self.translations[namespace][language] = result

		except:
			# fail
			pass

	def get_all_translations_from_namespace(self, namespace, language):
		if namespace not in self.translations.keys() or language not in self.translations[namespace].keys():
			self.fetch_from_locize(namespace, language)

		if namespace in self.translations.keys() and language in self.translations[namespace].keys():
			return self.translations[namespace][language]

		return {}

	def translate(self, namespace, language, key):
		if namespace not in self.translations.keys() or language not in self.translations[namespace].keys():
			self.fetch_from_locize(namespace, language)

		key_split = key.split('.')

		key_value = key_value = self.translations[namespace][language].get(key, key) if len(key_split) == 1 else reduce(
			lambda acc,
			item: {} if type(acc) is str else acc.get(item, {}),
			key_split,
			self.translations.get(namespace, {}).get(language, {}),
		)

		return key_value if type(key_value) is str else key
