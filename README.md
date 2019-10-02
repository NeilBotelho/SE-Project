# SE-Project
Flask Pharmacy stock manager website with an admin system.

# Uses
## Frontend:

	- HTML, CSS, Bootstrap 4 & JavaScript.

## Backend:

	- Python, Flask

## Database:

	- SQLite, SQL Alchemy

# Further Work

## Frontend:
The front end uses simple html generated using something called jinja. If you look in the templates folder youll find the templates used for the different pages, but they use jinja so theyre slightly different from normal html.

### Understanding jinja syntax
If you look at layout.html, it looks like its normal html, but youll notice some weird sytac where theres some stuff in curly braces. This one of the areas where jinja is different from html. Those curly braces can be used to run python code before you create your html page. So in layout.html, one of the things I'm using python for is to decide what the title should be.
Now what is layout.html? I'm using it as a template for all my pages. If you go through it, youll notice that layout.html has a head tag, abody tag and a navbar tag but not much else. And the other pages, home.html, about.html etc dont have a head or body tag. This is because all our pages will be having the same navbar, the same general html tags and css rules, jinja allows us to createa general template and then extend it in each of our individual pages. Layout.html is that template. 
Now how do we actually make a page from this template? 
In the layout.html template, youll find a div with the class 'container'. This div contains some python code that you can ignore, but at the end, youll see:
```
{% block content %}   {% endblock %}
```
This provides a spot in the layout template where you can insert code and in this above example that spot is named 'content'

If you open one of the pages(for example, about.html), youll notice that the page starts with 
```
{%extends 'layout.html'%}
```
As youu would expect this is basically telling jinja that my final html page that you generate should have all the content from the layout.html file. After the extends block there is a block saying block content. All of that particular pages content is placed inside the {%block content%} and {%endblock content%} tags. This tells jinja to put the contents of this page into the layout template in the spot where the layout template has the block content tag as mentioned above. 


Another weird thing about jinja is how you link a css stylesheet. Usually you would put the following tag in your html page
```
 <link rel="stylesheet" type="text/css" href="static/main.css">
```
But in jinja you have to use
```
 <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='main.css') }}">
```
and all the css and javascript files you use need to be put in the static folder.

I have put my own main.css file there(you can add additional css rules here or in another file but if its in another file you have to add the link tag to that file in the layout folder). 


### Styling
I am really terrible at styling. If you want to see just how terrible I am at styling go to te layout page and remove any lines that contain bootstrap in them and reload your page. That is what i styled. 
I used bootstrap to do most of the styling for me. Bootstrap is a css stylesheet that is predefined for you to use. 
If you looked through my html, you would have noticed that almost everything has multiple class, like in home.html, my h1 tag has ben given both the display-1 and title class. The display-1 class is predefined by bootstrap and so it is styled according to that. The navbar is also like this. I just wrote a list of my links and put the appropriate bootstrap class for the links and i got the B-E-A-U-tiful navbar that you see on the page. 


If you want to use bootstrap on a html item, just google "Bootstrap paragraph" or "Boostrap table" and go to the bootstrap website, look thorugh what the different classes look like and copy paste  the class you like to  your html page. 

If you want to put a custom style on a html item just put a unique class on it and define its style in the main.css file in the static folder.

_Note_ 
I have downloaded and linked the bootstrap css, bootstrap javascript and the jquery files so that you dont need internet connection to download those libraries everytime to see what your webpage looks like.


### The Forms
Flask doesn't use normal html forms, it uses a python object to make using forms easier in the backend. If you look at any page using a form, like the login page, the registration page, or even the search bar, theres a lot of complicated python and jinja syntax that you dont really need to understand. To style them just give the <div> tag the they are in a class and put whatever style you want. 
The big text at the top of a form is in the legend tag.

If you want to change the text that appears above a particular input field in a form then you need to change the label of that form element in the forms.py file (Mayank should know how to do this by now)

### Short note on the tables
I made a template on tables so that I dont have to update each page every time i want to make a change to the table. The tamplate is in the table.html file and to include it in a page i use the 
```
{% include 'table.html %}
```
command. If you want to style the table you can style it in the table.html file, and if you want to style it only for one particular page you can copy paste the code in the table.html file into that page(after removing the extends and block content lines) and style it there. 

_Note_
A cool feature that i added was that I used a javascript library that i found to sort tables synamically in the browser. So if you click on the header of a column in the table the table will sort according to that table. Now for this to work the table has to have the sortable class, So don't remove it if you want this feature. 