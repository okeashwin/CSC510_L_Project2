## CSC510_L_Project2
### Detection and Analysis of Bad Smells

#### Problem Statement
Objective of the project is to feed in data from other projects' GitHub repositories using public GitHub REST API and find deviations from normal good practices by looking at :
  * Github repo issues data
  * Github repo milestones data
  * Github repo commits data
  * Labels data
  * commit patterns

#### Prerequisites
  * Source in all the repositories for which the data needs to be collected in `repos.conf`
  * Add the `GitHub` auth token in `gitable.conf`. The file format should be the same as [ conf template ] (https://github.com/okeashwin/CSC510_L_Project2/blob/master/gitable.conf.sample)
  * Install `sqlite3` on the machine

#### Execution
  * Run `python exec.py` to see the data gathered in the folders `Group1Data`,`Group2Data`,`Group3Data`
