# Hello everyone
As my pet project I decided to make an online store of musical equipment.
Written on the Django Framework, it includes almost all of its basic features such as models with all kinds of relations, view fuctions and classes, forms, lightly customized admin panel, registering/deleting/updating user accounts and pagination.

# Main page

So this is what the main page looks like. You can navigate through the categories on the left, search on the top or filter and order items on the right panel.

![main](https://github.com/corridorofchameleons/MusicStore/assets/133913156/0cdc0169-b0bb-49a3-9e44-6132714fdac9)

# Product description page

And now we're moving on to the product description page. Here to the bottom from the main block there's a Review Form, where, if you're logged in, you can leave a comment and set from 1 to 5 stars. That value will be instantly added into calculation of the average rating, shown on the top.

![desc](https://github.com/corridorofchameleons/MusicStore/assets/133913156/de66940f-648e-4e1c-acde-849d2b040d0e)

# Personal account page

At this place you can change your personal data, password or delete your account.
Also there's a path to your cart. 
The cart looks like this:

![cart](https://github.com/corridorofchameleons/MusicStore/assets/133913156/6b11ba2e-836c-4deb-a49b-893bc088313c)

You can change the quantity of an item (but only within certain limits - not less than one and not more than left in stock). If you want to set 0, there's a delete button to the right, that kills the row in the database.
After you press the submit button, the cart gets empty and your order aquires a number. You can find all of your orders in Recent Orders at your account page.

The cart was probably the hardest part of the project, because it took me some time to invent the way it was gonna work to store all the necessary data. Eventually I had to manually implement a relation that is a bit more complex than regular many-to-many.

# Rest Framework

As a final step, I implemented the basic API for some parts of the project. Here's, for example, the reviews in JSON format:

![revs](https://github.com/corridorofchameleons/MusicStore/assets/133913156/3fc03e98-b093-41b2-bbbc-355f4632014f)
