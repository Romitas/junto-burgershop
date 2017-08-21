# Burgershop Backend Test Application

## Features

- Access using either seesion or token authorization
- REST Framework API
- Basic administration tools

## Usage

1. Open the app: https://junto-burgershop.herokuapp.com
2. Log in (admin:adminpassword) to view API in browser
3. Get the authorization token: https://junto-burgershop.herokuapp.com/auth-api-token, POST {'username':'admin', 'password':'adminpassword'}
4. Include header {'Authorization':'Token yourauthorizationtokenhere'} in the requests to provide access to the mobile app

## Hints

- All of the existing waiters already have their accounts, username:usernamepassword. Try clinteastwood for example
- Creating a waiter does NOT automatically create a new user
- Menu can be viewed in read-only mode
- Orders can be created, modified or deleted (using POST, PUT and DELETE accordingly)
- OrderRows and Items could be viewed in API but not modified. If you have to, use administration tools
- To add/edit/delete Restaurants and Waiters, use administration tools
- Do not use REST Framework HTML form to add/edit orders. Even if viewing in browser, use Raw data instead - HTML form cannot handle nested structures

Denis Surdeykin, surdeykin.denis@gmail.com, 2017
