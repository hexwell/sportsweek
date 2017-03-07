# SportsWeek
 A Django web application, built in occasion of the 2017 Sport Week at [I.T.I Marconi](https://www.marconiverona.gov.it/portal/) (Verona).
 
 [**Check it out!**](https://sportsweek.pythonanywhere.com/)
 
 Description:
 
 Tournaments of various sports, matches and single team's score are kept and presented by the application with simple views. Users don't need to login to watch the live stats roll, allowing free access to anyone interested in overviewing the results of current and past matches.
A ranking for each sport is generated so players can keep the competition high!

## Technical explanation, difficulties and considerations (Backend):

### Introduction

The project runs on [Django](https://www.djangoproject.com/) 1.10, a Python web framework to build web applications. Django uses the concepts of projects and apps: a project is a set of files (templates, static files...), configurations and *apps*, also formed by some of those elements, that altogether form the final Web Application. A single app can be used in multiple projects, and a single project can have multiple apps. To know more in regards to this awesome framework, feel free to check out [Django's documentation](https://docs.djangoproject.com) (That contains everything form url configs, views, database models to authentication system based on cookies and security features).

### Structure:

Our app is built by the *project* **SportsWeek** which contains the views that welcome and log users in and out of the Django-backed auth. It also contains the main *application* **Scoreboard**.
 
 Database design:
 
 The database is composed of three models:
 
 * The Sport - Which contains the sport's name;
 * The Team - Which is associated with one sport, has a score and a name;
 * The Event - Which is associated with one sport and two different teams of that sport, has a match date;
 
 ### Views realization:
 
 The application has a view with a list of all the Sports registered to it, with embedded links redirecting to the ranking of each sport.
 There, if there's an upcoming or imminent event, a card shows up with the scores. Every kind of input to application, at least for now, has to be done through the Django auto generated administration console.
 
 The views are realized with Django *generic views* which hugely simplified the development. We had only one single small issue: configuring the widgets in the admin panel to allow only only teams of the same sport to compete, upon the creation of an event.
 , because of the classes structure. We solved it by using the url parser arguments to get the sport id, and then select the corresponding teams.
 
 That was possible because the url that point to a sport is formed with it's id, which also allows sports' names to have spaces and other special characters in them.
 
 ### Templates:
 
 Templates all "extend" a base one with a header and a footer that are common to all pages, to follow the DRY principle.
 The same goes for the event "card", which will be used in both the ranking  and the "history" pages.
 
 ## Next steps:
 
 Next thing we have to face is the possibility to change scores from the app itself, only for users with permissions to do so. The scores also have to update live with Ajax, and we have to write the corresponding views to send the updated data.
 A "history" of matches have to be present also, with old current and future ones, all updating live.
 
 ## Developers:
 
 * **Ettore Forigo** ([Hexwell](https://github.com/Hexwell)) - *Backend*
 * **Tobia Valerio** ([TheItalianPeep](https://github.com/TheItalianPeep)) - *Frontend & Design*
