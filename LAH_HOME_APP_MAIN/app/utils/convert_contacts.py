import vobject
import json

vcf_file = 'contacts.vcf'  # Replace with your VCF file name
json_file = 'contacts.json'

def vcf_to_json(vcf_file, json_file):
    """Converts a VCF file to a JSON file with names and numbers."""
    contacts = []
    with open(vcf_file, 'r', encoding='utf-8') as f:
        for vcard in vobject.readComponents(f):
            name = vcard.fn.value if hasattr(vcard, 'fn') else ''
            numbers = [number.value for number in vcard.contents.get('tel', [])
                       if hasattr(number, 'value')]
            contacts.append({'name': name, 'numbers': numbers})

    with open(json_file, 'w') as f:
        json.dump(contacts, f, indent=2)

vcf_to_json(vcf_file, json_file)

