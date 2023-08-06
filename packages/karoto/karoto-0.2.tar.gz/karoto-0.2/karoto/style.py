_item_height = 18
_sixty = "white"
_thirty = "#fdc033"
_ten = "#80e241"

default = f"""
* {{
    background-color: {_sixty};
    font-size: 14px;
    color: black;
}}

QPushButton {{
    height: {_item_height}px;
    background-color: {_ten};
    border: 1px solid grey;
    border-radius: {_item_height/2}px;
    padding-top: 3px;
    padding-bottom: 3px;
    padding-left: 10px;
    padding-right: 10px;
}}

QLineEdit {{
    border-radius: 10px;
    padding: 2px;
    background-color: {_sixty};
}}

QLabel, QCheckBox {{
    background-color: {_thirty};
}}

.top_bar {{
    min-height: 40px;
    qproperty-iconSize: 40px;
}}

#error_bar QLabel {{
    min-height: 40px;
    font-weight: bold;
    padding-top: 3px;
    padding-bottom: 3px;
    padding-left: 10px;
    padding-right: 10px;
}}

.WARNING {{
    background-color: yellow;
}}

.ERROR {{
    background-color: red;
}}

#menu_button {{
    min-width: 60px;
}}

#search_field {{
    padding-left: 6px;
    border: 1px solid grey;
}}

QGroupBox {{
    background-color: {_thirty};
    border-radius: 6px;
}}

.short_line_edit {{
    width: 40px;
}}

.single_char_button {{
    padding: 2px;
    border: 1px solid grey;
    border-radius: {_item_height/2}px;
    width: {_item_height}px;
    height: {_item_height}px;
    font-weight: bold;
}}

QPushButton:disabled {{
    border: 1px solid #77AA77;
    background-color: #88BB88;
    color: #777777;
}}
"""

# Source: https://tabler-icons.io/ search for "filter"
filter_plus_icon_svg = b"""
<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler
icon-tabler-filter-plus" width="24" height="24" viewBox="0 0 24 24"
stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round"
stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <path d="M12 20l-3 1v-8.5l-4.48 -4.928a2 2 0 0 1 -.52
   -1.345v-2.227h16v2.172a2 2 0 0 1 -.586 1.414l-4.414 4.414v3"></path>
   <path d="M16 19h6"></path>
   <path d="M19 16v6"></path>
</svg>
"""

filter_minus_icon_svg = b"""
<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler
icon-tabler-filter-minus" width="24" height="24" viewBox="0 0 24 24"
stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round"
stroke-linejoin="round">
   <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
   <path d="M12 20l-3 1v-8.5l-4.48 -4.928a2 2 0 0 1 -.52
   -1.345v-2.227h16v2.172a2 2 0 0 1 -.586 1.414l-4.414 4.414v3"></path>
   <path d="M16 19h6"></path>
</svg>
"""

# Source: https://feathericons.com/?query=cart and
#         https://feathericons.com/?query=home (modified with Inkscape)
menu_home_icon_svg = b"""
<svg
   width="50"
   height="24"
   viewBox="0 0 13.229168 6.3499998"
   version="1.1"
   id="svg5"
   xml:space="preserve"
   sodipodi:docname="home.svg"
   inkscape:version="1.2.2 (b0a8486541, 2022-12-01)"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg"><sodipodi:namedview
     id="namedview7"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:showpageshadow="2"
     inkscape:pageopacity="0.0"
     inkscape:pagecheckerboard="0"
     inkscape:deskcolor="#d1d1d1"
     inkscape:document-units="mm"
     showgrid="false"
     inkscape:zoom="8.1933293"
     inkscape:cx="22.823445"
     inkscape:cy="20.809612"
     inkscape:window-width="1362"
     inkscape:window-height="744"
     inkscape:window-x="0"
     inkscape:window-y="0"
     inkscape:window-maximized="1"
     inkscape:current-layer="layer1" /><defs
     id="defs2" /><g
     inkscape:label="Ebene 1"
     inkscape:groupmode="layer"
     id="layer1"><g
       style="fill:none;fill-opacity:1;stroke:#535353;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;stroke-opacity:1"
       id="g342"
       transform="matrix(0.17637215,0,0,0.15656522,0,1.5875)"><circle
         cx="9"
         cy="21"
         r="1"
         id="circle327"
         style="fill:none;fill-opacity:1;stroke:#535353;stroke-opacity:1" />
       <circle
         cx="20"
         cy="21"
         r="1"
         id="circle329"
         style="fill:none;fill-opacity:1;stroke:#535353;stroke-opacity:1" />
       <path
         d="m 1,1 h 4 l 2.68,13.39 a 2,2 0 0 0 2,1.61 h 9.72 a 2,2 0 0 0 2,
         -1.61 L 23,6 H 6"
         id="path331"
         style="fill:none;fill-opacity:1;stroke:#535353;stroke-opacity:1" />
           </g><g
       style="fill:none;stroke:currentColor;stroke-width:2;
       stroke-linecap:round;stroke-linejoin:round"
       id="g958"
       transform="matrix(0.28863671,0,0,0.28863671,6.8575182,-0.28864441)">
       <path
         d="m 3,9 9,-7 9,7 v 11 a 2,2 0 0 1 -2,2 H 5 A 2,2 0 0 1 3,20 Z"
         id="path946" /><polyline
         points="9 22 9 12 15 12 15 22"
         id="polyline948" /></g></g></svg>
"""

menu_cart_icon_svg = b"""
<svg
   width="50"
   height="24"
   viewBox="0 0 13.229168 6.3499998"
   version="1.1"
   id="svg5"
   xml:space="preserve"
   sodipodi:docname="cart.svg"
   inkscape:version="1.2.2 (b0a8486541, 2022-12-01)"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg"><sodipodi:namedview
     id="namedview7"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:showpageshadow="2"
     inkscape:pageopacity="0.0"
     inkscape:pagecheckerboard="0"
     inkscape:deskcolor="#d1d1d1"
     inkscape:document-units="mm"
     showgrid="false"
     inkscape:zoom="8.1933293"
     inkscape:cx="22.88447"
     inkscape:cy="20.687561"
     inkscape:window-width="1362"
     inkscape:window-height="744"
     inkscape:window-x="0"
     inkscape:window-y="0"
     inkscape:window-maximized="1"
     inkscape:current-layer="layer1" /><defs
     id="defs2" /><g
     inkscape:label="Ebene 1"
     inkscape:groupmode="layer"
     id="layer1"><g
       style="fill:none;fill-opacity:1;stroke:#000000;stroke-width:2;
         stroke-linecap:round;stroke-linejoin:round;stroke-opacity:1"
       id="g342"
       transform="scale(0.31101448,0.27608696)"><circle
         cx="9"
         cy="21"
         r="1"
         id="circle327"
         style="fill:none;fill-opacity:1;stroke:#000000;stroke-opacity:1" />
       <circle
         cx="20"
         cy="21"
         r="1"
         id="circle329"
         style="fill:none;fill-opacity:1;stroke:#000000;stroke-opacity:1" />
       <path
         d="m 1,1 h 4 l 2.68,13.39 a 2,2 0 0 0 2,1.61 h 9.72 a 2,2 0 0 0 2,
         -1.61 L 23,6 H 6"
         id="path331"
         style="fill:none;fill-opacity:1;stroke:#000000;stroke-opacity:1" />
           </g><g
       style="fill:none;stroke:#545454;stroke-width:2;stroke-linecap:round;
         stroke-linejoin:round;stroke-opacity:1"
       id="g958"
       transform="matrix(0.19242448,0,0,0.19242448,8.981401,0.81298705)">
       <path
         d="m 3,9 9,-7 9,7 v 11 a 2,2 0 0 1 -2,2 H 5 A 2,2 0 0 1 3,20 Z"
         id="path946"
         style="stroke:#545454;stroke-opacity:1" /><polyline
         points="9 22 9 12 15 12 15 22"
         id="polyline948"
         style="stroke:#545454;stroke-opacity:1" /></g></g></svg>
"""
