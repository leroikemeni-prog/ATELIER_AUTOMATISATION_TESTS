# API Choice

- Étudiant : KEMENI DANIEL
- API choisie : Frankfurter (taux de change)
- URL base : https://api.frankfurter.app
- Documentation officielle : https://frankfurter.dev
- Auth : None
- Endpoints testés :
  - GET /latest?from=EUR
  - GET /latest?from=EUR&to=USD
  - GET /latest?from=XXX (cas d'erreur attendu)
- Hypothèses de contrat :
  - 200 + JSON avec les champs base (string), date (string), rates (objet de nombres)
  - Devise inconnue : code 4xx (404 ou 422)
- Limites / rate limiting connu : pas de clé, usage raisonnable demandé
- Risques : indisponibilité ponctuelle, latence variable
