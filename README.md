# Mobile Car Cleaning — site web

Site statique. Pas de base de données, pas de WordPress, pas de mise à jour de sécurité à faire.
Hébergement gratuit sur GitHub Pages.

---

## 1. À compléter avant la mise en ligne

Ouvrez les fichiers avec n'importe quel éditeur de texte (Bloc-notes, TextEdit, ou directement
sur github.com en cliquant sur le crayon) et cherchez ces textes :

| À chercher | Où | Remplacer par |
|---|---|---|
| `[06 XX XX XX XX]` | 7 endroits | Votre numéro affiché |
| `+33600000000` | 4 endroits | Votre numéro au format international, sans espaces |
| `votre-nom-utilisateur/votre-evenement` | `reserver.html` | Votre lien Cal.com (voir §3) |
| `[à compléter]` | pied de page + mentions légales | SIREN, adresse, assureur, etc. |
| `contact@mobilecarcleaning.fr` | partout | Votre email si différent |

**Astuce :** dans votre éditeur, utilisez Rechercher/Remplacer (Ctrl+H ou Cmd+H) et cochez
« dans tous les fichiers ». Tout se fait en une fois.

⚠️ Le numéro apparaît à **deux endroits par bloc** : dans `href="tel:..."` (ce qui se compose
quand on clique) et dans le texte affiché. Changez bien les deux, sinon le clic appelle un
mauvais numéro.

---

## 2. Mettre le site en ligne sur GitHub Pages

1. Créez un compte sur [github.com](https://github.com) (gratuit).
2. Cliquez sur **New repository**. Nommez-le par exemple `site-mcc`. Cochez **Public**.
3. Sur la page du dépôt, cliquez **uploading an existing file**.
4. Glissez-déposez **tout le contenu** de ce dossier, y compris le dossier `assets`.
5. Cliquez **Commit changes**.
6. Allez dans **Settings** → **Pages** (menu de gauche).
7. Sous *Source*, choisissez la branche **main** et le dossier **/ (root)**. Cliquez **Save**.
8. Attendez 1 à 2 minutes. Le site est en ligne sur
   `https://votre-pseudo.github.io/site-mcc/`

### Brancher votre nom de domaine

Pour utiliser `mobilecarcleaning.fr` :

1. Dans **Settings → Pages → Custom domain**, tapez `mobilecarcleaning.fr` puis **Save**.
2. Chez Infomaniak, dans la zone DNS, remplacez les enregistrements **A** de `@` par ces quatre
   adresses (celles de GitHub Pages) :
   ```
   185.199.108.153
   185.199.109.153
   185.199.110.153
   185.199.111.153
   ```
3. Créez un enregistrement **CNAME** pour `www` pointant vers `votre-pseudo.github.io`.
4. Revenez dans Settings → Pages et cochez **Enforce HTTPS** (disponible après quelques minutes).

**Vos emails KSuite ne sont pas affectés** : ils dépendent des enregistrements MX, que vous ne
touchez pas. En revanche, ce changement **remplace** le pointage vers LWS : le WordPress ne sera
plus accessible sur ce domaine.

---

## 3. Cal.com — déjà connecté

Le site pointe vers **cal.com/mobilecarcleaningeu**. Le calendrier de `reserver.html` affiche
automatiquement tous les types d'événement publiés sur votre profil : pas besoin de retoucher le
code quand vous en ajoutez un.

### À finir sur cal.com

1. **Supprimez les deux événements par défaut** « 15 min meeting » et « 30 min meeting ». Ils
   sont créés automatiquement à l'inscription et n'ont rien à faire sur votre page publique.
2. **Corrigez la durée d'Express extérieur** : elle est réglée sur 60 minutes alors que le site
   annonce 45 minutes. Alignez les deux.
3. **Créez les événements manquants**, avec la durée réelle :

   | Événement | URL suggérée | Durée |
   |---|---|---|
   | Intérieur | `interieur` | 60 min |
   | Complet | `complet` | 105 min |
   | Complet + protection | `complet-protection` | 150 min |
   | Rénovation intérieure | `renovation-interieure` | 180 min |
   | Rénovation des phares | `phares` | 30 min |
   | Devis sur site (pros) | `devis-pro` | 30 min |

4. Pour **chaque** événement, réglez :
   - **Location** → *Attendee address*, pour que le client saisisse l'adresse d'intervention.
   - **Buffer after event** → 30 à 45 min, pour couvrir les trajets entre deux rendez-vous.
   - **Minimum notice** → 12 h, pour éviter les réservations de dernière minute.
   - Dans **Advanced → Booking questions**, ajoutez : marque et modèle, « Disposez-vous d'un
     robinet extérieur et d'une prise ? » (oui/non), et un champ commentaire libre.
5. Connectez votre agenda Google dans **Apps → Calendar** pour que vos indisponibilités
   personnelles bloquent automatiquement les créneaux.

### Renvoyer vers un seul événement

Si vous préférez que la page de réservation n'affiche qu'une formule, ouvrez `reserver.html`,
cherchez `calLink` et remplacez :

```js
calLink: "mobilecarcleaningeu"
```
par exemple par :
```js
calLink: "mobilecarcleaningeu/complet"
```

---

## 4. Modifier le site au quotidien

### Changer un prix
Les prix sont écrits en clair dans le HTML. Cherchez par exemple `79 €` dans `index.html` et
`services.html`, et remplacez. Pensez à changer aussi la mention dans le sélecteur du hero.

### Changer une couleur
Tout est en haut de `assets/style.css`, dans le bloc `:root`. Modifiez une valeur, elle change
sur toutes les pages.

### Remplacer la vidéo d'accueil
Écrasez `assets/hero.mp4` par votre nouveau fichier, **en gardant le même nom**. Compressez-le
avant : visez moins de 3 Mo. Mettez aussi à jour `assets/hero.jpg` (l'image affichée sur mobile).

### Ajouter une photo dans Réalisations
Dans `realisations.html`, chaque chantier est un bloc `<article class="work">`. Copiez-en un,
collez-le, changez le texte, et remplacez la ligne du bloc `work__ph` par :
```html
<img src="assets/ma-photo.jpg" alt="Description de la photo">
```
L'attribut `data-cat` doit valoir `exterieur`, `interieur`, `renovation` ou `pro` pour que les
filtres fonctionnent.

### Ajouter un article de journal
Dupliquez un fichier `journal-xxx.html`, renommez-le, modifiez le contenu, puis ajoutez une
carte dans `journal.html` en copiant un bloc `<a class="post">`.

### ⚠️ En-tête et pied de page
Ils sont recopiés dans chaque page (c'est le prix d'un site sans logiciel). Si vous ajoutez une
entrée au menu, il faut la reporter dans **les 13 fichiers**. Le fichier `build.py` sert
justement à ça : modifiez la liste `NAV` en haut, lancez `python3 build.py`, et toutes les pages
sont régénérées. Attention : **cela écrase vos modifications manuelles**. Si vous préférez
éditer à la main, supprimez `build.py` et oubliez-le.

---

## 5. Après la mise en ligne

- [ ] Vérifier le site sur téléphone (la majorité de vos visiteurs)
- [ ] Tester le calendrier de réservation de bout en bout, en réservant vous-même
- [ ] Créer la fiche **Google Business Profile** en zone de service, adresse masquée
- [ ] Déclarer le site dans [Google Search Console](https://search.google.com/search-console)
- [ ] Compléter les mentions légales (obligatoire dès la mise en ligne)
- [ ] Remplacer les photos d'exemple par les vôtres

---

## Structure des fichiers

```
index.html                        Accueil
services.html                     Services particuliers
detailing.html                    Rénovation et restitution de leasing
b2b.html                          Pros, flottes, retour de leasing
realisations.html                 Galerie avec filtres
a-propos.html                     À propos
journal.html                      Liste des articles
journal-sel-hiver.html            Article
journal-restitution-leasing.html  Article
journal-sans-rincage.html         Article
reserver.html                     Calendrier Cal.com
mentions-legales.html             Obligatoire
confidentialite.html              Obligatoire (RGPD)
assets/style.css                  Tous les styles
assets/main.js                    Menu, onglets, filtres, jauge
assets/logo.png                   Logo blanc
assets/hero.mp4 / hero.jpg        Vidéo d'accueil et son image
build.py                          Régénère les pages (optionnel)
```

---

## 6. Les photos à fournir

Chaque cadre en pointillés sur le site indique une photo manquante, avec le nom de fichier
attendu et ce qu'il faut photographier. Déposez simplement le fichier dans `assets/` avec
**exactement ce nom**, puis remplacez le `<span>…</span>` du cadre par :

```html
<img src="assets/mon-fichier.jpg" alt="Description de la photo">
```

Format conseillé : JPG, 1600 px de large maximum, compressé sous 300 Ko (utilisez
[squoosh.app](https://squoosh.app), gratuit). Les bandes larges gagnent à être prises en paysage.


**Bandeaux de titre (image de fond, format paysage large)**

- `assets/header-services.jpg`
- `assets/header-renovation.jpg`
- `assets/header-pros.jpg`
- `assets/header-realisations.jpg`
- `assets/header-journal.jpg`
- `assets/header-reserver.jpg`
- `assets/header-mentions.jpg`
- `assets/header-confidentialite.jpg`
- `assets/header-journal-sel-hiver.jpg`
- `assets/header-journal-restitution-leasing.jpg`
- `assets/header-journal-sans-rincage.jpg`

> Ces images passent sous un dégradé sombre : privilégiez des photos plutôt contrastées, sans
> détail important au centre-gauche où se place le titre. La page À propos n'en a pas, elle garde
> son fond dégradé. Une pastille en bas à droite du bandeau rappelle le nom du fichier attendu —
> supprimez la ligne `<p class="ph-hint">…</p>` une fois la photo posée.

**Page d'accueil**

- `assets/reservation.jpg`
- `assets/arrivee.jpg`
- `assets/lavage.jpg`
- `assets/finition.jpg`
- `assets/intervention-domicile.jpg`
- `assets/methode-sans-rincage.jpg`
- `assets/methode-jet.jpg`

**Services**

- `assets/services-bande.jpg`

**Rénovation (avant / après)**

- `assets/avant-siege.jpg`
- `assets/apres-siege.jpg`
- `assets/avant-phare.jpg`
- `assets/apres-phare.jpg`
- `assets/protection-application.jpg`

**Pros & flottes**

- `assets/b2b-bande.jpg`

**À propos**

- `assets/equipe.jpg`
- `assets/vehicule.jpg`
- `assets/apropos-bande.jpg`

**Réserver**

- `assets/reserver-bande.jpg`

**Journal**

- `assets/journal-restitution-leasing.jpg`
- `assets/journal-sans-rincage.jpg`
- `assets/journal-sel-hiver.jpg`

**Réalisations**

- `assets/real-berline-allemande-peintu.jpg`
- `assets/real-break-familial-sieges-ti.jpg`
- `assets/real-citadine-entretien-mensu.jpg`
- `assets/real-marchand-vo-lot-de-quatr.jpg`
- `assets/real-monospace-optiques-opaci.jpg`
- `assets/real-retour-de-leasing-utilit.jpg`

> Photographiez toujours **avant et après au même endroit, même angle, même lumière**.
> C'est ce qui rend une galerie crédible. Et masquez les plaques d'immatriculation.
