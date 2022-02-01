# docs-recommendation-bot
Slackbot intended to respond to "how do I?" style messages with suggested docs. 

**Currently, only Bitbucket is supported.**

## Running the application

This app leverages `pipenv` ([see here](https://pipenv.pypa.io/en/latest/)). Packages are managed through the Pipfile. As a result, `pipenv` should be used to run the file.

To launch the application, run `pipenv run python app.py`.

## Configuration
The app takes a few configuration values:

### Environment Variables
Can be set as normal, or through a `.env` file in the working directory. These _must_ be set, as they give the tokens needed to talk to Slack.

| Name            | Description                                                 | Default |
| --------------- | ----------------------------------------------------------- | ------- |
| SLACK_BOT_TOKEN | The token used by the bot itself. Starts with `xoxb-`       | N/A     |
| SLACK_APP_TOKEN | Token used for the Socket Mode Handler. Starts with `xapp-` | N/A     |

### Application Configuration

Specified through creation of a `config.json` file in the working directory. 

| Name            | Description                                                                                                                                                                                                     | Default |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| GIT_URL         | The base URL of where the repos are stored. e.g `www.bitbucket.org`                                                                                                                                             | N/A     |
| DOC_DIRECTORIES | An array of objects with two fields, `project` and `path`. `project` describes the Bitbucket project the repo is in on the website, and `path` describes the path to the local version of the repo on your disk | N/A     |