# Scrumble's User Guide

![](https://raw.githubusercontent.com/CEN3031-group16/GroupProject/master/Docs/logo.bmp)

| Developers     | Email               |
| :---:          | :---:               |
| Bryan Fallin   | fallinbryan@ufl.edu |
| Jesse Martinez | kroronos@ufl.edu    |
| Ryan Feeney    | ryanq.feeney@ufl.edu|
| Stephen Berkner| sberkner@ufl.edu    |
| Kyle Collins   | Kcoll196@ufl.edu    |
| Tony Strother  | semphy@ufl.edu      |
 


# Table of Contents
   * [User Levels](#UserLevels)
      * [Views](#Views)
      * [Permissions](#Permissions)
   
   * [Work Flow](#WorkFlow)
      * [Developer Work Flow](#DeveloperWorkFlow)
   
   * [Glossary](#Glossary)
      * [Item](#ItemDefinition)
      * [Sprint](#SprintDefinition)
      * [Project](#ProjectDefinition)
      * [Comment](#CommentDefintion)




##  <a name="UserLevels"></a>User Levels

### <a name="Permissions"></a>Permissions
Each level user has the following permissions:

* Developer
   * Can create and manage items

* Scrum Master
   * All the permissions of a developer
   * Can create and manage sprints

* Admin
   * All the permissions of a Scrum Master
   * Can create and manage users

  
### <a name="Views"></a>Views
Scrumbles is built to show each user all of what they need and none of what they don’t. Depending on a user’s permission levels what they see on the screen will physically change. The views that are available to each user are as follows:

* Developer
   * Customized Developer Home View
   * Developer Main View
   * Team Manager
   * Analytics View

* Scrum Master
   * Scrum Master Home View
   * Developer Main View
   * Team Manager
   * Analytics View

* Admin
   * Admin Main View
   * Developer Home View
   * Team Manger
   * Analytics View

 
## <a name="WorkFlow"></a>Work Flow
### <a name="DeveloperWorkFlow"></a>Developer
The developer work flow is built around the creation and completion of items. As a developer the user is able to see what other members of the team is working on but only able to assign items to themselves then work on them to completion.

To create an item, the user can either click on the create item tab under the edit menu or use the <kbd>CTRL</kbd>+<kbd>I</kbd> hotkey. The create item dialog will pop up with the following fields/options:

   * Item Title
   * Item Description
   * Item Type
      * User Story
      * Epic
      * Bug
      * Chore
      * Feature
   * Number of points the item is worth
   * Comment

![CreateItemDialogue](https://github.com/CEN3031-group16/GroupProject/blob/master/Docs/UserGuideImages/ItemCreationDialog.png)



### <a name="DeveloperMainView"></a>Developer Main View
The Developer main view allows the user to see which items are on the backlog, the sprints that have been created, and the items that need to be completed during each sprint. The timestamped comments on each item are available on the right side of the screen. Users can view comments using the field on the bottom of the comment box.

![](https://github.com/CEN3031-group16/GroupProject/blob/master/Docs/UserGuideImages/DeveloperMainView.png)

### <a name = "DeveloperHomeView"></a>Developer Home View
When a developer is ready to begin assigning and submitting items for review they should switch to the Developer Home View. From within the Developer Home view users can see the items that are on the backlog and assign themselves items from this list by through a right-click dropdown menu. When an item is selected, its information will be displayed on in the center screen. Users can add and view comments in the same manner as they would in the main view.

![](https://github.com/CEN3031-group16/GroupProject/blob/master/Docs/UserGuideImages/DeveloperHomeView.png)

<em>Items are color coded to show to their status:</em>
* Red
   * Not assigned to anything
   * Assigned to a sprint but not to a user
   * Assinged to a user but not a spring
* Blue
   * Assinged to user and sprint
* Yellow
   * In Progress
* Orange
   * Submitted
* Violet
   * Item is epic
* Green
   * Complete 

<em>To add an item, use the plus on top of the backlog list while in developer home view.</em>

Right clicking an item on the lists will yield the following drop down menus:
   * My Items
      * <em>As the items assigned to the user under My Items are completed, the progress bar on the top of the list will change accordingly.</em>
      * Begin Work
         * When you are ready to begin working on an item select begin work to let the scrum manager on the project know.
      * Submit for review
         * When you are done working on an item submit it for review so the scrum master on the project can check it.
   * Backlog
      * Assign to Me
         * Click this to assign an item to yourself from the backlog.



### <a name="AnalyticsView"></a>Analytics View

* The Analytics view provides users with statistics on:
   * Sprints
      * The Sprint tab provides charts with the percentage of tasks completed as a bar graph and a progress bar.
      * Users can select which sprint they want to view using the list box on the left of the screen.
![Analytics Sprint View](https://github.com/CEN3031-group16/GroupProject/blob/master/Docs/UserGuideImages/AnalyticsSprintView.png)

   * Users
      * The percent of tasks completed by users will be displayed as a pie chart and a bar graph.
      * There is a text box displaying:
         * The User with the most completed tasks
         * The User who earned the most points
         * The average amount of tasks completed by a user in the project
         * The average amount of points earned by a user in the project.
      * Users can select which user they want to view from the list box on the left of the screen.
![Analytics User View](https://github.com/CEN3031-group16/GroupProject/blob/master/Docs/UserGuideImages/AnalyticsUserView.png)

   * Tasks (aka items)
      * Depending on the type of item selected, the graph displayed will change.
      * Users can select which item they want to view from the listbox on the left of the screen.
![Analytics Task View](https://github.com/CEN3031-group16/GroupProject/blob/master/Docs/UserGuideImages/AnalyticsTaskView.png)

<em>Analytics provide valuable information for users of all permission levels, so it's appropriate that everyone be able to access them here.</em>


## <a name = "ScrumMasterWorkFlow"></a>Scrum Master Work Flow

Technically a Scrum Master can be a developer on a project as well, so their workflows are very similar. While the developer level user focuses on the creation and completion of items, the Scrum Master level user focuses on the <em>organization and flow</em> of items. 

While the Scrum Master Main View might seem very similar to the Developer Main View, the difference lies in the drop down menus. Depending on an item's status, the options in the right click drop down will change. The standard options are:
   
   * Assign to User
   * Assign to Sprint
   * Assign to Epic
   * Edit Item
   * Delete Item

 ![Scrum Master Item Editing](https://github.com/CEN3031-group16/GroupProject/blob/UserGuidePatch/Docs/UserGuideImages/ScrumMasterItemEditing.gif)

 If an item has been submitted to the Scrum Master for approval, two additional options become available:
   * Approve Item
   * Reject Item

## <a name = "AdminWorkFlow"></a>Admin Work Flow

Like a Scrum Master, an admin can <em>also</em> be a developer on a project. Technically an admin can also be a Scrum Master as well. 

## <a name="Hotkeys"></a>Hot-Keys

Hot-keys are a great way to get around Scrumbles more quickly and efficiently. Available Hot-key combos are:
* Creation Shortcuts
   * Create User
      * <kbd>CTRL</kbd>+<kbd>U</kbd>
   * Create Item
      * <kbd>CTRL</kbd>+<kbd>I</kbd>
   * Create Sprint
      * <kbd>CTRL</kbd>+<kbd>S</kbd>

* View Switching
   * Show Main view
      * <kbd>CTRL</kbd>+<kbd>M</kbd>
   * Show Home View
      * <kbd>CTRL</kbd>+<kbd>H</kbd>
   * Show Team view
      * <kbd>CTRL</kbd>+<kbd>T</kbd>
   * Show Analytics View
      * <kbd>CTRL</kbd>+<kbd>A</kbd>

<em>Note: Hot key availability is determined by user level.</em>

## <a name="Glossary"></a>Glossary

The main terms to know in Scrumbles are:

* <a name="ItemDefinition"></a>Item
   * Items are the "meat and potatoes" of scrumbles. Every item appears in the backlog and, once assigned to a sprint, can be worked on by developers.

   * They have the following user editable fields:

      * Name/Title
      * Priority
      * Status
      * Description
      * Creation Date
      * Priority
      * A link to Github

* <a name="SprintDefinition"></a>Sprint

   * Sprints are the organizers of items. They dictate which items should be completed during a certain time period. Each sprint must belong to a certain project. 

   * They have the following user editable fields:

      * Name
      * Start Date
      * End Date
      * Assigned Project

* <a name="CommentDefinition"></a>Comment
   
   * Comments are the method by which user's interact with eachother through the application. Users can leave comments on items as they work on them.

   ![](https://github.com/CEN3031-group16/GroupProject/blob/master/Docs/UserGuideImages/CommentBox.png)

* <a name="ProjectDefinition"></a>Project
   * Projects are the top level entity in Scrumbles. They contain within them sprints and the sprints contain items. 

   * Once a project is created,

* <a name = "EpicDefintiEpic
   * E
