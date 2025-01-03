def compact_field_size(hex_string):
    # keep first byte of string as compact size length byte (field length in hex)
    compact_size_hex = hex_string[:2]
    # remove the first byte and convert reminder to a decimal (field length in deci) 
    compact_field_deci = int(hex_string[:2], 16)
    # Get hex value of compact size field.
    hex_value = hex_string[2:]  
    # convert compact size hex value to little endian
    num = bytes.fromhex(hex_value)[::-1].hex()
    # convert compact size hex to decimal 
    decimal = int(num, 16) 
       
    # Return each part of the compactField hex_string 
    return f"""\n------------\ncompact field length in hex:\
    '{compact_size_hex}'\ncompact field length in decimal:\
    {compact_field_deci}\ncompact field value in hex:\
    '{hex_value}'\ncompact field value in decimal:\
    {decimal}\n-------------\n"""

if __name__ == "__main__":
    # hex_strings = ["fe78623a0a", "fcab", "fe99999919", "ffe6ffffff09000000"]
    #
    # for n in hex_strings:
    #     print(compact_field_size(n))

    hex_string = "fdb505"
    print(compact_field_size(hex_string))
