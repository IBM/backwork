# CI

## Artifactory

At this time, .travis.yml is used directly for pushing the gem to
Artifactory.

If you need to encrypt a new Artifactory password, use this command:

```shell
travis encrypt <MY_PASSWORD> --add deploy.password
```

You can then paste the output in `.travis.yml` under `deploy: password:`

You may first need to install and log into the Travis client:

```shell
gem install travis --no-rdoc --no-ri
travis login -X -g <...>
```

## Slack

The value for `notifications/slack/secure` is obtained by running the following
command.

```sh
travis encrypt "<SLACK_TEAM_SUB_DOMAIN>:<SLACK_TOKEN>" --add notifications.slack
```
