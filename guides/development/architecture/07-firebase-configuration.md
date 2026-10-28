# 7. Firebase in the architecture

Firebase is a configurable external provider for authentication and push messaging. It is not the product database, media store, payment system or source of application authorization. See [security and integrations](04-security-and-integrations.md).

## Capabilities and flow

| Capability | Implemented path | Product boundary |
| --- | --- | --- |
| Sign-in | Angular auth service uses the web project; Java verifies the credential and resolves or links a user | Java session and domain policy determine roles and access |
| Push | Angular obtains a permitted web-push token; Java Messaging sends through notification delivery | Device, outbox and recipient rules remain product-owned |
| Operator setup | Public web settings are served after staged settings pass tests and are activated | Auth and messaging tests must match the active revision |

`DeploymentFirebaseRuntime` keeps separate Admin app identities for authentication and messaging, rejects live use in Explore/demo, and refreshes them after an activated revision changes. Startup `FIREBASE_ENABLED` is supported; the installed package defaults to `false` until Operator activation. Frontend flags alone do not activate the backend.

## Configuration inventory

| Surface | Settings or material | Treatment |
| --- | --- | --- |
| Browser web configuration | `apiKey`, `authDomain`, `projectId`, `storageBucket`, `messagingSenderId`, `appId`; optional `measurementId`; web-push `vapidKey` | Public client metadata, served only for the configured project; the API key is not a server credential |
| Frontend feature switches | `firebaseLoginEnabled`, `firebaseMessagingEnabled` per Angular environment | UI capability switches; they do not activate backend credentials or grant access |
| Server startup/packaging | `FIREBASE_ENABLED`, `FIREBASE_SERVICE_ACCOUNT_PATH`, mounted service-account file | Server-only deployment inputs; never put the private service-account JSON in this guide or browser bundle |
| Staged deployment configuration | Project ID, revision, active flag, public client fields, encrypted authentication and messaging credential envelopes | Operator-owned state; both credential types and test revisions are required for runtime readiness |
| Legacy `fcm` properties | `url`, `apiKey` in `FirebaseProperties` | Separate configuration binding in source; do not confuse it with the public Firebase web API key or activated Admin credentials |

`runtimeReady` requires an active revision, project ID, both encrypted credential envelopes, API key/auth domain/sender ID/app ID/VAPID key, and auth and messaging tests for that revision. `storageBucket` and `measurementId` are modeled but not required by this predicate. Example JSON files contain shapes, not deployable credentials.

## Trust and evidence boundary

The product still checks identity linkage, sessions, REAL/DEMO context, roles, group scope and notification rules. Activation tests do not prove every browser/device delivery. Rotate secrets through the application owner's procedure, preserving encrypted settings and the server credential path.
