/* ============================================================
   MOBILE CAR CLEANING — script commun à toutes les pages.
   Chaque bloc se désactive tout seul si l'élément est absent,
   donc le même fichier fonctionne sur toutes les pages.
   ============================================================ */

/* --- Menu mobile --- */
(function(){
  var b = document.getElementById('burger'), n = document.getElementById('nav');
  if(!b || !n) return;
  b.addEventListener('click', function(){
    var open = n.getAttribute('data-open') === 'true';
    n.setAttribute('data-open', String(!open));
    b.setAttribute('aria-expanded', String(!open));
    b.setAttribute('aria-label', !open ? 'Fermer le menu' : 'Ouvrir le menu');
  });
  n.addEventListener('click', function(e){
    if(e.target.tagName === 'A'){
      n.setAttribute('data-open','false');
      b.setAttribute('aria-expanded','false');
    }
  });
})();

/* --- Onglets (page d'accueil : déroulé d'une intervention) --- */
(function(){
  var tabs = [].slice.call(document.querySelectorAll('.tab'));
  if(!tabs.length) return;
  function show(i){
    tabs.forEach(function(t, j){
      var panel = document.getElementById(t.getAttribute('aria-controls'));
      t.setAttribute('aria-selected', String(j === i));
      if(panel) panel.hidden = (j !== i);
    });
  }
  tabs.forEach(function(t, i){
    t.addEventListener('click', function(){ show(i); });
    t.addEventListener('keydown', function(e){
      var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if(!d) return;
      e.preventDefault();
      var next = (i + d + tabs.length) % tabs.length;
      show(next); tabs[next].focus();
    });
  });
  show(0);
})();

/* --- Jauge d'eau : remplissage à l'arrivée dans l'écran --- */
(function(){
  var g = document.getElementById('gauge');
  if(!g) return;
  if(!('IntersectionObserver' in window)){ g.setAttribute('data-visible','true'); return; }
  var o = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(en.isIntersecting){ g.setAttribute('data-visible','true'); o.disconnect(); }
    });
  }, { threshold: .35 });
  o.observe(g);
})();

/* ============================================================
   SÉLECTEUR DE FORMULE DU HERO
   Chaque <label class="pick"> contient un bouton radio et un
   attribut data-cal indiquant le service Setmore à ouvrir.
   Le bouton "Réserver" emporte cette valeur dans son adresse.
   ============================================================ */
(function(){
  var picks = [].slice.call(document.querySelectorAll('.pick'));
  var cta = document.getElementById('pick-cta');
  /* Uniquement les boutons du groupe du hero : ceux des grilles de cartes
     portent un data-scope et sont pilotes par le bloc en bas de fichier. */
  var vtypeBtns = [].slice.call(document.querySelectorAll('.vtype:not([data-scope]) .vtype__btn'));
  if(!picks.length) return;

  var currentVtype = 'citadine';

  function updatePrices(){
    picks.forEach(function(p){
      var price = p.getAttribute('data-p-' + currentVtype);
      var out = p.querySelector('.tile-price');
      if(!price || !out) return;
      out.textContent = price + ' €';
      var sfx = out.getAttribute('data-suffix');
      if(sfx){
        var s = document.createElement('small');
        s.textContent = sfx;
        out.appendChild(s);
      }
    });
  }

  function sync(){
    picks.forEach(function(p){
      var input = p.querySelector('input');
      var on = input && input.checked;
      p.setAttribute('data-checked', String(!!on));
      if(on && cta){
        /* Le forfait choisi voyage dans l'URL du bouton : la page de
           reservation ouvre alors directement le bon creneau. Arriver
           sur reserver.html par le menu affiche toutes les formules. */
        var slug = p.getAttribute('data-cal') || '';
        cta.textContent = 'Réserver — ' + (p.getAttribute('data-label') || 'ce forfait');
        cta.href = slug ? 'reserver.html?f=' + encodeURIComponent(slug) : 'reserver.html';
      }
    });
  }

  picks.forEach(function(p){
    var input = p.querySelector('input');
    if(input) input.addEventListener('change', sync);
  });

  vtypeBtns.forEach(function(b){
    b.addEventListener('click', function(){
      currentVtype = b.getAttribute('data-vtype');
      vtypeBtns.forEach(function(x){ x.setAttribute('aria-pressed', String(x === b)); });
      updatePrices();
    });
  });

  updatePrices();
  sync();
})();
/* ============================================================
   FILTRES DE LA PAGE RÉALISATIONS
   Les boutons portent data-filter, les cartes data-cat.
   ============================================================ */
(function(){
  var btns = [].slice.call(document.querySelectorAll('[data-filter]'));
  var items = [].slice.call(document.querySelectorAll('[data-cat]'));
  if(!btns.length || !items.length) return;

  btns.forEach(function(b){
    b.addEventListener('click', function(){
      var f = b.getAttribute('data-filter');
      btns.forEach(function(x){ x.setAttribute('aria-selected', String(x === b)); });
      items.forEach(function(it){
        it.hidden = !(f === 'tout' || it.getAttribute('data-cat') === f);
      });
    });
  });
})();

/* --- Année automatique dans le pied de page --- */
(function(){
  var y = document.getElementById('year');
  if(y) y.textContent = new Date().getFullYear();
})();

/* --- Prix par type de véhicule, pour les grilles de cartes --- */
(function(){
  var groups = [].slice.call(document.querySelectorAll('.vtype[data-scope]'));
  groups.forEach(function(group){
    var scope = document.querySelector(group.getAttribute('data-scope'));
    if(!scope) return;
    var btns = [].slice.call(group.querySelectorAll('.vtype__btn'));
    var priceEls = [].slice.call(scope.querySelectorAll('[data-p-citadine]'));
    function apply(vtype){
      priceEls.forEach(function(el){
        var v = el.getAttribute('data-p-' + vtype);
        if(!v) return;
        el.textContent = v + ' €';
        /* Certains prix portent un suffixe (/mois, /véh.) : on le remet. */
        var sfx = el.getAttribute('data-suffix');
        if(sfx){
          var s = document.createElement('small');
          s.textContent = sfx;
          el.appendChild(s);
        }
      });
      btns.forEach(function(b){
        b.setAttribute('aria-pressed', String(b.getAttribute('data-vtype') === vtype));
      });
    }
    btns.forEach(function(b){
      b.addEventListener('click', function(){ apply(b.getAttribute('data-vtype')); });
    });
  });
})();
