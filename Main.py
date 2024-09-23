import eel
from functions import AI


@eel.expose
def Movie(movie_name, is_ind):
    print("Movie")
    if is_ind:
        links = AI.get_Ind_Movie_quality_links(movie_name)
        eel.Send_Quality_links(links)
    else:
        links = AI.get_NonInd_Movie_quality_links(movie_name)
        eel.Send_Quality_links(links)
@eel.expose
def Series(series_name, is_ind,season_no):
    if is_ind:
        links = AI.get_Ind_Series_quality_links(series_name,season_no)
        eel.Send_Quality_links(links)
    else:
        links = AI.get_NonInd_Series_quality_links(series_name,season_no)
        eel.Send_Quality_links(links)

@eel.expose
def Download(link):
    if link.startswith("https://links.modpro.blog/"):
        links = AI.Download_link(link)
        eel.Final_link(links)
    elif link.startswith("https://leechpro.blog/"):
        links = AI.Download_link(link)
        eel.Final_link(links)
    else:
        eel.Final_link(" You can manually download it from here: " + link)

eel.init('ui')
eel.start('index.html')