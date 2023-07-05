## What is this
This repo contains my pet project, based on Django. 
Basically this is a simple online shopping site, that includes Django basic features such as:
 - models with all kinds of relations
 - view fuctions and classes
 - forms
 - lightly customized admin panel
 - registering/deleting/updating user accounts
 - pagination

The frontend was written in **HTML** and **CSS** using standard Django templates.
And **MySQL** is used as a database management system.
   
# How it works

## Main page

We start on the main page. Here we have all of our products, paginated by 6 items. 
1. Initially items are not sorted in order to simplify the query.
But you can filter and change the order of items on the right panel.
2. On the left panel you can navigate through categories.
3. On the header from left to right there are link to the main page, search form, link to the account page.

You can put an item into a cart already at this point if you've logged in. 


![main](https://github.com/corridorofchameleons/MusicStore/assets/133913156/237cc590-ed5e-48d7-aa48-d0db9fe10909)


## Product description page

On this page we can find:
1. more detailed information about a product. 
2. To the bottom from the main block there's a Review Form, where, if you're logged in, you can leave a comment and set from 1 to 5 stars. That value will be instantly added into calculation of the average rating, shown on the top.
   

![desc](https://github.com/corridorofchameleons/MusicStore/assets/133913156/ae2adddc-75c2-4d95-adee-8d68934e2e40)


## Personal account page

### This page contains:
1. Change personal info.
2. Change user password.
3. Delete account.
   
4. My cart.
5. My recent orders.

### The cart looks like this:


![cart](https://github.com/corridorofchameleons/MusicStore/assets/133913156/a3ef2b27-902c-4089-8126-fcb8febf7e37)


- You can change the quantity of an item (but only within certain limits - not less than one and not more than left in stock). 
- If you want to set 0, there's a delete button to the right, that kills the row in the database.
- After you press the submit button, the cart gets empty and your order aquires a number. You can find all of your orders in Recent Orders at your account page.

Before the Order record is created in the database, CartItem relates to the User directly.
After Order is created, it becomes an intermediate table between the CartItem and User. This was made to make it possible to keep the proper orders history.

## Django Rest Framework

The last thing that is featured on the site, is the basic API for some parts of the project.
Here's, for example, the reviews in JSON format:


![revs](https://github.com/corridorofchameleons/MusicStore/assets/133913156/95ad4e0f-701e-480f-88e7-f0ec198de87e)

