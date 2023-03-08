
# OCR Receipt Data Extraction

This code extracts information from an OCR receipt in JSON format using regular expressions to match patterns.

## Requirements

This script requires Python 3.x to be installed on the system. Additionally, the following Python packages are required:

- re
- json
- pytest (for running unit tests)

## Installation (pytest)

pytest requires: Python 3.7+ or PyPy3

Install pytest with pip

```bash
  pip install -U pytest
```

## Programming paradigm

This code uses Object-Oriented Programming (OOP) paradigm in Python. The main class Receipt contains attributes and methods to extract the relevant data from the OCR output.

## Assumptions

This code assumes that the input JSON file has OCR output in the "fullTextAnnotation" key of the "pages" array of the JSON object. If there is no OCR output in that location, the code will fail.

This code also assumes that the receipt has a certain structure, such as the presence of a date, address, invoice number, and item prices in the text. If these elements are not present or are in a different format, the code may not extract the correct information.

## Coding Style

This script was developed following the PEP8 style guide for Python code.

## Usage

The script can be run from the command line with the following command:

```bash
  python receipt.py
```
Output file first ticket:

```bash
  {
    "date": "10/12/2021",
    "storeAddress": "AVENIDA CALLE 80 No 69Q- 50",
    "invoiceNumber": "J122 249302",
    "subtotal": 86160,
    "total": 86160,
    "lineItems": [
        {
            "sku": 8410270241140,
            "description": "Aceite oliva SU",
            "total": 27990,
            "taxCode": "N"
        },
        {
            "sku": 7707322030489,
            "description": "Quinua QUINOACL",
            "total": 7990,
            "taxCode": "A"
        },
        {
            "sku": 7707322030489,
            "description": "Quinua QUINOACL",
            "total": 7990,
            "taxCode": "A"
        },
        {
            "sku": 8004690751060,
            "description": "Cous cous LA MO",
            "total": 8990,
            "taxCode": ""
        },
        {
            "sku": 7702247011056,
            "description": "YOGURT LIQUIDO",
            "total": 2650,
            "taxCode": "N"
        },
        {
            "sku": 8410971033785,
            "description": "Aceitunas EXCEL",
            "total": 3490,
            "taxCode": ""
        },
        {
            "sku": 7707298470074,
            "description": "Tallarines BEST",
            "total": 8790,
            "taxCode": "A"
        },
        {
            "sku": 7702085003497,
            "description": "Quinua molida D",
            "total": 8690,
            "taxCode": "A"
        },
        {
            "sku": 7705326077837,
            "description": "Tortillinas BIM",
            "total": 5990,
            "taxCode": "N"
        },
        {
            "sku": 7702253800002,
            "description": "Maiz pira TOT-R",
            "total": 3590,
            "taxCode": ""
        }
    ]
}
```
## Testing

This script has been tested using pytest, with the tests located in the test_receipt_ticket1.py and test_receipt_ticket2.py files. To run the tests, simply run the following command:

```bash
  pytest -v
```
Note that currently, the script is failing to obtain the tax codes for one of the example invoices.

```bash
  ================================================== test session starts ===================================================
platform win32 -- Python 3.9.6, pytest-7.2.2, pluggy-1.0.0 -- d:\python 3.9.6\python.exe
cachedir: .pytest_cache
rootdir: ******
collected 12 items

test_receipt_ticket1.py::test_json_date PASSED                                                                      [  8%]
test_receipt_ticket1.py::test_json_store_address PASSED                                                             [ 16%] 
test_receipt_ticket1.py::test_json_invoice_number PASSED                                                            [ 25%] 
test_receipt_ticket1.py::test_json_subtotal PASSED                                                                  [ 33%] 
test_receipt_ticket1.py::test_json_total PASSED                                                                     [ 41%] 
test_receipt_ticket1.py::test_json_line_items FAILED                                                                [ 50%]
test_receipt_ticket2.py::test_json_date PASSED                                                                      [ 58%] 
test_receipt_ticket2.py::test_json_store_address PASSED                                                             [ 66%] 
test_receipt_ticket2.py::test_json_invoice_number PASSED                                                            [ 75%] 
test_receipt_ticket2.py::test_json_subtotal PASSED                                                                  [ 83%] 
test_receipt_ticket2.py::test_json_total PASSED                                                                     [ 91%]
test_receipt_ticket2.py::test_json_line_items PASSED                                                                [100%] 

======================================================== FAILURES ======================================================== 
__________________________________________________ test_json_line_items __________________________________________________ 

    def test_json_line_items():
        """
        Check if each line item in the JSON file generated by create_json_file()
        is equal to the corresponding line item in the sample JSON file.
        """
        with open("./data/valid_ticket1.json", "r") as f:
            true_data = json.load(f)
        with open("./sample_J122_249302.json", "r") as f:
            my_data = json.load(f)
        for i in range(len(my_data)):
            assert my_data['lineItems'][i]['sku'] \
                == true_data['lineItems'][i]['sku']
            assert my_data['lineItems'][i]['description'] \
                == true_data['lineItems'][i]['description']
            assert my_data['lineItems'][i]['total'] \
                == true_data['lineItems'][i]['total']
>           assert my_data['lineItems'][i]['taxCode'] \
                == true_data['lineItems'][i]['taxCode']
E           AssertionError: assert '' == 'A'
E             - A

test_receipt_ticket1.py:85: AssertionError
================================================ short test summary info ================================================= 
FAILED test_receipt_ticket1.py::test_json_line_items - AssertionError: assert '' == 'A'
```


## Author

- [@samuelgit95](https://github.com/samuelgit95)

