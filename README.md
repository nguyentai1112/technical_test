<b>Design ideas</b>
1. <b>Requirement:</b>\
		- Get the mean value of an product with UUID over the time.\
		- The solution needs to be generic and optimized enough to consume k requests successively with k is relative big.
2.  <b>Solution:</b>\
		- Store aggregrated total of number and total of score of product.\
		- Define a table (product_stat) with name, count, total score to store data and name field is unique key.\
		- With each product is pushed we increase number of that product in database by 1 and new total score will be current total score plus score of pushed product. This process is quick cause record is updated on unique key(name).\
		- For monitoring or review data or other usage (such as we want to get mean of a product on a specific time), I use trigger to log product (product will be inserted into table products, table products is defined with name, score, time), this feature is optional and can turn off by dropping trigger.

<b>All processes as follow:</b>
1. Client push product data by using api /api/push
2. The application validates data, name must not be empty and score must be number from 0 to 5
3. The application gets current count and total score of the above product (identified by name)
4. The application updates new count and new total score of that product to database, if product is new (did not exist on database) insert product with score and count (=1) into database.
5. For logging for other usage as well as monitor or review data, there is a trigger that when inserting or updating product_stat, the database will insert new record about that product(name, score, time), this process is not in requirement, and can turn off by dropping this trigger
6. The application calculates new mean (new_total_score/new_count) and returns the result to client.

<b>Steps to run app and tests:</b>
1. Clone/Download project from GitHub
2. Go to root folder of the project, install required modules\
    pip3 install -r requirements.txt
3. To run app and test app:\
    $ python3 route.py\
    $ python3 -m unittest tests/test_pushing_product.py
