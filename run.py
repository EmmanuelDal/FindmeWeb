#-*-coding:utf-8-*-
#importation des modules
from flask import Flask, request, render_template
import dns, dns.resolver, geocoder, socket, urllib2
from pierky.ipdetailscache import IPDetailsCache
from folium import Marker, Map
from ipwhois import IPWhois
from geocoder import google

#Fin d'importation des modules

app = Flask(__name__) #creation de l'objet app ou instanciation de la class Flask()

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST': #utilisation de la methode POST pour validation.

        msg = request.form['valeur'] #la variable msg prend comme valeur l'url rentré

        ip4 = socket.gethostbyname(msg)#affichage de l'ipv4

        sta = geocoder.maxmind(ip4) #la variable sta prend comme valeur l'url rentré
        sta1 = sta.json

        asn1 = IPDetailsCache()#instanciation de la classe IPDetailsCache()
        asn1_1 = asn1.GetIPInformation(ip4) #utilisation de la methode GetIPInformation()

        wh = IPWhois(str(ip4))#utilisation de la methode GetIPInformation()
        wh1 = wh.lookup_whois(get_referral=True)#utilisation de la methode GetIPInformation()

        son_r = msg.replace('www.', '')
        repnse = dns.resolver.query(son_r,'MX')#on obtient tout les serveurs de messagerie possible de notre domaine
        contenu = dns.resolver.query(son_r,'NS')#on obtient tout les serveurs DNS possible de notre domaine

        url = urllib2.urlopen("http://{0}".format(son_r))#on ouvre notre url grace a la methode urlopen du module urllib2
        url_result = dict(url.info())#recuperation de toute les reponse HTTP possible sur en provenance du serveur

        dat_a = google(str(msg))
        carto = Map(location=[dat_a.lat, dat_a.lng], zoom_start=15)
        Marker([dat_a.lat, dat_a.lng], popup=str(msg)).add_to(carto)
        carto.save('templates/cartographie.html')


        return render_template('resultat.html', ip4=ip4,
                               msg=msg, sta1=sta1,
                               asn1_1 = asn1_1, wh1=wh1,
                               repnse=repnse, contenu=contenu,
                               url_result=url_result)

    return render_template("acceuil.html") #affichage de la page d'acceuil

@app.route('/localisation-geographique')
def carte():
    return render_template("cartographie.html")

#interception des erreures 500 et 404
@app.errorhandler(500)
def eror_500(error):
    url = request.form['valeur']
    return render_template("erreurs/erreur_500.html", url=url), 500

@app.errorhandler(400)
def eror_400(error):
    url = request.form['valeur']
    return render_template("erreurs/erreur_400.html", url=url), 400
#fin d'interception des erreures 500 et 400

if __name__ == "__main__":
    app.run(debug=True) #Lancement de notre application web