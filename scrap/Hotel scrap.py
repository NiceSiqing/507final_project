import pandas as pd
import SoupCreation


url = 'https://www.tripadvisor.in/Hotels-g34438-Miami_Florida.html-Hotels.html'
# 'https://www.tripadvisor.in/Hotels-g60713-San_Francisco_California-Hotels.html'
# 'https://www.tripadvisor.in/Hotels-g32655-Los_Angeles_California-Hotels.html',
# 'https://www.tripadvisor.in/Hotels-g35805-Chicago_Illinois.html-Hotels.html',
# 'https://www.tripadvisor.in/Hotels-g34438-Miami_Florida.html-Hotels.html',
# 'https://www.tripadvisor.in/Hotels-g45963-Las_Vegas_Nevada.html-Hotels.html',

soup= SoupCreation.createSoup(url)

hotels = []
for name in soup.findAll('div', {'class': 'listing_title'}):
    hotels.append(name.text.replace('Sponsored', '').strip())



ratings = []
for rating in soup.findAll('a', {'class': 'ui_bubble_rating'}):
    ratings.append(rating['alt'])


Numberreviews = []
for review in soup.findAll('a', {'class': 'review_count'}):
    Numberreviews.append(review.text.strip())




reviews=[]
links=[]
def crawlReviews(urls):
    for url in urls:
        tempSoup= SoupCreation.createSoup(url)
        for review in tempSoup.findAll('q', {'class': 'QewHA H4 _a'}):
            reviews.append(review.text)
            links.append(url)

websites=[]
amenitiesList = []
for w in soup.findAll('div', {'class': 'listing_title'}):
    linksForReviews="https://www.tripadvisor.in"+ w.a.get("href")
    print(linksForReviews)
    soup1 = SoupCreation.createSoup(linksForReviews)
    amenities = ""
    for am in soup1.findAll('div', {'class': 'yplav f ME H3 _c'}):
        amenities = am.text + ',' + amenities

    print(amenities)
    amenitiesList.append(amenities)
    websites.append(linksForReviews)

location=[]
Descriptions=[]
def crawlLocationandDescr(urls):
    for url in urls:
        tempSoup = SoupCreation.createSoup(url)
        loc_element = tempSoup.find('span', {'class': 'fHvkI PTrfg'})
        if loc_element:
            location.append(loc_element.text)
        else:
            location.append('NA')

        descr_element = tempSoup.find('div', {'class': 'fIrGe _T'})
        if descr_element:
            Descriptions.append(descr_element.text)
        else:
            Descriptions.append('NA')


crawlReviews(websites)
crawlLocationandDescr(websites)

def fill_missing_values(arrays, fill_value=None):
    max_length = max(len(arr) for arr in arrays)
    return [arr + [fill_value] * (max_length - len(arr)) for arr in arrays]

hotels, ratings, Numberreviews, prices, amenitiesList, websites, location, Descriptions = fill_missing_values(
    [hotels, ratings, Numberreviews, amenitiesList, websites, location, Descriptions], fill_value='NA'
)

dict = {
    'Hotel Names': hotels,
    'Ratings': ratings,
    'Number of Reviews': Numberreviews,
    'amenities': amenitiesList,
    'links': websites,
    'location': location,
    'Description': Descriptions
}


cairo = pd.DataFrame.from_dict(dict)

print(cairo.head(10))

cairo.to_csv('hotels5.csv', index=False, header=True)