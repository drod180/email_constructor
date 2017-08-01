import spreadsheet_parser

module_types = {
    'Full Width': "    include ../components/full_width_card",
    'Left Image': "    include ../components/image_left_card",
    'Right Image': "    include ../components/image_right_card",
    'Half Width (right)': "    include ../components/half_width_card",
    'Half Width (left)': "    include ../components/half_width_card",
    'Partner': "    include ../components/partners_module",
    }

module_vars_standard = """
    -var image_link_url = %s_hero_image_link_url
    -var image_url = %s_hero_image_url
    -var section_headline = %s_headline
    -var section_body = %s_body
    -var cta_data = %s_cta_data
    -var promo_legal = %s_legal
    -var logo_image = %s_logo_image
    -var injected_header_style = %s
    -var injected_text_style = ""
    -var side_margin = "30"
    -var height = "auto"
"""
email_start_text = """
extends ../templates/%s_template

block copy_import
    include ../copy/%s_Copy

block content_area_1
    // Header Bar
    include ../content-sections/preheader_bar
"""
content_area_text = """

block content_area_%s"""


#hero: Bool - value for if module is hero module
#module_name: String - Name of the module used for variable names
#module_type: String - Key for modules_types dictionary
#content_area: int - Content area value
def build_module_text(hero, module_name, module_type, content_area):
    if (hero):
        headline_style = 'headline_feature'
    else:
        headline_style = '""'
    module_text = content_area_text % (content_area)
    module_text += module_vars_standard % (module_name,
                                          module_name,
                                          module_name,
                                          module_name,
                                          module_name,
                                          module_name,
                                          module_name,
                                          headline_style)
    module_text += module_types[module_type]
    return module_text

#email_name: String - Name of email
#email_data: Array of Dictionaries - Data parsed form CSV file
def build_emails_text(email_name, email_data):
    email_text = email_start_text % (email_name, email_name)
    for i in range (0, int(email_data[0]['Number of Modules'])):
        email_text += build_module_text((i == 1),
                                        email_data[i + 1]['moduleName'],
                                        email_data[i + 1]['moduleType'],
                                        i + 1)

    return email_text

#email_name: String - Name of email used for file name
#email_text: String - Email text to buid file with
def build_email_file(email_name, email_text):
    email_name = "../emails/%s_Email.pug" % (email_name)
    with open(email_name, 'w') as out_file:
        out_file.writelines(email_text)

def build_files():
    parsed_data = spreadsheet_parser.parse()
    email_name = parsed_data[0]['Email Name']
    email_text = build_emails_text(email_name, parsed_data)
    build_email_file(email_name, email_text)

build_files()
