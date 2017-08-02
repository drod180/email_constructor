import spreadsheet_parser


#######################Block Strings######################
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
- var %s_logo_image = image_path + ""
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
    email_file_name = "../emails/%s_Email.pug" % (email_name)
    with open(email_file_name, 'w') as out_file:
        out_file.writelines(email_text)

#content_count: Int - Number of content blocks
#link: Bool - Include bmw links content section or not
def build_template_text(module_count, links = True):
    template_text = template_start_text
    for i in range(0, module_count  +  1):
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
def build_template_file(email_name, template_text):
    template_file_name = "../templates/%s_Template.pug" % (email_name)
    with open(template_file_name, 'w') as out_file:
        out_file.writelines(template_text)

#body_data: String - body copy
def build_body_text(body_data):
    body_text = "["
    if body_data != "":
        body_data_split = body_data['bodyCopy'].splitlines()
        print(body_data_split)
        body_text += "{"
        body_text += "'body_text': \"%s\""
        body_text += "}"
    body_text = "]"



#module_name: String - Name of the module used for variable names
#module_data: Dictionary - Data used for variable values
def build_module_copy(module_name, module_data):
    if 'cUrl0' in module_data.keys():
        url_text = module_data['cUrl0']
    else:
        url_text = ""
    headline_text = module_data['headline']
    body_text = build_body_text(module_data['bodyCopy'])
    cta_text = ""
    legal_text = ""
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

def build_files():
    #Parse Data
    parsed_data = spreadsheet_parser.parse()
    #Build Email File
    email_name = parsed_data[0]['Email Name']
    email_text = build_emails_text(email_name, parsed_data)
    #build_email_file(email_name, email_text)
    #Build template
    template_text = \
        build_template_text(int(parsed_data[0]['Number of Modules']))
    #build_template_file(email_name, template_text)
    build_body_text(parsed_data[1]['bodyCopy'])
    build_body_text(parsed_data[2]['bodyCopy'])
    build_body_text(parsed_data[3]['bodyCopy'])
build_files()
