from os.path import dirname, abspath

PROTOCOL = 'http://'
HOST = 'localhost'
PORT = {'kernel':19701,
        'web':9701}

OPTIONS = ()

ORG = 'codykingham'
REPO = 'tischendorf_tf'
CORPUS = 'Tischendorf\'s 8th New Testament'
VERSION = '2.8'
RELATIVE = 'tf'

DOI_TEXT = '10.5281/zenodo.3265458'
DOI_URL = 'https://doi.org/10.5281/zenodo.3265458'

DOC_URL = f'https://github.com/{ORG}/{REPO}/blob/master/docs'
DOC_INTRO = 'features.md'
CHAR_URL = f'https://github.com/{ORG}/{REPO}/blob/master/docs/features.md'
CHAR_TEXT = 'Greek characters transcription',

FEATURE_URL = f'{DOC_URL}/features.md#{{feature}}'

MODULE_SPECS = ()

ZIP = [REPO]

CONDENSE_TYPE = 'verse'

NONE_VALUES = {None, 'NA', 'none', 'unknown'} # TO REVISIT 

STANDARD_FEATURES = '''

qere ketiv 
book chapter verse book_code
gloss

'''.strip().split()

EXCLUDED_FEATURES = set()

NO_DESCEND_TYPES = {}

EXAMPLE_SECTION = (
    f'<code>Matthew 1:1</code> (use'
    f' <a href="https://github.com/{ORG}/{REPO}'
    f'/blob/master/tf/{VERSION}/book%40en.tf" target="_blank">'
    f'English book names</a>)'
)
EXAMPLE_SECTION_TEXT = 'Matthew 1:1'

SECTION_SEP1 = ' '
SECTION_SEP2 = ':'

DEFAULT_CLS = 'trb'
DEFAULT_CLS_ORIG = 'grk'

FORMAT_CSS = {'orig':DEFAULT_CLS_ORIG,
              'trans':DEFAULT_CLS
             }

CLASS_NAMES = {'word':'word',
               'verse':'verse'}

# fonts are from 
FONT_NAME = 'SBL_BLit'
FONT = 'SBL_BLit.ttf'
FONTW = 'SBL_BLit.ttf'

TEXT_FORMATS = {}

BROWSE_NAV_LEVEL = 2
BROWSE_CONTENT_PRETTY = False


def deliver():
    return (globals(), dirname(abspath(__file__)))
