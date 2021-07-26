import folium                               # იმპორტს ვუკეთებთ folium მოდულს რუქებთან სამუშაოდ
import requests                             # იმპორტს ვუკეთებთ requests მოდულს(რომელიც მიმართავს ვებ გვერდს მონაცემების წამოსაღებად)
from bs4 import BeautifulSoup               # bs4 მოდულიდან იმპორტს ვუკეთებთ BeautifulSoup ბიბლიოთეკას(დაგვეხმარება პარსინგში მიღებული მონაცემების გაფილტვრა)
import pandas                               # იმპორტს ვუკეთებთ pandas მოდულს(დაამუშავებს დათას ანუ მონაცემებს)




def radius_gen(tcases):
    return tcases ** 0.3

def color_gen(tcases):
    if tcases>20000 and tcases<=40000:
        return "red"
    elif tcases>40000 and tcases<50000:
        return "green"
    elif tcases>50000:
        return "blue"




# პარსინგი
# requests.get მეთოდს გადავცემთ გასაპარს ლინკს

r = requests.get("http://treasury.ge/Rates")
c = r.content
soup = BeautifulSoup(c,"html.parser")
data= soup.find("tbody")
rows =data.find_all("tr", {"style":""})

d = {}


for item in rows:
    try:
        tcases=item.find_all("td",{"style":""})[2].text
        d[item.find_all("td")[0].text] = float(tcases.replace(",",""))

    except:
        pass




cdata = pandas.read_csv("countries.csv")
lat = list(cdata["latitude"])
lon = list(cdata["longitude"])
cnt = list(cdata["name"])



# ვქმნით map ობიექტს და მასში folium მოდულის მეთოდებით გადავცემთ რუქის კოორდინატებს(გრძედი-განედი) და ზუმს
map = folium.Map(location=[42.31, 43.35], zoom_start=4, tiles="Stamen Terrain")

# ვსვავთ მარკერს და პოპაპ შეტყობინებას კონკრეტულ კოორდინატზე
fg = folium.FeatureGroup(name="Countries")

for lt,ln,ct in zip(lat,lon,cnt):

    if ct in d.keys():

        fg.add_child(folium.CircleMarker(location=[lt,ln],popup=str(ct) + "\n" + str(d[ct]),
        radius=radius_gen(d[ct]),fill_color=color_gen(d[ct]),color="#ffffff",fill_opasity=0.7))

map.add_child(fg)

# ვინახავთ რუქის ობიექტს html ფორმატში
map.save("GelMap.html")

