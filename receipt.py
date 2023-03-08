import json
import re


class Receipt:
    """ Extract relevant info from an OCR Receipt.

    Attributes
    ----------
    - file : str
        Source OCR output, extracted from JSON File

    Methods
    -------
    - search_pattern(pattern)
        Returns a string that match the given pattern inside the receipt string
    - get_date()
        Returns receipt's date
    - get_address()
        Returns store's address
    - get_invoice_number()
        Returns receipt's number
    - get_all_matches(pattern)
        Returns a list with all pattern matches applied to recepit string
    - get_subtotal()
        Returns receipt's subtotal
    - get_total()
        Returns receipt's total
    - get_raw_sku_and_descriptions
        Returns a list with item's sku and descriptions
    - get_raw_prices()
        Returns a list with item's prices and tax codes
    - get_items_group()
        Returns a list with item's properties
        (SKU, Description, Total, Tax code)
    - get_receipt_dictionary()
        Returns a dictionary with all receipt's variables
        (Date, Store Address, Invoice Number, Subtotal, Total and Items)
    - create_json_file()
        Create a JSON File that contains all receipt's information
    """
    def __init__(self, file_name):
        """
        Constructs file attribute, that is necessary as a source of information
        for other methods.

        Parameters
        ----------
        file_name (str): OCR JSON File path
        """
        with open(file_name, "r") as f:
            data = json.load(f)
        self.file = data['pages'][0]['fullTextAnnotation']['text']

    def search_pattern(self, pattern):
        """
        Use a regular expression (regex) pattern to find a match inside
        of file string.

        Parameters
        ----------
        pattern (str): Regex

        Returns
        -------
        str: Match
        """
        return re.search(pattern, self.file, flags=re.M).group()

    def get_date(self):
        """
        Use a regular expression (regex) pattern to find a string with a
        date format inside a file.

        Parameters
        ----------
        None

        Returns
        -------
        str: Invoice date
        """
        return self.search_pattern(r'^(\d{2}\/){2}(\d{4})$')

    def get_address(self):
        """
        Use a regular expression (regex) pattern to find a string with an
        address format inside a file.

        Parameters
        ----------
        None

        Returns
        -------
        str: Invoice address
        """
        return self.search_pattern(r'.*(?=\nVENDEDOR)')\
            .split("TEL:")[0].strip()

    def get_invoice_number(self):
        """
        Use a regular expression (regex) pattern to find a string with
        the invoice number inside a file.

        Parameters
        ----------
        None

        Returns
        -------
        str: Invoice number
        """
        return self.search_pattern(r'(?<=TIQUETE\s).*')

    def get_all_matches(self, pattern):
        """
        Use a regular expression (regex) pattern to find all ocurrences
        of a string inside a file.

        Parameters
        ----------
        pattern (str): Regex

        Returns
        -------
        list: Matches
        """
        return re.findall(pattern, self.file, flags=re.M)

    def get_subtotal(self):
        """
        Returns the subtotal of the cart, which is the sum of the prices
        of all products in the cart.

        Returns:
        float: The subtotal of the cart.
        """
        self.numbers = [int(x) for x in self.get_all_matches(r'^\d+$')]
        return max(self.numbers)

    def get_total(self):
        """
        Returns the total price of the cart, including taxes and discounts.

        Returns:
        float: The total price of the cart.
        """
        negative_numbers = self.get_all_matches(r'^\d+-$')
        negative_numbers = [
            int(x.replace('-', ''))*-1 for x in negative_numbers
            ]
        discounts = sum(negative_numbers)
        if (self.get_subtotal() + discounts in self.numbers):
            return self.get_subtotal() + discounts
        return self.get_subtotal()

    def get_raw_sku_and_descriptions(self):
        """
        Use a regular expression (regex) pattern to find all item SKUs and
        descriptions inside a file.

        Parameters
        ----------
        None

        Returns
        -------
        list: List with item SKUs and descriptions
        """
        dirty_items = self.get_all_matches(
            r'(?:\b(\d{13})\s(.*)\b\n)|(?:\b(SUBTOTAL)\b\n)?'
        )
        out = []
        for item in dirty_items:
            if (item[0] != '' and item[1] != ''):
                out.append([item[0], item[1]])
            elif (item[2] != ''):
                out.append(['', item[2]])
        return out

    def get_raw_prices(self):
        """
        Use a regular expression (regex) pattern to find all item prices
        and tax codes inside a file.

        Parameters
        ----------
        None

        Returns
        -------
        list: List with item prices and tax codes
        """
        raw_prices = self.get_all_matches(
            r'(?:\b\d+\s?\w?\b\n)+(?:\b[0-9]{3,}\s\w\b\n)+(?:\b\d+\s?\w?\b\n)+'
        )
        prices_list = []
        for elem in raw_prices:
            for elem2 in elem.split('\n'):
                if (elem2 != '' and elem2 != ' '):
                    if (' ' in elem2):
                        elem2 = elem2.split(' ')
                        prices_list.append([elem2[0], elem2[1]])
                    else:
                        prices_list.append([elem2, ''])
        return prices_list

    def get_items_group(self):
        """
        Use the output of get_raw_sku_and_descriptions and
        get_raw_prices methods to create a list with all item
        properties (SKU, description, total and tax code)

        Parameters
        ----------
        None

        Returns
        -------
        list: List with item properties (SKU, description, total and tax code)
        """
        sku_and_descriptions = self.get_raw_sku_and_descriptions()
        prices_and_tax_codes = self.get_raw_prices()
        limit = range(
            min([len(sku_and_descriptions), len(prices_and_tax_codes)])
        )
        for i in limit:
            sku_and_descriptions[i].append(prices_and_tax_codes[i][0])
            sku_and_descriptions[i].append(prices_and_tax_codes[i][1])
        complete_items = []
        for x in sku_and_descriptions:
            if (len(x) == 4 and x[1] != 'SUBTOTAL'):
                complete_items.append(
                    {
                        'sku': int(x[0]),
                        'description': x[1],
                        'total': int(x[2]),
                        'taxCode': x[3]
                    })
        return complete_items

    def get_receipt_dictionary(self):
        """
        Create a dictionary with all receipt's variables: date, store address,
        invoice number, subtotal, total and items.

        Parameters
        ----------
        None

        Returns
        -------
        dict: Dictionary with all receipt's variables
        """
        return {
            'date': self.get_date(),
            'storeAddress': self.get_address(),
            'invoiceNumber': self.get_invoice_number(),
            'subtotal': self.get_subtotal(),
            'total': self.get_total(),
            'lineItems': self.get_items_group()
        }

    def create_json_file(self):
        """
        Create a JSON File that contains all receipt's information.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        receipt_dictionary = self.get_receipt_dictionary()
        json_object = json.dumps(receipt_dictionary, indent=4)
        file_name = "sample"
        invoice = receipt_dictionary['invoiceNumber'].replace(' ', '_')
        if (invoice != ''):
            file_name += f"_{invoice}"
        with open(f"{file_name}.json", "w") as out_file:
            out_file.write(json_object)
        print(f"JSON File created ({file_name}.json)")
        return True


if __name__ == "__main__":
    receipt1 = Receipt("./data/OCR_ticket1.json")
    receipt2 = Receipt("./data/OCR_ticket2.json")
    print(receipt1.get_receipt_dictionary())
    print(receipt2.get_receipt_dictionary())
