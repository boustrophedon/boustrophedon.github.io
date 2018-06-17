minimalXY0 Pelican Theme
=======================

minimalXY0 [Pelican](https://getpelican.com/) theme is extended from [minimalXY](https://github.com/petrnohejl/MinimalXY) by [petrnohejl](https://github.com/petrnohejl), which is itself extended from [minimalX](https://github.com/art1fa/minimalX) by [art1fa](https://github.com/art1fa).

The goal of this theme is to remove all of the analytics, comments, and social media sharing buttons, remove extra bundled fonts, and integrate the changes between the petrnohejl and art1fa versions.

The RSS, LinkedIn, GitHub icons are from [simple-icons][https://github.com/simple-icons/simple-icons]. To add more, simply download the svgs from their website and put them in the images directory, updating the relevant templates.

Design focus
------------

- Minimal flat design
- Good usability, simple & intuitive navigation
- Focus on what's really important &ndash; your articles
- Presented in a clean and straightforward way


Features
--------

- No comments or analytics
- No bundled font
- No Javascript
- Fully responsive and mobile-first
- W3.CSS CSS framework & HTML5 semantics


How to use
----------

```python
from datetime import date

# Theme
THEME = '/path/to/MinimalXY'

# Theme customizations
MINIMALXY_CUSTOM_CSS = 'static/custom.css'
MINIMALXY_FAVICON = 'favicon.ico'
MINIMALXY_START_YEAR = 2009
MINIMALXY_CURRENT_YEAR = date.today().year

# Author
AUTHOR_INTRO = u'Hello world! I’m John Doe.'
AUTHOR_DESCRIPTION = u'Hello world! I’m John Doe. I like coffee, birds and Python.'

# Social
SOCIAL = (
    ('facebook', 'http://www.facebook.com/johndoe'),
    ('twitter', 'http://twitter.com/johndoe'),
    ('github', 'https://github.com/johndoe'),
    ('linkedin', 'http://www.linkedin.com/in/johndoe'),
)

# Menu
MENUITEMS = (
    ('Categories', '/' + CATEGORIES_SAVE_AS),
    ('Archive', '/' + ARCHIVES_SAVE_AS),
)
```


License
-------

[MIT](LICENSE)
