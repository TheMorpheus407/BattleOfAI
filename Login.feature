Feature: Account-Management

Scenario: Registering
Given I have opened the browser and am viewing the "Register"-Site
And I have entered credentials i wish to use
And my credentials are unused
When I click on "Register"
Then I create a new account with the credentials
And I receive an email which contains a verify-link

Scenario: Logging In
Given I have opened the browser and am viewing the "Login"-Site
And i have entered my credentials
When I click on "Login"
Then I receive a cookie which lets me access my account page
//Cookie consists of userid, token, sessiontoken
//same login-function as for the AIs
//Remember-Me Cookies are just the same cookies with a longer lifetime

Scenario: Forgot Password
Given I have forgotten my password
And I am visiting the accoring page
When I reset the password
Then I receive an email with a link to reset my password
