Balance Tutorial
==============================

## INTRODUCTION TO PLUG AND TRANSFORMS

### OBJECTIVES
- Create a Transform that adds free money to a specific Users balance.
- Create a Transform that can transfer money between two Users

#### OBJECTIVE: CREATE A FREE MONEY TRANSFORM

##### Step One: Generating a User.

Before we can start handing out any free money we'll need someone to give it to. Navigate into the client repository and run `python client.py create_user`. This should add a new User into the blockchain, and print out their pertinent information in your console.

Make sure to keep a copy of that `signing_key`. We'll use it in all of the future transforms to interact with the User.

##### Step Two: Checking their balance.

All users are created equal in this blockchain. When a new User is added, they receive a starting balance of 100. Try running `python client.py balance_query` from your terminal and enter the `signing_key` from earlier when prompted. This should print the User balance in your log.

##### Step Three: Checking their balance.
