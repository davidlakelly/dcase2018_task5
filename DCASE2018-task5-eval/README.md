# DCASE 2018 - Task 5, Evaluation dataset
## Monitoring of domestic activities based on multi-channel acoustics

Authors:

- Gert Dekkers (<gert.dekkers@kuleuven.be>, <https://iiw.kuleuven.be/onderzoek/advise/People/Gert_Dekkers>)
- Peter Karsmakers (<peter.karsmakers@kuleuven.be>, <https://iiw.kuleuven.be/onderzoek/advise/People/PeterKarsmakers>)

[Advanced Integrated Sensing lab (ADVISE)  / Department of Electrical Engineering (ESAT) / KU Leuven](https://iiw.kuleuven.be/onderzoek/advise)

Other (Recording, supervision, ...):

- Steven Lauwereins,
- Bart Thoen,
- Mulu Weldegebreal Adhana,
- Henk Brouckxon,
- Bertold Van den Bergh,
- Toon van Waterschoot, and
- Bart Vanrumste.

# Table of Contents
1. [Dataset](#1-dataset)
2. [Content](#2-content)
4. [Changelog](#3-changelog)
5. [License](#4-license)

1. Dataset
=================================

The dataset is a derivative of the **SINS dataset** and is meant to be used as an evaluation set for the [DCASE2018 Task 5 challenge](http://dcase.community/challenge2018/task-monitoring-domestic-activities). The development set to be used can be found [here](https://zenodo.org/record/1247102#.WzIF_NUzZhE).  The SINS dataset contains a continuous recording of one person living in a vacation home over a period of one week.  It was collected using a network of 13 microphone arrays distributed over the entire home. The microphone array consists of 4 linearly arranged microphones. For this dataset 4 microphone arrays in the combined living room and kitchen area are used. Figure 2 shows the floorplan of the recorded environment along with the position of the used sensor nodes.
<figure>
    <p align="center">
        <img src="http://d33wubrfki0l68.cloudfront.net/5cb3f5d055aa8916eaafa831fefea69c113cbc5c/c201d/images/tasks/challenge2018/task5_2dplan.png" class="img img-responsive" style="width: 300px" align="center">
    </p>
	<p align="center">
        <figcaption>Figure 2: 2D floorplan of the combined kitchen and living room with the used sensor nodes.</figcaption>
    </p>
</figure>
<br>
Approximately 200 hours of data from 7 sensor nodes are taken from the SINS dataset. The partitioning of the data was done randomly. The segments belonging to one particular consecutive activity (e.g. a full session of cooking) were kept together. The data provided for each sensor node contain recordings of the same time period. This means that the performed activities are observed from multiple microphone arrays at the same time instant. 

The recordings were split into audio segments of 10s. Each segment represents one activity.  These audio segments are provided as individual files along with the ground truth. 
The daily activities for this dataset (9) are shown in Table 1 along with the available 10s segments in the dataset and the amount of full sessions of a certain activity (e.g. a cooking session).

<div class="table table-responsive">
<table class="table table-striped">
    <thead>
        <tr>
            <th>Activity</th>
            <th class="col-md-3"># 10s segments</th>
            <th class="col-md-3"># sessions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Absence (nobody present in the room)</td>
            <td>21112</td>
            <td>21</td>
        </tr>
        <tr>
            <td>Cooking</td>
            <td>4221</td>
            <td>6</td>
        </tr>
        <tr>
            <td>Dishwashing</td>
            <td>1477</td>
            <td>5</td>
        </tr>
        <tr>
            <td>Eating</td>
            <td>2100</td>
            <td>6</td>
        </tr>
        <tr>
            <td>Other (present but not doing any relevant activity)</td>
            <td>1960</td>
            <td>59</td>
        </tr>  
        <tr>
            <td>Social activity (visit, phone call)</td>
            <td>3815</td>
            <td>10</td>
        </tr>
        <tr>
            <td>Vacuum cleaning</td>
            <td>868</td>
            <td>4</td>
        </tr> 
        <tr>
            <td>Watching TV</td>
            <td>21116</td>
            <td>4</td>
        </tr>
        <tr>
            <td>Working (typing, mouse click, ...)</td>
            <td>16303</td>
            <td>16</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td><strong>Total</strong></td>
            <td><strong>72972</strong></td>
            <td><strong>131</strong></td>
        </tr>
    </tfoot>
</table>
</div>
<div class="clearfix"></div>

### Recording and annotation procedure

The sensor node configuration used in this setup is a control board together with a linear microphone array. The control board contains an EFM32 ARM cortex M4 microcontroller from Silicon Labs (EFM32WG980) used for sampling the analog audio. The microphone array contains four Sonion N8AC03 MEMS low-power (±17µW) microphones with an inter-microphone distance of 5 cm. The sampling for each audio channel is done sequentially at a rate of 16 kHz with a bit depth of 12.
The annotation was performed in two phases. First, during the data collection a smartphone application was used to let the monitored person(s) annotate the activities while being recorded. The person could only select a fixed set of activities. The application was easy to use and did not significantly influence the transition between activities. Secondly, the start and stop timestamps of each activity were refined by using our own annotation software. Postprocessing and sharing the database involves privacy-related aspects. Besides the person(s) living there, multiple people visited the home. Moreover, during a phone call, one can partially hear the person on the other end. A written informed consent was obtained from all participants.

2. Content
=================================

The content of the dataset is structured in the following manner:

	dataset root
	│   EULA.pdf				End user license agreement
	│   meta.txt				meta data, tsv-format, [audio file (str)][tab][label (str)][tab][session (str)]\n
	│   readme.md				Dataset description (markdown)
	│   readme.html				Dataset description (HTML)
	│
	└───audio					72984 audio segments, 16-bit 16kHz
	│   │   1.wav				name format {segmentID}.wav
	│   │   100.wav
	│   │   ...
	│
	└───evaluation_setup		
	    │   evaluation.txt		evaluation file list, tsv-format, [audio file (str)][tab][label (str)][tab][session (str)]\n
	    │   map.txt				mapping between filenames, tsv-format, [audio file (str)][tab][audio file (str)]\n
	    └───test.txt 			test file list, tsv-format, [audio file (str)]\n

The multi-channel audio files can be found under directory `audio` and are formatted in the following manner:

	{segmentID}.wav

The file `meta.txt` and the content of the folder `evaluation_setup` contain filenames and labels. Additionally, a filename mapping is available that will map the filenames to a filename similar as the [development dataset](https://zenodo.org/record/1247102#.WzIF_NUzZhE). The dataset is structured so that it can work with the [DCASE 2018 Task baseline code](https://github.com/DCASE-REPO/dcase2018_baseline/tree/master/task5). 

3. Changelog
=================================
#### 2.0.0 / 2018-06-26

* Added evaluation set labels
#### 1.0.0 / 2018-06-26

* Initial commit

4. License
=================================

See file [EULA.pdf](EULA.pdf)