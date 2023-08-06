# zhtelecode

`zhtelecode` is a Python package that converts between
[Chinese Telegraph Codes](https://en.wikipedia.org/wiki/Chinese_telegraph_code)
and Unicode Chinese characters (both simplified and traditional).

## Usage

Convert from Unicode to telegraph codes:
```python
>>> zhtelecode.to_telecode("中文信息")
['0022', '2429', '0207', '1873']

>>> zhtelecode.to_telecode("萧爱国")
['5618', '1947', '0948']

>>> zhtelecode.to_telecode("蕭愛國")
['5618', '1947', '0948']
```

Convert from telegraph codes back to Unicode:
```python
>>> telecode = ["0022", "2429", "0207", "1873"]
>>> zhtelecode.to_unicode(telecode)
'中文信息'

>>> telecode = ["5618", "1947", "0948"]
>>> zhtelecode.to_unicode(telecode, encoding="mainland")
'萧爱国'

>>> zhtelecode.to_unicode(telecode, encoding="taiwan")
'蕭愛國'
```

## Data

The codebooks are derived from the Unicode consortium's
[Unihan database](http://www.unicode.org/Public/UNIDATA/Unihan.zip) (last
updated 2022-08-03 17:20).

## License

[MIT License](LICENSE.txt).

Also see [Unicode terms of use](http://www.unicode.org/terms_of_use.html).
