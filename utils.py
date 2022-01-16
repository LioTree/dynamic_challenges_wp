import re
import os

def secure_filename(filename):
    """
    修改自werkzeug.utils.secure_filename，使其支持中文
    """
    _filename_ascii_add_strip_re = re.compile(r'[^A-Za-z0-9_\u4E00-\u9FBF.-]')

    if isinstance(filename, str):
        from unicodedata import normalize
        filename = normalize('NFKD', filename).encode('utf-8', 'ignore').decode('utf-8')
    for sep in os.path.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, ' ')
    
    filename = str(_filename_ascii_add_strip_re.sub('', '_'.join( 
                filename.split()))).strip('._')
    return filename