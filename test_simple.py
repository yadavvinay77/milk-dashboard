#!/usr/bin/env python3
"""
Simple ASCII-only test script for CI/CD
"""

try:
    import flask
    print("FLASK: OK")
    
    import flask_sqlalchemy
    print("FLASK_SQLALCHEMY: OK")
    
    import flask_migrate
    print("FLASK_MIGRATE: OK")
    
    import pandas
    print("PANDAS: OK - version " + pandas.__version__)
    
    import numpy
    print("NUMPY: OK - version " + numpy.__version__)
    
    import xlsxwriter
    print("XLSXWRITER: OK")
    
    # Test basic functionality
    from app.utils.calculations import calc_amount
    result = calc_amount(10, 0.220, 190)
    print("CALCULATION_TEST: PASSED - result: " + str(result))
    
    print("ALL_TESTS_PASSED")
    
except Exception as e:
    print("ERROR: " + str(e))
    exit(1)
