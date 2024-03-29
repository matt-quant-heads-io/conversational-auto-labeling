<h1 align="center">Conversational Auto-labeling for Computer Vision Tasks</h1>
<p align="center">
<img src="https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg" alt="Awesome Badge"/>
<!-- <img src="http://hits.dwyl.com/abhisheknaiidu/awesome-github-profile-readme.svg" alt="Hits Badge"/> -->
<img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99" alt="Star Badge"/>
  
<br>
<a href="https://github.com/matt-quant-heads-io/aimakr-automated-data-annotaton/stargazers"><img src="https://img.shields.io/github/stars/matt-quant-heads-io/aimakr-automated-data-annotaton" alt="Stars Badge"/></a>
<a href="https://github.com/abhisheknaiidu/awesome-github-profile-readme/network/members"><img src="https://img.shields.io/github/forks/matt-quant-heads-io/aimakr-automated-data-annotaton" alt="Forks Badge"/></a>
<a href="https://github.com/abhisheknaiidu/awesome-github-profile-readme/pulls"><img src="https://img.shields.io/github/issues-pr/matt-quant-heads-io/aimakr-automated-data-annotaton" alt="Pull Requests Badge"/></a>
<a href="https://github.com/abhisheknaiidu/awesome-github-profile-readme/issues"><img src="https://img.shields.io/github/issues/matt-quant-heads-io/aimakr-automated-data-annotaton" alt="Issues Badge"/></a>
<a href="https://github.com/abhisheknaiidu/awesome-github-profile-readme/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/matt-quant-heads-io/aimakr-automated-data-annotaton?color=2b9348"></a>
<a href="https://github.com/abhisheknaiidu/awesome-github-profile-readme/blob/master/LICENSE"><img src="https://img.shields.io/github/license/matt-quant-heads-io/aimakr-automated-data-annotaton?color=2b9348" alt="License Badge"/></a>
</p>
<br>
<br>
<p align="center">
  <img src="docs/media/conversational_autolabeling.gif" width="960" height="540" />
</p>


### Contents:
- [Sections](#sections)
  - [Install the dependencies via conda](#install-the-dependencies-via-conda)
  - [Install label studio dependencies via conda (in a new terminal)](#install-label-studio-dependencies-via-conda-in-a-new-terminal)
  - [Run Label Studio database migrations](#run-label-studio-database-migrations)
  - [Creating the Label Studio project](#creating-the-label-studio-project)
    - [Create a (free) account](#create-a-free-account)
- [Run the auto-label system](#run-the-auto-label-system)
- [Contribute](#contribute)
- [License](#license)

## Sections

### Install the dependencies via conda
```
git clone https://github.com/matt-quant-heads-io/conversational-auto-labeling.git
conda create -n auto_annotation python=3.10
conda activate auto_annotation
cd aimakr-automated-data-annotaton
python -m pip install -r requirements.txt
```
### Install label studio dependencies via conda (in a new terminal)
```
cd # i.e. from your home dir
git clone https://github.com/HumanSignal/label-studio.git
conda create -n label-studio python=3.10
conda activate label-studio
cd label-studio
python -m pip install -e .
```

### Run Label Studio database migrations
```
python label_studio/manage.py migrate
python label_studio/manage.py collectstatic
python label_studio/manage.py runserver
```

Access http://localhost:8080 from your browser. If the setup went smoothly you should see the following page.

<p align="center">
  <img src="docs/media/create_acct_screen.png" width="538" height="662" />
</p>



### Creating the Label Studio project
#### Create a (free) account
Create a project and call it “automated annotation 1”

Access the labelling interface in the project settings and copy and paste the following code snippet:
```
<View>
  <Image name="image" value="$image"/>
  <Header value="Rectangle Labels"/>
  <RectangleLabels name="tag1" toName="image">
    <Label value="Person" background="#1e05d6"/>
    <Label value="Car" background="#ed0707"/>
    <Label value="parking meter" background="#9effec"/>
    <Label value="fire hydrant" background="#d3cc0d"/>
    <Label value="stop sign" background="#FFC069"/>
  </RectangleLabels>
</View>
```

Your page should look like the page below.
<p align="center">
  <img src="docs/media/auto_labeling_interface.png" width="714" height="493" />
</p>

Click the save button.

## Run the auto-label system
Inside of chat_app/constants.py, update the following values specific to your setup. 
<p align="center">
  <img src="docs/media/input_ls_env_vars.png" width="638" height="72" />
</p>

Note: To grab your Access Token, navigate to the account page within the Label Studio UI and copy the token to your clipboard (see page below),
<p align="center">
  <img src="docs/media/example_ls_account_token.jpeg" width="861" height="315" />
</p>


Access the terminal, cd into aimakr-automated-data-annotation/chat_app and run via:
```
./run
```

After the script is complete you should see the auto-labeled images detailed in the header gif.

## Contribute

Contributions are always welcome!

## License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)
