/* ============================================================
   RÉSERVATION EN LIGNE (page reserver.html)

   La page affiche les créneaux libres et envoie la réservation à
   un petit programme Google Apps Script, relié à Google Agenda.

   À FAIRE UNE FOIS : coller entre les guillemets ci-dessous l'adresse
   de l'application web Apps Script (elle se termine par /exec).
   Tant qu'elle est vide, la page affiche le téléphone et WhatsApp.

   PRIX ET DURÉES : ils doivent rester identiques à ceux du fichier
   Apps Script (c'est lui qui fait foi dans l'email et l'agenda).
   ============================================================ */
(function () {
  'use strict';

  var ENDPOINT = '';
  if (window.MCC_ENDPOINT) ENDPOINT = window.MCC_ENDPOINT;

  var TELEPHONE = '06 23 32 64 82';
  var JOURS_AFFICHES = 21;

  var SERVICES = {
    'express-exterieur':   { label: 'Express extérieur',    minutes: 45,  prix: { citadine: 49,  berline: 59,  suv: 69 },
                             options: ['tres-sale', 'moteur', 'phares'] },
    'interieur':           { label: 'Intérieur',            minutes: 60,  prix: { citadine: 49,  berline: 59,  suv: 69 },
                             options: ['tres-sale', 'ozone', 'poils', 'cuir', 'phares'] },
    'complet':             { label: 'Complet',              minutes: 105, prix: { citadine: 89,  berline: 99,  suv: 109 },
                             options: ['tres-sale', 'ozone', 'poils', 'cuir', 'moteur', 'phares'] },
    'complet-protection':  { label: 'Complet + protection', minutes: 150, prix: { citadine: 129, berline: 145, suv: 165 },
                             options: ['tres-sale', 'ozone', 'poils', 'cuir', 'moteur', 'phares'] },
    'detailing-interieur': { label: 'Detailing intérieur',  minutes: 180, prix: { citadine: 129, berline: 139, suv: 149 },
                             options: ['ozone', 'poils', 'cuir', 'phares'] },
    'phares':              { label: 'Rénovation des phares', minutes: 30, prix: { citadine: 59,  berline: 59,  suv: 59 },
                             options: [] }
  };
  var OPTIONS = {
    'tres-sale': { minutes: 15, prix: 15 },
    'ozone':     { minutes: 30, prix: 29 },
    'poils':     { minutes: 20, prix: 20 },
    'cuir':      { minutes: 20, prix: 30 },
    'moteur':    { minutes: 30, prix: 30 },
    'phares':    { minutes: 30, prix: 59 }
  };

  var JOURS = ['dim.', 'lun.', 'mar.', 'mer.', 'jeu.', 'ven.', 'sam.'];
  var JOURS_LONGS = ['dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi'];
  var MOIS = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.'];
  var MOIS_LONGS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août',
                    'septembre', 'octobre', 'novembre', 'décembre'];

  var form = document.getElementById('resa');
  if (!form) return;
  function $(id) { return document.getElementById(id); }

  var el = {
    steps: $('resa-steps'), off: $('resa-off'), devis: $('resa-devis'), ok: $('resa-ok'),
    picks: [].slice.call(document.querySelectorAll('#resa-formules .pick')),
    vtype: [].slice.call(document.querySelectorAll('#resa-vtype .vtype__btn')),
    options: [].slice.call(document.querySelectorAll('#resa-options .pick')),
    optionsStep: $('resa-step-options'),
    prix: $('resa-prix'), duree: $('resa-duree'),
    days: $('resa-days'), slots: $('resa-slots'), status: $('resa-status'),
    submit: $('resa-submit'), recap: $('resa-recap'), erreur: $('resa-erreur')
  };

  var state = { service: 'complet', vtype: 'citadine', options: [], date: null, heure: null,
                jours: null, ouvertLe: Date.now(), envoi: false };
  var cache = {};
  var requete = 0;
  var minuterie = null;

  /* ---------- Outils ---------- */

  function duree(min) {
    var h = Math.floor(min / 60), m = min % 60;
    if (!h) return m + ' min';
    return h + ' h' + (m ? ' ' + (m < 10 ? '0' : '') + m : '');
  }
  function parts(ds) { var p = ds.split('-'); return { y: +p[0], m: +p[1] - 1, d: +p[2] }; }
  function weekday(ds) { var p = parts(ds); return new Date(Date.UTC(p.y, p.m, p.d)).getUTCDay(); }
  function dateLongue(ds) { var p = parts(ds); return JOURS_LONGS[weekday(ds)] + ' ' + p.d + ' ' + MOIS_LONGS[p.m]; }
  function heureLongue(h) { var p = h.split(':'); return (+p[0]) + ' h ' + p[1]; }
  function aujourdhui() {
    var d = new Date();
    return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
  }
  function majuscule(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

  function devis() {
    var s = SERVICES[state.service];
    var min = s.minutes, prix = s.prix[state.vtype];
    state.options.forEach(function (k) { min += OPTIONS[k].minutes; prix += OPTIONS[k].prix; });
    return { minutes: min, prix: prix };
  }

  /* ---------- Formule, gabarit, options ---------- */

  function choisirFormule(service, silencieux) {
    var estDevis = service === 'devis';
    if (!estDevis && !SERVICES[service]) service = 'complet';
    el.picks.forEach(function (p) {
      var on = p.getAttribute('data-service') === service;
      var input = p.querySelector('input');
      if (input) input.checked = on;
      p.setAttribute('data-checked', String(on));
    });
    try { history.replaceState(null, '', 'reserver.html?f=' + service); } catch (e) {}

    el.devis.hidden = !estDevis;
    el.steps.hidden = estDevis || !ENDPOINT;
    el.off.hidden = estDevis || !!ENDPOINT;
    if (estDevis) return;

    state.service = service;
    var permises = SERVICES[service].options;
    el.options.forEach(function (o) {
      var k = o.getAttribute('data-option');
      var ok = permises.indexOf(k) !== -1;
      o.hidden = !ok;
      var input = o.querySelector('input');
      if (!ok && input && input.checked) { input.checked = false; o.setAttribute('data-checked', 'false'); }
    });
    el.optionsStep.hidden = permises.length === 0;
    lireOptions();
    if (!silencieux) chargerCreneaux();
  }

  function lireOptions() {
    state.options = el.options.filter(function (o) {
      var input = o.querySelector('input');
      return !o.hidden && input && input.checked;
    }).map(function (o) { return o.getAttribute('data-option'); });
    majTotal();
  }

  function majTotal() {
    var q = devis();
    el.prix.textContent = q.prix + ' €';
    el.duree.textContent = duree(q.minutes);
    majBouton();
  }

  /* ---------- Créneaux ---------- */

  function cle() { return state.service + '|' + state.options.slice().sort().join(','); }

  function statut(texte, type) {
    el.status.className = 'resa__status' + (type === 'error' ? ' resa__status--error' : '');
    el.status.innerHTML = '';
    if (type === 'loading') {
      var sp = document.createElement('span');
      sp.className = 'booking__spinner';
      sp.setAttribute('aria-hidden', 'true');
      el.status.appendChild(sp);
    }
    el.status.appendChild(document.createTextNode(texte || ''));
    el.status.hidden = !texte;
  }

  function chargerCreneaux(forcer) {
    clearTimeout(minuterie);
    minuterie = setTimeout(function () { telecharger(forcer); }, 200);
  }

  function telecharger(forcer) {
    var k = cle();
    var c = cache[k];
    if (!forcer && c && Date.now() - c.t < 120000) { afficherJours(c.jours); return; }

    var num = ++requete;
    el.days.innerHTML = '';
    el.slots.innerHTML = '';
    state.heure = null;
    majBouton();
    statut('Recherche des créneaux libres…', 'loading');

    var qs = 'action=slots&service=' + encodeURIComponent(state.service) +
             '&vtype=' + encodeURIComponent(state.vtype) +
             '&options=' + encodeURIComponent(state.options.join(',')) +
             '&from=' + aujourdhui() + '&days=' + JOURS_AFFICHES;
    fetch(ENDPOINT + (ENDPOINT.indexOf('?') === -1 ? '?' : '&') + qs, { method: 'GET' })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (num !== requete) return;
        if (!data || !data.ok) throw new Error((data && data.message) || 'Réponse invalide');
        cache[k] = { t: Date.now(), jours: data.days };
        afficherJours(data.days);
      })
      .catch(function () {
        if (num !== requete) return;
        statut('Impossible de charger les créneaux pour le moment. Appelez-nous au ' + TELEPHONE +
               ' ou écrivez-nous sur WhatsApp, on cale le rendez-vous ensemble.', 'error');
      });
  }

  function afficherJours(jours) {
    state.jours = jours;
    el.days.innerHTML = '';
    el.slots.innerHTML = '';
    var premier = null, garder = false;
    /* Aujourd'hui sans créneau (préavis de 12 h) : on ne l'affiche pas. */
    if (jours.length && jours[0].date === aujourdhui() && !jours[0].slots.length) jours = jours.slice(1);
    jours.forEach(function (j) {
      var p = parts(j.date);
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'resa__day';
      b.setAttribute('data-date', j.date);
      b.setAttribute('aria-pressed', 'false');
      var n = j.slots.length;
      b.disabled = n === 0;
      b.setAttribute('aria-label', dateLongue(j.date) + (n ? ', ' + n + ' créneau' + (n > 1 ? 'x' : '') : ', complet'));
      b.innerHTML = '<small>' + JOURS[weekday(j.date)] + '</small><b>' + p.d + '</b><small>' + MOIS[p.m] +
                    '</small><span class="resa__count">' + (n ? n + ' libre' + (n > 1 ? 's' : '') : 'complet') + '</span>';
      b.addEventListener('click', function () { choisirJour(j.date, true); });
      el.days.appendChild(b);
      if (n && !premier) premier = j.date;
      if (n && j.date === state.date) garder = true;
    });
    if (!premier) {
      statut('Aucun créneau libre sur les trois prochaines semaines pour cette formule. Appelez-nous au ' +
             TELEPHONE + ', on trouve souvent une solution.', 'error');
      state.date = null;
      majBouton();
      return;
    }
    statut('');
    choisirJour(garder ? state.date : premier, false);
  }

  function choisirJour(ds, parUtilisateur) {
    var precedent = state.date;
    state.date = ds;
    if (precedent !== ds) state.heure = null;
    [].slice.call(el.days.children).forEach(function (b) {
      var on = b.getAttribute('data-date') === ds;
      b.setAttribute('aria-pressed', String(on));
      if (on && parUtilisateur && b.scrollIntoView) {
        try { b.scrollIntoView({ block: 'nearest', inline: 'nearest', behavior: 'smooth' }); } catch (e) {}
      }
    });
    var jour = (state.jours || []).filter(function (j) { return j.date === ds; })[0];
    var slots = jour ? jour.slots : [];
    if (state.heure && slots.indexOf(state.heure) === -1) state.heure = null;

    el.slots.innerHTML = '';
    var groupes = [['Matin', function (h) { return h < '12:00'; }],
                   ['Après-midi', function (h) { return h >= '12:00' && h < '18:00'; }],
                   ['Soir', function (h) { return h >= '18:00'; }]];
    groupes.forEach(function (g) {
      var liste = slots.filter(g[1]);
      if (!liste.length) return;
      var bloc = document.createElement('div');
      bloc.className = 'resa__slotgroup';
      var h = document.createElement('h4');
      h.textContent = g[0];
      var grille = document.createElement('div');
      grille.className = 'resa__slotlist';
      liste.forEach(function (heure) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'resa__slot';
        b.textContent = heure.replace(':', ' h ');
        b.setAttribute('data-heure', heure);
        b.setAttribute('aria-pressed', String(heure === state.heure));
        b.addEventListener('click', function () { choisirHeure(heure); });
        grille.appendChild(b);
      });
      bloc.appendChild(h);
      bloc.appendChild(grille);
      el.slots.appendChild(bloc);
    });
    majBouton();
  }

  function choisirHeure(h) {
    state.heure = h;
    [].slice.call(el.slots.querySelectorAll('.resa__slot')).forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-heure') === h));
    });
    el.erreur.hidden = true;
    majBouton();
  }

  function majBouton() {
    var q = devis();
    if (state.date && state.heure) {
      el.submit.textContent = 'Confirmer le rendez-vous du ' + JOURS[weekday(state.date)].replace('.', '') + ' ' +
        parts(state.date).d + ' ' + MOIS[parts(state.date).m] + ' à ' + heureLongue(state.heure);
      el.recap.textContent = SERVICES[state.service].label + ', ' + duree(q.minutes) + ', ' + q.prix +
        ' € à régler sur place. Sans acompte.';
    } else {
      el.submit.textContent = 'Choisissez un jour et une heure';
      el.recap.textContent = 'Sans acompte. Paiement sur place, par carte ou espèces.';
    }
  }

  /* ---------- Envoi ---------- */

  var champs = ['resa-nom', 'resa-tel', 'resa-email', 'resa-adresse'];

  function erreur(msg, champ) {
    el.erreur.textContent = msg;
    el.erreur.hidden = false;
    if (champ) {
      champ.setAttribute('aria-invalid', 'true');
      champ.focus();
    }
  }

  function verifier() {
    champs.forEach(function (id) { $(id).removeAttribute('aria-invalid'); });
    if (!state.date || !state.heure) {
      erreur('Choisissez un jour et une heure.');
      $('resa-step-creneau').scrollIntoView({ behavior: 'smooth', block: 'start' });
      return false;
    }
    var nom = $('resa-nom'), tel = $('resa-tel'), email = $('resa-email'), adr = $('resa-adresse');
    if (nom.value.trim().length < 2) return erreur('Indiquez votre nom.', nom), false;
    if (tel.value.replace(/[^\d]/g, '').length < 10) return erreur('Indiquez un numéro de téléphone valide.', tel), false;
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.value.trim())) return erreur('Indiquez une adresse email valide.', email), false;
    if (adr.value.trim().length < 6) return erreur('Indiquez l’adresse où se trouve le véhicule.', adr), false;
    if (!$('resa-consent').checked) return erreur('Cochez la case d’accord pour que nous puissions vous contacter.', $('resa-consent')), false;
    return true;
  }

  function envoyer(e) {
    e.preventDefault();
    if (state.envoi) return;
    el.erreur.hidden = true;
    if (!verifier()) return;
    if ($('resa-website').value || Date.now() - state.ouvertLe < 3000) return;

    var corps = {
      action: 'book', service: state.service, vtype: state.vtype, options: state.options,
      date: state.date, heure: state.heure,
      nom: $('resa-nom').value, tel: $('resa-tel').value, email: $('resa-email').value,
      adresse: $('resa-adresse').value, vehicule: $('resa-vehicule').value,
      message: $('resa-message').value, abonne: $('resa-abonne').checked,
      consent: $('resa-consent').checked, website: ''
    };
    state.envoi = true;
    el.submit.disabled = true;
    var texte = el.submit.textContent;
    el.submit.textContent = 'Réservation en cours…';

    fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' },
                      body: JSON.stringify(corps) })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        if (data && data.ok) return succes(data.recap, corps.email);
        if (data && data.code === 'slot_taken') {
          erreur(data.message);
          delete cache[cle()];
          telecharger(true);
          return;
        }
        erreur((data && data.message) || 'La réservation n’a pas abouti. Réessayez ou appelez le ' + TELEPHONE + '.');
      })
      .catch(function () {
        erreur('La réservation n’a pas pu être envoyée. Vérifiez votre connexion, ou appelez-nous au ' + TELEPHONE + '.');
      })
      .then(function () {
        state.envoi = false;
        el.submit.disabled = false;
        if (el.submit.textContent === 'Réservation en cours…') el.submit.textContent = texte;
        majBouton();
      });
  }

  function succes(r, email) {
    var dl = $('resa-ok-details');
    dl.innerHTML = '';
    [['Date', majuscule(r.dateLabel) + ' à ' + r.heureLabel],
     ['Formule', r.formule + ' (' + r.gabarit + ')'],
     ['Options', r.options.length ? r.options.join(', ') : 'aucune'],
     ['Durée prévue', r.duree],
     ['Prix', r.abonne ? 'inclus dans votre abonnement' : r.prix + ' €, à régler sur place'],
     ['Adresse', r.adresse],
     ['Référence', r.ref]].forEach(function (l) {
      var dt = document.createElement('dt'); dt.textContent = l[0];
      var dd = document.createElement('dd'); dd.textContent = l[1];
      dl.appendChild(dt); dl.appendChild(dd);
    });
    $('resa-ok-email').textContent = email;
    el.steps.hidden = true;
    el.ok.hidden = false;
    el.ok.scrollIntoView({ behavior: 'smooth', block: 'start' });
    el.ok.focus();
    cache = {};
  }

  /* ---------- Branchements ---------- */

  el.picks.forEach(function (p) {
    var input = p.querySelector('input');
    if (input) input.addEventListener('change', function () { choisirFormule(p.getAttribute('data-service')); });
  });
  el.vtype.forEach(function (b) {
    b.addEventListener('click', function () {
      state.vtype = b.getAttribute('data-vtype');
      el.vtype.forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
      majTotal();
    });
  });
  el.options.forEach(function (o) {
    var input = o.querySelector('input');
    if (input) input.addEventListener('change', function () {
      o.setAttribute('data-checked', String(input.checked));
      lireOptions();
      chargerCreneaux();
    });
  });
  form.addEventListener('submit', envoyer);
  champs.concat(['resa-consent']).forEach(function (id) {
    $(id).addEventListener('input', function () { $(id).removeAttribute('aria-invalid'); el.erreur.hidden = true; });
  });
  $('resa-encore').addEventListener('click', function () {
    el.ok.hidden = true;
    el.steps.hidden = false;
    state.heure = null;
    state.ouvertLe = Date.now();
    chargerCreneaux(true);
    $('booking').scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  var depart = 'complet';
  try { depart = new URLSearchParams(location.search).get('f') || 'complet'; } catch (e) {}
  choisirFormule(depart, !ENDPOINT);
})();
