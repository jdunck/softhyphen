from google.appengine.ext import webapp
from google.appengine.api import memcache
from google.appengine.ext.webapp import template

import hyphenate_html

class BaseHandler(webapp.RequestHandler):
    def render_template(self, template_name='base.html', values={}):
        values.update({
            'languages': LANGUAGES
        })
        return template.render(template_name, values)
    def hyphenate(self, content, lang):
        return hyphenate_html.hyphenate_html(content, lang,
                                               get_hyphenator(lang))

class HtmlHyphenator(BaseHandler):
    def get(self):
        self.response.out.write(self.render_template('base.html', {
            'lang': 'en-us',
            'lang_name': 'English'
        }))

    def post(self):
        content = self.request.get('content')
        lang = self.request.get('lang', 'en-us')
        output = self.hyphenate(content, lang)
        self.response.out.write(self.render_template('base.html', {
            'content': content,
            'lang': lang,
            'output': output
        }))

class APIHyphenator(BaseHandler):
    def get(self):
        pass #return list of supported langs
    def post(self):
        content = self.request.get('content')
        lang = self.request.get('lang', 'en-us')
        self.response.out.write(self.hyphenate(content, lang))

LANGUAGES = [
    ('cs-cz', 'Czech'),
    ('da-dk', 'Danish'),
    ('de-de', 'German'),
    ('de-ch', 'German (Swiss)'),
    ('el-gr', 'Greek'),
    ('en-ca', 'English (Canadian)'),
    ('en-gb', 'English (UK)'),
    ('en-us', 'English (US)'),
    ('es-es', 'Spanish'),
    ('fi-fi', 'Finish'),
    ('ga-ie', 'Irish'),
    ('hu-hu', 'Hungarian'),
    ('ia', 'Interlingua'),
    ('id-id', 'Indonesian'),
    ('is-is', 'Icelandic'),
    ('it-it', 'Italian'),
    ('lt-lt', 'Lithuanian'),
    ('nl-nl', 'Dutch (Standard)'),
    ('pl-pl', 'Polish'),
    ('pt-br', 'Portuguese (Brazil)'),
    ('pt-pt', 'Portuguese (Portugal)'),
    ('ro-ro', 'Romanian'),
    ('ru-ru', 'Russian'),
    ('sh', 'Serbo-Croatian'),
    ('sk-sk', 'Slovak'),
    ('sl-si', 'Slovenian'),
    ('sr', 'Sorbian'),
    ('sv-se', 'Swedish'),
    ('uk-ua', 'Ukranian')
]
def get_hyphenator(lang='en-us'):
    """Get the hyphenator for language, defaults to en-us

    Uses memcache
    """
    hyphenator = memcache.get('hyp-' + lang)

    if not hyphenator:
        hyphenator = hyphenate_html.get_hyphenator_for_language(lang)
        memcache.set('hyp-' + lang, hyphenator)

    return hyphenator
