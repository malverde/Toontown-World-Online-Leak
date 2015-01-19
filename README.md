# README #

# IMPORTANT PLEASE READ! #

### Version ###

2.0.0

* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

### Summary of set up ###
1. Set up a Windows Server 2008 R2
2. Install vns_full.exe
3. Install both Panda3D versions
4. Download tcp.reg and the .bat that goes with it and run the .BAT
5. Download a Branch, either TTW-PROD-Cluster or TTW-DEV-Cluster 
6. Extract downloaded ZIP and then open start_astron.bat, start_ubderdog.bat and start_ai.bat

Basic set-up has been completed.


### Configuration ###
Enable TCP traffic ports from 700 through 800
Disable the FIREWALL (incoming and outbound traffic)

### Dependencies ###
1. Panda3D 
2. vfs_full.exe

### Database configuration ###
Database is currently in the /astron/databases/astrondb/ folder located within the server/client BRANCH.

### How to run tests ###
Have the server deployed and make sure you have everything setup. 
Ensure a client version has been made/modified and download it. Edit the connecting IP address in the starting file.

### Deployment instructions ###

### Contribution guidelines ###

### Writing tests ###
Commits will be made in the **Branch** - features that are new or **VERY** **unstable** will go in a **new** Branch titled "TTW-DEV-Cluster-" followed by the feature name.

### Code review ###
Once changes to the source code have been applied they will go into  a **new** Branch titled "TTW-DEV-Cluster-" followed by the feature name and will be deployed to a test server (see instructions above). 

When the code gets in a more stable state it can be moved to the TTW-DEV-Cluster where the Community Managers can freely test.

### Other guidelines ###
Commits **MUST NOT BE MADE** **directly** to the **master Branch**. Features that are new or **VERY** **unstable** will go in a **new** Branch titled "TTW-DEV-Cluster-" followed by the feature name. If the code gets in a more stable state it can be moved to the TTW-DEV-Cluster where the Community Managers can freely test.

Once the Community Managers are happy and it has been tested multiple times it **can** be moved to the **TTW-PROD-Cluster** at a scheduled release. The updated version of TTW-PROD-Cluster can then be merged into the **master** Branch.

The Developer(s) must include notes in each commit to help understand changes and must write a changelog to give to the Community Managers so they can make a news release about it. 

Changes will be bulked together in a TTW-PROD-Cluster maintenance release.
If there is an **EMERGENCY bug fix** that is breaking or **hindering performance** of the game it may be necessary to speed up the developing and testing process - if that cannot happen (not enough time - issue** too severe**) it will be quickly **released** to **TTW-PROD-Cluster**

### Who do I talk to? ###

* Repo owner or admin
Repo Owner: Reese Jenner

### Other community or team contact ###
Game Admins:

Mgracer (Michael) - administrator, coder

Purrty (Julieanne) - in-game admin and Community Manager
## How to edit from other branches:
Just clickt he branch master and you can select different branches like election dev cluster, 
Dont push anything to the branch if not approved, u have to fork this repo to make changes.
