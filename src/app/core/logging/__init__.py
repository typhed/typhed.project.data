# -*- encoding: utf-8 -*-

"""
Structured Logging Configuration - TyPhed Project Data Core
-----------------------------------------------------------

Configures the root logger with a single stream handler that emits one
JSON object per line. JSON logs are trivially parseable by log shippers
(Loki, the ELK stack, CloudWatch, ...) which keeps the service observable
in production without pulling in a third-party logging dependency.
"""

