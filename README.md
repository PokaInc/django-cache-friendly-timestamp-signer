# django-cache-friendly-timestamp-signer
Signed URLs that can be kept in browser's cache.

Extension to Django's [django.core.signing.TimestampSigner](https://docs.djangoproject.com/en/1.11/topics/signing/#verifying-timestamped-values) allowing signature to remain identical within a given time frame.
Primary use case is for signed URLs that are fetched by a browser multiple times within a given duration. Making sure the URL (and query params) won't change from request to request will allow a browser to reuse its cached data.

[![Build Status](https://travis-ci.org/PokaInc/django-cache-friendly-timestamp-signer.svg?branch=master)](https://travis-ci.org/PokaInc/django-cache-friendly-timestamp-signer)

## Requirements
* Python: 2.7, 3.4, 3.5, 3.6
* Django 1.11, 2.0

## Installation

Using pip:
```bash
pip install django-cache-friendly-timestamp-signer
```

## Usage

```python
import datetime
from django_cache_friendly_timestamp_signer.signer import TimeFramedTimestampSigner

signer = TimeFramedTimestampSigner(
    time_frame=datetime.timedelta(minutes=30),
)

signer.sign("/my/secret/image.png")

```

### Uniform distribution
Optional (_enabled by default_) `uniform_distribution` option will pseudo-randomly distribute multiple signatures' reference-timestamp across the time frame. Doing so has the effect of limiting the number of URLs for which the signature changes at a given moment. Given a page load with 50 images loaded via signed URLs, limiting the number of rotated signatures to a few will lessen the browser's cache-misses. 