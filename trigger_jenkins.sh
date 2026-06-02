#!/bin/bash
TRIGGER_NAME="$1"
TRIGGER_SEVERITY=$(echo "$2" | cut -d'|' -f1)
HOST_NAME=$(echo "$2" | cut -d'|' -f2)
JENKINS_URL="http://192.168.211.50:8080"
JENKINS_USER="nourchene"
JENKINS_TOKEN="1165d6489afe072af158f9ac6e44330d44"
FASTAPI_URL="http://192.168.211.10:8001/alerts/"

# Choisir le bon job selon le trigger
if echo "$TRIGGER_NAME" | grep -qi "cpu\|load"; then
    JOB="Fix-CPU"
    LEVEL="critical"
elif echo "$TRIGGER_NAME" | grep -qiP "m[eé]moire|memory|mem"; then
    JOB="Fix-Memory"
    LEVEL="warning"
elif echo "$TRIGGER_NAME" | grep -qi "disque\|disk\|space"; then
    JOB="Fix-Disk"
    LEVEL="warning"
elif echo "$TRIGGER_NAME" | grep -qi "docker\|container"; then
    JOB="Fix-Docker"
    LEVEL="critical"
else
    JOB="Fix-CPU"
    LEVEL="info"
fi

echo "🚀 Déclenchement du job Jenkins: $JOB"
echo "📋 Trigger: $TRIGGER_NAME"
echo "⚠️ Sévérité: $TRIGGER_SEVERITY"
echo "🖥️ Hôte: $HOST_NAME"

# 1. Déclencher le job Jenkins
curl -X POST "$JENKINS_URL/job/$JOB/build?token=zabbix-docker-token" \
  --user "$JENKINS_USER:$JENKINS_TOKEN" \
  -s
# 2. Envoyer l'alerte à FastAPI → GLPI
curl -X POST "$FASTAPI_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"$TRIGGER_NAME\",
    \"description\": \"Hôte: $HOST_NAME | Sévérité: $TRIGGER_SEVERITY | Job Jenkins: $JOB lancé automatiquement\",
    \"level\": \"$LEVEL\",
    \"source\": \"Zabbix-Jenkins\"
  }" \
  -s

echo "✅ Alerte envoyée à FastAPI → GLPI !"
