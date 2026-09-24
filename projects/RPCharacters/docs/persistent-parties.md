# Persistent parties

Parties created with `/rpcharacter party create <name>` persist across member and
leader logouts and server restarts. Party chat automatically finds online members
from the restored membership. Character switching does not change membership;
parties use player UUIDs.

Membership is saved after creation, joining, leaving, kicking, and disbanding in
`RPCharacters/data/parties.json`. Include this file in server backups. Saves use a
temporary file and replacement, and invalid saved data causes loading to fail
instead of silently resetting the parties.

Explicit `/rpcharacter party leave` still removes a member. If the leader leaves,
the party is disbanded. Pending invites
remain temporary and are not restored on restart.

## Manual checks

- [ ] Create a party with two players and exchange party chat messages
- [ ] Disconnect both players and restart the server
- [ ] After reconnecting, party chat still reaches both players
