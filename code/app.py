'''
This module contains code for building the 
Tischendorf New Testament Text-Fabric app,
which visualizes queries and results in TF.
'''

from tf.core.helpers import mdhtmlEsc, htmlEsc
from tf.applib.helpers import dh as display_HTML
from tf.applib.display import prettyPre, getFeatures
from tf.applib.highlight import hlText, hlRep
from tf.applib.api import setupApi
from tf.applib.links import outLink
from textwrap import dedent, indent

plain_link = 'https://github.com/morphgnt/tischendorf-data/tree/master/word-per-line/{version}/Unicode/{bookcode}.txt'
sections = {'book', 'chapter', 'verse'}

class TfApp:

    def __init__(*args, **kwargs):
        '''
        Set up a standard TF API for the app.
        '''
        setupApi(*args, **kwargs)
        
    def webLink(app, n, text=None, className=None, _asString=False, _noUrl=False):
        '''
        Formats an HTML link to a source text
        that contains a supplied TF node.
        '''
                
        # make TF methods available
        api = app.api
        F, T = api.F, api.T
        version = app.version
        
        # get section data for link
        book, chapter, verse = T.sectionFromNode(n)
        book_node = T.nodeFromSection((book,))
        book_code = F.book_code.v(book_node)
        passageText = app.sectionStrFromNode(n)
        
        # format the link
        if not _noUrl:
            href = plain_link.format(version=version, bookcode=book_code)
        else:
            href = '#'
            
        # format the link text
        if text is None:
            text = passageText
            title = 'see this passage in its source document'
        else:
            title = passageText
            
        # return formatted HTML with anchor
        target = '' if _noUrl else None
        link = outLink(text,
                       href,
                       title=title,
                       className=className,
                       target=target,
                       passage=passageText)
        
        # return the link
        if _asString:
            return link
        # or show the link
        else:
            display_HTML(link)
            
    def _plain(app, n, passage, isLinked, _asString, secLabel, **options):
        '''
        Format a plain HTML representation of a TF node.
        '''
        
        # get display settings
        display = app.display
        d = display.get(options)
        
        # prepare api methods
        _asApp = app._asApp # determine whether running in browser?
        api = app.api
        L, T, F = api.L, api.T, api.F
        
        # format and return HTML with format {section}{nodeUTF8}
        # the representation of the node depends on the node type and embedding
        otype = F.otype.v(n)
        result = passage
        
        # configure HTML for node number rendering if requested
        if _asApp:
            nodeRep = f' <a href="#" class="nd">{n}</a> ' if d.withNodes else ''
        else:
            nodeRep = f' <i>{n}</i> ' if d.withNodes else ''
            
        # span class depends on whether node is text
        is_text = d.fmt is None or '-orig-' in d.fmt
            
        # format words
        if otype == 'word':
            rep = hlText(app, [n], d.highlights, fmt=d.fmt)
            
        # format objects bigger than a word
        elif otype not in sections:
            rep = hlText(app, L.d(n, otype='word'), d.highlights, fmt=d.fmt)
            
        # format sections (e.g. book, chapter, verse)
        elif otype in sections:
                                     
            # get the section string
            if secLabel and d.withPassage:
                rep = app.sectionStrFromNode(n)
            else:
                rep = ''
                
            if otype == 'verse':
                
                is_text = True
                
                # wrap section string with hyperlink 
                if isLinked:
                    rep = app.webLink(n, text=rep, className='vn', _asString=True)
                else:
                    rep = f'<span class="vn">{rep}</span>'
                
                # add words contained in the verse
                rep += hlText(app, L.d(n, otype='word'), d.highlights, fmt=d.fmt)
                
            else:
                is_text = False

        # add a text link to non-verse objects
        if isLinked and otype != 'verse':
            rep = app.webLink(n, text=rep, _asString=True)
            
        # finalize span
        tClass = display.formatClass[d.fmt] if is_text else 'trb'
        rep = f'<span class="{tClass}">{rep}</span>'
        result += f'{rep}{nodeRep}'
        
        # deliver
        if _asString or _asApp:
            return result
        else:
            display_HTML(result)
        
    def _pretty(app, n, outer, html, firstSlot, lastSlot, **options):
        '''
        Formats a TF node with pretty HTML.
        '''
    
        # get display settings
        display = app.display
        d = display.get(options)
        
        # preprocess and validate node
        pre = prettyPre(app, n, firstSlot, lastSlot, d.withNodes, d.highlights)
        
        # error out
        if not pre:
            return
        
        # unpackage preprocessed data
        slotType = pre[0] # slot type in databe
        otype = pre[1] # node's object type in database
        className = pre[2] # default div class for this otype
        boundaryClass = pre[3] # ?div class for boundary?
        hlAtt = pre[4] # div class for highlighted nodes
        nodePart = pre[5] # html repre. of node number
        myStart = pre[6] # first slot number in node
        myEnd = pre[7] # last slot number in node
        
        # prepare TF api methods and data
        api = app.api
        F, L, T = api.F, api.L, api.T
        otypeRank = api.otypeRank
        isHtml = options.get('fmt', None) in app.textFormats
        
        # determine size of object
        # objects bigger than condense type will not have
        # any children
        bigType = False
        condense = d.condenseType
        if condense and otypeRank[otype] > otypeRank[condense]:
            bigType = True
            
        # determine whether object is outermost object
        if outer:
            html.append('<div class="outeritem">')
            
        # determine embedded objects to show
        # these will be called recursively
        if bigType or otype in {'word', 'lex'}:
            children = ()
        elif otype == 'verse':
            children = L.d(n, 'word')
            
        # --
        # OPEN the div for the node
        # set the border attribute and other classes accordingly
        # --
                                
        hlClass, hlStyle = hlAtt # highlighting attributes
        
        html.append(f'<div class="{className} {boundaryClass} {hlClass}" {hlStyle}>')
        
        # format section text to appear over all items
        if otype in sections:
            passage = app.webLink(n, _asString=True)
            featurePart = getFeatures(app, n, (), **options)
            
            sectionHTML = f'''
            <div class="ll">
                <div class="line">{passage}</div>
                {nodePart}
                {featurePart}
            </div>
            '''
            sectionHTML = indent(dedent(sectionHTML), '    ')
            html.append(sectionHTML)
            
        elif otype == 'word':
            text = T.text([n], fmt=d.fmt)
            text = htmlEsc(text)
            textHTML = f'<div class="grk">{text}</div>'
            html.append(textHTML)
            
            # do features of word
            nodePart = nodePart or ''
            featurePart = getFeatures(app, n, (), **options)
            html.append(f'{nodePart}{featurePart}')
            
        # format children with recursive call
        for child in children:
            app._pretty(child, False, html, firstSlot, lastSlot, **options)
            
        # --
        # CLOSE the node's div
        # --
        html.append('</div>')
        
        # close outer div if necessary
        if outer:
            html.append('</div>')