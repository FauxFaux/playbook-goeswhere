#!/bin/sh

VCSUSER="git"

# NOTE: Replace this with the path to your Phabricator directory.
ROOT="/opt/phabricator/phabricator"

if [ "$1" != "$VCSUSER" ];
then
  exit 1
fi

exec "$ROOT/bin/ssh-auth" $@
