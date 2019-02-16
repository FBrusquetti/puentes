import requests
import json
import bs4
import io

foo = requests.get("https://puentes.mopc.gov.py/")
bridges_dirty = (foo.text[foo.text.find("bridges.push"):foo.text.find("var map;")]).split(";")
bridges_dirty.pop()#elimina el ultimo elemento del array que es un \n
bridges=[]
for bridge in bridges_dirty:
    bridge_aux = bridge[bridge.find("{"):bridge.find(")")] #se elmina el bridges.push
    bridge_aux= bridge_aux.replace("'", '"')
    bridge_aux = bridge_aux.replace("lat", '"lat"')
    bridge_aux= bridge_aux.replace("lng", '"lng"')
    bridge_aux = bridge_aux.replace("icon:", '"icon":')
    bridge_aux = bridge_aux.replace("url", '"url"')
    bridge_object_py=json.loads(bridge_aux)
    bridge_object_py['url_final']="https://puentes.mopc.gov.py"+bridge_object_py['url']
    bridges.append(bridge_object_py)

final_bridges=[]
for bridge in bridges:
    request_bridge = requests.get(bridge['url_final'])
    soup = bs4.BeautifulSoup(request_bridge.text, 'html.parser')
    divs = (soup.find_all('div'))
    print(bridge)
    for div in divs:
        if (div.get('id')) == 'info':
            for div2 in div.children:
                if isinstance(div2, bs4.element.Tag):
                    for div3 in div2.children:
                        if isinstance(div3, bs4.element.Tag) and div3.get('id') != 'bridge_carousel':
                            bridge[div3.label.text] = div3.p.span if div3.p.text is None else div3.p.text
                            '''print(div3.label.text)
                            print( div3.p.span if div3.p.text is None  else div3.p.text)'''

        if (div.get('id')) == 'job-orders':
            for div2 in div.children:
                if isinstance(div2, bs4.element.Tag):
                    if (div2.table.tbody.tr.td.text) == 'El puente aún no ha tenido intervenciones.':
                        bridge['Intervención'] = 'NO'
                    else:
                        bridge['Intervención'] = 'SI'

    final_bridges.append(bridge)

with io.open('puentes.json', 'w', encoding='utf8') as json_file:
    json.dump(final_bridges, json_file, ensure_ascii=False,indent=4, sort_keys=True)

print(json.dumps(final_bridges))











