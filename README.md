# POC Docker - Authentification centralisée avec Flask et Nginx

Ce projet est un **POC simple et sécurisé** utilisant Docker, Flask et Nginx pour créer une authentification centralisée avec une vérification via 2FA (Google Authenticator). Une fois connecté, l'utilisateur peut accéder à deux applications web protégées.

---

## 📂 Structure du projet

```
poc-docker-auth/
├── docker-compose.yml
├── nginx/               → Reverse Proxy avec gestion des domaines et auth
├── flask_auth/          → Application Flask pour l'authentification sécurisée
└── demo_app/            → Application web simple pour démonstration
```

---

## ⚙️ Les différents blocs

### 1. Reverse Proxy Nginx (`nginx/`)
- Gère l'accès à l'application d'authentification et aux deux applications protégées.
- Vérifie systématiquement si l'utilisateur est connecté avant d'autoriser l'accès aux applications.

### 2. Application Flask Authentification (`flask_auth/`)
- Fournit une page de login sécurisée avec 2FA.
- Utilise Flask-Login et PyOTP pour générer les OTP compatibles avec Google Authenticator.
- Gère les sessions utilisateurs et expose une route pour que Nginx puisse vérifier l'authentification.

### 3. Applications Web démo (`demo_app/`)
- Deux instances simples affichant chacune une page HTML différente.
- L'accès à ces applications est protégé par la connexion via Flask.

---

## 🚀 Démarrage rapide

### Prérequis
- Docker (https://docs.docker.com/engine/install/)
- Docker Compose (https://docs.docker.com/compose/install/linux/)

### Étapes

1\. Clonez le projet et positionnez-vous dans le dossier racine :

```bash
git clone [URL_DU_REPO]
cd poc-docker-auth
```

2\. Construisez et lancez les conteneurs Docker :

```bash
docker-compose up --build
```

3\. Modifiez votre fichier `/etc/hosts` pour tester localement :

```bash
127.0.0.1 auth.client.com app1.client.com app2.client.com
```

---

## 🔑 Tester le POC

- Rendez-vous sur `http://app1.client.com` ou `http://app2.client.com`.
- Vous serez automatiquement redirigé vers la page de connexion sécurisée `http://auth.client.com`.
- Identifiants de test :
  - **Username :** `demo`
  - Le QR code affiché sur la page permet d'obtenir l'OTP via l'application Google Authenticator.

Une fois connecté, vous pourrez accéder librement aux applications sécurisées.

---

✨ **POC prêt à l'emploi !** ✨

