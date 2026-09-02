# -*- coding: utf-8 -*-
"""Génère les pages HTML du site à partir d'un gabarit commun."""
import os, io

OUT = os.path.dirname(os.path.abspath(__file__))

# --- Coordonnées : modifiez ici, c'est répercuté sur toutes les pages ---
TEL_TXT  = "[06 XX XX XX XX]"
TEL_HREF = "+33600000000"
MAIL     = "contact@mobilecarcleaning.fr"
SITE     = "https://mobilecarcleaning.fr"

NAV = [
    ("services.html",     "Services"),
    ("detailing.html",    "Rénovation"),
    ("b2b.html",          "Pros &amp; flottes"),
    ("realisations.html", "Réalisations"),
    ("journal.html",      "Journal"),
    ("a-propos.html",     "À propos"),
]

def head(title, desc, page, extra=""):
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- ===== SEO : titre et description de CETTE page ===== -->
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#06070F">
<link rel="canonical" href="{SITE}/{page}">

<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">

<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}/{page}">
<meta property="og:image" content="{SITE}/assets/hero.jpg">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=Instrument+Sans:wght@400;500;600&display=swap" rel="stylesheet">

<!-- Tous les styles du site sont dans ce fichier unique -->
<link rel="stylesheet" href="assets/style.css">
{extra}</head>
<body>
<a class="skip" href="#main">Aller au contenu principal</a>

<!-- ============================================================
     EN-TÊTE — identique sur toutes les pages.
     Si vous le modifiez, reportez la modification sur chaque page.
     ============================================================ -->
<header class="header">
  <div class="wrap header__inner">
    <a class="brand" href="index.html" aria-label="Mobile Car Cleaning, accueil">
      <img src="assets/logo.png" alt="Mobile Car Cleaning" width="492" height="160">
    </a>

    <button class="burger" id="burger" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="nav">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>

    <nav class="nav" id="nav" aria-label="Navigation principale">
""" + "".join(
        f'      <a href="{h}"{" aria-current=\"page\"" if h == page else ""}>{lbl}</a>\n'
        for h, lbl in NAV
    ) + """      <a class="btn btn--primary btn--sm" href="reserver.html">Réservez</a>
    </nav>

    <a class="btn btn--primary btn--sm header__cta" href="reserver.html">Réservez</a>
  </div>
</header>

<main id="main">
"""

FOOT = f"""</main>

<!-- ============================================================
     PIED DE PAGE — identique sur toutes les pages
     ============================================================ -->
<footer class="footer">
  <div class="wrap">
    <div class="footer__cols">
      <div class="footer__brand">
        <img src="assets/logo.png" alt="Mobile Car Cleaning" width="492" height="160">
        <p>Lavage et nettoyage automobile mobile en Alsace. Sur rendez-vous, 7 jours sur 7.</p>
      </div>
      <div>
        <h3>Prestations</h3>
        <ul>
          <li><a href="services.html">Lavage extérieur</a></li>
          <li><a href="services.html">Nettoyage intérieur</a></li>
          <li><a href="services.html">Formule complète</a></li>
          <li><a href="detailing.html">Rénovation</a></li>
          <li><a href="b2b.html">Pros &amp; flottes</a></li>
        </ul>
      </div>
      <div>
        <h3>Le site</h3>
        <ul>
          <li><a href="realisations.html">Réalisations</a></li>
          <li><a href="journal.html">Journal</a></li>
          <li><a href="a-propos.html">À propos</a></li>
          <li><a href="reserver.html">Réserver</a></li>
        </ul>
      </div>
      <div>
        <h3>Zone</h3>
        <ul>
          <li><span>Strasbourg</span></li>
          <li><span>Mulhouse</span></li>
          <li><span>Colmar</span></li>
          <li><span>Saint-Louis</span></li>
        </ul>
      </div>
    </div>

    <div class="footer__legal">
      <p>© <span id="year">2026</span> Mobile Car Cleaning — Micro-entreprise · SIREN [à compléter]<br>
         TVA non applicable, article 293 B du CGI</p>
      <p><a href="mentions-legales.html">Mentions légales</a> &nbsp;·&nbsp;
         <a href="confidentialite.html">Confidentialité</a></p>
    </div>
  </div>
</footer>

<script src="assets/main.js"></script>
</body>
</html>
"""

# Bloc réservation Cal.com réutilisable
def cal_block(title="Réservez votre créneau",
              intro="Choisissez le jour et l'heure qui vous arrangent. Confirmation immédiate par email."):
    return f"""
<!-- ============================================================
     RÉSERVATION — WIDGET CAL.COM
     Relié au compte Cal.com : cal.com/mobilecarcleaningeu
     ============================================================ -->
<section class="section" id="booking">
  <div class="wrap">
    <div class="head">
      <h2>{title}</h2>
      <p>{intro}</p>
    </div>
    <div class="booking__frame">
      <div id="my-cal-inline">
        <p class="booking__fallback">Chargement du calendrier…<br>Si rien ne s'affiche, appelez-nous au {TEL_TXT}.</p>
      </div>
    </div>
  </div>
</section>
"""

CAL_SCRIPT = """
<!-- ============================================================
     WIDGET CAL.COM — début
     Compte relié : cal.com/mobilecarcleaningeu
     Pour changer, modifiez calLink ci-dessous.
     ============================================================ -->
<script type="text/javascript">
(function (C, A, L) { let p = function (a, ar) { a.q.push(ar); }; let d = C.document; C.Cal = C.Cal || function () { let cal = C.Cal; let ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; } if (ar[0] === L) { const api = function () { p(api, arguments); }; const namespace = ar[1]; api.q = api.q || []; if (typeof namespace === "string") { cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ["initNamespace", namespace]); } else p(cal, ar); return; } p(cal, ar); }; })(window, "https://app.cal.com/embed/embed.js", "init");

Cal("init", "lavage", { origin: "https://cal.com" });

Cal.ns["lavage"]("inline", {
  elementOrSelector: "#my-cal-inline",
  config: { "layout": "month_view", "theme": "light" },
  calLink: "mobilecarcleaningeu"   /* votre page Cal.com : toutes vos formules y sont listées */
});

Cal.ns["lavage"]("ui", { "hideEventTypeDetails": false, "layout": "month_view" });
</script>
<!-- WIDGET CAL.COM — fin -->
"""

def ph(fichier, ratio="16x9", quoi="", classe=""):
    """Emplacement photo. Remplacez le <span> par <img src=...> le moment venu."""
    return (f'<div class="ph ph--{ratio}{(" " + classe) if classe else ""}">'
            f'<span><b>Photo à ajouter</b>{quoi}<br><code>assets/{fichier}</code></span></div>')


def pagehead(crumb, h1, lede, bg=None):
    """bg = nom du fichier image de fond, ou None pour un fond dégradé simple."""
    media = ""
    if bg:
        media = f"""  <!-- IMAGE DE FOND : déposez le fichier dans assets/ sous ce nom exact.
       Tant qu'il n'existe pas, le dégradé reste affiché. -->
  <div class="pagehead__media">
    <img src="assets/{bg}" alt="" onerror="this.remove()">
  </div>
  <p class="ph-hint">Image de fond : <code>assets/{bg}</code></p>
"""
    return f"""
<!-- ===== BANDEAU DE TITRE ===== -->
<section class="pagehead">
{media}  <div class="wrap">
    <p class="crumb"><a href="index.html">Accueil</a> — {crumb}</p>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
</section>
"""

def write(name, body, title, desc, extra="", script=""):
    html = head(title, desc, name, extra) + body + FOOT.replace(
        "<script src=\"assets/main.js\"></script>",
        "<script src=\"assets/main.js\"></script>" + script)
    with io.open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(html)
    print("  " + name)

# ============================================================
#  PAGE D'ACCUEIL
# ============================================================
HOME = """
<!-- ============================================================
     HERO — la vidéo est dans assets/hero.mp4 (compressée, muette).
     Pour la changer : remplacez le fichier en gardant le même nom.
     ============================================================ -->
<section class="hero">
  <div class="hero__media">
    <video autoplay muted loop playsinline poster="assets/hero.jpg" aria-hidden="true">
      <source src="assets/hero.mp4" type="video/mp4">
    </video>
  </div>

  <div class="wrap hero__inner">
    <div>
      <p class="badge"><span class="dot"></span> Alsace — <b>on se déplace 7j/7</b></p>
      <h1>Le lavage auto qui vient à vous</h1>
      <p class="lede">Chez vous, au bureau, sur le parking de l'entreprise. Sans eau courante si vous n'en avez pas, au jet si vous préférez.</p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="reserver.html">Réserver un créneau</a>
        <a class="btn btn--ghost" href="services.html">Voir les services</a>
      </div>
    </div>

    <!-- ===== SÉLECTEUR DE FORMULE : choisir puis réserver ===== -->
    <aside class="tile">
      <div class="tile__head">
        <h2>Choisissez votre formule</h2>
        <span>Citadine</span>
      </div>

      <label class="pick" data-label="Extérieur" data-cal="exterieur">
        <input type="radio" name="formule" value="exterieur">
        <span class="pick__row">
          <span class="pick__name">Express extérieur<small class="pick__meta">45 minutes</small></span>
          <span class="tile-price">39 €</span>
        </span>
      </label>

      <label class="pick" data-label="Intérieur" data-cal="interieur">
        <input type="radio" name="formule" value="interieur">
        <span class="pick__row">
          <span class="pick__name">Intérieur<small class="pick__meta">1 heure</small></span>
          <span class="tile-price">49 €</span>
        </span>
      </label>

      <label class="pick" data-label="Complet" data-cal="complet">
        <input type="radio" name="formule" value="complet" checked>
        <span class="pick__row">
          <span class="pick__name">Complet<small class="pick__meta">1 h 45 — le plus choisi</small></span>
          <span class="tile-price">79 €</span>
        </span>
      </label>

      <a class="btn btn--primary btn--full" id="pick-cta" href="reserver.html">Réserver</a>
      <p class="tile__note">Sans acompte. Annulation libre jusqu'à 24 h avant.</p>
    </aside>
  </div>
</section>

<!-- ===== BANDEAU DÉFILANT (texte dupliqué pour la boucle) ===== -->
<div class="marquee" aria-hidden="true">
  <div class="marquee__track">
    <span>Lavage à domicile</span><span>Sans rinçage ou au jet</span><span>Sans restriction sécheresse</span><span>Strasbourg · Mulhouse · Colmar</span><span>Sur rendez-vous</span>
    <span>Lavage à domicile</span><span>Sans rinçage ou au jet</span><span>Sans restriction sécheresse</span><span>Strasbourg · Mulhouse · Colmar</span><span>Sur rendez-vous</span>
  </div>
</div>

<!-- ===== DÉCLARATION ===== -->
<section class="section claim">
  <div class="wrap">
    <h2>Pas de station.</h2>
    <h2>Pas de file d'attente.</h2>
    <div class="claim__foot">
      <p>Vous donnez une adresse et un créneau. On arrive avec l'eau, les produits et le matériel. Vous récupérez la voiture propre sans avoir bougé.</p>
      <p>Le prix est fixé avant l'intervention. Pas de supplément découvert au moment de payer, pas de vente additionnelle sur le pas de la porte.</p>
    </div>
    """ + ph("intervention-domicile.jpg", "wide", " — plan large : la voiture en cours de lavage devant chez le client", "ph--band") + """
  </div>
</section>

<!-- ===== FORMULES ===== -->
<section class="section section--deep" id="services">
  <div class="wrap">
    <div class="head">
      <h2>Le lavage, à la carte</h2>
      <p>Tarifs pour une citadine. Berline, break et SUV un cran au-dessus.</p>
    </div>

    <div class="grid-svc">
      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 17h14M3 17v-5l2-5h14l2 5v5"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Express extérieur</h3><span class="svc__price">39 €</span></div>
          <p>L'entretien régulier, en moins d'une heure.</p>
          <ul><li>Carrosserie lavée et séchée à la microfibre</li><li>Jantes, passages de roue et bas de caisse</li><li>Vitres et rétroviseurs</li></ul>
          <a class="btn btn--ghost btn--full" href="reserver.html">Réserver</a>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20v-6a4 4 0 0 1 4-4h8a4 4 0 0 1 4 4v6"/><path d="M9 10V6a3 3 0 0 1 6 0v4"/><path d="M3 20h18"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Intérieur</h3><span class="svc__price">49 €</span></div>
          <p>Aspiration en profondeur et surfaces remises à neuf.</p>
          <ul><li>Aspiration sièges, tapis et coffre</li><li>Plastiques, console et aérateurs</li><li>Vitres intérieures</li></ul>
          <a class="btn btn--ghost btn--full" href="reserver.html">Réserver</a>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v3M5.6 5.6l2.1 2.1M3 12h3M18 12h3M16.3 7.7l2.1-2.1"/><circle cx="12" cy="14" r="5"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Complet</h3><span class="svc__price">79 €</span></div>
          <p>L'extérieur et l'intérieur dans le même rendez-vous.</p>
          <ul><li>Tout l'Express extérieur</li><li>Tout l'Intérieur</li><li>Seuils de porte et montants</li></ul>
          <a class="btn btn--primary btn--full" href="reserver.html">Réserver</a>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a9 9 0 1 1-3.3-6.9"/><path d="M21 4v5h-5"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Abonnement</h3><span class="svc__price">35 €<small>/mois</small></span></div>
          <p>Un créneau réservé chaque mois, sans y penser.</p>
          <ul><li>Le rendez-vous est posé à l'avance</li><li>Report possible sur le mois suivant</li><li>Engagement de 3 mois seulement</li></ul>
          <a class="btn btn--ghost btn--full" href="services.html">En savoir plus</a>
        </div>
      </article>
    </div>
  </div>
</section>

<!-- ===== DEUX MÉTHODES : sans rinçage ou au jet ===== -->
<section class="section">
  <div class="wrap">
    <div class="head">
      <h2>Deux méthodes, selon votre situation</h2>
      <p>On s'adapte à ce dont vous disposez. Vous n'avez rien à préparer : dites-nous simplement à la réservation si un point d'eau et une prise sont accessibles.</p>
    </div>

    <div class="duo">
      <article class="method method--lead">
        <span class="method__tag">Par défaut — partout</span>
        <h3>Lavage sans rinçage</h3>
        <p>Notre méthode standard. La saleté est encapsulée dans un lubrifiant puis retirée à la microfibre. Aucun ruissellement, donc utilisable en sous-sol, sur un parking d'entreprise ou en pleine restriction sécheresse.</p>
        <ul>
          <li>15 litres d'eau, que nous apportons</li>
          <li>Aucun raccordement nécessaire</li>
          <li>Autorisé là où le lavage au jet ne l'est pas</li>
          <li>Fonctionne aussi en hiver, sel compris</li>
        </ul>
        """ + ph("methode-sans-rincage.jpg", "16x9", " — le seau, le pulvérisateur et les microfibres pliées", "ph--band") + """
      </article>

      <article class="method">
        <span class="method__tag">Sur demande — si vous êtes équipé</span>
        <h3>Lavage classique au jet</h3>
        <p>Si vous disposez d'un robinet extérieur et d'une prise sur un terrain privé, on peut travailler au nettoyeur haute pression : prélavage à la mousse active, rinçage, séchage. Recommandé pour les véhicules très encrassés et les 4×4 sortis des chemins.</p>
        <ul>
          <li>Prélavage mousse active et haute pression</li>
          <li>Idéal après un hiver ou un chantier</li>
          <li>Nécessite eau + électricité sur place</li>
          <li>Soumis aux arrêtés sécheresse en vigueur</li>
        </ul>
        """ + ph("methode-jet.jpg", "16x9", " — la mousse active sur la carrosserie au nettoyeur haute pression", "ph--band") + """
      </article>
    </div>
  </div>
</section>

<!-- ===== JAUGE D'EAU ===== -->
<section class="section section--deep">
  <div class="wrap gauge" id="gauge">
    <div>
      <h2>15 litres au lieu de 250</h2>
      <p class="lede" style="margin-top:1.15rem">C'est l'écart entre notre méthode sans rinçage et un lavage au jet classique. Pas de tuyau, pas de ruissellement, aucun rejet dans les caniveaux.</p>
    </div>
    <div class="gauge__bars">
      <div class="bar bar--them">
        <div class="bar__label"><span class="bar__name">Station de lavage classique</span><span class="bar__value">250 L</span></div>
        <div class="bar__track"><div class="bar__fill"></div></div>
      </div>
      <div class="bar bar--us">
        <div class="bar__label"><span class="bar__name">Mobile Car Cleaning</span><span class="bar__value">15 L</span></div>
        <div class="bar__track"><div class="bar__fill"></div></div>
      </div>
      <p class="gauge__note">Chaque été, des arrêtés préfectoraux restreignent le lavage de véhicules dans le Bas-Rhin et le Haut-Rhin. Notre méthode sans rinçage nous permet de continuer.</p>
    </div>
  </div>
</section>

<!-- ===== DÉROULÉ EN ONGLETS ===== -->
<section class="section">
  <div class="wrap">
    <div class="head"><h2>Comment ça se passe</h2></div>

    <div class="tabs" role="tablist" aria-label="Déroulé d'une intervention">
      <button class="tab" role="tab" aria-selected="true"  aria-controls="p1" id="t1">Vous réservez</button>
      <button class="tab" role="tab" aria-selected="false" aria-controls="p2" id="t2">On arrive</button>
      <button class="tab" role="tab" aria-selected="false" aria-controls="p3" id="t3">On lave</button>
      <button class="tab" role="tab" aria-selected="false" aria-controls="p4" id="t4">Vous validez</button>
    </div>

    <div class="panel" role="tabpanel" id="p1" aria-labelledby="t1">
      <div class="panel__txt">
        <p class="panel__step">Étape 1 sur 4</p><h3>Vous réservez</h3>
        <p>Choisissez la formule, le créneau et l'adresse d'intervention. Deux minutes en ligne, sans créer de compte ni verser d'acompte. La confirmation arrive par email dans la foulée.</p>
      </div>
      """ + ph("reservation.jpg", "4x3", " — Capture du calendrier sur téléphone, ou un client qui réserve") + """
    </div>
    <div class="panel" role="tabpanel" id="p2" aria-labelledby="t2" hidden>
      <div class="panel__txt">
        <p class="panel__step">Étape 2 sur 4</p><h3>On arrive</h3>
        <p>On se gare à côté du véhicule avec tout le matériel. Il nous faut environ un mètre de dégagement autour de la voiture, et c'est tout. Ni tuyau ni équipement de votre côté, sauf si vous avez choisi le lavage au jet.</p>
      </div>
      """ + ph("arrivee.jpg", "4x3", " — Le véhicule d'intervention garé devant une maison, coffre ouvert") + """
    </div>
    <div class="panel" role="tabpanel" id="p3" aria-labelledby="t3" hidden>
      <div class="panel__txt">
        <p class="panel__step">Étape 3 sur 4</p><h3>On lave</h3>
        <p>Une face de microfibre propre par panneau, séchage à la main. Comptez 45 minutes pour un extérieur, 1 h 45 pour un complet. Votre présence n'est pas nécessaire si le véhicule est accessible.</p>
      </div>
      """ + ph("lavage.jpg", "4x3", " — Gros plan sur la microfibre en action, ou la mousse sur une aile") + """
    </div>
    <div class="panel" role="tabpanel" id="p4" aria-labelledby="t4" hidden>
      <div class="panel__txt">
        <p class="panel__step">Étape 4 sur 4</p><h3>Vous validez</h3>
        <p>On fait le tour du véhicule ensemble si vous êtes là. Paiement par carte sur place ou en ligne, au tarif annoncé à la réservation. Facture envoyée par email.</p>
      </div>
      """ + ph("finition.jpg", "4x3", " — La voiture propre, portière ouverte, ou le paiement par carte") + """
    </div>
  </div>
</section>

<!-- ===== APPEL AUX PROS ===== -->
<section class="section section--deep">
  <div class="wrap cta">
    <h2>Vous gérez plusieurs véhicules ?</h2>
    <p class="lede">Garages, concessions, loueurs, restitutions de leasing et flottes d'entreprise : on se déplace sur votre parc et on facture à la ligne.</p>
    <div class="cta__actions">
      <a class="btn btn--primary" href="b2b.html">Voir l'offre professionnelle</a>
      <a class="btn btn--ghost" href="realisations.html">Voir nos réalisations</a>
    </div>
  </div>
</section>
"""

print("Generation des pages :")
write("index.html", HOME,
      "Lavage auto à domicile en Alsace | Mobile Car Cleaning",
      "Lavage et nettoyage automobile à domicile ou sur votre lieu de travail en Alsace. Sans rinçage ou au jet. Strasbourg, Mulhouse, Colmar, Saint-Louis. Sur rendez-vous 7j/7.")

# ============================================================
#  PAGE SERVICES (particuliers)
# ============================================================
SERVICES = pagehead("Services", "Tous nos services pour les particuliers",
  "Du lavage d'entretien à la remise en état avant restitution. Tout se fait chez vous, sur rendez-vous.", bg="header-services.jpg") + """

<!-- ===== LES DEUX MÉTHODES ===== -->
<section class="section">
  <div class="wrap">
    <div class="head">
      <h2>Sans rinçage, ou au jet</h2>
      <p>On choisit la méthode selon votre situation. Indiquez-nous simplement à la réservation si un robinet extérieur et une prise sont accessibles.</p>
    </div>
    <div class="duo">
      <article class="method method--lead">
        <span class="method__tag">Par défaut — partout</span>
        <h3>Lavage sans rinçage</h3>
        <p>La saleté est encapsulée dans un lubrifiant puis retirée à la microfibre. Aucun ruissellement, donc utilisable en parking souterrain, sur un parking d'entreprise ou pendant une restriction sécheresse.</p>
        <ul><li>15 litres d'eau, que nous apportons</li><li>Aucun raccordement nécessaire</li><li>Fonctionne en hiver, sel compris</li></ul>
        """ + ph("methode-sans-rincage.jpg", "16x9", " — le matériel sans rinçage en situation", "ph--band") + """
      </article>
      <article class="method">
        <span class="method__tag">Sur demande — si vous êtes équipé</span>
        <h3>Lavage classique au jet</h3>
        <p>Sur terrain privé avec eau et électricité, on travaille au nettoyeur haute pression : prélavage à la mousse active, rinçage, séchage. Recommandé pour les véhicules très encrassés et les 4×4 sortis des chemins.</p>
        <ul><li>Prélavage mousse active et haute pression</li><li>Idéal après un hiver ou un chantier</li><li>Soumis aux arrêtés sécheresse en vigueur</li></ul>
        """ + ph("methode-jet.jpg", "16x9", " — nettoyeur haute pression et mousse active", "ph--band") + """
      </article>
    </div>
  </div>
</section>

<!-- ===== CATALOGUE — MODIFIEZ LES PRIX ICI ===== -->
<section class="section section--deep">
  <div class="wrap">
    <div class="head">
      <h2>Le catalogue</h2>
      <p>Tarifs pour une citadine. Comptez environ +10 € pour une berline ou un break, +20 € pour un SUV ou un utilitaire.</p>
    </div>

    <div class="grid-svc">
      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 17h14M3 17v-5l2-5h14l2 5v5"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Express extérieur</h3><span class="svc__price">39 €</span></div>
          <p>45 minutes. L'entretien régulier pour garder une voiture nette.</p>
          <ul><li>Carrosserie lavée et séchée</li><li>Jantes et passages de roue</li><li>Vitres et rétroviseurs</li></ul>
          <a class="btn btn--ghost btn--full" href="reserver.html">Réserver</a>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 20v-6a4 4 0 0 1 4-4h8a4 4 0 0 1 4 4v6"/><path d="M9 10V6a3 3 0 0 1 6 0v4"/><path d="M3 20h18"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Intérieur</h3><span class="svc__price">49 €</span></div>
          <p>1 heure. Aspiration en profondeur et surfaces remises à neuf.</p>
          <ul><li>Sièges, tapis et coffre</li><li>Plastiques et aérateurs</li><li>Vitres intérieures</li></ul>
          <a class="btn btn--ghost btn--full" href="reserver.html">Réserver</a>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v3M5.6 5.6l2.1 2.1M3 12h3M18 12h3M16.3 7.7l2.1-2.1"/><circle cx="12" cy="14" r="5"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Complet</h3><span class="svc__price">79 €</span></div>
          <p>1 h 45. Notre formule la plus demandée.</p>
          <ul><li>Tout l'extérieur</li><li>Tout l'intérieur</li><li>Seuils de porte et montants</li></ul>
          <a class="btn btn--primary btn--full" href="reserver.html">Réserver</a>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Complet + protection</h3><span class="svc__price">129 €</span></div>
          <p>2 h 30. Un complet avec décontamination et protection longue durée.</p>
          <ul><li>Tout le Complet</li><li>Décontamination fer et goudron</li><li>Protection tenant environ 3 mois</li></ul>
          <a class="btn btn--ghost btn--full" href="reserver.html">Réserver</a>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h16M7 7V5h10v2M6 7l1 13h10l1-13"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Restitution de leasing</h3><span class="svc__price">Dès 129 €</span></div>
          <p>Avant la reprise de votre LOA ou LLD. L'état de propreté pèse dans l'expertise de restitution, et les frais de remise en état facturés par le loueur dépassent souvent le coût d'un nettoyage.</p>
          <ul><li>Complet + rénovation intérieure ciblée</li><li>Traitement des taches et des odeurs</li><li>Rénovation des phares en option</li></ul>
          <a class="btn btn--ghost btn--full" href="detailing.html">En savoir plus</a>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a9 9 0 1 1-3.3-6.9"/><path d="M21 4v5h-5"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Abonnement</h3><span class="svc__price">35 €<small>/mois</small></span></div>
          <p>Un créneau posé à l'avance chaque mois, reportable si vous sautez un tour.</p>
          <ul><li>Essentiel : 1 extérieur — 35 €</li><li>Confort : 1 complet — 75 €</li><li>Premium : 2 complets — 139 €</li></ul>
          <a class="btn btn--ghost btn--full" href="#contact-cta">Nous écrire</a>
        </div>
      </article>
    </div>

    <p class="pricing__foot">Options : véhicule très sale +15 à 25 € · poils d'animaux +20 € · sièges cuir +30 € · compartiment moteur +30 € · rénovation des phares +59 €. Déplacement offert dans un rayon de 15 km, puis 0,50 €/km. Prix nets de taxes, TVA non applicable.</p>
    """ + ph("services-bande.jpg", "wide", " — plan large d'une intervention, idéalement avec le logo visible", "ph--band") + """
  </div>
</section>

<!-- ===== FAQ ===== -->
<section class="section">
  <div class="wrap">
    <div class="head"><h2>Les questions qu'on nous pose</h2></div>
    <div class="faq">
      <details open><summary>Avez-vous besoin de mon eau et de mon électricité ?</summary>
        <p>Pas pour la méthode sans rinçage : nous apportons les 15 litres nécessaires. Une prise nous aide pour l'aspirateur sur les formules intérieures, mais nous avons une solution autonome. Le lavage au jet, lui, nécessite un robinet et une prise sur terrain privé.</p></details>
      <details><summary>Où l'intervention peut-elle avoir lieu ?</summary>
        <p>Devant chez vous, sur une place de parking, dans une allée privée, sur un parking d'entreprise ou en sous-sol. Il nous faut environ un mètre de dégagement autour du véhicule.</p></details>
      <details><summary>Dois-je être présent pendant le lavage ?</summary>
        <p>Pour un extérieur, non : il suffit que le véhicule soit accessible. Pour une formule intérieure, nous avons besoin des clés, donc soit vous êtes là au début et à la fin, soit vous nous les confiez.</p></details>
      <details><summary>Et s'il pleut le jour du rendez-vous ?</summary>
        <p>Si le véhicule est à l'abri, on intervient normalement. Sinon on décale à un autre créneau, sans aucun frais. On vous prévient la veille en cas de doute sur la météo.</p></details>
      <details><summary>Intervenez-vous en hiver ?</summary>
        <p>Oui. La méthode sans rinçage fonctionne par temps froid et gère bien les résidus de sel. Sur un véhicule vraiment encrassé, on applique un prélavage renforcé, facturé en option.</p></details>
      <details><summary>Comment se passe le paiement ?</summary>
        <p>Par carte bancaire sur place, ou en ligne au moment de la réservation. Facture envoyée par email après l'intervention. Nos prix sont nets de taxes, la TVA n'étant pas applicable.</p></details>
    </div>
  </div>
</section>

<section class="section section--deep" id="contact-cta">
  <div class="wrap cta">
    <h2>Prêt à réserver ?</h2>
    <p class="lede">Choisissez votre créneau en ligne, ou appelez-nous pour un cas particulier.</p>
    <div class="cta__actions">
      <a class="btn btn--primary" href="reserver.html">Réserver un créneau</a>
      <a class="btn btn--ghost" href="tel:""" + TEL_HREF + """\">""" + TEL_TXT + """</a>
    </div>
  </div>
</section>
"""

write("services.html", SERVICES,
      "Nos services de lavage auto à domicile | Mobile Car Cleaning",
      "Lavage extérieur, nettoyage intérieur, formule complète, restitution de leasing et abonnement. À domicile en Alsace, sans rinçage ou au jet.")

# ============================================================
#  PAGE RÉNOVATION (detailing)
# ============================================================
DETAILING = pagehead("Rénovation", "Rénovation et remise en état",
  "Quand le lavage ne suffit plus : intérieurs très marqués, peinture terne, optiques jaunies, et préparation avant restitution de leasing.", bg="header-renovation.jpg") + """

<section class="section">
  <div class="wrap">
    <div class="head">
      <h2>Ce qu'on sait faire, et ce qu'on ne fait pas</h2>
      <p>Trois interventions maîtrisées, réalisées chez vous. Nous ne posons ni céramique longue durée ni film de protection : ces traitements exigent un atelier fermé, à température et hygrométrie contrôlées.</p>
    </div>

    <div class="grid-svc">
      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 21h18"/><path d="M6 21v-7l6-9 6 9v7"/><path d="M9 21v-4h6v4"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Rénovation intérieure</h3><span class="svc__price">149 €</span></div>
          <p>3 heures. Sièges et moquettes traités à l'injection-extraction, pour les taches installées et les intérieurs très marqués.</p>
          <ul><li>Injection-extraction sièges et moquettes</li><li>Traitement des taches localisées</li><li>Poils d'animaux sur demande</li><li>Séchage avant restitution du véhicule</li></ul>
          <a class="btn btn--ghost btn--full" href="reserver.html">Réserver</a>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16"/><path d="M9.5 9.5l5 5"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Éclat &amp; brillance</h3><span class="svc__price">279 €</span></div>
          <p>5 à 6 heures. Décontamination puis polissage une passe, pour retirer le voile terne et raviver la profondeur de la couleur.</p>
          <ul><li>Lavage complet préalable</li><li>Décontamination fer et goudron</li><li>Polissage une passe à la machine</li><li>Protection longue durée appliquée</li></ul>
          <a class="btn btn--ghost btn--full" href="#devis">Demander un devis</a>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12a5 5 0 0 1 5-5h1a6 6 0 0 1 0 10H9a5 5 0 0 1-5-5Z"/><path d="M17 9h4M17 12h4M17 15h4"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Rénovation des phares</h3><span class="svc__price">59 €</span></div>
          <p>30 minutes, la paire. Ponçage progressif puis vernis de protection sur les optiques jaunies.</p>
          <ul><li>Ponçage progressif multi-grains</li><li>Vernis de protection anti-UV</li><li>Effet immédiat au-delà de 8 ans d'âge</li><li>Se combine avec n'importe quelle formule</li></ul>
          <a class="btn btn--ghost btn--full" href="reserver.html">Réserver</a>
        </div>
      </article>
    </div>
  </div>
</section>

<!-- ===== AVANT / APRÈS ===== -->
<section class="section section--tight">
  <div class="wrap">
    <div class="head">
      <h2>Avant, après</h2>
      <p>Le même véhicule, le même angle, la même lumière. C'est la seule comparaison qui veut dire quelque chose.</p>
    </div>
    <div class="ph-duo">
      """ + ph("avant-siege.jpg", "4x3", " — AVANT : siège taché, cadrage serré") + """
      """ + ph("apres-siege.jpg", "4x3", " — APRÈS : même siège, même angle, même lumière") + """
    </div>
    <div class="ph-duo" style="margin-top:1.35rem">
      """ + ph("avant-phare.jpg", "4x3", " — AVANT : optique jaunie") + """
      """ + ph("apres-phare.jpg", "4x3", " — APRÈS : optique rénovée") + """
    </div>
  </div>
</section>

<!-- ===== RESTITUTION DE LEASING ===== -->
<section class="section section--deep">
  <div class="wrap fleet">
    <div>
      <h2>Restitution de leasing : ne payez pas deux fois</h2>
      <p class="lede" style="margin-top:1.15rem">À la fin d'une LOA ou d'une LLD, l'expert mandaté par le loueur passe le véhicule en revue. La propreté n'est pas qu'un détail : elle conditionne l'inspection de l'état intérieur, et les frais de remise en état facturés dépassent très souvent le coût d'un nettoyage.</p>
      <ul class="fleet__list">
        <li>Intervention 8 à 15 jours avant la date de restitution</li>
        <li>Nettoyage complet intérieur et extérieur</li>
        <li>Traitement ciblé des taches sur sièges et moquettes</li>
        <li>Rénovation des optiques si elles sont voilées</li>
        <li>Photos avant/après remises au client sur demande</li>
      </ul>
      <a class="btn btn--primary" style="margin-top:2rem" href="#devis">Demander un devis restitution</a>
    </div>

    <div class="sheet">
      <div class="sheet__top">
        <div><strong>Forfait Restitution</strong><small>Exemple pour une berline compacte</small></div>
        <p class="sheet__total">188 €</p>
      </div>
      <table>
        <caption class="sr">Composition d'un forfait de préparation avant restitution de leasing</caption>
        <thead><tr><th scope="col">Prestation</th><th scope="col">Détail</th><th scope="col">Tarif</th></tr></thead>
        <tbody>
          <tr><td>Complet</td><td class="hide-sm">Extérieur + intérieur</td><td>89 €</td></tr>
          <tr><td>Rénovation intérieure</td><td class="hide-sm">Sièges et moquettes</td><td>169 €</td></tr>
          <tr><td>Phares</td><td class="hide-sm">La paire</td><td>59 €</td></tr>
          <tr><td>Remise forfait</td><td class="hide-sm">Prestations groupées</td><td>−129 €</td></tr>
        </tbody>
      </table>
      <p class="sheet__foot">Le forfait s'ajuste selon l'état réel du véhicule. Envoyez-nous quelques photos, on vous répond sous 24 h.</p>
    </div>
  </div>
</section>

<!-- ===== POURQUOI PAS DE CÉRAMIQUE ===== -->
<section class="section">
  <div class="wrap split">
    <div>
      <h2>Pourquoi nous ne posons pas de céramique</h2>
      <div class="prose" style="margin-top:1.5rem">
      <p>C'est une question honnête, et la réponse l'est aussi. Un revêtement céramique longue durée se pose dans un local fermé, à température stable, sans poussière ni pollen, avec un temps de prise de plusieurs heures. En extérieur, dans une allée ou sur un parking, le résultat est aléatoire et la garantie constructeur ne tient pas.</p>
      <p>Plutôt que de vendre un traitement que nous ne pouvons pas exécuter dans les règles, nous proposons une <strong>protection longue durée appliquée à la main</strong>, incluse dans la formule Éclat et dans le Complet + protection. Elle tient plusieurs mois, se renouvelle facilement, et coûte une fraction du prix d'une céramique.</p>
      <p>Si vous cherchez spécifiquement une céramique certifiée ou un film de protection, dites-le-nous : nous vous orienterons vers un atelier sérieux de la région plutôt que de vous vendre autre chose.</p>
      </div>
    </div>
    """ + ph("protection-application.jpg", "4x3", " — application de la protection à la main sur la carrosserie") + """
  </div>
</section>

<section class="section section--deep" id="devis">
  <div class="wrap cta">
    <h2>Envoyez-nous quelques photos</h2>
    <p class="lede">Trois ou quatre photos du véhicule suffisent pour un devis précis. Réponse sous 24 h, sans engagement.</p>
    <div class="cta__actions">
      <a class="btn btn--primary" href="mailto:""" + MAIL + """">Envoyer par email</a>
      <a class="btn btn--ghost" href="tel:""" + TEL_HREF + """\">""" + TEL_TXT + """</a>
    </div>
  </div>
</section>
"""

write("detailing.html", DETAILING,
      "Rénovation intérieure, polissage et restitution de leasing | Mobile Car Cleaning",
      "Rénovation intérieure à l'injection-extraction, polissage une passe, rénovation des phares et préparation avant restitution de LOA ou LLD, à domicile en Alsace.")

# ============================================================
#  PAGE PROS ET FLOTTES (B2B)
# ============================================================
B2B = pagehead("Pros &amp; flottes", "Garages, concessions et flottes",
  "On se déplace sur votre parc et on traite plusieurs véhicules d'affilée. Une seule facture, détaillée à la ligne.", bg="header-pros.jpg") + """

<section class="section">
  <div class="wrap">
    <div class="head">
      <h2>Ce qu'on fait pour les professionnels</h2>
      <p>Tarifs dégressifs dès 5 véhicules. Intervention sur votre parking, en journée ou en début de matinée avant l'ouverture.</p>
    </div>

    <div class="grid-svc">
      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 17h14M3 17v-5l2-5h14l2 5v5"/><circle cx="7.5" cy="17" r="2"/><circle cx="16.5" cy="17" r="2"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Préparation VO</h3><span class="svc__price">45–55 €</span></div>
          <p>Mise en valeur avant mise en vente ou passage en photo studio.</p>
          <ul><li>Extérieur complet et jantes</li><li>Intérieur aspiré et plastiques traités</li><li>Minimum 3 véhicules</li></ul>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Préparation livraison</h3><span class="svc__price">89–110 €</span></div>
          <p>Le niveau au-dessus, pour une remise de clés soignée.</p>
          <ul><li>Préparation VO complète</li><li>Polissage léger de la carrosserie</li><li>Finition de présentation</li></ul>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h16M7 7V5h10v2M6 7l1 13h10l1-13"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Retour de leasing</h3><span class="svc__price">Sur devis</span></div>
          <p>Restitution de LOA, LLD ou fin de contrat de flotte. On remet le véhicule en état avant le passage de l'expert, pour limiter les frais de remise en état refacturés.</p>
          <ul><li>Complet + traitement des taches</li><li>Rénovation des optiques si besoin</li><li>Photos avant/après sur demande</li><li>Traitement par lots de véhicules</li></ul>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a9 9 0 1 1-3.3-6.9"/><path d="M21 4v5h-5"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Retour de location</h3><span class="svc__price">30–40 €</span></div>
          <p>Remise en état rapide entre deux locations courte durée.</p>
          <ul><li>Extérieur et intérieur express</li><li>Cadence soutenue sur site</li><li>Minimum 5 véhicules</li></ul>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="7" width="18" height="12" rx="2"/><path d="M8 7V5h8v2M3 12h18"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Flotte d'entreprise</h3><span class="svc__price">65–75 €<small>/véh.</small></span></div>
          <p>Contrat mensuel pour véhicules de fonction et utilitaires.</p>
          <ul><li>Formule complète par véhicule</li><li>Passage planifié à date fixe</li><li>Une facture par mois</li></ul>
        </div>
      </article>

      <article class="svc">
        <div class="svc__art"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></div>
        <div class="svc__body">
          <div class="svc__top"><h3>Journée sur parking</h3><span class="svc__price">450–500 €<small>/jour</small></span></div>
          <p>Un avantage salarié qui ne coûte rien à l'entreprise : on vient une journée sur votre parking et les collaborateurs réservent leur créneau.</p>
          <ul><li>5 à 7 véhicules dans la journée</li><li>Facturation entreprise ou salarié</li><li>Récurrence mensuelle possible</li></ul>
        </div>
      </article>
    </div>
  </div>
</section>

<!-- ===== RÉCAPITULATIF ===== -->
<section class="section section--deep">
  <div class="wrap fleet">
    <div>
      <h2>Une seule facture, détaillée à la ligne</h2>
      <p class="lede" style="margin-top:1.15rem">Chaque véhicule traité apparaît avec sa plaque, la prestation réalisée et son tarif. Vous recevez le récapitulatif en fin de mois, prêt à passer en comptabilité.</p>
      <ul class="fleet__list">
        <li>Remise de 10 % dès 5 véhicules</li>
        <li>Remise de 15 % dès 10 véhicules</li>
        <li>Remise de 20 % sur contrat annuel</li>
        <li>Paiement à 30 jours pour les contrats récurrents</li>
        <li>Prix nets de taxes — TVA non applicable, article 293 B du CGI</li>
      </ul>
      <a class="btn btn--primary" style="margin-top:2rem" href="#devis-pro">Demander une proposition</a>
    </div>

    <div class="sheet">
      <div class="sheet__top">
        <div><strong>Exemple d'intervention sur parc</strong><small>5 véhicules, une demi-journée</small></div>
        <p class="sheet__total">312 €</p>
      </div>
      <table>
        <caption class="sr">Exemple de récapitulatif d'intervention sur une flotte de cinq véhicules</caption>
        <thead><tr><th scope="col">Plaque</th><th scope="col" class="hide-sm">Véhicule</th><th scope="col">Prestation</th><th scope="col">Statut</th></tr></thead>
        <tbody>
          <tr><td>EA-482-KL</td><td class="hide-sm">Renault Clio</td><td>Préparation VO</td><td><span class="pill pill--ok">Livré</span></td></tr>
          <tr><td>FT-193-BD</td><td class="hide-sm">Peugeot 308</td><td>Préparation VO</td><td><span class="pill pill--ok">Livré</span></td></tr>
          <tr><td>GH-660-XR</td><td class="hide-sm">Dacia Duster</td><td>Complet + phares</td><td><span class="pill pill--ok">Livré</span></td></tr>
          <tr><td>CD-207-MN</td><td class="hide-sm">Ford Transit</td><td>Retour de leasing</td><td><span class="pill pill--ok">Livré</span></td></tr>
          <tr><td>BJ-914-QS</td><td class="hide-sm">VW Golf</td><td>Rénovation intérieure</td><td><span class="pill pill--wait">Jeudi</span></td></tr>
        </tbody>
      </table>
      <p class="sheet__foot">Exemple illustratif. Votre récapitulatif reprend vos véhicules et vos tarifs négociés.</p>
    </div>
  </div>
</section>

<!-- ===== POURQUOI NOUS ===== -->
<section class="section">
  <div class="wrap">
    <div class="head"><h2>Pourquoi travailler avec nous</h2></div>
    <div class="values">
      <article class="value"><h3>On vient à vous</h3><p>Pas de véhicule à convoyer, pas de place immobilisée dans un tunnel de lavage. Vos voitures restent sur votre parc.</p></article>
      <article class="value"><h3>Sans point d'eau</h3><p>Notre méthode sans rinçage fonctionne sur n'importe quel parking, y compris en sous-sol, sans raccordement ni évacuation.</p></article>
      <article class="value"><h3>Pas d'arrêt en été</h3><p>Les arrêtés sécheresse ne nous concernent pas. Vos préparations continuent quand les stations sont à l'arrêt.</p></article>
      <article class="value"><h3>Interlocuteur unique</h3><p>Vous avez notre numéro direct. Pas de plateforme, pas de centre d'appels, pas de sous-traitance.</p></article>
    </div>
    """ + ph("b2b-bande.jpg", "wide", " — intervention sur un parking professionnel, plan large", "ph--band") + """
  </div>
</section>

<section class="section section--deep" id="devis-pro">
  <div class="wrap cta">
    <h2>Parlons de votre parc</h2>
    <p class="lede">Dites-nous combien de véhicules, à quelle fréquence et où. On revient vers vous avec une grille tarifaire sous 24 h.</p>
    <div class="cta__actions">
      <a class="btn btn--primary" href="mailto:""" + MAIL + """">Écrire à l'équipe</a>
      <a class="btn btn--ghost" href="tel:""" + TEL_HREF + """\">""" + TEL_TXT + """</a>
    </div>
  </div>
</section>
"""

write("b2b.html", B2B,
      "Lavage de flotte, préparation VO et retour de leasing en Alsace | Mobile Car Cleaning",
      "Préparation de véhicules d'occasion, retours de location, restitutions de leasing et lavage de flotte d'entreprise. Intervention sur votre parc en Alsace, facture unique détaillée.")

# ============================================================
#  PAGE RÉALISATIONS
#  Pour ajouter un chantier : copiez un bloc <article class="work">
#  et changez data-cat (exterieur / interieur / renovation / pro)
# ============================================================
def work(cat, catlabel, titre, desc, meta, photo=None):
    import unicodedata
    slug = unicodedata.normalize('NFKD', titre.lower()).encode('ascii', 'ignore').decode()
    slug = ''.join(c if c.isalnum() else '-' for c in slug)
    slug = '-'.join(x for x in slug.split('-') if x)[:24]
    art = (f'<img src="{photo}" alt="{titre}">' if photo
           else f'<span class="work__ph"><b>Photo à ajouter</b>{desc[:0]}Le véhicule terminé, plaque masquée<br><code>assets/real-{slug}.jpg</code></span>')
    return f"""      <article class="work" data-cat="{cat}">
        <div class="work__art">{art}</div>
        <div class="work__body">
          <p class="work__cat">{catlabel}</p>
          <h3>{titre}</h3>
          <p>{desc}</p>
          <p class="work__meta">{meta}</p>
        </div>
      </article>
"""

WORKS = (
  work("interieur","Intérieur","Break familial, sièges tissu",
       "Trois ans de trajets école et de miettes de goûter. Injection-extraction sur les cinq places et la moquette de coffre.",
       "Rénovation intérieure · 3 h · Strasbourg") +
  work("exterieur","Extérieur","Citadine, entretien mensuel",
       "Cliente en abonnement Confort. Lavage sans rinçage sur le parking de son immeuble, sans point d'eau.",
       "Formule complète · 1 h 45 · Schiltigheim") +
  work("renovation","Rénovation","Berline allemande, peinture noire",
       "Voile terne et micro-rayures visibles au soleil. Décontamination puis polissage une passe, protection appliquée à la main.",
       "Éclat & brillance · 6 h · Colmar") +
  work("renovation","Rénovation","Monospace, optiques opacifiées",
       "Phares jaunis d'un véhicule de onze ans. Ponçage progressif puis vernis anti-UV sur la paire.",
       "Rénovation phares · 30 min · Mulhouse") +
  work("pro","Professionnel","Retour de leasing, utilitaire",
       "Préparation avant passage de l'expert : complet, traitement des taches de sièges et rénovation des optiques.",
       "Retour de leasing · 4 h · Illkirch") +
  work("pro","Professionnel","Marchand VO, lot de quatre",
       "Passage mensuel sur le parc avant mise en ligne des annonces. Quatre véhicules dans la demi-journée.",
       "Préparation VO · Demi-journée · Haguenau")
)

REAL = pagehead("Réalisations", "Nos réalisations",
  "Quelques interventions récentes, chez des particuliers comme chez des professionnels.", bg="header-realisations.jpg") + """

<section class="section">
  <div class="wrap">

    <!-- ===== FILTRES ===== -->
    <div class="filters" role="tablist" aria-label="Filtrer les réalisations">
      <button class="tab" role="tab" aria-selected="true"  data-filter="tout">Tout</button>
      <button class="tab" role="tab" aria-selected="false" data-filter="exterieur">Extérieur</button>
      <button class="tab" role="tab" aria-selected="false" data-filter="interieur">Intérieur</button>
      <button class="tab" role="tab" aria-selected="false" data-filter="renovation">Rénovation</button>
      <button class="tab" role="tab" aria-selected="false" data-filter="pro">Professionnel</button>
    </div>

    <!-- ===== GALERIE — ajoutez vos chantiers ici ===== -->
    <div class="gallery">
""" + WORKS + """    </div>

    <p class="pricing__foot">Les photos de vos véhicules ne sont publiées qu'avec votre accord, et les plaques sont systématiquement masquées.</p>
  </div>
</section>

<section class="section section--deep">
  <div class="wrap cta">
    <h2>Votre voiture peut être la prochaine</h2>
    <p class="lede">Réservez un créneau en ligne, ou envoyez-nous des photos si vous voulez un devis avant.</p>
    <div class="cta__actions">
      <a class="btn btn--primary" href="reserver.html">Réserver un créneau</a>
      <a class="btn btn--ghost" href="mailto:""" + MAIL + """">Demander un devis</a>
    </div>
  </div>
</section>
"""

write("realisations.html", REAL,
      "Nos réalisations | Mobile Car Cleaning Alsace",
      "Exemples d'interventions récentes : rénovation intérieure, polissage, rénovation de phares, préparation VO et retour de leasing en Alsace.")


# ============================================================
#  PAGE À PROPOS
# ============================================================
APROPOS = pagehead("À propos", "Deux frères, une camionnette et beaucoup de microfibres",
  "Mobile Car Cleaning est une micro-entreprise alsacienne. Pas de franchise, pas de centre d'appels : vous parlez directement à la personne qui lavera votre voiture.") + """

<section class="section">
  <div class="wrap split">
    <div>
      <h2>Pourquoi on s'est lancés</h2>
      <p class="lede" style="margin-top:1.15rem">Parce que laver sa voiture correctement demande du temps qu'on n'a pas, et que les alternatives sont soit rapides et médiocres, soit soignées et hors de prix.</p>
      <div class="prose" style="margin-top:1.5rem">
        <p>Le rouleau de station raye la peinture. Le lavage à la main en centre-ville coûte cher et suppose de déposer sa voiture puis de revenir. Quant au lavage devant chez soi, il est interdit dans beaucoup de communes et devient impossible dès le premier arrêté sécheresse de l'été.</p>
        <p>Notre réponse tient en une phrase : on vient à vous, avec notre eau. La méthode sans rinçage consomme 15 litres au lieu de 250, ne produit aucun ruissellement, et fonctionne donc là où le lavage classique est interdit — parking d'entreprise, sous-sol, voie publique.</p>
        <p>On a démarré en Alsace parce qu'on y vit. On couvre Strasbourg, Mulhouse, Colmar, Saint-Louis et les communes autour.</p>
      </div>
    </div>
    """ + ph("equipe.jpg", "4x3", " — vous deux devant le véhicule, en tenue de travail") + """
  </div>
</section>

<section class="section section--deep">
  <div class="wrap">
    <div class="head"><h2>Ce sur quoi on ne transige pas</h2></div>
    <div class="values">
      <article class="value"><h3>Une microfibre propre par panneau</h3><p>C'est la règle qui évite les micro-rayures. On préfère utiliser vingt serviettes et repartir avec un sac de linge sale.</p></article>
      <article class="value"><h3>Le prix annoncé est le prix payé</h3><p>Le tarif est fixé à la réservation. Si le véhicule demande vraiment plus de travail, on vous appelle avant de commencer, jamais après.</p></article>
      <article class="value"><h3>On dit non quand il faut</h3><p>Céramique longue durée, film de protection : ces poses exigent un atelier fermé. On préfère vous orienter ailleurs plutôt que mal faire.</p></article>
      <article class="value"><h3>Le même interlocuteur</h3><p>Vous réservez, on arrive, on vous rappelle. C'est la même personne du début à la fin.</p></article>
    </div>

    <div class="stats">
      <div class="stat"><p class="figure">15 L</p><p>d'eau par lavage, contre 250 en station</p></div>
      <div class="stat"><p class="figure">7j/7</p><p>sur rendez-vous, de 8 h à 19 h</p></div>
      <div class="stat"><p class="figure">15 km</p><p>de déplacement offert autour de nos bases</p></div>
      <div class="stat"><p class="figure">24 h</p><p>pour recevoir un devis après vos photos</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    """ + ph("vehicule.jpg", "4x3", " — le coffre ouvert avec le matériel rangé") + """
    <div>
      <h2>Comment on travaille</h2>
      <div class="prose" style="margin-top:1.25rem">
        <p>On arrive avec l'eau, l'électricité et les produits. Il nous faut environ un mètre de dégagement autour du véhicule, et rien d'autre.</p>
        <p>Si vous disposez d'un robinet extérieur et d'une prise sur terrain privé, on peut aussi travailler au nettoyeur haute pression, avec prélavage à la mousse active. C'est le meilleur choix pour un véhicule très encrassé, sortie d'hiver ou retour de chemin. Vous nous le dites à la réservation, on adapte.</p>
        <p>Les produits utilisés sont des références professionnelles, biodégradables, et dosés au strict nécessaire. La question n'est pas seulement écologique : un produit mal dosé laisse des traces.</p>
      </div>
      <a class="btn btn--primary" style="margin-top:2rem" href="reserver.html">Réserver un créneau</a>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="wrap">
    """ + ph("apropos-bande.jpg", "wide", " — plan large en intervention, à Strasbourg ou Colmar") + """
  </div>
</section>

<section class="section section--deep">
  <div class="wrap cta">
    <h2>Une question avant de réserver ?</h2>
    <p class="lede">Appelez-nous, on répond nous-mêmes.</p>
    <div class="cta__actions">
      <a class="btn btn--primary" href="tel:""" + TEL_HREF + """\">""" + TEL_TXT + """</a>
      <a class="btn btn--ghost" href="mailto:""" + MAIL + """">""" + MAIL + """</a>
    </div>
  </div>
</section>
"""

write("a-propos.html", APROPOS,
      "À propos | Mobile Car Cleaning, lavage auto mobile en Alsace",
      "Mobile Car Cleaning est une micro-entreprise alsacienne de lavage automobile à domicile. Notre méthode, nos engagements et notre zone d'intervention.")

# ============================================================
#  JOURNAL — liste + articles
# ============================================================
ARTICLES = [
 ("journal-sel-hiver.html","Entretien saisonnier","6 min",
  "Le sel de déneigement, et pourquoi vos passages de roue vieillissent plus vite que le reste",
  "Ce n'est pas la neige qui abîme une voiture en Alsace, c'est ce qu'on met dessus pour la faire fondre. Où le sel s'accumule, et à quelle fréquence il faut le déloger."),
 ("journal-restitution-leasing.html","Leasing","7 min",
  "Restitution de LOA : les frais qu'un nettoyage évite, et ceux qu'il n'évitera pas",
  "L'expert de restitution suit une grille précise. Voici ce qui relève de la propreté, ce qui relève de l'usure normale, et où se situe la limite."),
 ("journal-sans-rincage.html","Méthode","5 min",
  "Lavage sans rinçage : comment ça marche vraiment, et quand ça ne suffit pas",
  "Passer une microfibre sur une voiture sale devrait la rayer. Voilà pourquoi ce n'est pas le cas, et dans quels cas on sort quand même le nettoyeur haute pression."),
]

cards = "".join(f"""      <a class="post" href="{u}">
        <div class="post__art ph"><span><b>Photo à ajouter</b><br><code>assets/{u.replace('.html','')}.jpg</code></span></div>
        <div class="post__body">
          <p class="post__cat">{cat} · {mins} de lecture</p>
          <h3>{t}</h3>
          <p>{d}</p>
          <span class="post__more">Lire l'article</span>
        </div>
      </a>
""" for u, cat, mins, t, d in ARTICLES)

JOURNAL = pagehead("Journal", "Le journal",
  "Ce qu'on apprend sur le terrain : entretien saisonnier, restitution de leasing, méthodes de lavage.", bg="header-journal.jpg") + """
<section class="section">
  <div class="wrap">
    <div class="posts">
""" + cards + """    </div>
  </div>
</section>
"""
write("journal.html", JOURNAL,
      "Journal | Conseils entretien automobile — Mobile Car Cleaning",
      "Conseils d'entretien automobile en Alsace : sel de déneigement, restitution de leasing, lavage sans rinçage.")


def article(url, cat, mins, titre, chapo, corps, desc):
    body = pagehead(f'<a href="journal.html">Journal</a> — {cat}', titre, chapo,
                    bg="header-" + url.replace(".html", "") + ".jpg").replace(
        "  </div>\n</section>",
        f'    <p class="postmeta"><span>{cat}</span><span>{mins} de lecture</span></p>\n  </div>\n</section>', 1)
    slug = url.replace('.html', '')
    body += f"""
<section class="section section--tight">
  <div class="wrap">
    {ph(slug + '.jpg', '16x9', ' — image d\'ouverture de l\'article')}
  </div>
</section>

<section class="section">
  <div class="wrap prose">
{corps}
  </div>
</section>

<section class="section section--deep">
  <div class="wrap cta">
    <h2>On s'occupe de votre voiture ?</h2>
    <p class="lede">Lavage à domicile en Alsace, sur rendez-vous 7j/7.</p>
    <div class="cta__actions">
      <a class="btn btn--primary" href="reserver.html">Réserver un créneau</a>
      <a class="btn btn--ghost" href="journal.html">Retour au journal</a>
    </div>
  </div>
</section>
"""
    write(url, body, titre + " | Mobile Car Cleaning", desc)


article("journal-sel-hiver.html","Entretien saisonnier","6 min",
 "Le sel de déneigement, et pourquoi vos passages de roue vieillissent plus vite que le reste",
 "Ce n'est pas la neige qui abîme une voiture en Alsace, c'est ce qu'on met dessus pour la faire fondre.",
 """    <p>Entre décembre et mars, les routes du Bas-Rhin et du Haut-Rhin reçoivent des quantités importantes de sel de déneigement. Ce sel ne reste pas sur la chaussée : il est projeté par les roues sur tout le soubassement du véhicule, où il se mélange à l'eau et forme une saumure qui reste humide bien plus longtemps que de l'eau claire.</p>

    <h2>Où le sel s'accumule</h2>
    <p>La carrosserie visible est rarement le problème : elle est peinte, vernie, et l'eau de pluie en rince une bonne partie. Les zones à surveiller sont ailleurs.</p>
    <ul>
      <li><strong>Les passages de roue</strong>, où la projection est permanente et où l'humidité stagne derrière les protections plastiques.</li>
      <li><strong>Les bas de caisse</strong>, en particulier les points de soudure et les trous d'évacuation qui se bouchent avec le mélange sel-gravillon.</li>
      <li><strong>Le dessous des portes</strong>, où l'eau salée s'infiltre par les joints puis stagne dans le corps de porte.</li>
      <li><strong>Les jantes</strong>, surtout en alliage non protégé : le sel attaque le vernis, puis le métal se pique.</li>
    </ul>

    <h2>À quelle fréquence intervenir</h2>
    <p>La règle utile n'est pas un calendrier mais un déclencheur : après chaque épisode de salage suivi d'un redoux. C'est au moment où la température remonte que la saumure reste liquide au contact du métal, et c'est là qu'elle travaille le plus.</p>
    <p>En pratique, sur un hiver alsacien moyen, cela représente trois à cinq passages entre décembre et mars. Un lavage extérieur avec attention portée aux passages de roue suffit ; il n'est pas nécessaire de faire un complet à chaque fois.</p>

    <blockquote><p>Un véhicule lavé quatre fois dans l'hiver avec un vrai traitement des soubassements vieillit sensiblement mieux qu'un véhicule lavé douze fois en rouleau, où le dessous n'est jamais touché.</p></blockquote>

    <h2>Sans rinçage ou au jet ?</h2>
    <p>Pour le sel, c'est un des cas où l'on recommande volontiers le lavage au jet lorsque c'est possible. La haute pression déloge mécaniquement les dépôts accumulés dans les passages de roue, ce qu'une microfibre ne fait pas.</p>
    <p>Mais l'hiver est aussi la période où les restrictions et le gel compliquent le lavage classique. Notre méthode sans rinçage traite parfaitement la carrosserie, les vitres et les jantes ; on complète alors les soubassements au pulvérisateur basse pression, ce qui suffit dans la grande majorité des cas.</p>

    <h2>Un mot sur le lavage par temps de gel</h2>
    <p>Laver un véhicule quand il gèle demande quelques précautions : eau tiède plutôt que froide, séchage soigné des joints de porte, et surtout ne pas laisser d'eau stagner dans les serrures. Un véhicule mal séché à −3 °C, ce sont des portes qui ne s'ouvrent plus le lendemain matin.</p>""",
 "Pourquoi le sel de déneigement abîme les passages de roue et les bas de caisse, où il s'accumule, et à quelle fréquence laver sa voiture en hiver en Alsace.")


article("journal-restitution-leasing.html","Leasing","7 min",
 "Restitution de LOA : les frais qu'un nettoyage évite, et ceux qu'il n'évitera pas",
 "L'expert de restitution suit une grille précise. Voici où se situe la limite entre propreté et usure.",
 """    <p>À la fin d'une location avec option d'achat ou d'une location longue durée, le véhicule est inspecté par un expert mandaté par le loueur. Son rapport détermine les frais de remise en état qui vous seront refacturés. Beaucoup de conducteurs découvrent la facture au dernier moment, alors qu'une partie était évitable.</p>

    <h2>Ce qu'un nettoyage change réellement</h2>
    <p>Un véhicule sale n'est pas seulement mal noté sur la propreté : il est mal inspecté. Une moquette tachée, des plastiques poussiéreux et des vitres opaques donnent le ton du rapport, et l'expert regarde le reste avec plus d'attention. À l'inverse, un intérieur impeccable oriente favorablement l'ensemble de l'évaluation.</p>
    <p>Concrètement, un nettoyage sérieux avant restitution agit sur :</p>
    <ul>
      <li><strong>Les taches sur sièges et moquettes</strong>, qui relèvent de la remise en état facturable et non de l'usure normale.</li>
      <li><strong>Les odeurs persistantes</strong> (tabac, animaux), souvent facturées séparément.</li>
      <li><strong>Les plastiques et le tableau de bord</strong>, où l'accumulation passe pour de la négligence.</li>
      <li><strong>Les optiques de phares voilées</strong>, considérées comme un défaut d'entretien et non comme de l'usure.</li>
      <li><strong>Les jantes encrassées</strong>, qui masquent parfois de simples traces de poussière de frein prises pour des dommages.</li>
    </ul>

    <h2>Ce qu'un nettoyage ne changera pas</h2>
    <p>Autant être clair : le nettoyage n'est pas de la carrosserie. Il ne fera rien pour un impact sur le pare-brise, une jante rayée sur un trottoir, une bosse de portière, une déchirure de sellerie ou des pneus sous la limite légale. Ces postes suivent la grille d'usure du loueur et se règlent, le cas échéant, avec un carrossier.</p>
    <p>De même, les micro-rayures profondes qui atteignent le vernis ne se corrigent pas entièrement à la machine en une passe. Un polissage améliore l'aspect général et gomme le voile terne, mais ne fait pas disparaître un rayure qui accroche l'ongle.</p>

    <blockquote><p>La bonne question n'est pas « est-ce que ça va tout effacer », mais « est-ce que le coût du nettoyage est inférieur aux frais de remise en état que j'éviterai ». Dans la majorité des cas, oui.</p></blockquote>

    <h2>Quand s'y prendre</h2>
    <p>Idéalement entre huit et quinze jours avant la date de restitution. Assez tôt pour que les textiles soient parfaitement secs et que les odeurs soient dissipées, assez tard pour que le véhicule n'ait pas le temps de se resalir.</p>
    <p>Si vous voulez contester un poste du rapport, prenez vos propres photos datées juste après le nettoyage. Elles vous serviront de référence.</p>

    <h2>Et pour les flottes</h2>
    <p>Le raisonnement vaut à plus grande échelle pour les entreprises qui restituent plusieurs véhicules à la même échéance. Traiter un lot de véhicules avant le passage de l'expert coûte moins cher au véhicule et évite des refacturations qui se cumulent. Nous intervenons directement sur le parc.</p>""",
 "Ce qu'un nettoyage avant restitution de LOA ou LLD permet d'éviter comme frais de remise en état, et ce qui relève de la carrosserie ou de l'usure normale.")


article("journal-sans-rincage.html","Méthode","5 min",
 "Lavage sans rinçage : comment ça marche vraiment, et quand ça ne suffit pas",
 "Passer une microfibre sur une voiture sale devrait la rayer. Voilà pourquoi ce n'est pas le cas.",
 """    <p>L'objection est légitime, et c'est la première qu'on nous oppose. Frotter une carrosserie couverte de poussière avec un chiffon, c'est le meilleur moyen de la marquer. Si le lavage sans rinçage fonctionne, c'est parce qu'il ne consiste pas à frotter.</p>

    <h2>Le principe : encapsuler avant de retirer</h2>
    <p>Le produit utilisé contient des polymères qui viennent entourer chaque particule de saleté et la décoller de la peinture, en formant autour d'elle une couche lubrifiante. La particule ne repose alors plus directement sur le vernis : elle flotte dans un film glissant.</p>
    <p>Le geste consiste ensuite à <em>soulever</em> cette particule, pas à la faire glisser. D'où les trois règles de méthode qui font toute la différence :</p>
    <ul>
      <li>Pulvériser abondamment avant tout contact, et laisser agir. Un panneau sec ne se touche jamais.</li>
      <li>Une face de microfibre propre par panneau. Une serviette repliée offre huit faces ; au-delà, on en change.</li>
      <li>Un seul passage dans un sens, sans revenir en arrière sur la même zone.</li>
    </ul>

    <h2>Ce que ça permet</h2>
    <p>Quinze litres d'eau au lieu de deux cent cinquante, mais surtout : aucun ruissellement. C'est ce point, plus que l'économie d'eau, qui change la donne au quotidien. Sans écoulement, on peut intervenir sur un parking d'entreprise, dans un sous-sol, sur une place en voirie — des endroits où le lavage au jet est interdit parce que les eaux chargées partiraient dans un avaloir pluvial.</p>
    <p>Et pendant les arrêtés sécheresse de l'été, qui restreignent le lavage de véhicules dans le Bas-Rhin comme dans le Haut-Rhin, cette méthode reste utilisable.</p>

    <h2>Quand ça ne suffit pas</h2>
    <p>Le sans-rinçage a une limite claire : la quantité de saleté. Sur un véhicule couvert de boue séchée, de gravillons ou de résidus de sel accumulés, il n'y a pas assez de lubrifiant pour encapsuler la totalité des particules. Insister à ce stade, c'est effectivement rayer.</p>
    <p>Dans ces cas-là, deux options. Si vous disposez d'un robinet extérieur et d'une prise sur terrain privé, on passe au nettoyeur haute pression avec prélavage à la mousse active : la saleté est décollée sans contact avant toute intervention manuelle. Sinon, on applique un prélavage renforcé au pulvérisateur, plus long, facturé en supplément.</p>

    <blockquote><p>La bonne méthode n'est pas celle qu'on préfère, c'est celle qui correspond à l'état du véhicule et au lieu de l'intervention.</p></blockquote>

    <h2>Comment savoir avant de réserver</h2>
    <p>Regardez simplement votre voiture. Si la saleté s'enlève au doigt en laissant une trace nette, le sans-rinçage convient. Si vous ne voyez plus la couleur d'origine sur les bas de caisse, prévenez-nous à la réservation : on prévoit le prélavage renforcé et le temps qui va avec.</p>""",
 "Comment fonctionne le lavage sans rinçage, pourquoi il ne raye pas la peinture, et dans quels cas il faut passer au nettoyeur haute pression.")

# ============================================================
#  PAGE RÉSERVATION
# ============================================================
RESERVER = pagehead("Réserver", "Réservez votre créneau",
  "Choisissez la formule, le jour et l'heure. Sans acompte, annulation libre jusqu'à 24 h avant.", bg="header-reserver.jpg") + cal_block(
  "Calendrier de réservation",
  "Si vous ne trouvez pas de créneau qui vous convient, appelez-nous : on trouve souvent une solution.") + """

<section class="section section--tight">
  <div class="wrap">
    """ + ph("reserver-bande.jpg", "wide", " — une voiture fraîchement lavée, plan large") + """
  </div>
</section>

<section class="section section--deep">
  <div class="wrap">
    <div class="head"><h2>Avant de réserver</h2></div>
    <div class="faq">
      <details open><summary>Quelle formule choisir ?</summary>
        <p>Express extérieur pour un entretien régulier, Intérieur si c'est l'habitacle qui pose problème, Complet dans le doute — c'est la formule la plus demandée. Pour un intérieur très marqué ou une restitution de leasing, passez plutôt par la page Rénovation.</p></details>
      <details><summary>Que dois-je préparer ?</summary>
        <p>Rien. Laissez simplement environ un mètre de dégagement autour du véhicule. Si vous avez un robinet extérieur et une prise sur terrain privé, signalez-le dans le champ commentaire : on pourra travailler au nettoyeur haute pression.</p></details>
      <details><summary>Et si je dois annuler ?</summary>
        <p>Annulation ou report libre jusqu'à 24 h avant le rendez-vous, depuis le lien reçu dans l'email de confirmation. Aucun acompte n'est demandé à la réservation.</p></details>
      <details><summary>Je préfère réserver par téléphone</summary>
        <p>Aucun problème. Appelez-nous au """ + TEL_TXT + """, on cale le créneau ensemble.</p></details>
    </div>
  </div>
</section>
"""

write("reserver.html", RESERVER,
      "Réserver un lavage auto à domicile | Mobile Car Cleaning",
      "Réservez en ligne votre lavage automobile à domicile en Alsace. Sans acompte, annulation libre jusqu'à 24 h avant le rendez-vous.",
      script=CAL_SCRIPT)


# ============================================================
#  MENTIONS LÉGALES
# ============================================================
ML = pagehead("Mentions légales", "Mentions légales",
  "Informations légales relatives au site mobilecarcleaning.fr et à l'entreprise qui l'édite.", bg="header-mentions.jpg") + """
<section class="section">
  <div class="wrap prose">

    <h2>Éditeur du site</h2>
    <p>Le présent site est édité par <strong>Mobile Car Cleaning</strong>, entreprise individuelle sous le régime de la micro-entreprise.</p>
    <ul>
      <li><strong>Dénomination :</strong> Mobile Car Cleaning</li>
      <li><strong>Forme juridique :</strong> entreprise individuelle (micro-entreprise)</li>
      <li><strong>Responsable de la publication :</strong> [Prénom NOM du gérant]</li>
      <li><strong>Siège social :</strong> [adresse complète]</li>
      <li><strong>SIREN :</strong> [numéro à 9 chiffres]</li>
      <li><strong>SIRET :</strong> [numéro à 14 chiffres]</li>
      <li><strong>Code APE :</strong> [code, ex. 45.20A]</li>
      <li><strong>Téléphone :</strong> """ + TEL_TXT + """</li>
      <li><strong>Email :</strong> <a href="mailto:""" + MAIL + """">""" + MAIL + """</a></li>
      <li><strong>TVA :</strong> TVA non applicable, article 293 B du Code général des impôts</li>
    </ul>
    <p><em>Note à supprimer une fois la page complétée : renseignez chaque champ entre crochets. Le SIREN et le SIRET figurent sur votre avis de situation INSEE. L'adresse du siège est celle déclarée lors de l'immatriculation ; si c'est votre domicile, la loi vous oblige à la mentionner ici.</em></p>

    <h2>Hébergement</h2>
    <p>Le site est hébergé par <strong>GitHub, Inc.</strong>, 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis — <a href="https://github.com">github.com</a>.</p>
    <p><em>Si vous changez d'hébergeur, mettez ce paragraphe à jour.</em></p>

    <h2>Activité et assurance</h2>
    <p>Mobile Car Cleaning exerce une activité de nettoyage et d'entretien de véhicules automobiles, réalisée sur le lieu choisi par le client.</p>
    <p>L'entreprise est couverte par une assurance responsabilité civile professionnelle souscrite auprès de [nom de l'assureur], police n° [numéro], couvrant les interventions réalisées sur le territoire français.</p>

    <h2>Propriété intellectuelle</h2>
    <p>L'ensemble des contenus présents sur ce site (textes, photographies, logo, éléments graphiques) est la propriété de Mobile Car Cleaning, sauf mention contraire. Toute reproduction, représentation ou diffusion, totale ou partielle, sans autorisation écrite préalable, est interdite.</p>
    <p>Les photographies de véhicules publiées dans la rubrique Réalisations le sont avec l'accord de leurs propriétaires. Les plaques d'immatriculation y sont systématiquement masquées.</p>

    <h2>Liens externes</h2>
    <p>Ce site peut contenir des liens vers des sites tiers. Mobile Car Cleaning n'exerce aucun contrôle sur ces sites et décline toute responsabilité quant à leur contenu.</p>

    <h2>Prix et prestations</h2>
    <p>Les tarifs affichés sur ce site sont exprimés en euros, nets de taxes (TVA non applicable, article 293 B du CGI), et s'entendent pour un véhicule de la catégorie indiquée, en état d'entretien courant.</p>
    <p>Ils sont donnés à titre indicatif et peuvent être ajustés après constat de l'état réel du véhicule. Dans ce cas, le client en est informé <strong>avant</strong> le début de l'intervention et reste libre de l'annuler sans frais.</p>

    <h2>Médiation de la consommation</h2>
    <p>Conformément à l'article L.612-1 du Code de la consommation, tout consommateur a le droit de recourir gratuitement à un médiateur de la consommation en vue de la résolution amiable d'un litige.</p>
    <p>Médiateur compétent : [nom et coordonnées du médiateur — l'adhésion à un dispositif de médiation est obligatoire pour toute entreprise vendant à des particuliers].</p>

    <h2>Droit applicable</h2>
    <p>Le présent site et les prestations proposées sont soumis au droit français. En cas de litige, et à défaut de résolution amiable, les tribunaux français sont seuls compétents.</p>

    <p style="margin-top:2.5rem"><em>Dernière mise à jour : [date].</em></p>
  </div>
</section>
"""

write("mentions-legales.html", ML,
      "Mentions légales | Mobile Car Cleaning",
      "Mentions légales du site mobilecarcleaning.fr : éditeur, hébergeur, propriété intellectuelle, tarifs et médiation de la consommation.")

# ============================================================
#  POLITIQUE DE CONFIDENTIALITÉ
# ============================================================
CONF = pagehead("Confidentialité", "Politique de confidentialité",
  "Quelles données nous collectons, pourquoi, combien de temps nous les gardons, et comment exercer vos droits.", bg="header-confidentialite.jpg") + """
<section class="section">
  <div class="wrap prose">

    <p>Cette page explique comment Mobile Car Cleaning traite les données personnelles des visiteurs du site et de ses clients, conformément au Règlement général sur la protection des données (RGPD) et à la loi Informatique et Libertés.</p>

    <h2>Qui est responsable du traitement</h2>
    <p>Le responsable du traitement est <strong>Mobile Car Cleaning</strong>, micro-entreprise dont les coordonnées figurent dans les <a href="mentions-legales.html">mentions légales</a>.</p>
    <p>Pour toute question relative à vos données : <a href="mailto:""" + MAIL + """">""" + MAIL + """</a></p>

    <h2>Quelles données nous collectons</h2>
    <p>Nous ne collectons que ce qui est nécessaire pour vous fournir la prestation.</p>
    <table>
      <thead><tr><th>Donnée</th><th>Pourquoi</th><th>Base légale</th></tr></thead>
      <tbody>
        <tr><td>Nom et prénom</td><td>Identifier la réservation</td><td>Exécution du contrat</td></tr>
        <tr><td>Email</td><td>Confirmation et facture</td><td>Exécution du contrat</td></tr>
        <tr><td>Téléphone</td><td>Vous prévenir en cas d'imprévu</td><td>Exécution du contrat</td></tr>
        <tr><td>Adresse d'intervention</td><td>Se rendre sur place</td><td>Exécution du contrat</td></tr>
        <tr><td>Véhicule et prestation</td><td>Préparer l'intervention et facturer</td><td>Exécution du contrat</td></tr>
        <tr><td>Photos du véhicule</td><td>Établir un devis, publier une réalisation</td><td>Consentement</td></tr>
      </tbody>
    </table>
    <p>Nous ne collectons <strong>aucune donnée bancaire</strong> : les paiements en ligne sont traités directement par notre prestataire de paiement, qui ne nous transmet que la confirmation du règlement.</p>

    <h2>Le formulaire de réservation</h2>
    <p>La prise de rendez-vous en ligne est assurée par <strong>Cal.com</strong>, qui agit comme sous-traitant. Les données saisies dans le calendrier (nom, email, créneau, commentaire) sont hébergées sur son infrastructure. Sa politique de confidentialité est consultable sur <a href="https://cal.com/privacy">cal.com/privacy</a>.</p>

    <h2>Cookies et mesure d'audience</h2>
    <p>Ce site ne dépose <strong>aucun cookie publicitaire</strong> et n'utilise aucun traceur à des fins de profilage.</p>
    <p>Le module de réservation Cal.com peut déposer des cookies techniques nécessaires à son fonctionnement. Les polices de caractères sont chargées depuis Google Fonts, ce qui implique la transmission de votre adresse IP à Google au moment du chargement de la page.</p>
    <p><em>Note à supprimer : si vous ajoutez un outil de statistiques, il faudra compléter ce paragraphe et, selon l'outil, mettre en place une bannière de consentement. Un outil sans cookies comme Plausible ou Matomo configuré en mode exempté évite cette contrainte.</em></p>

    <h2>Photographies des véhicules</h2>
    <p>Nous photographions parfois les véhicules avant et après intervention. Ces photos servent d'abord à documenter notre travail et, le cas échéant, à établir un devis.</p>
    <p>Elles ne sont publiées sur ce site ou sur nos réseaux sociaux <strong>qu'avec votre accord explicite</strong>. Les plaques d'immatriculation sont systématiquement masquées. Vous pouvez retirer votre accord à tout moment par simple email, et la photo sera retirée sans délai.</p>

    <h2>Combien de temps nous gardons vos données</h2>
    <ul>
      <li><strong>Données de réservation :</strong> 3 ans à compter du dernier contact.</li>
      <li><strong>Factures :</strong> 10 ans, durée légale de conservation des pièces comptables.</li>
      <li><strong>Photos publiées :</strong> jusqu'à retrait de votre accord.</li>
      <li><strong>Emails :</strong> 3 ans après le dernier échange.</li>
    </ul>

    <h2>Qui a accès à vos données</h2>
    <p>Vos données ne sont ni vendues, ni louées, ni cédées à des fins commerciales. Elles sont accessibles aux seules personnes intervenant dans l'entreprise, ainsi qu'à nos sous-traitants techniques : l'outil de réservation, le prestataire de paiement, l'hébergeur du site et, le cas échéant, notre comptable.</p>

    <h2>Vos droits</h2>
    <p>Vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation, d'opposition et de portabilité sur vos données. Vous pouvez également retirer votre consentement à tout moment lorsque le traitement repose sur celui-ci.</p>
    <p>Pour exercer ces droits, écrivez à <a href="mailto:""" + MAIL + """">""" + MAIL + """</a>. Nous répondons sous un mois. Une pièce d'identité pourra être demandée en cas de doute sur votre identité.</p>
    <p>Si vous estimez que vos droits ne sont pas respectés, vous pouvez saisir la <strong>CNIL</strong> : 3 place de Fontenoy, TSA 80715, 75334 Paris Cedex 07 — <a href="https://www.cnil.fr">www.cnil.fr</a>.</p>

    <h2>Sécurité</h2>
    <p>Nous mettons en œuvre des mesures raisonnables pour protéger vos données : accès aux comptes protégés par mot de passe, connexion au site chiffrée (HTTPS), et limitation des données collectées au strict nécessaire.</p>

    <h2>Modification de cette politique</h2>
    <p>Cette politique peut évoluer, notamment si nous ajoutons un nouvel outil. La date de dernière mise à jour figure ci-dessous.</p>

    <p style="margin-top:2.5rem"><em>Dernière mise à jour : [date].</em></p>
  </div>
</section>
"""

write("confidentialite.html", CONF,
      "Politique de confidentialité | Mobile Car Cleaning",
      "Comment Mobile Car Cleaning collecte et protège vos données personnelles : réservation, photos de véhicules, durées de conservation et exercice de vos droits.")

print("\nTermine.")
