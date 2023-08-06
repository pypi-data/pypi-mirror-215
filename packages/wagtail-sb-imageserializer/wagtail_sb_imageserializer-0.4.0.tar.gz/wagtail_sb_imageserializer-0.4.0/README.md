![Community-Project](https://gitlab.com/softbutterfly/open-source/open-source-office/-/raw/master/banners/softbutterfly-open-source--banner--community-project.png)

![PyPI - Supported versions](https://img.shields.io/pypi/pyversions/wagtail-sb-imageserializer)
![PyPI - Package version](https://img.shields.io/pypi/v/wagtail-sb-imageserializer)
![PyPI - Downloads](https://img.shields.io/pypi/dm/wagtail-sb-imageserializer)
![PyPI - MIT License](https://img.shields.io/pypi/l/wagtail-sb-imageserializer)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/329484ea99434c708f5c8dbd611f3d35)](https://app.codacy.com/gl/softbutterfly/wagtail-sb-imageserializer/dashboard?utm_source=gl&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Coverage Badge](https://app.codacy.com/project/badge/Coverage/900411c7b5e443f89f85c7978f7504e5)](https://app.codacy.com/gl/softbutterfly/wagtail-sb-imageserializer/dashboard?utm_source=gl&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)

# Wagtail Image Serializer

Wagtail package to render images with rendition in a single API Field.

## Requirements

- Python 3.8.1 or higher
- Wagtail 3.0 or higher
- Django 3.2 or higher
- Django Rest Framework 3.13 or higher

## Install

```bash
pip install wagtail-sb-imageserializer
```

## Usage

Add `wagtail.api.v2`, `rest_framework` and `wagtail_sb_imageserializer` to your `INSTALLED_APPS` settings

```
INSTALLED_APPS = [
  # ...
  "wagtail.api.v2",
  "rest_framework",
  "wagtail_sb_imageserializer",
  # ...
]
```

In your model specify the `ImageSerializerField` as serializer for the `APIField` related to the image field and add the `renditions` parameter with the renditions you want to render.

```python
from wagtail.models import Page
from wagtail.api import APIField
from wagtail_sb_imageserializer.fields import ImageSerializerField

class SamplePage(Page):
    image = ImageSerializerField()

    api_fields = [
        APIField(
          "image",
          serializer=ImageSerializerField(
              renditions={
                  "lazy": "fill-50x50",
                  "mobile": "fill-128x128",
                  "tablet": "fill-256x256",
                  "desktop": "fill-512x512",
              }
          ),
        ),
    ]
```

When yo require your page from the API, the image filed will looks like this

```json
{
    "id": 1234567890,
    "meta": {
        "type": "wagtailimages.Image",
        "title": "Image title",
        "alt": "Image alt text"
    },
    "original": {
        "width": 123456788890,
        "height": 123456788890,
        "download_url": "https://your-cdn-domain/path/to/original_images/image_name.png"
    },
    "renditions": {
        "lazy": {
            "width": 50,
            "height": 50,
            "download_url": "https://your-cdn-domain/path/to/reditions/image_name.fill-50x50.png"
        },
        "mobile": {
            "width": 128,
            "height": 128,
            "download_url": "https://your-cdn-domain/path/to/reditions/image_name.fill-128x128.png"
        },
        "tablet": {
            "width": 256,
            "height": 256,
            "download_url": "https://your-cdn-domain/path/to/reditions/image_name.fill-256x256.png"
        },
        "desktop": {
            "width": 512,
            "height": 512,
            "download_url": "https://your-cdn-domain/path/to/reditions/image_name.fill-512x512.png"
        }
    }
},
```

## Docs

- [Ejemplos](https://gitlab.com/softbutterfly/open-source/wagtail-sb-imageserializer/-/wikis)
- [Wiki](https://gitlab.com/softbutterfly/open-source/wagtail-sb-imageserializer/-/wikis)

## Changelog

All changes to versions of this library are listed in the [change history](CHANGELOG.md).

## Development

Check out our [contribution guide](CONTRIBUTING.md).

## Contributors

See the list of contributors [here](https://gitlab.com/softbutterfly/open-source/wagtail-sb-imageserializer/-/graphs/develop).
