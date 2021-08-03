# SHOWROOM Event Scheduler

[![Test](https://github.com/road-master/showroom-event-scheduler/workflows/Test/badge.svg)](https://github.com/road-master/showroom-event-scheduler/actions?query=workflow%3ATest)
[![Test Coverage](https://api.codeclimate.com/v1/badges/5c0288c1e946f8be48c0/test_coverage)](https://codeclimate.com/github/road-master/showroom-event-scheduler/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/5c0288c1e946f8be48c0/maintainability)](https://codeclimate.com/github/road-master/showroom-event-scheduler/maintainability)
[![Updates](https://pyup.io/repos/github/road-master/showroom-event-scheduler/shield.svg)](https://pyup.io/repos/github/road-master/showroom-event-scheduler/)
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Froad-master%2Fshowroom-event-scheduler)](http://twitter.com/share?text=SHOWROOM%20Event%20Scheduler&url=https://github.com/road-master/showroom-event-scheduler/&hashtags=python)

Registers live schedules into Google Calendar as event at once.

## Feature

It's no longer need to spend time to register such a much events for live, spending stars, and star collection start prohibition period into your calendar for notification. All you have to do is just only to list today's live schedule into YAML.

## Quickstart

### 1. Enable API in GCP

It's OK to use different Google account from the account who owning calendar.

see: [Create a project and enable the API  |  Google Workspace for Developers](https://developers.google.com/workspace/guides/create-project#enable-api)

### 2. Create desktop application in GCP

Create Desktop application credentials (`credentials.json`).

see: [Create credentials  |  Google Workspace for Developers](https://developers.google.com/workspace/guides/create-credentials#create_a_oauth_client_id_credential)

Register Google account who owning calendar for registering schedule as test user.

[APIs & Services] -> [OAuth consent screen] -> [Test users] -> [+ ADD USERS]

### 3. Set up

Put `credentials.json` into `.gcp` directory.

Copy `config.yml.dist` as `config.yml` and input values of each keys.

Then:

```console
docker-compose up
```

At first time, it requires to OAuth login with Google account who owning calendar.
