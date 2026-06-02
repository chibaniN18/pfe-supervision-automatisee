# PFE - Supervision Automatisée et Auto-Remédiation
## Réalisé par : Chibani Nourchene - Everience Tunisie

## Architecture
- **Zabbix** : Supervision et détection des incidents
- **Jenkins** : Orchestration des jobs de remédiation  
- **Ansible** : Exécution des playbooks de remédiation
- **Docker** : Conteneurisation de l'application FastAPI
- **FastAPI** : API de liaison entre Zabbix et GLPI
- **GLPI** : Gestion automatique des tickets d'incidents
- **GitHub** : Gestion du code source

## Flux automatique
## Triggers configurés
| Trigger | Job Jenkins | Playbook Ansible |
|---------|-------------|-----------------|
| Docker arrêté | Fix-Docker | fix_docker.yml |
| Disque plein | Fix-Disk | fix_disk.yml |
| Mémoire élevée | Fix-Memory | fix_memory.yml |
| CPU élevé | Fix-CPU | fix_cpu.yml |
