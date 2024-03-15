<img src="docs/media/auto_annotation_demo.gif" width="960" height="540" />

# Automated Data Annotation for Computer Vision Applications

## Setup & Install
Install aimakr auto annotation 
Git clone repo
git clone https://github.com/matt-quant-heads-io/aimakr-automated-data-annotaton.git
Create conda environment
conda create -n auto_annotation python=3.8
Activate conda environment
conda activate auto_annotation
Install the dependencies
python -m pip install -R requirements.txt
Install open source label studio UI
Git clone repo 
git clone https://github.com/HumanSignal/label-studio.git
Create conda environment
conda create --name label-studio
Activate conda environment
conda activate label-studio
Install all package dependencies
python -m pip install -e .
Run database migrations
python label_studio/manage.py migrate
python label_studio/manage.py collectstatic
Start the server in development mode at http://localhost:8080
python label_studio/manage.py runserver

Setup the project within Label Studio
Access http://localhost:8080 in your browser
You should see this:



Create a login account
Create a project and call it “automated annotation 1”
Access the labelling interface in the project settings and copy and paste the following code snippet:
<View>
  <Image name="image" value="$image"/>
  <Header value="Rectangle Labels"/>
  <RectangleLabels name="tag1" toName="image">
    <Label value="Person" background="#1e05d6"/>
  <Label value="Car" background="#ed0707"/></RectangleLabels>
</View>


Select the save button
Run the auto annotation code
 Access the terminal within the aimakr-automated-data-annotation repo and run the following command:
python main.py --annotator_type detection_annotator
After the script is complete you should see the following uploaded images and the corresponding annotated bounding boxes for the Person and Car labels contained therein.




