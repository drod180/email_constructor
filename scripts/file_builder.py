import spreadsheet_parser
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
#######################Block Strings######################
module_types = {
    'Full Width': "    include ../components/full_width_card",
    'Left Image': "    include ../components/image_left_card",
    'Right Image': "    include ../components/image_right_card",
    'Half Width (right)': "    include ../components/half_width_card",
    'Half Width (left)': "    include ../components/half_width_card",
    'Partner': "    include ../components/partners_module",
    'BYO': "    include ../content-sections/byo_module"
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

module_vars_byo = """
    -var image_url = byo_image_url
    -var image_link_url = byo_image_link_url
    -var section_headline = byo_headline
    -var section_data = byo_series
    -var section_data_tracking_parameter = byo_url_tracking_parameter
    -var height = "auto"
"""

email_start_text = """
extends ../templates/%s_Template

block copy_import
    include ../copy/%s_Copy

block content_area_1
    // Header Bar
    include ../content-sections/preheader_bar
"""
content_area_text = """

block content_area_%s"""

template_start_text = """
include ../scripts/helper-functions
include ../mixins/main
include ../stylesheets/main
block stylesheet_import
    // No stylesheet import
block copy_import
    // No copy import

|#{"\\n"}

doctype transitional
html(xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office")
    head
        title
            block header_title
                | BMW Email

        +meta_tag_headers
        +web_font_declarations

        style(type="text/css")
            include ../stylesheets/embed.css
        <!--[if (gte mso 9)|(IE)]>
        style(type="text/css")
            include ../stylesheets/outlook_embed.css
        <td><![endif]-->
    body(style=body_style)
        +table(table_style, "center", "100%")
            tr
                td(style=td_style) &nbsp;
                td(style=td_style) &nbsp;
                td(style=td_style) &nbsp;

            tr(style=body_style)
                td(style=td_style)
                td(style=td_style width="600")
                    +if_outlook
                        +table(table_style+body_style, "center", "100%")

"""

template_content_areas = """
                            tr
                                td(style=td_style)
                                    block content_area_%s
                                        h1 Content Area %s
"""

template_content_areas_card = """
                            tr
                                td(style=td_style + card)
                                    block content_area_%s
                                        h1 Content Area %s
"""
template_content_sections = """
                            tr
                                td(style=td_style)
                                    include ../content-sections/%s
"""

template_content_spacer = """
                            tr
                                td(style=td_style) &nbsp;
"""

template_end_text = """
                td(style=td_style)
"""

copy_start_text = """
- var static_image_path = "images/"
- var image_path = "images/"

//- Email Components
- var email_subject = "%s"

- var email_preheader = "%s"
- var view_in_browser_link_url = ""
- var view_in_browser_link_text = "View in Browser"

"""

copy_module_text = """
//- %s Overview
- var %s_hero_image_url = image_path + ""
- var %s_hero_image_link_url = "%s"
- var %s_logo_image = ""
- var %s_headline = "%s"
-
    var %s_body = %s
-
    var %s_cta_data = %s
-
    var %s_legal = %s
"""

copy_end_text = """
//- Footer
- var footer_copy = "%s"
//- END
"""

open_bracket = """
    {
"""

close_bracket = """
    }"""

close_bracket_comma = """
    },"""

close_array = """
    ]"""

copy_byo_text = """
//- Build Your Own
- var byo_headline = "BUILD YOUR OWN BMW."
- var byo_image_link_url = "https://www.bmwusa.com/byo.html"
- var byo_image_url = image_path+"eExclusive_BYO.jpg"
- var byo_url_tracking_parameter = ""
-
    var byo_series = [
    {
    'name':'2',
    'url':'2',
    'parameter':'Series='
    },{
    'name':'3',
    'url':'3',
    'parameter':'Series='
    },{
    'name':'4',
    'url':'4',
    'parameter':'Series='
    },{
    'name':'5',
    'url':'5',
    'parameter':'Series='
    },{
    'name':'6',
    'url':'6',
    'parameter':'Series='
    },{
    'name':'7',
    'url':'7',
    'parameter':'Series='
    },{
    'name':'X',
    'url':'X',
    'parameter':'Series='
    },{
    'name':'BMWi',
    'url':'BMWi',
    'parameter':'Series='
    },{
    'name':'M',
    'url':'M',
    'parameter':'Series='
    },{
    'name':'View All',
    'url':'2,3,4,5,6,7,X,M,BMWi',
    'parameter':'Series='
    }
    ]
"""
#######################End of Block Strings######################



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
    if module_type == 'BYO':
        module_text += module_vars_byo
    else:
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
        email_text += build_module_text((i == 0),
                                        email_data[i + 1]['moduleName'],
                                        email_data[i + 1]['moduleType'],
                                        i + 2)

    return email_text

#email_name: String - Name of email used for file name
#email_text: String - Email text to buid file with
def build_email_file(email_name, parsed_data):
    email_text = build_emails_text(email_name, parsed_data)
    email_file_name = "/../emails/%s_Email.pug" % (email_name)
    with open(dir_path + email_file_name, 'w') as out_file:
        out_file.writelines(email_text)

#parsed_data: array of dictionaries - all parsed data
#link: Bool - Include bmw links content section or not
def build_template_text(parsed_data, links = True):
    template_text = template_start_text
    for i in range(0, int(parsed_data[0]['Number of Modules'])  +  1):
        if ('moduleType' in parsed_data[i].keys() and
            (parsed_data[i]['moduleType'] == 'Left Image' or
            parsed_data[i]['moduleType'] == 'Right Image')):
            template_text += template_content_areas_card % (i + 1, i + 1)
        else:
            template_text += template_content_areas % (i + 1, i + 1)
        if i != 0:
            template_text += template_content_spacer

    if links:
        template_text += template_content_sections % ("footer_bmw_links")
    template_text += template_content_sections % ("social_media")
    template_text += template_content_sections % ("footer_legalese")
    template_text += template_end_text

    return template_text

#email_name: String - Name of email used for file name
#template_text: String - Template text to buid file with
def build_template_file(email_name, parsed_data):
    template_text = build_template_text(parsed_data,
                            parsed_data[0]['BMW Links (Footer)'] == 'Include')
    template_file_name = "/../templates/%s_Template.pug" % (email_name)
    with open(dir_path + template_file_name, 'w') as out_file:
        out_file.writelines(template_text)

#body_data: String - body copy
def build_body_text(body_data):
    body_text = "["
    if body_data != "":
        body_data_split = body_data.splitlines()
        for i, copy in enumerate(body_data_split):
            body_text += open_bracket
            body_text += "   'body_text': \"%s\"" % (copy)
            if i == len(body_data_split) - 1:
                body_text += close_bracket
            else:
                body_text += close_bracket_comma
    body_text += close_array

    return body_text

#legal_data: String - legal copy
def build_legal_text(legal_data):
    legal_text = "["
    if legal_data != "":
        legal_data_split = legal_data.splitlines()
        for i, copy in enumerate(legal_data_split):
            legal_text += open_bracket
            legal_text += "   'legal_text': \"%s\"" % (copy)
            if i == len(legal_data_split) - 1:
                legal_text += close_bracket
            else:
                legal_text += close_bracket_comma
    legal_text += close_array

    return legal_text

#cta_color: String - word to be swapped with appropriate keyword
def cta_color_swap(cta_color):
    if cta_color == "Primary":
        return "brand_color"
    else:
        return "brand_color_alt"

#module_data: dictionary - all the module data
def build_cta_text(module_data):
    cta_text = "["

    for i in range(0, int(module_data['ctaCount'])):
        cta_dict = {}
        cta_dict['cta_key_copy'] = "cCopy" + str(i)
        cta_dict['cta_key_url'] = "cUrl" + str(i)
        cta_dict['cta_key_type'] = "cType" + str(i)
        cta_dict['cta_key_color'] = "cColor" + str(i)

        cta_text += open_bracket
        cta_text += "   'cta_text': \"%s\",\n" % \
            (module_data[cta_dict['cta_key_copy']])
        cta_text += "   'cta_type': \"%s\",\n" % \
            (module_data[cta_dict['cta_key_type']].lower())
        cta_text += "   'cta_color': %s,\n" % \
            (cta_color_swap(module_data[cta_dict['cta_key_color']]))
        cta_text += "   'cta_link_url': \"%s\"" % \
            (module_data[cta_dict['cta_key_url']])
        if i == int(module_data['ctaCount']) - 1:
            cta_text += close_bracket
        else:
            cta_text += close_bracket_comma
    cta_text += close_array
    return cta_text

#module_name: String - Name of the module used for variable names
#module_data: Dictionary - Data used for variable values
def build_module_copy(module_name, module_data):
    if module_data['moduleType'] == "BYO":
        module_copy_text = copy_byo_text
    else:
        if 'cUrl0' in module_data.keys():
            url_text = module_data['cUrl0']
        else:
            url_text = ""
        headline_text = module_data['headline']
        body_text = build_body_text(module_data['bodyCopy'])
        cta_text = build_cta_text(module_data)
        legal_text = build_legal_text(module_data['legalCopy'])

        module_copy_text = copy_module_text % (module_name,
                                               module_name,
                                               module_name,
                                               url_text,
                                               module_name,
                                               module_name,
                                               headline_text,
                                               module_name,
                                               body_text,
                                               module_name,
                                               cta_text,
                                               module_name,
                                               legal_text)

    return module_copy_text

#module_count: Int - Number of modules in email_name
#copy_data: Array of Dictionaries - All the parsed data
def build_copy_text(copy_data):
    copy_text = copy_start_text % (copy_data[0]['Subject Line'],
                                   copy_data[0]['Preheader Copy'])
    for i in range(0, int(copy_data[0]['Number of Modules'])):
        copy_text += build_module_copy(copy_data[i + 1]['moduleName'],
                                       copy_data[i + 1])
                                       
    copy_text += copy_end_text % (copy_data[0]['Additional Legal'])
    return copy_text

def build_copy_file(email_name, parsed_data):
    copy_text = build_copy_text(parsed_data)
    copy_file_name = "/../copy/%s_Copy.pug" % (email_name)
    with open(dir_path + copy_file_name, 'w') as out_file:
        out_file.writelines(copy_text)

def build_files():
    #Parse Data
    parsed_data = spreadsheet_parser.parse()
    email_name = parsed_data[0]['Email Name']
    #Build Email File
    build_email_file(email_name, parsed_data)
    #Build template
    build_template_file(email_name, parsed_data)
    #Build copy
    build_copy_file(email_name, parsed_data)


############################ Run Script ####################################
build_files()
